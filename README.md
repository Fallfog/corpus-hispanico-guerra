# Corpus Hispánico de la Guerra

Enciclopedia y repertorio documental independiente. Versión inicial conservada y ampliada, sin dependencias Python externas.

## Estado real

- **111 monografías incorporadas al archivo publicado de GitHub al 30-10-2026**. Nueva publicación manual: Los Gelves (1560), CHG-A-0126, después de Elviña y La Coruña (1809), CHG-A-0117.
- **Volumen I — edición de investigación histórico-documental en blanco y negro:** 92 estudios completos (88 acciones militares y 4 historia de la guerra), excluidas del libro las 8 biografías de personajes. Selección histórica congelada en `ediciones/volumen-I/seleccion-volumen-I.json`, sin incorporar automáticamente publicaciones posteriores. PDF, EPUB, índices y manifiesto en `ediciones/volumen-I/`, con criterios de edición en `ediciones/volumen-I/criterios-edicion-academica.md`. No se declara arbitraje científico externo; el volumen conserva el corte editorial histórico de 100 fichas, mientras el archivo vivo contiene 111.
- **Cola editorial:** 8 fichas revisadas pendientes de publicación manual; sin ejecución programada.
- **Publicación solo manual cuando el titular la solicite**: investigación → contraste → monografía ≥3.000 palabras → revisión → GitHub → pruebas y compilación → comprobación HTTP de Cloudflare. El cron de publicación está eliminado de `.github/workflows/publicar.yml`, y `editorial/config.json` permanece con `paused: true`.
- Generación autónoma: desactivada. No se ha contratado ninguna API.
- El hecho de tener estos archivos no acredita que Cloudflare esté conectado o desplegado. Consultar el panel del alojamiento y el historial de Actions.

## Compilar y comprobar

Python 3.12 recomendado:

```sh
python -m unittest discover -s tests -v
python scripts/check.py
```

**Pendiente de SEO:** faltan `sitemap.xml`, RSS y enlaces canónicos en el HTML generado porque `SITE_URL` no tiene una dirección pública real configurada. Definir `SITE_URL` con la URL verificada del Worker y recompilar; si no está disponible, se admite `CF_PAGES_URL`. `example.org` se usa exclusivamente en pruebas, nunca como dominio público.

## Alojamiento actual: Cloudflare Workers + GitHub

El proyecto existente es un Cloudflare Worker con recursos estáticos (`wrangler.jsonc`, directorio `dist`), no un proyecto Pages. Las GitHub Actions validan y generan `dist`; la conexión de Cloudflare Workers con `main` no está verificada desde este repositorio. El resultado de las comprobaciones en GitHub/Cloudflare no equivale a verificar la navegación pública desde fuera. La URL real del Worker y el valor de `SITE_URL` deben verificarse antes de declarar las canónicas como definitivas.

## Administración desde GitHub

1. **Añadir:** abrir `content/cola`, Add file → Create new file. Usar el siguiente identificador libre, p. ej. `CHG-A-0004.json` (A acciones, P personajes, D demás). Partir del esquema de las fichas existentes; dejar `status: borrador`. No copiar una aprobación anterior. La carpeta de cola nunca se incorpora a la web.
2. **Documentar:** incluir **al menos 3.000 palabras de desarrollo**, **ocho apartados** y **cinco fuentes identificadas con verificación documentada**, además de referencias `[1]` en cada párrafo. Cada fuente necesita `verified_at` (AAAA-MM-DD) y `verification_note` con el contenido realmente comprobado. El campo `topic_key` representa el acontecimiento/persona, no el enfoque del artículo: conservarlo para evitar publicar versiones como temas nuevos.
3. **Revisar:** contrastar los hechos y derechos de uso; resolver o expresar discrepancias. La comprobación informática NO realiza esta revisión histórica ni detecta todas las paráfrasis duplicadas.
4. **Aprobar:** Actions → Aprobar ficha revisada → Run workflow. Indicar ID y acta de revisión; marcar la confirmación solo tras efectuar las comprobaciones. Se registra el usuario de GitHub y un resumen criptográfico del contenido. Cambiar el contenido invalida esa aprobación.
5. **Publicar:** solo por orden expresa del titular. Crear y revisar la ficha o seleccionar una previamente aprobada, moverla a `content/entries` por el procedimiento editorial, actualizar inventario y acta y comprobar Actions. **No existe cron activo**. El workflow manual de publicación tiene un modo de simulación por defecto, y el script `publish_next.py` respeta `paused: true`. No reactivar un calendario ni cambiar `paused` sin consentimiento específico.
6. **Modificar:** editar el JSON con el lápiz. Para una revisión sustancial de un piloto, conservar ID y slug. En artículos aprobados, volver a revisar el contenido y registrar su aprobación; el procedimiento de actualización de publicados todavía exige edición técnica. No crear otro artículo del mismo tema.
7. **Retirar:** cambiar `status` a `retirado` en la ficha publicada. Conservar el registro en `editorial/inventory.json`; no reutilizar ID, slug ni topic_key. El generador elimina la página en la siguiente compilación.
8. **Pausar:** editar `editorial/config.json` y cambiar `paused` a `true`. Reanudar con `false`. También puede deshabilitarse el workflow desde Actions.

