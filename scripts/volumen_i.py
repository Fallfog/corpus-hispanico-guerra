#!/usr/bin/env python3
"""Volumen I: edición académica documental de los 92 estudios no biográficos.

Fuentes: content/entries/*.json en la revisión del repositorio que ejecuta el proceso.
Salidas: PDF paginado, EPUB3 navegable, índices y manifiesto editorial.
La compilación no edita ningún estudio ni atribuye arbitraje académico externo.
"""
from __future__ import annotations
from collections import defaultdict
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit
import hashlib, json, re, unicodedata, uuid, zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "entries"
OUTPUT = ROOT / "ediciones" / "volumen-I"
DATE = "2026-10-30"
TITLE = "Corpus Hispánico de la Guerra"
SUBTITLE = "Volumen I. Guerra y conflicto en el mundo hispánico: 92 estudios documentales"
PDF = OUTPUT / "corpus-hispanico-guerra-volumen-I.pdf"
EPUB = OUTPUT / "corpus-hispanico-guerra-volumen-I.epub"
PERIODS = ["Antigüedad", "Edad Media", "Edad Moderna", "Edad Contemporánea"]
ISBN_NOTE = "Edición documental independiente; sin ISBN asignado."
EDITORIAL = [
    ("Objeto de la edición",
     "Este primer volumen reúne, de manera íntegra, noventa y dos estudios de historia militar vinculada al mundo hispánico. El objeto de análisis comprende batallas, campañas, asedios, operaciones navales e instituciones y sistemas de guerra. Se excluyen expresamente las ocho biografías clasificadas como Protagonistas en el archivo general de cien publicaciones. La selección no supone una evaluación comparativa del mérito de las personas históricas: responde a la delimitación del objeto científico de este volumen."),
    ("Delimitación cronológica y espacial",
     "La colección abarca desde la Antigüedad hasta la época contemporánea. El criterio de adscripción territorial comprende acontecimientos librados en el espacio de la actual España, incluso cuando preceden al Estado moderno. El criterio histórico incluye las entidades políticas de la península y sus actuaciones en otros territorios. No se atribuyen identidades nacionales actuales a poblaciones romanas, prerromanas o medievales."),
    ("Preguntas y ejes analíticos",
     "Los estudios examinan, en la medida permitida por las fuentes, el contexto político y territorial, los objetivos de las operaciones, la organización de los ejércitos, el mando, la logística y el abastecimiento, la acción táctica, las consecuencias y la memoria historiográfica. La colección no pretende responder con un modelo causal único a conflictos de épocas muy diferentes: cada monografía delimita sus problemas, sus pruebas y sus incertidumbres."),
    ("Naturaleza de la investigación y criterios de selección",
     "Esta es una recopilación crítica de investigaciones histórico-documentales previamente publicadas en el Corpus. Los criterios formales de admisión fueron disponer de estructura analítica, extensión suficiente, fuentes identificadas, notas sobre el grado de acceso a estas y referencias numeradas en los párrafos. Se preserva la formulación de las monografías originales; esta edición modifica únicamente la selección de capítulos y su dispositivo tipográfico, no los hechos ni las citas de los estudios."),
    ("Crítica de fuentes y niveles de evidencia",
     "La documentación consultada combina, según el capítulo, fuentes narrativas antiguas, crónicas, testimonios institucionales, archivos, estudios de arqueología, investigaciones académicas y obras de síntesis. Se diferencia la lectura íntegra de una obra de la consulta de fichas bibliográficas, resúmenes o fragmentos. La mera presencia de un enlace, un DOI o una referencia no valida por sí sola una afirmación. Las cifras de efectivos, discursos atribuidos, topografías y secuencias tácticas controvertidas se presentan como tales cuando la evidencia no permite cerrarlas."),
    ("Normas de citación y aparato bibliográfico",
     "Cada capítulo conserva íntegramente su sistema de referencias numeradas entre corchetes. La numeración se reinicia en cada estudio, de manera que [1] remite a la primera referencia de ese capítulo. La bibliografía del final de cada monografía identifica las obras utilizadas y conserva sus advertencias de verificación. El repertorio final consolida entradas por combinación de título bibliográfico y dirección de consulta e indica las fichas en las que aparece cada una."),
    ("Alcance de la revisión y límites de certificación",
     "Los textos proceden de un proceso de revisión documental asistido por inteligencia artificial y de verificaciones técnicas sobre su estructura e integridad. El volumen no ha sido sometido en su conjunto a arbitraje académico independiente ni a una revisión historiográfica externa de todas las referencias. Numancia (CHG-D-0001) y Lepanto (CHG-A-0001) mantienen un aviso de revisión especializada pendiente. No se atribuyen al libro acreditaciones universitarias, científicas, editoriales, ISBN o DOI no concedidos."),
    ("Integridad, trazabilidad y futuras correcciones",
     "Los identificadores de las fichas enlazan esta edición con el archivo histórico del Corpus. El índice por etapas y el índice de identificadores facilitan localizar cada investigación. Las rectificaciones ulteriores deberán documentar la lectura o prueba que las motive, las versiones afectadas y su fecha. Un resultado de compilación correcto demuestra la integridad técnica del archivo, pero no sustituye el juicio crítico de la comunidad investigadora."),
]
NOTE = ("EDICIÓN DOCUMENTAL DE FORMATO ACADÉMICO. No se declara revisión por pares "
        "ni arbitraje científico independiente. Los estudios de Numancia y Lepanto "
        "conservan advertencias explícitas de revisión especializada pendiente.")

