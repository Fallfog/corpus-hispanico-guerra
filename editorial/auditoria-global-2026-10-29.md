# Auditoría global del Corpus Hispánico de la Guerra — 29 de octubre de 2026

## Alcance de la auditoría

Supervisión de la rama principal de `Fallfog/corpus-hispanico-guerra`: inventario, fuentes JSON de artículos, cola editorial, página estática compilada, registro de publicaciones, workflows y configuración de Cloudflare Workers declarada en el repositorio. Se han inspeccionado programáticamente **las 90 fichas publicadas** y **las 14 fichas en cola**. **No es una revisión historiográfica independiente e íntegra de los 90 textos ni una auditoría externa de todas sus URL bibliográficas.**

## Estado confirmado

- **90 fichas publicadas** bajo `content/entries/`, con 90 páginas HTML correspondientes en `dist/articulos/`.
- **90 registros en `editorial/inventory.json`**; sin duplicados de identificador, slug o `topic_key`; ni referencias cruzadas internas sin destino según `scripts/check.py`.
- **14 fichas pendientes en `content/cola/`**, revisadas y selladas documentalmente; ninguna se ha publicado durante esta supervisión.
- **87 anotaciones en `editorial/publications.json`**: las tres fichas iniciales `CHG-A-0001`, `CHG-D-0001`, `CHG-P-0001` constan publicadas e inventariadas, pero no están anotadas en ese registro de publicaciones; la diferencia es legado editorial, no pérdida de archivos.
- Todas las 90 fichas publicadas y las 14 revisadas en cola poseen un desarrollo superior a 3.000 palabras, al menos ocho apartados y cinco fuentes referenciadas. Todos los párrafos de las 90 publicaciones contienen referencias numeradas válidas y no aparecen fuentes sin nota de verificación.
- GitHub Actions: pruebas de integridad, compilación de 90 páginas y comprobación de destinos de enlaces internos **correctas** en el commit de verificación `4d3cb6d` (29-10-2026).
- La web es un proyecto **Cloudflare Workers** con recursos estáticos `dist`, configurado en `wrangler.jsonc`; no es un proyecto Cloudflare Pages.

## Incidencias corregidas

### I-01 — Disparador automático no autorizado (resuelta)

El workflow `.github/workflows/publicar.yml` contenía `schedule: cron: */15 * * * *` y `editorial/config.json` mostraba `paused: false` y límite de 96 publicaciones automáticas por día, en contradicción con las instrucciones del titular y lo registrado en los informes editoriales.

Acciones realizadas:
- Cambiado `paused: true` y mantenido `generation_enabled: false`.
- Limitada preventivamente la cadencia automática potencial a una al día **si alguna vez se autorizara su reactivación**, sin que esta auditoría autorice reactivar nada.
- Eliminado el evento `schedule` del workflow de publicación; permanece exclusivamente `workflow_dispatch` con simulación por defecto. La compilación técnica tras commits sigue activa.
- Añadido control de seguridad en `scripts/check.py` que falla si se activa el cron o se elimina la pausa sin modificar expresamente las garantías.
- Corregidas contradicciones del README y de la política editorial sobre cron y frecuencia de publicaciones.

### I-02 — Revisión formal de publicados incompleta (corregida con excepción visible)

El verificador previo no exigía de forma explícita el estándar prospectivo de 3.000 palabras, ocho apartados y cinco fuentes en todas las fichas ya publicadas, ni cotejaba inventario y cola en cada compilación.

Acciones realizadas:
- Reforzado `scripts/check.py` para aplicar estándares, sellos de aprobación, inventario, control de duplicados e inactividad del calendario.
- Se detectaron **tres fichas piloto del archivo original con `review_notice` vigente y un sello de aprobación no aplicable al contenido actual**: `CHG-A-0001` (Lepanto), `CHG-D-0001` (Numancia), `CHG-P-0001` (Juan de Austria). El verificador las enumera como advertencia explícita y exige en ellas el mínimo estructural. No se ha emitido un sello falso ni eliminado el aviso.
- Las restantes 87 fichas sí se validan a través de la comprobación criptográfica de `scripts/editorial.py` y las nuevas reglas estructurales.
- La primera ejecución de la prueba reforzada detectó una de esas fichas piloto, y la siguiente versión, adaptada para preservar la excepcionalidad histórica sin ocultarla, **superó correctamente las pruebas**.

