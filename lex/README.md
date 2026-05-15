# lex — datons legislation plugin

Acceso a un corpus de 101 654 leyes (708 899 unidades legales) de tres jurisdicciones: España (BOE + boletines autonómicos), Italia (Gazzetta Ufficiale) y Chile (Diario Oficial).

## Corpus (snapshot mayo 2026)

| Jurisdicción | Leyes |
|---|---|
| Italia | 65 931 |
| España | 17 880 (incluye CCAA: Extremadura 7 211, Andalucía 1 115) |
| Chile | 17 782 |

Rangos normativos cubiertos: Real Decreto, Ley, Ley Orgánica, Real Decreto-ley, Resolución, Decreto, Decreto-ley, Decreto Legislativo, Decreto Presidencial, Reglamento, Circular, Instrucción, Constitución, Acuerdo, Código.

## MCP tools (servidor `mcp.datons.com/lex/mcp/`)

- `describe` — overview del corpus con facetas (geo, rango, fuente, estado, tipo de unidad). Llamada inicial recomendada para preguntas tipo "¿qué tienes?".
- `list_laws` — listado paginado y faceteable de leyes. Parámetros: `q` (texto en título), `jurisdiction` (`es`/`cl`/`it`), `status`, `facets` (Lucene), `sort_by`.
- `search_units` — búsqueda BM25 sobre el texto completo de los artículos. Parámetro `facets` con sintaxis `key:value` (claves válidas: `capitulo`, `date`, `doc_type`, `epigrafe`, `geo`, `law`, `law_id`, `rank`, `sector`, `source`, `status`, `unit_type`).
- `read_unit` — lee una unidad específica (artículo, disposición, anexo) por `law_id` (ELI) + `unit_type` + `number`. Acepta `date` (YYYYMMDD) para versión histórica.
- `resolve_citation` — parsea una cita textual y devuelve el contenido del artículo resuelto. **Cuidado**: sin contexto de jurisdicción puede mis-resolver a corpus italiano por volumen — usa `/lex:resolver-cita` que envuelve esta llamada con la jurisdicción forzada.
- `explore_law` — TOC completa de una ley + metadatos (estado, modificadores, versiones disponibles).
- `compare_versions` — diff entre versiones de una ley o de una unidad concreta. Tres modos: `changes`, `unit`, `law`.

## Skills

- `/lex:resolver-cita` — Resuelve cita textual a contenido del artículo, con jurisdicción inferida.
- `/lex:buscar-norma` — Lista leyes por tema o título.
- `/lex:comparar-versiones` — Cambios entre versiones de una ley.
- `/lex:explorar-ley` — Estructura (TOC) y metadatos de una ley.
- `/lex:texto-en-fecha` — Lee el texto vigente de una unidad a una fecha pasada.
- `/lex:citar-formato` — Estandariza una cita en formato canónico (BOE + ELI + URL datons).

## Autenticación

OAuth en primera invocación. Una cuenta datons.com es suficiente. El token queda cacheado por sesión del cliente.

## Trazabilidad

Cada respuesta de las skills incluye, cuando aplica, la URL oficial (BOE, GU, DO) y el `law_id` interno (ELI format, e.g. `es-l-2013-12-26-24`) para auditoría.
