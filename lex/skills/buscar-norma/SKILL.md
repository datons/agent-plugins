---
name: buscar-norma
description: "Busca leyes en el corpus (España, Italia, Chile) por tema o título. Devuelve hasta N resultados con cita formateada, jurisdicción, estado (vigente/derogada), número de unidades y URL a datons.com. Use when the user says 'busca leyes sobre <tema>', 'qué normativa cubre <tema>', 'lista RDs sobre <tema>', 'norma vigente de <tema>', 'leyes españolas/italianas/chilenas de <tema>'. Llama a `mcp__lex__list_laws` con `q` y filtros de jurisdicción/rango/estado para acotar."
argument-hint: "<tema> [jurisdicción] [rango]"
---

# Buscar normas por tema

Listado faceteado de leyes que contienen el término de búsqueda en su título.

## Cuándo NO usar esta skill

- Si el usuario quiere texto literal de un artículo concreto → `/lex:resolver-cita`.
- Si el usuario tiene un `law_id` y quiere la TOC → `/lex:explorar-ley`.
- Si quiere buscar dentro del contenido (no en el título) → usar `mcp__lex__search_units` directamente con el flag `include_content=true`, no esta skill.

## Pasos al ejecutarse

1. **Parsear el input** del usuario en tres dimensiones: `tema` (string), `jurisdicción` opcional (`es`/`it`/`cl`), `rango` opcional (`real-decreto`, `ley`, `resolución`...).
2. **Inferir jurisdicción** si el usuario no la dio. Si en el `tema` hay palabras como "BOE", "Real Decreto", "España" → `es`. Si "Italia", "Gazzetta" → `it`. Si "Chile" → `cl`. Sin marcadores claros, **preguntar** antes de buscar — el corpus italiano es 3-4× mayor y eclipsa los resultados de otras jurisdicciones.
3. **Inferir rango** si el usuario dijo "Real Decreto", "RD", "Ley" → mapear al valor del facet `rank`.
4. **Llamar** `mcp__lex__list_laws(q=<tema>, jurisdiction=<x>, sort_by='relevance', limit=20)`. Si el usuario especificó rango, añadir `facets='rank:<x>'`.
5. **Filtrar ruido** post-respuesta: descartar resultados cuyo `law_id` empieza por `es-x-` (son anuncios sueltos del BOE, no normas vigentes propiamente) salvo que el usuario haya pedido explícitamente "anuncios" o "resoluciones individuales".
6. **Devolver** una tabla con: `citation_md` (link a datons.com), título completo, jurisdicción, estado (vigente/derogada), `unit_count`, fecha de publicación. Ordenado por relevancia.
7. **Sugerir refinamientos** si hay >15 resultados — proponer al usuario filtrar por rango o por jurisdicción.

## Llamada de referencia (validada en sesión)

`mcp__lex__list_laws(q='autoconsumo', jurisdiction='es', limit=5)` devuelve 8 resultados, incluido el RD 244/2019 (Reglamento de Autoconsumo, 53 unidades, vigente) como top match.

## Ejemplos

- *"busca leyes sobre autoconsumo en España"* → `list_laws(q='autoconsumo', jurisdiction='es')`
- *"qué Reales Decretos sobre subastas eléctricas hay"* → `list_laws(q='subastas eléctricas', jurisdiction='es', facets='rank:royal-decree')`
- *"normativa italiana de cybersecurity"* → `list_laws(q='cybersecurity', jurisdiction='it')`
- *"leyes sobre comunidades energéticas vigentes en España"* → `list_laws(q='comunidades energéticas', jurisdiction='es', status='in_force')`

## Errores

- **0 resultados** — sugerir al usuario sinónimos o ampliar jurisdicción.
- **Demasiados resultados (>50)** — sugerir filtrar por `rank` o por status.
- **El término aparece en muchos títulos administrativos genéricos** (típico con "energía" en boletines autonómicos) — sugerir filtrar por rango legal sustantivo (RD, Ley) en vez de Resolución.
