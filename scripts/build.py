#!/usr/bin/env python3
"""Generador estático del Corpus Hispánico de la Guerra. Solo biblioteca estándar."""
from __future__ import annotations
from editorial import validate
import datetime as dt
import html
import json
import os
import pathlib
import re
import shutil
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content' / 'entries'
OUTPUT = ROOT / 'dist'
SITE_NAME = 'Corpus Hispánico de la Guerra'
SITE_URL = os.getenv('SITE_URL', os.getenv('CF_PAGES_URL', '')).strip().rstrip('/')
DESC = 'Archivo documental y enciclopedia de historia militar del mundo hispánico.'

def esc(value):
    return html.escape(str(value), quote=True)

def read_entries():
    entries = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(CONTENT.glob('*.json'))]
    visible = [e for e in entries if e['status'] == 'publicado']
    ids, slugs = set(), set()
    for e in entries:
        if e['status']=='publicado' and not e.get('review_notice'):
            valid,reason=validate(e)
            if not valid: raise ValueError(e['id']+': '+reason)
        assert e['id'] not in ids, f"ID repetido: {e['id']}"
        assert e['slug'] not in slugs, f"Slug repetido: {e['slug']}"
        ids.add(e['id']); slugs.add(e['slug'])
        assert re.fullmatch(r'[a-z0-9-]+', e['slug'])
        assert e.get('sources') and len(e['sources']) >= 2, f"Fuentes insuficientes: {e['id']}"
        assert all(src['url'].startswith('https://') for src in e['sources'])
        assert e.get('sections') and all(s.get('paragraphs') for s in e['sections'])
    return sorted(visible, key=lambda e:(e['publication_date'],e['id']),reverse=True)

def write(path, value):
    p = OUTPUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value, encoding='utf-8')

def cite_paragraph(text):
    escaped=esc(text)
    return re.sub(r'\[(\d+)\]', lambda m:f'<a class="note" href="#fuente-{m.group(1)}" aria-label="Ir a fuente {m.group(1)}">[{m.group(1)}]</a>',escaped)

def absolute(path):
    return SITE_URL + path if SITE_URL else path