### I-03 — Documentación editorial contradictoria (resuelta)

README y política editorial conservaban indicaciones heredadas de publicaciones diarias o cada quince minutos incompatibles con la práctica manual autorizada. Documentación y manual se han alineado: se publica únicamente cuando el titular lo solicite; puede haber varias publicaciones manuales en un día sin comprometer calidad ni reactivar calendario.

## Incidencias abiertas

### I-04 — Acceso público a Cloudflare sin prueba independiente (prioridad alta)

El repositorio declara un Cloudflare Worker con recursos en `dist`, pero **no dispone de una URL pública de Worker/domino contrastada**. La validación de GitHub y el archivo HTML generado **no acreditan** que Cloudflare sirva la revisión actual. Comprobación pendiente de URL HTTPS, respuesta del artículo, fecha/versión servida, estado de despliegue y vinculación de la rama `main` en el panel de Cloudflare. No inventar un dominio.

### I-05 — SEO técnico incompleto sin `SITE_URL` (prioridad alta)

`scripts/build.py` solo genera `sitemap.xml`, `rss.xml`/feed y etiquetas canónicas `rel=canonical` cuando `SITE_URL` o `CF_PAGES_URL` contienen una URL pública real. En el árbol inspeccionado no existe sitemap y el HTML no incluye canónica por faltar esa variable. **Pendiente obtener dominio verificado, configurar `SITE_URL`, ejecutar nueva compilación y comprobar sitemap, RSS, metadatos y enlaces canónicos con host real.** No se ha aplicado un dominio supuesto ni `example.org` a producción.

### I-06 — Pendientes de revisión externa completa (prioridad editorial)

Lepanto, Numancia y Juan de Austria conservan avisos de revisión documental pendiente. Deben pasar nueva verificación histórica y de bibliografía con responsable antes de retirar `review_notice` y regenerar aprobación criptográfica. El paso de controles técnicos no constituye arbitraje académico.

### I-07 — Verificación externa de enlaces bibliográficos (prioridad media)

Las fichas tienen URL HTTPS y notas de verificación, pero las pruebas de integridad solo comprueban referencias **internas**. Muestreo del 29-10-2026: DARA Alfonso I y Fundación Castillo de La Estrella respondieron con contenido; PARES devolvió 429, CSIC Gladius 502, Castilla-La Mancha timeout y Tesauros del Ministerio 502. Estos errores no demuestran por sí solos que la referencia esté rota: requieren reintentos, comprobación del servidor de origen o localización de DOI/enlace alternativo. **No se han comprobado individualmente todas las URL de la bibliografía**.

## Criterios de continuidad

1. Conservar pausa editorial y ausencia de cron; solo actuar tras orden expresa para cada monografía.
2. Antes de publicar, comprobar inventario y cola simultáneamente para evitar colisiones concurrentes; el histórico de Montiel sirve de precedente.
3. Registrar lugar y fecha con nivel de incertidumbre, diferenciar fuente íntegra de ficha, resumen o indexación, y no declarar arbitraje académico realizado.
4. Verificar GitHub Actions final tras cada commit; una ejecución fallida debe resolverse y no confundirse con un despliegue correcto.
5. Resolver el dominio público de Cloudflare y entonces terminar SEO canónico y comprobación HTTP de los artículos.

## Verificación técnica documentada

- GitHub Actions, validación correcta: https://github.com/Fallfog/corpus-hispanico-guerra/actions/runs/40965117562
- GitHub Actions, compilación correcta: https://github.com/Fallfog/corpus-hispanico-guerra/actions/runs/40965117618
- Estado del repositorio: https://github.com/Fallfog/corpus-hispanico-guerra
- Alcance de esta acta: revisión técnica/editorial documental asistida, sin acceso al panel Cloudflare y sin revisión historiográfica individual externa de la totalidad del Corpus.
