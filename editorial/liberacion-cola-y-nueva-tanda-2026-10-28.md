# Acta de liberación extraordinaria y preparación de nueva tanda — 28/10/2026

**Proyecto:** Corpus Hispánico de la Guerra.
**Autorización:** petición directa del titular: «Venga vamos a darles salida a todas ellas y prepara más», 28 octubre 2026.

## Tres publicaciones liberadas de la cola

Las siguientes monografías, que constaban como `revisado`, se han conservado íntegramente y pasado a `content/entries/` con estado `publicado`, sin crear versiones duplicadas. Se actualizaron **inventario** `editorial/inventory.json` y **asientos** `editorial/publications.json` y se eliminaron sus versiones ya consumidas de `content/cola/`.

| ID | Monografía | Palabras | Apartados | Fuentes | Asiento |
| --- | --- | ---: | ---: | ---: | --- |
| CHG-A-0004 | Pavía, 1525: sitio, batalla y cautiverio de Francisco I | 4.176 | 14 | 8 | 2026-10-28/extra-A-0004 |
| CHG-A-0034 | Guadalajara, 1937: CTV, Brihuega y contraofensiva republicana | 4.844 | 17 | 10 | 2026-10-28/extra-A-0034 |
| CHG-A-0035 | San Juan de Puerto Rico, 1797: defensa ante invasión británica | 4.982 | 17 | 16 | 2026-10-28/extra-A-0035 |

La fecha reservada para Pavía (`2026-10-28T21:17:00+01:00`) quedó **superada por una autorización expresa posterior de publicación inmediata**. Una vez publicada la entrada original `CHG-A-0004`, se retiró la reserva de `editorial/config.json` para evitar que aparezca como compromiso pendiente.

**Resultado al terminar la liberación: 42 entradas publicadas** (39 anteriores + 3). Las páginas estáticas de Pavía, Guadalajara y San Juan han sido comprobadas individualmente en `dist/articulos/`, con el ID respectivo incluido en cada HTML.

## Tres monografías nuevas preparadas y revisadas

Se han preparado entradas originales que respetan el mínimo de 3.000 palabras, ocho apartados y cinco fuentes:

| ID | Tema | Palabras | Apartados | Fuentes | Estado |
| --- | --- | ---: | ---: | ---: | --- |
| CHG-P-0006 | Blas de Lezo: Mediterráneo, Pacífico y Cartagena de Indias | 4.260 | 15 | 9 | revisado, en cola |
| CHG-P-0007 | Agustina de Aragón: artillera del Portillo y vida posterior | 4.319 | 15 | 8 | revisado, en cola |
| CHG-D-0003 | Camino Español: logística, diplomacia y tercios en Flandes | 4.249 | 15 | 8 | revisado, en cola |

En total, la nueva tanda incorpora **12.828 palabras de desarrollo** en textos revisados para los siguientes ciclos del publicador. Su estado actual en `content/cola/` deberá comprobarse dinámicamente, porque GitHub Actions puede moverlas en ejecuciones posteriores.

### Bibliografía y cautelas

- **Blas de Lezo:** Fondo de correspondencia SANTA_FE,1021 del Archivo General de Indias (PARES), exposición del Museo Naval y hallazgos de arqueología hidrográfica de la bahía. Se distinguen discrepancias de nacimiento, cifras de fuerzas, enfrentamiento Lezo–Eslava y propaganda.
- **Agustina de Aragón:** estudios de Ana María Freire López basados en el expediente de Segovia, Ayuntamiento de Zaragoza, Museo del Ejército, PARES y análisis museográfico de Goya en el Prado. Se hacen visibles discrepancias de nacimiento, fecha del Portillo y denominación de su grado de 1809. Se explica la diferencia entre persona histórica y leyenda.
- **Camino Español:** Instituto Cervantes, unidad didáctica del IEEE, fichas académicas sobre Geoffrey Parker y artículos históricos sobre logística y contratistas. Se identifican explícitamente referencias bibliográficas repetidas, y no se afirma haber leído íntegramente los libros o revistas solo consultados mediante ficha o extractos.

Todas las nuevas fichas tienen referencias al pie de sus párrafos y campos de verificación de fuentes; se registra aprobación documental asistida por IA con huella de integridad. **La validación automática no equivale a arbitraje histórico académico externo**. No se han copiado imágenes de terceros ni se ofrecen como pruebas los materiales artísticos de memoria.

## Operación del sistema

El publicador está configurado con intervalos de quince minutos, pero **no genera investigaciones por sí solo** (`generation_enabled=false`). En ausencia de monografías previamente revisadas, no añade artículos ficticios. La disponibilidad pública efectiva del sitio Cloudflare debe comprobarse separadamente; GitHub y HTML compilado no bastan para confirmarla.