def shell(title, main, description=DESC, path='/', page=''):
    og=f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:type" content="article">'
    canonical=f'<link rel="canonical" href="{esc(SITE_URL+path)}"><meta property="og:url" content="{esc(SITE_URL+path)}">' if SITE_URL else ''
    navs=[('/', 'Inicio','inicio'),('/archivo/','Archivo','archivo'),('/cronologia/','Cronología','cronologia'),('/metodo/','Método y fuentes','metodo'),('/temas/','Temas','temas'),('/proyecto/','Proyecto','proyecto')]
    nav=''.join(f'<a href="{h}" '+('aria-current="page" ' if active==page else '')+f'>{esc(t)}</a>' for h,t,active in navs)
    year=dt.date.today().year
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · {SITE_NAME}</title><meta name="description" content="{esc(description)}"><meta name="color-scheme" content="light">
<meta name="theme-color" content="#171d23">{og}{canonical}
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css">
</head><body><a class="skip" href="#contenido">Saltar al contenido</a>
<div class="topline"><span>EDICIÓN PILOTO / ARCHIVO HISTÓRICO</span><span>ESTUDIOS SOBRE LA GUERRA EN EL MUNDO HISPÁNICO</span></div>
<header class="site-header"><div class="header-inner"><a class="brand" href="/" aria-label="Corpus Hispánico de la Guerra · Inicio"><span class="brand-mark" aria-hidden="true">CHG<span class="brand-dot">.</span></span><span class="brand-sub">CORPUS HISPÁNICO<br>DE LA GUERRA</span></a>
<nav aria-label="Navegación principal">{nav}</nav><a class="issue" href="/metodo/">N.º 001 / PROYECTO EDITORIAL</a></div></header>
<main id="contenido">{main}</main>
<footer class="footer"><div class="container footer-top"><div><span class="footer-title">CORPUS HISPÁNICO<br>DE LA GUERRA<span class="brand-dot">.</span></span><p>Un archivo abierto de historia militar: documentos, contextos, protagonistas y análisis.</p></div><div><strong>EXPLORAR</strong><a href="/archivo/">Archivo documental</a><a href="/cronologia/">Cronología</a><a href="/metodo/">Método y fuentes</a></div><div><strong>CRITERIOS</strong><span>Fuentes identificadas</span><span>Incertidumbres explícitas</span><span>Referencias cruzadas</span></div></div><div class="container footer-bottom"><span>© {year} Corpus Hispánico de la Guerra. Proyecto editorial independiente.</span><span>HISTORIA, DOCUMENTACIÓN Y ANÁLISIS</span></div></footer>
<script src="/assets/site.js" defer></script></body></html>'''

def link_for(e): return '/articulos/'+e['slug']+'/'

def article_card(e, num=None, cls='article-card'):
    sequence=f'<span class="card-number">{num:02d}</span>' if num else '<span class="card-number">↗</span>'
    return f'''<a class="{cls}" href="{link_for(e)}" data-cat="{esc(e['category'])}" data-period="{esc(e['period'])}" data-search="{esc((' '.join([e['title'],e['summary'],e['era'],e['category'],e['period']]+e['keywords'])).lower())}"><div class="card-meta"><span>{esc(e['category'])}</span><span>{esc(e['era'])}</span></div><div class="card-heading"><h3>{esc(e['title'])}</h3>{sequence}</div><p>{esc(e['summary'])}</p><div class="card-bottom"><span>{esc(e['id'])}</span><span>LEER FICHA <span aria-hidden="true">↗</span></span></div></a>'''

def home(entries):
    if not entries: return shell('Inicio','<section class="container interior-hero"><h1>Corpus Hispánico de la Guerra</h1><p>El archivo no contiene fichas publicadas actualmente.</p><a href="/temas/">Explorar áreas del Corpus</a></section>')
    featured=next((e for e in entries if e.get('featured')),entries[0])
    others=[e for e in entries if e['id']!=featured['id']][:3]
    main=f'''<div class="hero"><div class="container hero-grid"><div class="hero-text"><div class="eyebrow"><span class="line"></span> ARCHIVO DE HISTORIA MILITAR HISPÁNICA</div><h1>La historia<br>de la guerra.<br><em>Con fuentes.</em></h1><p>Un repertorio documental para estudiar las acciones militares, sus protagonistas y las estructuras que hicieron posible la guerra a través de los siglos.</p><div class="hero-actions"><a class="primary" href="/archivo/">Explorar el archivo <span aria-hidden="true">↗</span></a><a class="text-link" href="/metodo/">Nuestro método <span aria-hidden="true">→</span></a></div></div><div class="hero-aside"><div class="mono-large">CHG<span>.</span></div><div class="thin-rule"></div><p>UN CORPUS.<br>MUCHAS ESCALAS<br>DE ANÁLISIS.</p><div class="side-stat"><span>001</span><span>VOL. INICIAL</span></div><div class="side-stat"><span>{len(entries):03d}</span><span>FICHAS PILOTO</span></div></div></div><div class="hero-bottom container"><span>DEL MUNDO ANTIGUO A LA ÉPOCA CONTEMPORÁNEA</span><span>EDICIÓN EN DESARROLLO / {dt.date.today().year}</span></div></div>
