---
name: explorar-ley
description: "Devuelve la estructura jerárquica completa (TOC) de una ley — títulos, capítulos, secciones, artículos, anexos — junto con metadatos como estado, versión consolidada vigente, lista de versiones disponibles y rango. Útil para entender la organización de una ley antes de leer artículos concretos. Use when the user says 'estructura de la <ley>', 'índice del RD <N>', 'qué tiene la <ley>', 'TOC de <X>', 'cuántos artículos tiene <X>', 'capítulos del Real Decreto <N>'. Llama a `mcp__lex__explore_law`."
argument-hint: "<ley o law_id>"
---

# Explorar la estructura de una ley

TOC navegable + metadatos. Skill de orientación: el usuario usa esto antes de pedir un artículo concreto.

## Pasos al ejecutarse

1. **Resolver al `law_id`** si el usuario dio una cita textual (`mcp__lex__list_laws` con jurisdicción inferida). Si la cita es ambigua y devuelve varias leyes, pedir confirmación.
2. **Llamar** `mcp__lex__explore_law(law_id=<resuelto>, format='toon', view='summary')`. El `format='toon'` da una tabla compacta; cambiar a `view='full'` solo si el usuario pide explícitamente "todos los detalles" (incluye modificadores, versiones disponibles, referencias entrantes).
3. **Presentar el resultado** organizado por nivel jerárquico:
   - Cabecera: título completo, jurisdicción, fecha publicación, estado, número total de unidades, fecha de versión consolidada vigente.
   - TOC indentada por niveles (libro > título > capítulo > sección > artículo). Cada entrada con su `unit_number` y `name` corto.
   - Si el usuario pidió `view='full'`, añadir al final: lista de normas modificadoras (citas con BOE id), versiones disponibles (con fechas), referencias entrantes (qué otras leyes citan esta).
4. **Sugerir siguiente paso** — basado en la TOC, ofrecer al usuario el comando para leer un artículo concreto: *"para leer el Art. 4 usa `/lex:resolver-cita Art. 4 RD 244/2019`"*.

## Ejemplos

- *"estructura del RD 244/2019"*: resolver a `es-royal-decree-2019-04-05-244` y `explore_law(law_id=..., format='toon')`. Devuelve los 53 capítulos/artículos/disposiciones del Reglamento de Autoconsumo.
- *"cuántos artículos tiene la Ley del Sector Eléctrico"*: resolver `es-law-2013-12-26-24` → `explore_law` → contar entries con `unit_type='articulo'`.
- *"detalles completos del RD 244/2019 incluyendo modificaciones"*: añadir `view='full'` para incluir el bloque de `modifiers` y `available_versions`.

## Caveats

- Para leyes con muchos artículos (Ley del Sector Eléctrico tiene >100 artículos), el output puede ser largo. El `format='toon'` lo hace compacto, pero considera sugerir al usuario "¿quieres solo el índice de capítulos o los artículos completos?" antes de devolver todo.
- El campo `available_versions` solo aparece en `view='full'`. Si el usuario pregunta "qué versiones tengo disponibles" → forzar `view='full'`.