def clean(s):
    s=str(s or "")
    return "".join(c for c in s if c in "\n\t\r" or ord(c)>=32)

def year(e):
    value=e.get("chronology")
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        return int(value)
    # Algunos artículos conservan una secuencia de eventos con días y meses.
    # Nunca ordenar por el primer día (24) de una cronología narrativa de 1625.
    candidates=[str(e.get("title","")),str(e.get("date","")),str(value)]
    for candidate in candidates:
        m=re.search(r"(?<!\d)(\d{3,4})(?!\d)",candidate)
        if m:
            y=int(m.group(1))
            if re.search(r"\ba\.\s*C\.|\bantes de (?:nuestra era|Cristo)\b",candidate,re.I):
                y=-y
            return y
    for candidate in candidates:
        m=re.search(r"(?<!\d)(\d{1,2})(?!\d)\s*a\.?\s*C\.?",candidate,re.I)
        if m:return -int(m.group(1))
    raise ValueError("Cronología no reconocible: "+e["id"])

def load():
    entries=[json.loads(p.read_text(encoding="utf-8")) for p in sorted(CONTENT.glob("*.json"))]
    published=[e for e in entries if e.get("status")=="publicado"]
    snapshot=json.loads((OUTPUT/"seleccion-volumen-I.json").read_text(encoding="utf-8"))
    included=set(snapshot["included_ids"])
    excluded_ids=set(snapshot["excluded_biography_ids"])
    if len(included)!=92 or len(excluded_ids)!=8 or included.intersection(excluded_ids):
        raise ValueError("Selección editorial congelada del Volumen I incoherente")
    available={e["id"]:e for e in published}
    if not (included|excluded_ids).issubset(available):
        raise ValueError("Faltan fichas originales del Volumen I")
    excluded=[available[x] for x in excluded_ids]
    entries=[available[x] for x in included]
    if any(e.get("category")=="Protagonistas" for e in entries) or any(e.get("category")!="Protagonistas" for e in excluded):
        raise ValueError("Selección de contenido biográfico incorrecta")
    ids=set();slugs=set()
    for e in entries:
        if e["id"] in ids or e["slug"] in slugs: raise ValueError("Duplicado: "+e["id"])
        ids.add(e["id"]);slugs.add(e["slug"])
        paragraphs=[p for s in e["sections"] for p in s["paragraphs"]]
        if len(e["sections"])<8 or len(e["sources"])<5 or len(" ".join(paragraphs).split())<3000:
            raise ValueError("Estudio incompleto: "+e["id"])
        nums={int(s["n"]) for s in e["sources"]}
        for p in paragraphs:
            found=[int(x) for x in re.findall(r"\[(\d+)\]",p)]
            if not found or any(x not in nums for x in found):
                raise ValueError("Referencia rota: "+e["id"])
        e["_year"]=year(e)
    if set(PERIODS)!=set(e["period"] for e in entries):
        raise ValueError("Periodización inesperada, revisar categorías históricas")
    return sorted(entries,key=lambda e:(PERIODS.index(e["period"]),e["_year"],e["id"]))

