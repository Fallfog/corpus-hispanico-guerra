#!/usr/bin/env python3
"""Chequeos rápidos de contenido, enlaces internos y HTML generado."""
import json, pathlib, re, subprocess, sys
R=pathlib.Path(__file__).resolve().parents[1]
records=[json.loads(p.read_text(encoding='utf-8')) for p in (R/'content/entries').glob('*.json')]
records=[r for r in records if r.get('status')=='publicado']
assert records is not None
ids=[r['id'] for r in records]
assert len(ids)==len(set(ids))
urls=[r['slug'] for r in records]
assert len(urls)==len(set(urls))
for r in records:
    assert r['sources'] and len(r['sources'])>=2
    validnums={s['n'] for s in r['sources']}
    for section in r['sections']:
        for paragraph in section['paragraphs']:
            for num in re.findall(r'\[(\d+)\]',paragraph):
                assert int(num) in validnums,(r['id'],num)
    for other in r['related']:
        assert any(json.loads(f.read_text())['id']==other for f in (R/'content/entries').glob('*.json')),(r['id'],other)
subprocess.run([sys.executable,str(R/'scripts'/'build.py')],check=True)
for r in records:
    p=R/'dist'/'articulos'/r['slug']/'index.html'
    assert p.exists() and r['id'] in p.read_text(encoding='utf-8')
for page in ['index.html','archivo/index.html','cronologia/index.html','metodo/index.html','assets/style.css']:
    assert (R/'dist'/page).exists()
print(f'OK: {len(records)} fichas, referencias cruzadas, numeración de fuentes y estructura web.')

from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v:self.links.append(v)
for file in (R/'dist').rglob('*.html'):
    parser=Links();parser.feed(file.read_text())
    for url in parser.links:
        path=unquote(urlsplit(url).path)
        if path.startswith('/') and not urlsplit(url).scheme and not url.startswith('//'):
            target=R/'dist'/path.lstrip('/')
            if path.endswith('/'):target=target/'index.html'
            assert target.exists(),(str(file),url)
print('OK: todos los enlaces internos y recursos estáticos tienen destino.')