<section class="container section feature-section"><div class="section-title"><span>01 — LECTURA DESTACADA</span><span>ANÁLISIS HISTÓRICO</span></div><div class="feature-grid"><div class="feature-copy"><span class="micro">{esc(featured['id'])} / {esc(featured['era'])}</span><h2>{esc(featured['title'])}</h2><p>{esc(featured['summary'])}</p><a href="{link_for(featured)}" class="inline-button">Leer la investigación <span aria-hidden="true">↗</span></a></div><div class="feature-poster" aria-hidden="true"><span class="poster-top">CORPUS / HISTORIA NAVAL</span><div class="poster-core"><span class="poster-roman">MDLXXI</span><span class="poster-dash"></span><span class="poster-label">ESTUDIO DE CASO<br>{esc(featured['id'])}</span></div><span class="poster-bottom">UNA BATALLA · MUCHOS DOCUMENTOS</span></div></div></section>
<section class="paper-section"><div class="container section"><div class="section-title"><span>02 — EL ARCHIVO</span><a href="/archivo/">VER TODAS LAS FICHAS ↗</a></div><div class="section-heading"><h2>Historia ordenada.<br><em>No simplificada.</em></h2><p>Cada artículo conserva su contexto, fuentes, incertidumbres y conexiones con otros registros.</p></div><div class="cards-grid {'cards-grid-two' if len(others)==2 else ''}">{''.join(article_card(e,i+1) for i,e in enumerate(others))}</div></div></section>
<section class="container section subject-section"><div class="section-title"><span>03 — ÁREAS DEL CORPUS</span><span>TRES LÍNEAS EDITORIALES</span></div><div class="subjects"><a href="/archivo/?categoria=Acciones%20militares"><span>01</span><h3>Acciones<br>militares</h3><p>Batallas, campañas, asedios y enfrentamientos navales.</p><span class="subject-go">↗</span></a><a href="/archivo/?categoria=Protagonistas"><span>02</span><h3>Protagonistas<br>históricos</h3><p>Mandos, figuras militares y agentes políticos vinculados a la guerra.</p><span class="subject-go">↗</span></a><a href="/archivo/?categoria=Historia%20de%20la%20guerra"><span>03</span><h3>Sistemas<br>de guerra</h3><p>Estrategias, ejércitos, instituciones, asedios y organización militar.</p><span class="subject-go">↗</span></a></div></section>
<section class="manifesto"><div class="container manifesto-inner"><span>DECLARACIÓN EDITORIAL</span><h2>La fuente precede<br>a la afirmación.</h2><p>Nos interesa tanto reconstruir los hechos como indicar dónde terminan las certezas y comienzan las interpretaciones.</p><a class="light-link" href="/metodo/">Leer nuestros principios ↗</a></div></section>'''
    return shell('Inicio',main,page='inicio',description=DESC)

def archive(entries):
    cards=''.join(article_card(e) for e in entries)
    main=f'''<section class="container interior-hero"><div class="eyebrow"><span class="line"></span> ARCHIVO DOCUMENTAL / ÍNDICE GENERAL</div><h1>El archivo<span class="period">.</span></h1><p>Fichas históricas con identificador propio, fuentes enlazadas y contexto interpretativo.</p></section><section class="container archive-controls" aria-label="Filtrar el archivo"><label class="search-box"><span>BUSCAR</span><input id="archive-search" type="search" placeholder="Batalla, figura histórica, época..." autocomplete="off"></label><label class="select-box"><span>CATEGORÍA</span><select id="archive-category"><option value="">Todas las áreas</option><option>Acciones militares</option><option>Protagonistas</option><option>Historia de la guerra</option></select></label><label class="select-box"><span>PERÍODO</span><select id="archive-period"><option value="">Todos los períodos</option><option>Antigüedad</option><option>Edad Media</option><option>Edad Moderna</option><option>Edad Contemporánea</option></select></label></section><section class="container section archive-list"><div class="section-title"><span id="results-count" role="status" aria-live="polite">{len(entries)} FICHAS EN EL ARCHIVO</span><span>DOCUMENTACIÓN ABIERTA</span></div><div id="archive-grid" class="cards-grid">{cards}</div><p id="no-results" hidden>No se encontraron fichas con esos criterios.</p></section>'''
    return shell('Archivo',main,page='archivo',description='Índice general de fichas históricas documentadas',path='/archivo/')

def chronology_sort_key(entry):
    """Normalize numeric years and older descriptive chronologies without editing approved records.

    The article title supplies the event's year if chronology contains prose
    (e.g. a campaign range), so those records still sort within the timeline.
    """
    raw=entry['chronology']
    if isinstance(raw,(int,float)) and not isinstance(raw,bool):
        return int(raw)
    text=str(raw).strip()
    if re.fullmatch(r'-?\\d{1,5}',text):
        return int(text)
    # Descriptive fields occasionally contain multiple years; the title
    # names the year that identifies the published event.
    for candidate in (entry.get('title',''),text,entry.get('date','')):
        match=re.search(r'(?<!\\d)(\\d{3,4})(?!\\d)',candidate)
        if match:
            return int(match.group(1))
    raise ValueError(f"Fecha cronológica no interpretable: {entry['id']}: {raw!r}")

def timeline(entries):
    chronological=sorted(entries,key=lambda e:(chronology_sort_key(e),e['id']))
    blocks=''.join(f'<div class="timeline-item"><div class="timeline-year">{esc(e["era"])}</div><div class="timeline-body"><span class="micro">{esc(e["id"])} · {esc(e["category"])}</span><h2><a href="{link_for(e)}">{esc(e["title"])} ↗</a></h2><p>{esc(e["summary"])}</p></div></div>' for e in chronological)
    return shell('Cronología',f'<section class="container interior-hero"><div class="eyebrow"><span class="line"></span> CONTEXTO Y SECUENCIA</div><h1>Cronología<span class="period">.</span></h1><p>Recorre los acontecimientos y las trayectorias del Corpus por fecha histórica aproximada, no por fecha de publicación.</p></section><section class="container section timeline">{blocks}</section>',page='cronologia',path='/cronologia/')

def method():
    main='''<section class="container interior-hero"><div class="eyebrow"><span class="line"></span> CRITERIO, FUENTES Y TRANSPARENCIA</div><h1>El método<span class="period">.</span></h1><p>Una enciclopedia histórica debe ayudar a comprobar sus afirmaciones, no pedir confianza ciega.</p></section>
