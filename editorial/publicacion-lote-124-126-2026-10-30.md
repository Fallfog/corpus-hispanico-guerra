# Acta editorial de lote triple — publicaciones 124, 125 y 126

Fecha 2026-10-30, momento de incorporación 2026-10-30T13:09:29.074Z. Petición expresa del titular «Pues nada otros 3» en continuidad del sistema de tres entradas por lote.

## Control de selección

- Archivo inicial: 123 monografías y 1 expediente aprobado en cola. Comprobados ID, título, slug y topic_key contra inventario vigente. Los tres temas estaban inéditos.
- Se incorpora Teruel desde la cola revisada y se redactan dos nuevas monografías: la batalla de Olmedo (1445), distinta de Olmedo (1467), y el puente de Alcolea (1868), distinta de otras batallas homónimas.
- Los tres trabajos cumplen 3.000 palabras, ocho secciones, cinco referencias y citas válidas por párrafo. El texto archivado conserva huellas editoriales SHA-256 individuales y aprobaciones registradas.

## Dossier de monografías

- **CHG-A-0128** Teruel, 1937–1938: la ofensiva republicana, el invierno y el desgaste que abrió Aragón — 3.524 palabras, 12 secciones, 40 párrafos referenciados, 11 referencias. SHA-256 editorial: `b821d19c60d98f84851ecafc46ca502192739afcb3c3c31722a05150dc101123`.
- **CHG-A-0132** Olmedo, 1445: Juan II, Álvaro de Luna y la batalla entre guerra y caballería — 3.750 palabras, 10 secciones, 40 párrafos referenciados, 6 referencias. SHA-256 editorial: `5bd7cec8778164b8889c1d9b029480ff080cea87b8c93e8764d91805dcb4050a`.
- **CHG-A-0133** Alcolea, 1868: Serrano, Novaliches y la batalla que precipitó el final de Isabel II — 3.850 palabras, 10 secciones, 40 párrafos referenciados, 6 referencias. SHA-256 editorial: `1824133c28ae08130f266154daba030bacae7a4e207d8f8e20f4174d970b5ec0`.

- Balance de lote: 11124 palabras de desarrollo y 120 párrafos con referencias.

## Auditoría histórica y cautelas

- **Teruel:** se conserva íntegra la revisión anterior. Se diferencian ofensiva de diciembre de 1937, rendición de la guarnición en enero de 1938, ofensiva de febrero, batalla de Alfambra y recuperación franquista de la ciudad; cifras de bajas y destrucción se tratan como estimaciones con alcance de lectura declarado.
- **Olmedo:** fecha 19 de mayo de 1445 y enfrentamiento entre Juan II de Castilla y los infantes de Aragón confirmados por PARES; herida y muerte posterior del infante Enrique confirmadas por su ficha archivística. Recompensas y restituciones posteriores acreditadas por índices de archivo. Artículo de Castillo Cáceres consultado por resumen, no completo.
- **Alcolea:** fecha 28 de septiembre de 1868 confirmada por el Congreso y el catálogo militar; la derrota de las fuerzas leales a Isabel II precede al exilio real del día 30. La descripción manuscrita, mapas de 1868 y el estudio de Viñas Cebrián se registran con alcance de consulta real, sin afirmar lectura completa de los originales.
- Revisión de documentos y literatura asistida por IA; sin dictamen externo de especialistas, sin reproducción de imágenes ajenas ni citas extensas. La validación estructural no certifica verdad histórica.

## Operación técnica

- Se incorporan las tres fichas publicadas a `content/entries`, se elimina solo `content/cola/CHG-A-0128.json`, y se actualizan inventario, historial y README de manera atómica en un único commit de la rama principal.
- La selección congelada de 92 estudios del Volumen I y `editorial/config.json` permanecen intactas (`paused: true`, `generation_enabled: false`).
- La terminación de GitHub Actions y la generación de los tres HTML deben comprobarse después del commit. Cloudflare Workers no se declara públicamente operativo sin su URL y una verificación HTTP efectiva.
