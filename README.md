# Corpus Hispánico de la Guerra

Enciclopedia y repertorio documental independiente. Versión inicial conservada y ampliada, sin dependencias Python externas.

## Estado real

- Siete fichas visibles, con tres textos piloto (Lepanto, Juan de Austria, Numancia) y cuatro entradas añadidas el 27-10-2026, incluida la monografía de Cartagena de Indias. La revisión histórica externa no está acreditada; distinguir los pilotos de la revisión documental asistida de las publicaciones posteriores.
- Cola aprobada: vacía. El sistema no genera investigaciones ni publica sin monografías verificadas y aprobadas.
- Publicador configurado para una única revisión diaria a las 21:17 (Europe/Madrid). Puede seleccionar una monografía aprobada de cualquiera de las tres categorías, con un máximo de una nueva publicación por día.
- Generación autónoma: desactivada. No se ha contratado ninguna API.
- El hecho de tener estos archivos no acredita que Cloudflare esté conectado o desplegado. Consultar el panel del alojamiento y el historial de Actions.

## Compilar y comprobar

Python 3.12 recomendado:

```sh
python -m unittest discover -s tests -v
python scripts/check.py
```

Para generar sitemap, RSS y canónicas, definir `SITE_URL` con la URL pública real. Si no existe, se utiliza `CF_PAGES_URL` cuando Cloudflare la proporciona. Las pruebas usan example.org exclusivamente como dominio de prueba.

## Alojamiento actual: Cloudflare Workers + GitHub

El proyecto existente es un Cloudflare Worker con recursos estáticos (`wrangler.jsonc`, directorio `dist`), no un proyecto Pages. Las GitHub Actions validan y generan `dist` y Cloudflare despliega los cambios en `main`. El resultado de las comprobaciones en GitHub/Cloudflare no equivale a verificar la navegación pública desde fuera. La URL real del Worker y el valor de `SITE_URL` deben verificarse antes de declarar las canónicas como definitivas.

## Administración desde GitHub

1. **Añadir:** abrir `content/cola`, Add file → Create new file. Usar el siguiente identificador libre, p. ej. `CHG-A-0004.json` (A acciones, P personajes, D demás). Partir del esquema de las fichas existentes; dejar `status: borrador`. No copiar una aprobación anterior. La carpeta de cola nunca se incorpora a la web.
2. **Documentar:** incluir **al menos 3.000 palabras de desarrollo**, **ocho apartados** y **cinco fuentes identificadas con verificación documentada**, además de referencias `[1]` en cada párrafo. Cada fuente necesita `verified_at` (AAAA-MM-DD) y `verification_note` con el contenido realmente comprobado. El campo `topic_key` representa el acontecimiento/persona, no el enfoque del artículo: conservarlo para evitar publicar versiones como temas nuevos.
3. **Revisar:** contrastar los hechos y derechos de uso; resolver o expresar discrepancias. La comprobación informática NO realiza esta revisión histórica ni detecta todas las paráfrasis duplicadas.
4. **Aprobar:** Actions → Aprobar ficha revisada → Run workflow. Indicar ID y acta de revisión; marcar la confirmación solo tras efectuar las comprobaciones. Se registra el usuario de GitHub y un resumen criptográfico del contenido. Cambiar el contenido invalida esa aprobación.
5. **Publicar:** el calendario único de las 21:17 selecciona una monografía revisada de cualquiera de las tres categorías, como máximo una al día. Sin una ficha elegible, no publica nada. `not_before: AAAA-MM-DD` permite reservarla hasta una fecha. Para simular: Actions → Publicación editorial → Run workflow → dry_run activado. Las horas de inicio pueden retrasarse en GitHub; no son un servicio con garantía de puntualidad.
6. **Modificar:** editar el JSON con el lápiz. Para una revisión sustancial de un piloto, conservar ID y slug. En artículos aprobados, volver a revisar el contenido y registrar su aprobación; el procedimiento de actualización de publicados todavía exige edición técnica. No crear otro artículo del mismo tema.
7. **Retirar:** cambiar `status` a `retirado` en la ficha publicada. Conservar el registro en `editorial/inventory.json`; no reutilizar ID, slug ni topic_key. El generador elimina la página en la siguiente compilación.
8. **Pausar:** editar `editorial/config.json` y cambiar `paused` a `true`. Reanudar con `false`. También puede deshabilitarse el workflow desde Actions.

No incluir claves, contraseñas ni información privada: este repositorio es público. Las incidencias públicas sirven para propuestas de corrección, no para correspondencia privada.

## Controles y límites

El sistema retiene fichas sin revisión, con referencias incompletas, contenido alterado después de aprobación, estructura insuficiente, duplicados de ID/slug/tema o referencias cruzadas inexistentes. Registra el día y franja, y bloquea cualquier segunda publicación automatizada en el mismo día. Con cola vacía finaliza sin cambios. La concurrencia de Actions serializa aprobación y publicación. Una construcción fallida no confirma los cambios en GitHub.

El control formal necesita un revisor responsable: una URL y una casilla no prueban la veracidad de un texto. No se promete detectar automáticamente todos los errores históricos, plagios o fuentes inventadas.

## Costes y continuidad

Documentación consultada el 27-10-2026:

- [GitHub Actions](https://docs.github.com/en/actions/concepts/billing-and-usage): runners estándar gratuitos en repositorios públicos.
- [Cloudflare Pages Free](https://developers.cloudflare.com/pages/platform/limits/): 500 compilaciones mensuales y 20.000 archivos por sitio. Un máximo de una publicación diaria equivale a hasta 28–31 compilaciones editoriales al mes, más las correcciones y pruebas.
- [Programaciones](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): posibles retrasos y desactivación tras 60 días sin actividad en un repositorio público. Vigilar especialmente cuando la cola permanece vacía.
- Dominio propio: opcional y de pago, no contratado. El subdominio de Pages se obtiene al desplegar.
- IA: ninguna API activada ni precio asumido. Antes de habilitar generación, verificar tarifas, cuotas, derechos de uso y presupuesto del proveedor elegido.

## Segunda fase de generación asistida

Un proceso separado puede investigar y generar JSON en `content/cola` siempre como `borrador`, con registro de fuentes consultadas, evidencias por afirmación y notas de incertidumbre. No debe escribir `approval`, publicar ni cambiar las reglas de validación. Las claves se guardarían en Secrets de GitHub, jamás en los JSON o la web. La aprobación corresponde a un revisor; el calendario solo consume material aprobado. Este productor no está implementado ni operativo.

## Errores corregidos en esta revisión

- La publicación original organizaba tres franjas temáticas; desde 27-10-2026 usa una única franja diaria (21:17), con selección entre todas las categorías, solo si existe una monografía aprobada.
- No existía registro de franjas ni inventario permanente: añadidos.
- Cambiar un texto no invalidaba la aprobación: ahora se comprueba su hash.
- La validación solo comprobaba presencia de URL: exige notas de verificación y acta explícita, sin confundirlo con comprobación histórica automática.
- Archivo, método y cronología apuntaban canónicamente a la portada: corregidos.
- Faltaban índices temáticos e información institucional: añadidos.
- El filtrado dependía de estilos del navegador: regla explícita `[hidden]` y contador accesible.

Las pruebas automatizadas utilizan datos sintéticos en directorios temporales y nunca publican fichas ficticias en el Corpus.
