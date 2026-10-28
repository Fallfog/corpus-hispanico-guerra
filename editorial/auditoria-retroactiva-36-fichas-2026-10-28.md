# Acta extraordinaria de auditoría editorial — homologación retrospectiva del Corpus

**Fecha:** 28 de octubre de 2026 (Europe/Madrid).
**Objeto:** auditoría y ampliación de las **36 fichas publicadas** del Corpus Hispánico de la Guerra.

## Norma y método de auditoría

Norma establecida en `editorial/politica-editorial.md` y `editorial/config.json`: **3.000 palabras de desarrollo** en `sections[].paragraphs`, **8 apartados** y **5 fuentes identificadas y con nota de verificación**, más referencias numéricas válidas en los párrafos. El recuento excluye título, resumen, metadatos y bibliografía y utiliza la separación de palabras por espacios, igual que el control editorial de Python.

Se obtuvieron desde el repositorio GitHub las **36 entradas publicadas**. La auditoría inicial del 28/10 encontró **30 entradas que cumplían los tres umbrales y seis que no**. Las otras treinta se conservaron sin modificación por esta tarea. La ficha de Pavía (`CHG-A-0004`) está en la cola editorial y no se incluye entre las 36 publicaciones; no se modificó.

## Seis monografías ampliadas

| ID | Tema | Palabras antes | Palabras después | Apartados después | Fuentes después |
| --- | --- | ---: | ---: | ---: | ---: |
| CHG-A-0001 | Lepanto 1571 | 506 | 4108 | 16 | 8 |
| CHG-A-0002 | Las Navas de Tolosa 1212 | 836 | 3905 | 14 | 5 |
| CHG-P-0001 | Juan de Austria | 437 | 3528 | 14 | 7 |
| CHG-P-0002 | Gonzalo Fernández de Córdoba | 981 | 3336 | 12 | 5 |
| CHG-D-0001 | Numancia | 506 | 4632 | 18 | 8 |
| CHG-D-0002 | Los tercios de la Monarquía Hispánica | 1105 | 3222 | 15 | 6 |

Se han añadido **18.360 palabras de desarrollo** distribuidas entre seis fichas. Las revisiones se realizaron sobre los **archivos originales**, conservando `id`, `slug`, `topic_key` y sus enlaces históricos. No se crearon publicaciones duplicadas.

### Alcance por tema

- **Lepanto**: Liga Santa, Chipre, galeras y galeazas, combate por alas, tripulaciones y cautivos, memoria literaria, reconstrucción de la flota otomana.
- **Las Navas de Tolosa**: política almohade, Alarcos, logística, alianza de tres monarcas, pasos de Sierra Morena, arqueología, leyendas de las cadenas y del desafío de al-Nasir.
- **Juan de Austria**: genealogía, infancia, formación, Alpujarras, mando naval, Liga Santa, Túnez, Edicto Perpetuo, Gembloux y gobierno de los Países Bajos.
- **Gonzalo Fernández de Córdoba**: juventud, Granada, primeras guerras italianas, Seminara, Barletta, Ceriñola, Garellano, gobierno de Nápoles y crítica de la tradición de las «cuentas».
- **Numancia**: guerra celtibérica, Mancino, Escipión Emiliano, cerco y logística, arqueología de campamentos, proyectiles etolios, necrópolis, capitulación y memoria posterior.
- **Los tercios**: coronelías, organización y administración, armas combinadas, servicio social, sanidad, reclutamiento, Flandes, motines, logística, asedios y crítica de la leyenda de Rocroi.

## Control documental y límites

- Todos los párrafos ampliados contienen referencias numéricas a fichas `sources[]`; todas las nuevas fuentes incluyen `verified_at` y `verification_note`.
- Para las tres entradas piloto (Lepanto, Juan de Austria y Numancia), se añadieron también los metadatos y actos de revisión que faltaban al archivo original.
- La bibliografía distingue páginas completas, resúmenes de revista, catálogos de manuscritos y bibliografía no accesible íntegramente. **No se afirma una lectura directa de manuscritos solo conocidos por su ficha ni revisión académica externa**.
- Se han documentado controversias sobre cronologías, cálculos militares, atribuciones arqueológicas y tradiciones legendarias, en lugar de sustituirlas por certezas inventadas.
- Cada cambio de cuerpo textual actualizó `last_reviewed`, el registro `approval` y el resumen criptográfico `approval.content_sha256`, conforme al control que invalida cambios sin revisión.
- La comprobación automatizada de repositorio y la compilación son verificaciones **formales**, no un arbitraje histórico especializado.
- Se respeta el calendario del publicador y los registros `editorial/publications.json`; **no se han creado nuevos asientos de publicación**, puesto que se trata de correcciones retrospectivas sobre artículos ya publicados.

## Resultado

**36 de 36** entradas publicadas alcanzan ahora el mínimo de extensión, apartados y fuentes documentadas. Se debe comprobar de forma separada el estado final de `Verificar Corpus`, `Compilar web estática` y la URL pública de Cloudflare. La accesibilidad web pública desde el Worker no se declara confirmada por el mero éxito de GitHub Actions.

## Adenda de cierre — 38 fichas en el repositorio

Tras comenzar la auditoría de **36** entradas, otras dos monografías se incorporaron al repositorio durante la misma jornada, sin ser parte de las seis ampliaciones:

- **CHG-A-0031, El Salado (1340):** 6.506 palabras, 22 apartados y 11 fuentes.
- **CHG-A-0032, Maipú (1818):** 7.489 palabras, 26 apartados y 18 fuentes.

Ambas tienen referencias en todos sus párrafos y cumplen el umbral de monografía. Por tanto, al cierre de esta adenda, **38 de 38 fichas publicadas cumplen el requisito cuantitativo**. Las 18.360 palabras añadidas corresponden exclusivamente a las seis entradas antiguas corregidas. Las fichas nuevas no se contabilizan como ampliaciones ni se han alterado en esta auditoría.

La presencia de referencias identificadas no garantiza la veracidad de cada afirmación; sigue siendo necesaria revisión historiográfica especializada antes de declarar una evaluación académica externa.
