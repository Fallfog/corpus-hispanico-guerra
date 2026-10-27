"""Controles de publicación: verifican evidencia de revisión, no verdad histórica."""
import datetime as dt
import hashlib
import json
import re

CATEGORIES = {'09:17':'Acciones militares', '15:17':'Protagonistas', '21:17':'Historia de la guerra'}
CHECKS = ('hechos_contrastados','bibliografia_verificada','contradicciones_resueltas','originalidad_y_derechos','profundidad_suficiente')

def digest(d):
    excluded={'approval','status','publication_date','publication_time','last_reviewed','publication_slot'}
    return hashlib.sha256(json.dumps({k:v for k,v in d.items() if k not in excluded},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate(d):
    try:
        for key in ('id','slug','title','category','period','era','date','location','summary','facts','sections','sources','editorial_note','keywords','eyebrow','topic_key','related','chronology'):
            if key not in d or d[key] is None: return False,'Falta '+key
        if not re.fullmatch(r'CHG-[APD]-\d{4,}',d['id']): return False,'ID inválido'
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',d['slug']): return False,'Slug inválido'
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',d['topic_key']): return False,'Clave de tema inválida'
        if d['category'] not in CATEGORIES.values(): return False,'Categoría inválida'
        if d['status'] not in ('revisado','publicado'): return False,'Pendiente de revisión'
        sources=d['sources']; nums={s['n'] for s in sources}
        if len(sources)<2 or len(nums)!=len(sources): return False,'Bibliografía insuficiente o repetida'
        for s in sources:
            if not s.get('name') or not s.get('kind') or not s.get('url','').startswith('https://'): return False,'Referencia incompleta'
            if not s.get('verification_note') or not s.get('verified_at'): return False,'Referencia sin verificación documentada'
            dt.date.fromisoformat(s['verified_at'])
        if len(d['sections'])<3: return False,'Faltan secciones'
        paragraphs=[p for s in d['sections'] for p in s['paragraphs']]
        if sum(len(p.split()) for p in paragraphs)<600: return False,'Menos de 600 palabras de desarrollo'
        for p in paragraphs:
            refs={int(n) for n in re.findall(r'\[(\d+)\]',p)}
            if not refs or not refs <= nums: return False,'Párrafo sin referencia válida'
        a=d.get('approval',{})
        if not a.get('reviewer') or not a.get('notes'): return False,'Falta acta de revisión'
        dt.date.fromisoformat(a['date'])
        if any(a.get('checks',{}).get(k) is not True for k in CHECKS): return False,'Lista de revisión incompleta'
        if a.get('content_sha256') != digest(d): return False,'El texto cambió después de la revisión'
        return True,''
    except (KeyError,TypeError,ValueError): return False,'Estructura editorial inválida'
