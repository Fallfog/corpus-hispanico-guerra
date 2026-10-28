#!/usr/bin/env python3
"""Máximo una monografía aprobada al día; sin reserva no se inventa contenido."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
from zoneinfo import ZoneInfo
from editorial import CATEGORIES, validate, validate_monograph

ROOT=Path(__file__).resolve().parents[1]

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); tmp.replace(path)

def run(root,slot,now=None,dry_run=False):
    now=(now or dt.datetime.now(dt.timezone.utc)).astimezone(ZoneInfo('Europe/Madrid'))
    config=json.loads((root/'editorial/config.json').read_text())
    if config.get('paused',True): return {'result':'paused'}
    if slot not in CATEGORIES: raise ValueError('Franja inválida')
    if now.strftime('%H:%M')<slot: return {'result':'not_due'}
    date=now.date().isoformat(); key=date+'/'+slot
    ledger_path=root/'editorial/publications.json'
    ledger=json.loads(ledger_path.read_text())
    # Incluye las ediciones extraordinarias y cualquier franja antigua del mismo día.
    if any(str(k).startswith(date+'/') for k in ledger):
        return {'result':'already_published','slot':key}
    records=[json.loads(p.read_text()) for p in (root/'content/entries').glob('*.json')]
    keys={k:{d.get(k) for d in records} for k in ('id','slug','topic_key')}
    history=root/'editorial/inventory.json'
    if history.exists():
        for d in json.loads(history.read_text()):
            for k in keys: keys[k].add(d.get(k))
    held=[]
    for path in sorted((root/'content/cola').glob('*.json')):
        try: d=json.loads(path.read_text())
        except (ValueError,UnicodeError): held.append({'file':path.name,'reason':'JSON inválido'}); continue
        # La única ejecución programada (21:17) admite todas las secciones.
        # Se conservan las franjas antiguas para pruebas y compatibilidad manual.
        if slot!='21:17' and d.get('category')!=CATEGORIES[slot]: continue
        valid,reason=validate(d)
        if valid: valid,reason=validate_monograph(d)
        if not valid: held.append({'file':path.name,'reason':reason}); continue
        if d.get('not_before','')>date: continue
        if any(d[k] in keys[k] for k in keys): held.append({'file':path.name,'reason':'Identidad o tema duplicado'}); continue
        if any(r not in keys['id'] for r in d['related']): held.append({'file':path.name,'reason':'Referencia interna inexistente'}); continue
        result={'result':'would_publish' if dry_run else 'published','id':d['id'],'slot':key,'held':held}
        if dry_run: return result
        d.update(status='publicado',publication_date=date,publication_time=now.isoformat(),publication_slot=key,last_reviewed=d['approval']['date'])
        save(root/'content/entries'/str(d['id']+'.json'),d)
        ledger[key]={'id':d['id'],'at':now.isoformat()};save(ledger_path,ledger)
        inventory=json.loads(history.read_text()) if history.exists() else []
        inventory.append({k:d[k] for k in ('id','slug','topic_key','title','category')});save(history,inventory)
        path.unlink()
        return result
    return {'result':'empty_or_held','slot':key,'held':held}


def run_quarter_hour(root,now=None,dry_run=False):
    """At most one approved entry per 15-minute window; never generate content.

    GitHub schedules can arrive late. A separate 15-minute cooldown protects
    against two delayed invocations publishing almost simultaneously.
    """
    now=(now or dt.datetime.now(dt.timezone.utc)).astimezone(ZoneInfo('Europe/Madrid'))
    config=json.loads((root/'editorial/config.json').read_text(encoding='utf-8'))
    if config.get('paused',True): return {'result':'paused'}
    date=now.date().isoformat()
    slot=f"auto-{now.hour:02d}:{(now.minute//15)*15:02d}"
    key=date+'/'+slot
    ledger_path=root/'editorial/publications.json'
    ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
    if key in ledger: return {'result':'already_published','slot':key}
    automated=[(k,v) for k,v in ledger.items() if k.startswith(date+'/auto-')]
    if len(automated)>=int(config.get('max_publications_per_day',96)):
        return {'result':'daily_limit','slot':key}
    # A delayed run must not cause two publications in a couple of minutes.
    for oldkey,record in ledger.items():
        if '/auto-' not in oldkey or not isinstance(record,dict): continue
        try:
            before=dt.datetime.fromisoformat(record['at'])
            if before.tzinfo is not None and dt.timedelta(0)<now-before.astimezone(now.tzinfo)<dt.timedelta(minutes=15):
                return {'result':'cooldown','slot':key}
        except (KeyError,ValueError,TypeError): pass
    records=[json.loads(p.read_text(encoding='utf-8')) for p in (root/'content/entries').glob('*.json')]
    keys={k:{d.get(k) for d in records} for k in ('id','slug','topic_key')}
    history=root/'editorial/inventory.json'
    inventory=json.loads(history.read_text(encoding='utf-8')) if history.exists() else []
    for item in inventory:
        for k in keys: keys[k].add(item.get(k))
    held=[]
    for path in sorted((root/'content/cola').glob('*.json')):
        try:d=json.loads(path.read_text(encoding='utf-8'))
        except (ValueError,UnicodeError):
            held.append({'file':path.name,'reason':'JSON inválido'});continue
        valid,reason=validate(d)
        if valid:valid,reason=validate_monograph(d)
        if not valid:held.append({'file':path.name,'reason':reason});continue
        if d.get('not_before','')>date:continue
        # Preserve scheduled commitments predating the new cadence.
        release_at=(config.get('reserved_release_times') or {}).get(d['id'])
        if release_at:
            try:
                if now<dt.datetime.fromisoformat(release_at).astimezone(now.tzinfo):continue
            except ValueError:
                held.append({'file':path.name,'reason':'Reserva horaria inválida'});continue
        if any(d[k] in keys[k] for k in keys):
            held.append({'file':path.name,'reason':'Identidad o tema duplicado'});continue
        if any(r not in keys['id'] for r in d['related']):
            held.append({'file':path.name,'reason':'Referencia interna inexistente'});continue
        result={'result':'would_publish' if dry_run else 'published','id':d['id'],'slot':key,'held':held}
        if dry_run:return result
        d.update(status='publicado',publication_date=date,publication_time=now.isoformat(),publication_slot=key,last_reviewed=d['approval']['date'])
        save(root/'content/entries'/str(d['id']+'.json'),d)
        ledger[key]={'id':d['id'],'at':now.isoformat(),'mode':'publicación automática cada 15 minutos con ficha aprobada'}
        save(ledger_path,ledger)
        inventory.append({k:d[k] for k in ('id','slug','topic_key','title','category')})
        save(history,inventory)
        path.unlink()
        return result
    return {'result':'empty_or_held','slot':key,'held':held}

def main():
    p=argparse.ArgumentParser();p.add_argument('--slot',choices=list(CATEGORIES));p.add_argument('--dry-run',action='store_true');p.add_argument('--interval-15',action='store_true');a=p.parse_args()
    slot=a.slot or {'17 21 * * *':'21:17'}.get(os.getenv('SCHEDULE'))
    if not slot and not a.interval_15: p.error('Indica --slot o --interval-15')
    result=run_quarter_hour(ROOT,dry_run=a.dry_run) if a.interval_15 else run(ROOT,slot,dry_run=a.dry_run);print(json.dumps(result,ensure_ascii=False))
    if os.getenv('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as f:f.write('## Estado editorial\n```json\n'+json.dumps(result,ensure_ascii=False,indent=2)+'\n```\n')
if __name__=='__main__':main()
