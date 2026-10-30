# Volumen I — Edición académica documental, blanco y negro

**Corpus Hispánico de la Guerra.** Edición revisada con fecha de referencia: 30 de octubre de 2026.

## Identificación bibliográfica

- **Título:** Corpus Hispánico de la Guerra. Volumen I: Guerra y conflicto en el mundo hispánico.
- **Subtítulo:** 92 estudios de investigación documental.
- **Naturaleza:** compilación monográfica histórica, edición independiente, sin ISBN ni DOI asignados.
- **Sistema editorial:** orden cronológico por cuatro épocas, aparato de referencias por capítulo, índice general, índice de identificadores, clasificación por objeto y bibliografía consolidada.
- **Estética:** blanco y negro, tipografía de cuerpo serif, titulares de investigación, cubierta tipográfica sin color ni ilustraciones, paginación y jerarquía académica.
- **Formatos:** PDF A4 con referencias enlazadas, EPUB3 y bibliografía en Markdown.
- **Corte documental:** fichas del Corpus publicadas hasta el 30-10-2026.

## Criterio de exclusión

El archivo digital sigue incluyendo 100 publicaciones históricas. **El Volumen I no incluye las 8 fichas clasificadas como «Protagonistas»**, que siguen publicadas en el Corpus pero no pertenecen al objeto de investigación militar de este libro. El volumen reúne 88 estudios de «Acciones militares» y 4 de «Historia de la guerra»: **92 monografías íntegras**.

No se han eliminado biografías del repositorio ni de la web. Solo quedan fuera de la obra impresa/digital. Su posible reunión en un volumen biográfico posterior no supone una decisión editorial cerrada.

## Estatuto científico y límites

El formato, los índices y el aparato bibliográfico responden a convenciones de investigación histórica. Los textos mantienen sus párrafos, notas y referencias originales. **No se declara revisión por pares, afiliación universitaria, certificación científica ni arbitraje académico externo**. La compilación es una edición de documentación histórica de investigación asistida. Las fichas piloto **CHG-A-0001 (Lepanto)** y **CHG-D-0001 (Numancia)** continúan con avisos de revisión especializada pendiente, reproducidos en el volumen; la tercera ficha piloto original, **CHG-P-0001 (Juan de Austria)**, está excluida por ser biográfica.

El sistema de citas [n] se reinicia en cada monografía. Las  referencias bibliográficas se consolidan al final por combinación de título y URL, sin omitir los listados particulares de cada investigación.

## Integridad editorial y técnica

La compilación se realiza a partir de `content/entries/*.json` mediante `scripts/volumen_i.py`. La selección excluye exclusivamente `category == "Protagonistas"`, sin editar el contenido fuente de las 92 investigaciones. Las pruebas exigen 100 fichas publicadas en el archivo, exactamente 8 biografías excluidas y 92 capítulos en el EPUB. Se genera un manifiesto SHA-256 de PDF, EPUB e índice.

Una compilación correcta garantiza estructura de los archivos, no la veracidad individual de las afirmaciones históricas. Las comprobaciones visuales se realizan a través de `.github/workflows/vista-previa-volumen-i.yml` con páginas de portada, preliminares, índice, cuerpo y bibliografía.

## Entregables principales

- `ediciones/volumen-I/corpus-hispanico-guerra-volumen-I.pdf`
- `ediciones/volumen-I/corpus-hispanico-guerra-volumen-I.epub`
- `ediciones/volumen-I/indice-historico-bibliografia.md`
- `ediciones/volumen-I/manifiesto-volumen-I.json`

## Estado

La fecha del expediente no implica que los PDF/EPUB estén terminados antes de las pruebas: comprobar la última ejecución de **Publicar Volumen I — edición documental académica**, las páginas y las huellas del manifiesto antes de afirmar la publicación final.
