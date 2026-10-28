# Acta de publicación extraordinaria — Curalaba (1598)

**Fecha:** 28 de octubre de 2026 (Europe/Madrid).
**Entrada:** CHG-A-0036.
**Título:** Curalaba, 1598: Pelantaro, la muerte de Óñez de Loyola y la transformación de la frontera mapuche.
**Slug:** `curalaba-1598-pelantaro-muerte-onez-loyola-rebelion-mapuche`.
**Categoría:** Acciones militares · Edad Moderna.
**Modalidad:** Publicación manual inmediata bajo petición del titular: investigar → contrastar → redactar → revisar → publicar → comprobar compilación y despliegue.

## Control editorial

- **5.099 palabras** de desarrollo, 13 secciones y 52 párrafos de prosa original con referencias.
- **Diez fuentes documentadas**, incluidas dos investigaciones académicas sobre la frontera, el estudio de Francis Goicovich sobre alianzas reche-mapuches, la Biblioteca Nacional de Chile (Memoria Chilena) y la Academia de Historia Militar de Chile.
- Revisado directamente el artículo de Goicovich en SciELO (Historia, 2006): https://www.scielo.cl/scielo.php?pid=S0717-71942006000100004&script=sci_arttext.
- Contrastada la síntesis institucional de Memoria Chilena: https://www.memoriachilena.gob.cl/602/w3-article-691.html.
- Detectada discrepancia en la página de Academia de Historia Militar: presenta el 23/12/1598 como fecha del combate, pero sitúa la salida del gobernador el 25/12/1598; no se trató como cronología probada: https://www.academiahistoriamilitar.cl/academia/desastre-de-curalaba/.
- Las fuentes difieren sobre los días **23 y 26 de diciembre**: se indica la controversia y no se inventa un consenso.
- Se distinguen las consecuencias políticas a medio plazo, incluida la reorganización militar y el sistema del situado, de los hechos estrictos de la emboscada.
- No se afirma consulta íntegra de manuscritos primarios originales ni arbitraje académico externo; la validación documental ha sido asistida por IA.

## Publicación comprobada en GitHub

- Ficha original: `content/entries/CHG-A-0036.json`, `status=publicado`.
- Registro de inventario: `editorial/inventory.json`, incorporando `CHG-A-0036`.
- Asiento: `editorial/publications.json`, `2026-10-28/extra-A-0036`.
- Ficha retirada de `content/cola/` después de registrar la publicación.
- HTML generado: `dist/articulos/curalaba-1598-pelantaro-muerte-onez-loyola-rebelion-mapuche/index.html`, con ID CHG-A-0036, título y notas de referencias comprobados.
- **Total en el momento de publicación: 47 entradas.**

## Verificación de Github Actions

La revisión de contenido y el compilador HTML terminaron en `success` después de todos los cambios:
- Verificar Corpus: https://github.com/Fallfog/corpus-hispanico-guerra/actions/runs/40716542644
- Compilar web estática: https://github.com/Fallfog/corpus-hispanico-guerra/actions/runs/40716542725

## Cloudflare

La integración **Cloudflare Workers Builds** está conectada con el repositorio y ha comunicado comprobaciones de producción por medio de GitHub Check Runs. Hay al menos una comprobación `success` para una revisión anterior (SHA `f3a67263ea2de98ced2fe72579bbe1a868f73b09`), enlace: https://dash.cloudflare.com/ea17a6c531d8d5eabf32220cdeb8edc9/workers/services/view/corpus-hispanico-guerra/production/builds/da2e0213-d449-4014-acb3-297823f39148.

**Pendiente de confirmación para la revisión actual:** no se ha recibido en la comprobación de GitHub correspondiente al `HEAD` de esta acta un resultado Cloudflare independiente que confirme esta nueva versión. No se debe afirmar desplegada la nueva página hasta recibir dicho resultado. El enlace público directo de Worker tampoco está verificado por apertura externa.

## Publicación manual como norma

Se ha eliminado el cron de quince minutos de `.github/workflows/publicar.yml` y ajustado `editorial/config.json` a `paused=true`. El titular ordenará las futuras publicaciones y se ejecutará el proceso completo de manera individual; la generación autónoma sigue desactivada.
