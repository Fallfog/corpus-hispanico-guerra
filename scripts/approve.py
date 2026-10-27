"""Sella una revisión explícita; no realiza la investigación por el revisor."""
import datetime as dt,json,os,re
from pathlib import Path
from editorial import digest,validate,validate_monograph,CHECKS
root=Path(__file__).resolve().parents[1]
id=os.environ['ENTRY_ID']
if not re.fullmatch(r'CHG-[APD]-\d{4,}',id):raise SystemExit('ID inválido')
if os.getenv('REVIEW_CONFIRMED')!='true':raise SystemExit('Debes confirmar la revisión completa')
p=root/'content/cola'/f'{id}.json';d=json.loads(p.read_text())
if d['id']!=id:raise SystemExit('El identificador no coincide con el archivo')
notes=os.getenv('REVIEW_NOTES','').strip()
if len(notes)<40:raise SystemExit('Documenta la revisión con al menos 40 caracteres')
d['status']='revisado';d['approval']={'reviewer':os.environ['GITHUB_ACTOR'],'date':dt.date.today().isoformat(),'notes':notes,'checks':dict.fromkeys(CHECKS,True),'content_sha256':digest(d)}
valid,reason=validate(d)
if not valid:raise SystemExit(reason)
valid,reason=validate_monograph(d)
if not valid:raise SystemExit(reason)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Revisión registrada: '+id)