<section class="container method-layout"><aside><span>PROTOCOLO / CHG-000</span><p>Estándar editorial inicial.<br>Versión de trabajo.</p></aside><div class="method-main"><div class="method-part"><span>01</span><div><h2>Identificación inequívoca</h2><p>Cada artículo tiene un identificador estable, una categoría y un período histórico. Una misma batalla o persona no se crea de nuevo porque figure en otra campaña o cronología.</p></div></div><div class="method-part"><span>02</span><div><h2>Fuentes trazables</h2><p>Los hechos centrales se acompañan de referencias a archivos, museos, repositorios científicos u obras historiográficas localizables. Las referencias se enumeran y enlazan dentro de cada ficha.</p></div></div><div class="method-part"><span>03</span><div><h2>Incertidumbre sin disfraz</h2><p>Las discrepancias de fechas, cifras, atribuciones y localizaciones se hacen visibles. Ninguna reconstrucción moderna se presenta como certeza cuando subsiste debate entre especialistas.</p></div></div><div class="method-part"><span>04</span><div><h2>Revisión antes de publicar</h2><p>La automatización solo puede extraer de la cola artículos marcados expresamente como revisados, con un mínimo de dos referencias, estructura completa e identificador exclusivo. Si no hay fichas revisadas, no se publica nada.</p></div></div><div class="method-part"><span>05</span><div><h2>Transparencia del proyecto</h2><p>Este sitio es una edición piloto de un proyecto documental independiente. Los textos han sido preparados con apoyo de inteligencia artificial y requieren supervisión editorial especializada antes de considerarse publicaciones académicas definitivas.</p></div></div></div></section>'''
    return shell('Método y fuentes',main,page='metodo',description='Política editorial y criterios de verificación histórica',path='/metodo/')

def article(e, by_id):
    facts=''.join(f'<div class="fact"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k,v in e['facts'])
    sections=''.join(f'<section class="entry-section" id="seccion-{i}"><h2>{esc(s["heading"])}</h2>'+''.join(f'<p>{cite_paragraph(p)}</p>' for p in s['paragraphs'])+'</section>' for i,s in enumerate(e['sections'],1))
    sources=''.join(f'<li id="fuente-{s["n"]}"><span>[{s["n"]}]</span><div><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["name"])} ↗</a><small>{esc(s["kind"])}</small></div></li>' for s in e['sources'])
    related=''.join(article_card(by_id[r]) for r in e['related'] if r in by_id)
    toc=''.join(f'<a href="#seccion-{i}">{i:02d} &nbsp; {esc(s["heading"])}</a>' for i,s in enumerate(e['sections'],1))
    related_section=f'<section class="container section"><div class="section-title"><span>LECTURAS RELACIONADAS</span><span>OTRAS FICHAS</span></div><div class="cards-grid">{related}</div></section>' if related else ''
    body=f'''<article><header class="entry-header"><div class="container"><nav class="breadcrumb" aria-label="Ruta"><a href="/">Inicio</a><span>/</span><a href="/archivo/">Archivo</a><span>/</span><span>{esc(e['id'])}</span></nav><div class="eyebrow"><span class="line"></span> {esc(e['eyebrow'])}</div><h1>{esc(e['title'])}</h1><p class="entry-deck">{esc(e['summary'])}</p><div class="entry-meta"><span>{esc(e['id'])}</span><span>{esc(e['date'])}</span><span>{esc(e['period'])}</span><span>EDICIÓN PILOTO</span></div></div></header><div class="container entry-body-grid"><aside class="entry-aside"><div class="aside-title">FICHA DOCUMENTAL</div><dl>{facts}</dl><div class="aside-title on-this-page">EN ESTE ARTÍCULO</div><nav class="toc" aria-label="Contenido de la ficha">{toc}<a href="#bibliografia">Fuentes y bibliografía</a></nav></aside><div class="entry-content"><div class="entry-intro">SÍNTESIS Y ANÁLISIS HISTÓRICO</div><p class="editorial-note">{esc(e.get("review_notice", "Ficha con acta de revisión editorial registrada."))}</p><p>Publicación: {esc(e["publication_date"])} · Última revisión registrada: {esc(e["last_reviewed"])}</p>{sections}<div class="editorial-note"><strong>NOTA DE CRITERIO HISTÓRICO</strong><p>{esc(e['editorial_note'])}</p></div><section class="sources" id="bibliografia"><div class="section-title"><span>FUENTES Y BIBLIOGRAFÍA</span><span>{len(e['sources'])} REFERENCIAS</span></div><ol>{sources}</ol></section></div></div></article>{related_section}'''
    structured={'@context':'https://schema.org','@type':'Article','headline':e['title'],'description':e['summary'],'datePublished':e['publication_date'],'dateModified':e['last_reviewed'],'inLanguage':'es','publisher':{'@type':'Organization','name':SITE_NAME}}
    if SITE_URL: structured['mainEntityOfPage']=SITE_URL+link_for(e)
    body+='<script type="application/ld+json">'+json.dumps(structured,ensure_ascii=False).replace('</','<\\/')+'</script>'
    return shell(e['title'],body,description=e['summary'],path=link_for(e))

def rss(entries):
    if not SITE_URL: return
    rss_root=ET.Element('rss',version='2.0'); channel=ET.SubElement(rss_root,'channel')
    for name,value in [('title',SITE_NAME),('link',SITE_URL+'/'),('description',DESC),('language','es')]: ET.SubElement(channel,name).text=value
    for e in entries:
        item=ET.SubElement(channel,'item')
        for name,value in [('title',e['title']),('description',e['summary']),('link',SITE_URL+link_for(e)),('guid',SITE_URL+link_for(e)),('pubDate',dt.datetime.strptime(e['publication_date'],'%Y-%m-%d').strftime('%a, %d %b %Y 12:00:00 +0000'))]: ET.SubElement(item,name).text=value
    write('feed.xml',ET.tostring(rss_root,encoding='unicode',xml_declaration=True))

def sitemap(entries):
    if not SITE_URL: return
    root=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for path in ['/','/archivo/','/cronologia/','/metodo/','/proyecto/','/temas/']+['/temas/'+k+'/' for k in TOPICS]+[link_for(e) for e in entries]:
        item=ET.SubElement(root,'url'); ET.SubElement(item,'loc').text=SITE_URL+path
    write('sitemap.xml',ET.tostring(root,encoding='unicode',xml_declaration=True))
    write('robots.txt',f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')


TOPICS = {
 'guerras-y-conflictos':'Guerras y conflictos',
 'campanas-y-operaciones':'Campañas y operaciones',
 'batallas-combates-y-asedios':'Batallas, combates y asedios',
 'historia-naval':'Historia naval',
 'personajes-historicos':'Personajes históricos',
 'ejercitos-e-instituciones':'Ejércitos e instituciones militares'
}
def thematic_pages(entries):
    links=''.join(f'<a class="article-card" href="/temas/{k}/"><h2>{esc(v)}</h2><p>Consultar el índice temático →</p></a>' for k,v in TOPICS.items())
    write('temas/index.html',shell('Índices temáticos','<section class="container interior-hero"><h1>Áreas del Corpus</h1><p>Clasificación documental por objetos de estudio.</p></section><section class="container section cards-grid">'+links+'</section>',path='/temas/',page='temas'))
    for key,title in TOPICS.items():
        selected=[e for e in entries if key in e.get('topics',[])]
        cards=''.join(article_card(e) for e in selected) or '<p>Esta sección todavía no contiene fichas. Su inclusión no implica que exista contenido revisado.</p>'
        write('temas/'+key+'/index.html',shell(title,f'<section class="container interior-hero"><a href="/temas/">Todos los temas</a><h1>{esc(title)}</h1><p>{len(selected)} fichas disponibles.</p></section><section class="container section cards-grid">{cards}</section>',path='/temas/'+key+'/'))
def project():
    return shell('El proyecto','''<section class="container interior-hero"><div class="eyebrow">IDENTIDAD Y ALCANCE</div><h1>Corpus Hispánico<br>de la Guerra</h1><p>Enciclopedia, repertorio historiográfico y archivo documental digital dedicado al estudio de la historia militar vinculada al mundo hispánico.</p></section><section class="container section"><h2>Un proyecto independiente</h2><p>El Corpus estudia acontecimientos, personas, instituciones y prácticas militares desde la Antigüedad hasta la época contemporánea. El estudio de los pueblos de la península anteriores a España no presupone una identidad nacional moderna.</p><h2>Estado de esta edición</h2><p>La edición inicial contiene tres textos piloto, conservados para evaluación y expresamente señalados como pendientes de revisión especializada. No representan una publicación académica certificada ni un consejo científico constituido.</p><h2>Compromisos documentales</h2><p>Se distinguirán hechos documentados, interpretaciones, hipótesis y tradiciones. Las discrepancias se explicarán y las correcciones conservarán su historial. No se emplean imágenes generadas por inteligencia artificial para representar sucesos históricos.</p><h2>Correcciones y trazabilidad</h2><p>Se pueden comunicar correcciones mediante <a href="https://github.com/Fallfog/corpus-hispanico-guerra/issues">las incidencias del repositorio</a>, indicando el identificador de la ficha y las fuentes que sustentan la propuesta. No incluyas datos privados en las incidencias públicas.</p></section>''',path='/proyecto/',page='proyecto')

def main():
    if OUTPUT.exists(): shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    shutil.copytree(ROOT/'assets',OUTPUT/'assets')
    entries=read_entries()
    by_id={e['id']:e for e in entries}
    write('index.html',home(entries))
    write('archivo/index.html',archive(entries))
    write('cronologia/index.html',timeline(entries))
    write('metodo/index.html',method())
    thematic_pages(entries)
    write('proyecto/index.html',project())
    write('_headers','/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: DENY\n')
    for e in entries: write('articulos/'+e['slug']+'/index.html',article(e,by_id))
    write('404.html',shell('Página no encontrada','<section class="container interior-hero"><div class="eyebrow">ERROR 404</div><h1>No consta en el archivo<span class="period">.</span></h1><p>La página solicitada no existe. Puedes volver al <a href="/archivo/">índice de fichas</a>.</p></section>'))
    write('robots.txt','User-agent: *\nAllow: /\n')
    rss(entries); sitemap(entries)
    print(f'Generadas {len(entries)} fichas y 4 secciones en {OUTPUT}')

if __name__=='__main__': main()
