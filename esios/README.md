# esios — datons Iberian electricity market plugin

Acceso a la API ESIOS (Sistema de Información del Operador del Sistema) de Red Eléctrica de España: precios del mercado mayorista MIBEL, demanda, generación por tecnología, servicios de balance, indicadores macro del sistema eléctrico ibérico.

## MCP tools (servidor `mcp.datons.com/esios/mcp/`)

El MCP expone wrappers sobre la API de ESIOS oficial. Los indicadores (precios, demanda, generación) se acceden por su ID numérico ESIOS o por nombre semántico. Datons añade caching, paginación inteligente y traducción a estructuras analíticas (matrices horarias).

> **Nota**: las skills de este plugin se han diseñado a partir de la documentación pública de ESIOS y de las tools que ofrece el MCP datons en preview. Cada SKILL.md incluye un comentario `<!-- TODO validate live -->` cerca del bloque de ejemplo — el ejemplo concreto se actualiza cuando la query se valida contra el endpoint en producción.

## Skills

- `/esios:precio-md` — Precio del mercado diario (€/MWh) por hora.
- `/esios:demanda-real` — Demanda peninsular real, hora a hora.
- `/esios:generacion-por-tecnologia` — Reparto de generación por tecnología.
- `/esios:subastas-srad` — Resultados de subastas SRAD (Servicios de Reserva Adicional a Disposición).
- `/esios:precio-banda-secundaria` — Precios de banda secundaria (servicio de regulación).
- `/esios:comparar-periodos` — Compara cualquiera de las series anteriores entre dos rangos de fechas.

## Autenticación

OAuth en primera invocación. Una cuenta datons.com activa con permiso a ESIOS es suficiente. ESIOS por sí solo requeriría token API REE; el MCP datons proxy lo gestiona internamente.

## Trazabilidad

Cada respuesta incluye el indicador ID ESIOS oficial, el rango temporal exacto consultado, y un enlace a `datons.com/apps/esios/<indicator>` para verificación cruzada.