def source_key(s):
    # La misma URL puede apuntar a distintos trabajos. Conservar ambos si
    # el título bibliográfico difiere; consolidar las repeticiones exactas.
    return (" ".join(clean(s.get("name")).lower().split()),clean(s.get("url")).strip().rstrip("/"))

def bibliography(entries):
    combined={}
    for e in entries:
        for src in e["sources"]:
            key=source_key(src)
            item=combined.setdefault(key,{"name":clean(src["name"]),"url":clean(src["url"]),
                                         "kind":clean(src.get("kind","")),"uses":set()})
            item["uses"].add(e["id"])
    return sorted(combined.values(),key=lambda a:unicodedata.normalize("NFKD",a["name"]).casefold())

def write_indices(entries,refs):
    lines=[
        "# Corpus Hispánico de la Guerra — Volumen I",
        "",
        "**Cien estudios de historia militar hispánica. Edición documental de 30 de octubre de 2026.**",
        "",
        "> "+NOTE, "",
        "## Índice histórico",
        ""
    ]
    for p in PERIODS:
        grp=[e for e in entries if e["period"]==p]
        lines.extend(["### "+p+f" ({len(grp)} estudios)",""])
        lines.extend([f"- **{e['id']}** · {e['title']} — {e.get('date','Fecha histórica no precisada')} · {e['category']}" for e in grp])
        lines.append("")
    lines.extend(["## Índice por clase de estudio",""])
    for cat in sorted({e["category"] for e in entries}):
        subset=[e for e in entries if e["category"]==cat]
        lines.extend(["### "+cat+f" ({len(subset)})",""])
        lines.extend([f"- {e['id']} · {e['title']}" for e in subset])
        lines.append("")
    lines.extend(["## Índice de identificadores",""])
    lines.extend([f"- {e['id']}: {e['title']}" for e in sorted(entries,key=lambda e:e["id"])])
    lines.extend(["","## Bibliografía consolidada","",
                  f"Referencias distintas identificadas: **{len(refs)}**. Se conserva la forma de cita empleada por los estudios.", ""])
    for i,r in enumerate(refs,1):
        lines.append(f"{i}. {r['name']} — {r['url']} — *Fichas: {', '.join(sorted(r['uses']))}*.")
    (OUTPUT/"indice-historico-bibliografia.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

def pdf_book(entries,refs):
    from reportlab.lib import colors, pagesizes
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
        PageBreak, Spacer, KeepTogether, NextPageTemplate, Table, TableStyle)
    from reportlab.platypus.tableofcontents import TableOfContents

    fonts=Path("/usr/share/fonts/truetype/dejavu")
    reg={"Serif":"DejaVuSerif.ttf","Serif-Bold":"DejaVuSerif-Bold.ttf",
         "Serif-Italic":"DejaVuSerif-Italic.ttf","Sans":"DejaVuSans.ttf",
         "Sans-Bold":"DejaVuSans-Bold.ttf"}
    if all((fonts/f).exists() for f in reg.values()):
        for name,fn in reg.items(): pdfmetrics.registerFont(TTFont(name,str(fonts/fn)))
        pdfmetrics.registerFontFamily("Serif",normal="Serif",bold="Serif-Bold",italic="Serif-Italic",boldItalic="Serif-Bold")
        pdfmetrics.registerFontFamily("Sans",normal="Sans",bold="Sans-Bold",italic="Sans",boldItalic="Sans-Bold")
        serif="Serif";bold="Serif-Bold";sans="Sans";sansbold="Sans-Bold"
    else:
        serif="Times-Roman";bold="Times-Bold";sans="Helvetica";sansbold="Helvetica-Bold"
    DARK=colors.black
    RUST=colors.black
    LIGHT=colors.black
    PAGE=pagesizes.A4
    width,height=PAGE
    LM,RM,TM,BM=21*mm,20*mm,22*mm,21*mm
    f=Frame(LM,BM,width-LM-RM,height-TM-BM,id="body",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
    class Book(BaseDocTemplate):
        def afterFlowable(self,flowable):
            level=getattr(flowable,"toc_level",None)
            if level is None:return
            key=getattr(flowable,"toc_key","")
            title=flowable.getPlainText()
            self.canv.bookmarkPage(key)
            self.notify("TOCEntry",(level,title,self.page,key))
            self.canv.addOutlineEntry(title,key,level=level,closed=(level==0))
            if level==1:self.running_title=title
    def cover(c,doc):
        # Portada de monografía académica: fondo blanco, tinta negra, sin acentos de color.
        c.setFillColor(colors.white)
        c.rect(0,0,width,height,stroke=0,fill=1)
        c.setStrokeColor(colors.black)
        c.setLineWidth(.75)
        c.line(31*mm,height-45*mm,width-31*mm,height-45*mm)
        c.setFont(sansbold,10.7)
        c.setFillColor(colors.black)
        c.drawCentredString(width/2,height-34*mm,"CORPUS HISPÁNICO DE LA GUERRA")
        c.setFont(sans,10)
        c.drawCentredString(width/2,height-56*mm,"SERIE DE INVESTIGACIÓN HISTÓRICO-DOCUMENTAL")
        c.setFont(serif,31)
        c.drawCentredString(width/2,height-100*mm,"VOLUMEN I")
        c.setFont(serif,19)
        c.drawCentredString(width/2,height-121*mm,"GUERRA Y CONFLICTO")
        c.drawCentredString(width/2,height-133*mm,"EN EL MUNDO HISPÁNICO")
        c.setLineWidth(.65)
        c.line(57*mm,height-147*mm,width-57*mm,height-147*mm)
        c.setFont(sans,11)
        c.drawCentredString(width/2,height-162*mm,"92 ESTUDIOS DE INVESTIGACIÓN DOCUMENTAL")
        c.setFont(serif,11)
        c.drawCentredString(width/2,48*mm,"DE LA ANTIGÜEDAD A LA ÉPOCA CONTEMPORÁNEA")
        c.setFont(sans,9.2)
        c.drawCentredString(width/2,37*mm,"EDICIÓN DE INVESTIGACIÓN · OCTUBRE DE 2026")
        c.setFont(sans,8)
        c.drawCentredString(width/2,24*mm,"PROYECTO EDITORIAL INDEPENDIENTE · SIN ARBITRAJE EXTERNO")
        c.line(31*mm,19*mm,width-31*mm,19*mm)
    def inner(c,doc):
        c.setFillColor(DARK);c.setFont(sans,7.2)
        c.drawString(LM,height-13*mm,"CORPUS HISPÁNICO DE LA GUERRA")
        c.setStrokeColor(colors.black)
        c.setLineWidth(.45);c.line(LM,height-16*mm,width-RM,height-16*mm)
        c.setFont(sans,7.3);c.setFillColor(LIGHT)
        c.drawString(LM,11.5*mm,"VOLUMEN I · EDICIÓN ACADÉMICA DOCUMENTAL")
        c.drawRightString(width-RM,11.5*mm,str(doc.page))
    doc=Book(str(PDF),pagesize=PAGE,leftMargin=LM,rightMargin=RM,topMargin=TM,bottomMargin=BM,
             title=SUBTITLE,author=TITLE,subject="Noventa y dos investigaciones históricas no biográficas; fuentes documentales e índices")
    doc.addPageTemplates([PageTemplate(id="Portada",frames=[f],onPage=cover),
                          PageTemplate(id="Interior",frames=[f],onPage=inner)])
    styles={}
    def st(name,font,size,leading,spaceBefore=0,spaceAfter=0,color=DARK,**kwargs):
        styles[name]=ParagraphStyle(name,fontName=font,fontSize=size,leading=leading,
                                     spaceBefore=spaceBefore,spaceAfter=spaceAfter,
                                     textColor=color,allowWidows=0,allowOrphans=0,**kwargs)
    st("title",sansbold,19,25,spaceAfter=16)
    st("h0",sansbold,15,20,spaceBefore=14,spaceAfter=10)
    st("h1",sansbold,13.8,19,spaceBefore=10,spaceAfter=12)
    st("h2",sansbold,10.8,15.5,spaceBefore=15,spaceAfter=8)
    st("body",serif,10,15.6,spaceAfter=8.2,alignment=TA_JUSTIFY)
    st("lead",serif,11.2,17.3,spaceAfter=15)
    st("small",serif,8.5,12.7,spaceAfter=5)
    st("source",serif,8.0,11.6,spaceAfter=7)
    st("caption",sans,8.4,12,spaceAfter=5,color=LIGHT)
    st("stat",sans,8.6,13.3,spaceAfter=5)
    st("toc0",sansbold,10,14,spaceBefore=9,spaceAfter=2)
    st("toc1",serif,8.5,12,leftIndent=14,firstLineIndent=-3,spaceAfter=2)
    st("intro",serif,10.3,16.1,spaceAfter=10,alignment=TA_JUSTIFY)
    st("bib",serif,8.15,12.1,spaceAfter=6,alignment=TA_LEFT)
    story=[Spacer(1,175*mm),NextPageTemplate("Interior"),PageBreak()]
    story.extend([
        Spacer(1,17*mm),
        Paragraph("CORPUS HISPÁNICO DE LA GUERRA",styles["title"]),
        Paragraph("Volumen I · Guerra y conflicto en el mundo hispánico",styles["lead"]),
        Paragraph("92 estudios no biográficos · Edición de investigación documental · 30 de octubre de 2026",styles["caption"]),
        Spacer(1,8*mm),
        Paragraph("Créditos y alcance",styles["h0"]),
        Paragraph("Coordinación editorial: Corpus Hispánico de la Guerra, proyecto independiente.",styles["intro"]),
        Paragraph("Textos: selección íntegra de los 92 estudios de campañas, batallas, asedios y sistemas militares del archivo. Se excluyen las ocho biografías de personajes. Las referencias de cada investigación permanecen al final de su capítulo.",styles["intro"]),
        Paragraph(ISBN_NOTE,styles["caption"]),
        Spacer(1,7*mm),
        Paragraph("Advertencia de edición",styles["h0"]),
        Paragraph(escape(NOTE),styles["intro"]),
        PageBreak(),
        Paragraph("Introducción y metodología de esta edición",styles["h0"])
    ])
    for heading,description in EDITORIAL:
        story.append(Paragraph(escape(heading),styles["h2"]))
        story.append(Paragraph(escape(description),styles["intro"]))
    story.extend([PageBreak(),Paragraph("Índice general",styles["h0"]),
                  Paragraph("El índice indica la página de comienzo de cada bloque y estudio; su contenido es navegable en el PDF.",styles["caption"])])
    toc=TableOfContents()
    toc.levelStyles=[styles["toc0"],styles["toc1"]]
    story.extend([toc,PageBreak(),Paragraph("Guía cronológica",styles["h0"])])
    for period in PERIODS:
        gp=[e for e in entries if e["period"]==period]
        story.append(Paragraph(escape(period)+f" · {len(gp)} estudios",styles["h2"]))
        for e in gp:
            story.append(Paragraph(f'<font color="#000000">{escape(e["id"])}</font>  {escape(e["title"])}',styles["small"]))
    story.extend([PageBreak(),Paragraph("Índice por clases de estudio",styles["h0"])])
    for category in sorted({e["category"] for e in entries}):
        group=[e for e in entries if e["category"]==category]
        story.append(Paragraph(f"{escape(category)} · {len(group)}",styles["h2"]))
        for e in group:
            story.append(Paragraph(escape(e["id"]+" · "+e["title"]),styles["small"]))
    story.extend([PageBreak(),Paragraph("Índice por identificadores",styles["h0"])])
    for e in sorted(entries,key=lambda x:x["id"]):
        story.append(Paragraph(escape(e["id"]+" · "+e["title"]),styles["small"]))
    story.append(PageBreak())
    def toc_para(text,style,level,key):
        p=Paragraph(escape(text),style)
        p.toc_level=level;p.toc_key=key
        return p
    for period in PERIODS:
        group=[e for e in entries if e["period"]==period]
        story.extend([toc_para(period,styles["h0"],0,"period-"+str(PERIODS.index(period))),
                      Paragraph(f"{len(group)} monografías de esta etapa",styles["caption"])])
        for e in group:
            story.append(PageBreak())
            story.append(toc_para(e["title"],styles["h1"],1,"chapter-"+e["id"]))
            story.append(Paragraph(escape(e["id"]+"   ·   "+e["category"]+"   ·   "+str(e.get("date",""))),styles["caption"]))
            story.append(Paragraph("RESUMEN",styles["caption"]))
            story.append(Paragraph(escape(e.get("summary","")),styles["lead"]))
            if e.get("review_notice"):
                story.append(Paragraph('<font color="#000000"><b>AVISO DE REVISIÓN PENDIENTE:</b> '+escape(e["review_notice"])+'</font>',styles["small"]))
            if e.get("facts"):
                for label,value in e["facts"]:
                    story.append(Paragraph("<b>"+escape(label)+":</b> "+escape(value),styles["stat"]))
            story.append(Spacer(1,3*mm))
            for section in e["sections"]:
                story.append(Paragraph(escape(section["heading"]),styles["h2"]))
                for paragraph in section["paragraphs"]:
                    def ref(m):
                        n=m.group(1)
                        dest="ref-"+e["id"]+"-"+n
                        return f'<super><link href="#{dest}" color="#000000">[{n}]</link></super>'
                    marked=re.sub(r"\[(\d+)\]",ref,escape(clean(paragraph)))
                    story.append(Paragraph(marked,styles["body"]))
            story.append(Paragraph("Nota de criterio documental",styles["h2"]))
            story.append(Paragraph(escape(e.get("editorial_note","")) or "Sin nota adicional.",styles["small"]))
            story.append(Paragraph("Fuentes y bibliografía del estudio",styles["h2"]))
            for s in e["sources"]:
                n=int(s["n"]); dest="ref-"+e["id"]+"-"+str(n)
                name=escape(clean(s["name"])); url=escape(clean(s["url"]),quote=True)
                note=escape(clean(s.get("verification_note","")))
                line=(f'<a name="{dest}"/><b>[{n}] {name}</b>. '
                      f'<link href="{url}" color="#000000">{url}</link>')
                story.append(Paragraph(line,styles["source"]))
                if note:story.append(Paragraph("Verificación declarada: "+note,styles["source"]))
            story.append(Spacer(1,6*mm))
    story.append(PageBreak())
    story.append(toc_para("Bibliografía consolidada",styles["h0"],0,"bib-consolidated"))
    story.append(Paragraph(f"{len(refs)} referencias bibliográficas distintas por combinación de obra y URL. "
        "Se conservan los títulos y los enlaces de las fichas; cada registro indica las monografías que lo utilizan.",styles["intro"]))
    for i,s in enumerate(refs,1):
        url=escape(clean(s["url"]),quote=True)
        story.append(Paragraph(f'<b>{i:04d}. {escape(s["name"])}</b>. <link href="{url}" color="#000000">{url}</link>. '
            f'<i>Fichas: {escape(", ".join(sorted(s["uses"])))}</i>.',styles["bib"]))
    story.append(Spacer(1,10*mm))
    story.append(Paragraph("Cierre editorial",styles["h0"]))
    story.append(Paragraph("Fin del Volumen I. Esta edición contiene 92 investigaciones no biográficas procedentes del archivo de cien fichas al 30 de octubre de 2026. "
        "Los identificadores se mantienen como referencia permanente para futuras correcciones documentadas.",styles["intro"]))
    doc.multiBuild(story,maxPasses=4)

def epub_book(entries,refs):
    # EPUB 3 autocontenido: cubierta tipográfica y 92 investigaciones no biográficas.
    ns="http://www.idpf.org/2007/opf"
    base="OEBPS/"
    uid=str(uuid.uuid5(uuid.NAMESPACE_URL,"https://github.com/Fallfog/corpus-hispanico-guerra/volumen-I/2026-10-30"))
    css="""body{font-family:Georgia,serif;line-height:1.6;color:#000;background:#ffffff;margin:4%;text-align:justify}h1,h2,h3{font-family:Georgia,serif;line-height:1.3;text-align:left;color:#000}h1{font-size:1.55em}h2{font-size:1.2em;margin-top:1.6em}h3{font-size:1.05em;margin-top:1.3em}.kicker{font-family:Georgia,serif;color:#000;font-size:.85em}.small{font-size:.84em;color:#000}.source{font-size:.85em;border-bottom:1px solid #000;padding:.5em 0}.cover{background:#ffffff;color:#000;text-align:center;padding:8em 1em 9em;border-top:1px solid #000;border-bottom:1px solid #000}.cover h1,.cover h2,.cover p{color:#000;text-align:center}a,a:visited{color:#000;text-decoration:underline}.warning{padding:.7em;border-left:2px solid #000}section{break-before:page}"""
    def xhtml(title,body):
        return ('<?xml version="1.0" encoding="UTF-8"?>'
          '<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es" lang="es">'
          '<head><meta charset="UTF-8"/><title>'+escape(title)+'</title>'
          '<link rel="stylesheet" type="text/css" href="style.css"/></head>'
          '<body>'+body+'</body></html>')
    chapter_files=[]
    content={}
    front="<section><h1>Introducción, alcance y metodología</h1>"+''.join("<h2>"+escape(h)+"</h2><p>"+escape(x)+"</p>" for h,x in EDITORIAL)
    front+='<p class="warning">'+escape(NOTE)+"</p></section>"
    content["front.xhtml"]=xhtml("Presentación editorial",front)
    for i,e in enumerate(entries,1):
        fn=f"chapter-{i:03d}.xhtml";chapter_files.append((fn,e))
        body=f'<section id="chapter-{escape(e["id"])}"><p class="kicker">{escape(e["id"])} · {escape(e["period"])}</p><h1>{escape(e["title"])}</h1>'
        body+='<p class="small">'+escape(e.get("date",""))+" · "+escape(e["category"])+'</p>'
        body+="<p>"+escape(e.get("summary",""))+"</p>"
        if e.get("review_notice"):body+='<p class="warning">'+escape(e["review_notice"])+"</p>"
        if e.get("facts"):
            body+="<h2>Datos de identificación</h2>"
            for label,value in e["facts"]:
                body+="<p><b>"+escape(str(label))+":</b> "+escape(str(value))+"</p>"
        for sec in e["sections"]:
            body+="<h2>"+escape(clean(sec["heading"]))+"</h2>"
            for p in sec["paragraphs"]:
                def link(m):
                    n=m.group(1)
                    return f'<sup><a href="#reference-{n}">[{n}]</a></sup>'
                body+="<p>"+re.sub(r"\[(\d+)\]",link,escape(clean(p)))+"</p>"
        body+="<h2>Nota de criterio documental</h2><p>"+escape(e.get("editorial_note",""))+"</p>"
        body+="<h2>Fuentes y bibliografía</h2><ol>"
        for src in e["sources"]:
            n=int(src["n"])
            body+=f'<li id="reference-{n}" class="source"><b>{escape(src["name"])}</b>. '
            body+=f'<a href="{escape(src["url"],quote=True)}">{escape(src["url"])}</a>. '
            body+=escape(src.get("verification_note",""))+"</li>"
        body+="</ol></section>"
        content[fn]=xhtml(e["title"],body)
    bib="<section><h1>Bibliografía consolidada</h1><p>Referencias por obra y URL, con identificadores de los estudios donde aparecen.</p><ol>"
    for r in refs:
        bib+="<li class=\"source\">"+escape(r["name"])+'. <a href="'+escape(r["url"],quote=True)+'">'+escape(r["url"])+"</a>. Fichas: "+escape(", ".join(sorted(r["uses"])))+".</li>"
    bib+="</ol></section>"
    content["bibliografia.xhtml"]=xhtml("Bibliografía consolidada",bib)
    nav=['<nav xmlns:epub="http://www.idpf.org/2007/ops" epub:type="toc" id="toc"><h1>Índice</h1><ol>',
         '<li><a href="front.xhtml">Presentación</a></li>']
    for period in PERIODS:
        nav.append("<li>"+escape(period)+"<ol>")
        for filename,e in chapter_files:
            if e["period"]==period:
                nav.append('<li><a href="'+filename+'">'+escape(e["title"])+"</a></li>")
        nav.append("</ol></li>")
    nav.append('<li><a href="bibliografia.xhtml">Bibliografía consolidada</a></li></ol></nav>')
    content["nav.xhtml"]=xhtml("Índice",''.join(nav))
    cover='<section class="cover"><p>CORPUS HISPÁNICO DE LA GUERRA</p><h1>VOLUMEN I</h1><h2>92 ESTUDIOS DE INVESTIGACIÓN DOCUMENTAL</h2><p>Octubre de 2026</p></section>'
    content["cover.xhtml"]=xhtml(SUBTITLE,cover)
    manifest=['<item id="css" href="style.css" media-type="text/css"/>',
              '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
              '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>',
              '<item id="front" href="front.xhtml" media-type="application/xhtml+xml"/>']
    spine=['<itemref idref="cover"/>','<itemref idref="front"/>']
    for i,(fn,e) in enumerate(chapter_files,1):
        manifest.append(f'<item id="c{i}" href="{fn}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="c{i}"/>')
    manifest.append('<item id="bibliografia" href="bibliografia.xhtml" media-type="application/xhtml+xml"/>')
    spine.append('<itemref idref="bibliografia"/>')
    package=f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="{ns}" version="3.0" unique-identifier="bookid"
xmlns:dc="http://purl.org/dc/elements/1.1/">
<metadata><dc:identifier id="bookid">urn:uuid:{uid}</dc:identifier>
<dc:title>{escape(SUBTITLE)}</dc:title><dc:language>es</dc:language>
<dc:creator>{escape(TITLE)}</dc:creator><dc:publisher>{escape(TITLE)}</dc:publisher>
<dc:date>{DATE}</dc:date><meta property="dcterms:modified">{DATE}T00:00:00Z</meta></metadata>
<manifest>{''.join(manifest)}</manifest><spine>{''.join(spine)}</spine></package>'''
    container=('<?xml version="1.0" encoding="UTF-8"?>'
    '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
    '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
    '</rootfiles></container>')
    with zipfile.ZipFile(EPUB,"w") as z:
        z.writestr("mimetype","application/epub+zip",compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",container,compress_type=zipfile.ZIP_DEFLATED)
        z.writestr(base+"content.opf",package,compress_type=zipfile.ZIP_DEFLATED)
        z.writestr(base+"style.css",css,compress_type=zipfile.ZIP_DEFLATED)
        for name,html in content.items():
            # Test XML well-formedness before packaging each document.
            ET.fromstring(html.split("<!DOCTYPE html>",1)[-1])
            z.writestr(base+name,html,compress_type=zipfile.ZIP_DEFLATED)

def main():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    entries=load();refs=bibliography(entries)
    write_indices(entries,refs)
    pdf_book(entries,refs)
    epub_book(entries,refs)
    from pypdf import PdfReader
    reader=PdfReader(str(PDF))
    with zipfile.ZipFile(EPUB) as z:
        assert z.testzip() is None
        assert z.namelist()[0]=="mimetype"
        assert len([n for n in z.namelist() if re.fullmatch(r"OEBPS/chapter-\d{3}.xhtml",n)])==92
    pages=len(reader.pages)
    if pages<300:raise ValueError("PDF demasiado corto para incluir los estudios íntegros")
    manifest={"title":SUBTITLE,"date":DATE,"monographs":len(entries),
             "pages":pages,"periods":{p:sum(e["period"]==p for e in entries) for p in PERIODS},
             "classifications":{k:sum(e["category"]==k for e in entries) for k in sorted({e["category"] for e in entries})},
             "bibliographic_records":len(refs),
             "words_of_monographs":sum(len(" ".join(p for s in e["sections"] for p in s["paragraphs"]).split()) for e in entries),
             "pilot_records_with_review_notice":[e["id"] for e in entries if e.get("review_notice")],
             "excluded_biographies":sorted(snapshot["excluded_biography_ids"]),
             "edition":"Revisión de investigación documental, sin biografías; monocroma blanco y negro; sin arbitraje académico externo.",
             "files":{}}
    for path in (PDF,EPUB,OUTPUT/"indice-historico-bibliografia.md"):
        manifest["files"][path.name]={"bytes":path.stat().st_size,
            "sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
    (OUTPUT/"manifiesto-volumen-I.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("VOLUMEN_I_EDICION_ACADEMICA_VERIFICADA",json.dumps({k:v for k,v in manifest.items() if k!="files"},ensure_ascii=False))
if __name__=="__main__":
    main()