No incluir claves, contraseñas ni información privada: este repositorio es público. Las incidencias públicas sirven para propuestas de corrección, no para correspondencia privada.

## Controles y límites

El sistema valida fichas, referencias, integridad de aprobación y enlaces internos. La automatización de cola existe solo como código desactivado, sin calendario; la opción futura queda limitada a una publicación automatizada diaria en configuración y requeriría aprobación expresa. Las acciones de compilación siguen ejecutándose automáticamente tras los commits para mantener `dist` actualizado. Una compilación fallida no acredita un despliegue.

El control formal necesita un revisor responsable: una URL y una casilla no prueban la veracidad de un texto. La revisión documental asistida por IA no equivale a arbitraje académico independiente. No se promete detectar automáticamente todos los errores históricos, plagios o fuentes inventadas.

## Costes y continuidad

Documentación consultada el 27-10-2026:

- [GitHub Actions](https://docs.github.com/en/actions/concepts/billing-and-usage): runners estándar gratuitos en repositorios públicos.
- El proyecto declara un Cloudflare Worker con recursos estáticos en `dist`. **No se ha podido demostrar desde GitHub el dominio público o el despliegue en Cloudflare**, por lo que no debe afirmarse una integración operativa sin comprobar su panel y la URL HTTP real.
- [Programaciones](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows): posibles retrasos y desactivación tras 60 días sin actividad en un repositorio público. Vigilar especialmente cuando la cola permanece vacía.
- Dominio propio: opcional; no consta una URL pública verificada. Este repositorio configura **Cloudflare Workers**, no Cloudflare Pages, por lo que no debe suponerse la existencia de un dominio Pages.
- IA: ninguna API activada ni precio asumido. Antes de habilitar generación, verificar tarifas, cuotas, derechos de uso y presupuesto del proveedor elegido.

## Segunda fase de generación asistida

Un proceso separado puede investigar y generar JSON en `content/cola` siempre como `borrador`, con registro de fuentes consultadas, evidencias por afirmación y notas de incertidumbre. No debe escribir `approval`, publicar ni cambiar las reglas de validación. Las claves se guardarían en Secrets de GitHub, jamás en los JSON o la web. La aprobación corresponde a un revisor; el calendario solo consume material aprobado. Este productor no está implementado ni operativo.

## Errores corregidos en esta revisión

- La programación histórica por franjas y los intervalos de quince minutos quedan desactivados; desde la supervisión del 29-10-2026 solo se publica mediante órdenes manuales expresas.
- No existía registro de franjas ni inventario permanente: añadidos.
- Cambiar un texto no invalidaba la aprobación: ahora se comprueba su hash.
- La validación solo comprobaba presencia de URL: exige notas de verificación y acta explícita, sin confundirlo con comprobación histórica automática.
- Archivo, método y cronología apuntaban canónicamente a la portada: corregidos.
- Faltaban índices temáticos e información institucional: añadidos.
- El filtrado dependía de estilos del navegador: regla explícita `[hidden]` y contador accesible.

Las pruebas automatizadas utilizan datos sintéticos en directorios temporales y nunca publican fichas ficticias en el Corpus.
