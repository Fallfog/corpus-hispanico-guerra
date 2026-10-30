# Acta editorial de lote triple — publicaciones 121 a 123

Fecha: 2026-10-30. Petición del titular: «Vamos a probar este sistema», referido a tres monografías en un despliegue. Publicación colectiva registrada: 2026-10-30T12:48:14.427Z.

## Integridad de la producción

- Inventario original: 120 entradas. Se redactaron tres investigaciones originales sobre batallas en suelo ibérico, una medieval, una moderna y una contemporánea. Se revisó el inventario para excluir duplicados de título, ID, clave temática y slug.
- Durante la preparación del lote apareció un expediente independiente CHG-A-0128 (Teruel, 1937–1938) en la cola de GitHub. Se **preservó íntegro**, reasignando a Cuarte el identificador libre CHG-A-0131. No se publica ni modifica dicho expediente reservado.
- **CHG-A-0131: Cuarte, 1094: el Cid, Valencia y la ruptura del cerco almorávide** — 3354 palabras, 9 secciones, 36 párrafos citados, 6 referencias. Firma SHA-256 del desarrollo editorial: `6a3aade07eac0c030dace481d95d96f1fe7567f26eb6a8b93c0a57c3356a9e3b`.
- **CHG-A-0129: Almenar, 1710: Stanhope, Felipe V y la victoria de caballería que abrió Aragón** — 3436 palabras, 9 secciones, 36 párrafos citados, 6 referencias. Firma SHA-256 del desarrollo editorial: `4bb39e90cdc52b569c526fcbdef2ff2f7ada83968d66dcabb816f9e05fc1d051`.
- **CHG-A-0130: Almonacid, 1809: Venegas, Sébastiani y la derrota del Ejército de La Mancha** — 3421 palabras, 9 secciones, 36 párrafos citados, 7 referencias. Firma SHA-256 del desarrollo editorial: `a913c39903d859a856465a4cddfea5ed802c9b7a9044881ecebf70666bc153cf`.
- **Total del lote:** 10211 palabras, 27 secciones y 108 párrafos referenciados.

## Fuentes, tratamiento crítico y limitaciones

- **Cuarte:** se utilizaron el Museo del Ejército, la guía sobre Historia Roderici y las fichas de una monografía académica de Montaner y Boix, distinguiendo catálogos repetidos y falta de lectura íntegra de la obra.
- **Almenar:** se contrastó la historia municipal con la guía de la Generalitat (página 42 PDF inspeccionada) y extractos del artículo militar de Segura; las bajas se atribuyen por tipos y fuentes, sin estimaciones falsamente exactas.
- **Almonacid:** se verificó la fecha del 11 de agosto de 1809 en PARES, IGN y ficha académica, y se documenta la discordancia del encabezamiento de 9 de agosto del CIDA.
- Los textos son originales y no incluyen imágenes ajenas. La revisión es asistida por IA, sin arbitraje científico externo ni cotejo paleográfico de originales. Los niveles reales de consulta se detallan individualmente en cada referencia.

## Control tecnológico y alcance de despliegue

- Un solo commit incorpora las tres entradas, actualiza inventario, registro cronológico, README y esta acta, sin tocar la cola existente. Las GitHub Actions deben superar validación y compilación, y se debe comprobar el HTML individual de las tres entradas.
- El Volumen I académico de 92 estudios permanece congelado; `editorial/config.json` continúa pausado y generación automática desactivada.
- La accesibilidad real del sitio en Cloudflare Workers sigue pendiente de verificación externa: generar `dist` en GitHub no demuestra desplegar en Cloudflare.
