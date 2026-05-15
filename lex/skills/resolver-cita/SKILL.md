---
name: resolver-cita
description: "Resuelve una cita textual (p. ej. 'Art. 4 RD 244/2019', 'art. 14 Ley 24/2013', 'art. 9.1.b LSE') y devuelve el contenido literal del artículo en su versión vigente, con la ruta jerárquica (capítulo/título), la URL oficial del BOE y un resumen de modificaciones aplicadas. Use when the user says 'qué dice el artículo X de Y', 'dame el texto del art. X', 'cita literal del art. X', 'resuélveme art. X de la Ley/RD Y', 'qué pone el art. X.Y del RD Z'. Llama a `mcp__lex__list_laws` para resolver la ley correctamente (fuerza jurisdicción) y luego `mcp__lex__read_unit` para leer el artículo. Esto es crítico porque `mcp__lex__resolve_citation` por sí solo puede mis-resolver a corpus italiano cuando hay ambigüedad."
argument-hint: "<cita textual> [jurisdicción]"
---

# Resolver cita legal

Resuelve una cita en lenguaje natural ("Art. 4 RD 244/2019") al texto literal del artículo, con metadatos legales que el agente legal necesita.

## Por qué este wrapper y no `resolve_citation` directamente

La tool `mcp__lex__resolve_citation` no sabe inferir jurisdicción. El corpus italiano tiene 65 931 leyes vs 17 880 españolas — una cita ambigua como "RD 244/2019" puede mis-resolver a un decreto italiano de 2025 con alta confianza. Esta skill **siempre fuerza la jurisdicción correcta** antes de leer.

## Pasos al ejecutarse

1. **Detectar jurisdicción** desde la cita:
   - `RD`, `Real Decreto`, `Ley orgánica`, `LSE` (Ley Sector Eléctrico), `Constitución Española`, `Resolución CNMC`, `Reglamento UE` aplicado en España → `jurisdiction='es'`
   - `Decreto Legislativo`, `Codice`, `Gazzetta Ufficiale` → `jurisdiction='it'`
   - `Diario Oficial`, `Ley chilena` → `jurisdiction='cl'`
   - Si no hay marcador claro, **preguntar al usuario** antes de seguir. No asumir.
2. **Extraer número y año** de la cita (regex sobre patrones tipo `244/2019`, `24/2013`, `RD 1955/2000`).
3. **Resolver la ley** llamando `mcp__lex__list_laws(jurisdiction=<x>, q='<número>/<año>', limit=5)`:
   - Si hay un resultado tipo `royal-decree` / `law` con el número/año exacto → ese es el `law_id`.
   - Si hay ambigüedad (varios resultados), pedir confirmación al usuario.
   - Si 0 resultados, devolver error claro: "No encuentro <cita> en la jurisdicción <x>. Verifica el número/año."
4. **Extraer unidad** de la cita:
   - `Art. 4` → `unit_type='articulo'`, `number='4'`
   - `Art. 4.1.b` → `unit_type='articulo'`, `number='4'` (los puntos son apartados; `read_unit` devuelve el artículo entero, el usuario localiza el apartado)
   - `Anexo I` → `unit_type='anexo'`, `number='1'`
   - `Disposición transitoria primera` → `unit_type='disposicion'`, `number='1'`
5. **Leer la unidad** llamando `mcp__lex__read_unit(law_id=<resuelto>, unit_type=..., number=..., format='text')`.
6. **Presentar al usuario** en este orden: cita estandarizada (`<rango> <número>/<año>, art. <X>` + título corto de la ley); ruta jerárquica del `path` que devuelve `read_unit`; texto literal del artículo (campo `content`); URL oficial del BOE (campo `official_url`); si hay modificaciones recientes detectadas en el content (líneas tipo "Se modifica el apartado X por ..."), listarlas como notas al pie; `law_id` y `consolidated_date` para auditoría.

## Ejemplos validados

### "Art. 4 RD 244/2019" → modalidades de autoconsumo

Pasos concretos:

- Paso 1: `mcp__lex__list_laws(jurisdiction='es', q='244/2019')` → `es-royal-decree-2019-04-05-244` (Reglamento de Autoconsumo)
- Paso 2: `mcp__lex__read_unit(law_id='es-royal-decree-2019-04-05-244', unit_type='articulo', number='4', format='text')`
- Devuelve: `path='Reglamento de Autoconsumo > CAPÍTULO I > Artículo 4'`, content con el texto literal del artículo, `official_url='https://www.boe.es/buscar/act.php?id=BOE-A-2019-5089#a4'`

Respuesta al usuario incluye: título "Real Decreto 244/2019, art. 4 — Clasificación de modalidades de autoconsumo", la ruta jerárquica, el texto literal completo, fecha de versión consolidada (2026-03-22), URL oficial BOE, y modificaciones detectadas (apartado 5 modificado por RD-ley 7/2026 BOE-A-2026-6544; apartado 7 añadido por RD-ley 18/2022 BOE-A-2022-17040).

### "Art. 14 Ley 24/2013" → LSE precios mercado

Pasos: `mcp__lex__list_laws(jurisdiction='es', q='24/2013')` → `es-law-2013-12-26-24` (Ley del Sector Eléctrico). Luego `mcp__lex__read_unit(law_id='es-law-2013-12-26-24', unit_type='articulo', number='14', format='text')`.

### Cita ambigua: "Art. 4 Decreto 244"

Sin año → preguntar al usuario: *"¿Te refieres al Real Decreto 244/2019 español sobre autoconsumo o a otro Decreto 244 de otra jurisdicción/año?"*. No asumir.

## Errores comunes

- **0 resultados en `list_laws`** — cita mal formateada o ley no en el corpus. Sugerir verificar número/año o probar `/lex:buscar-norma <tema>`.
- **`read_unit` devuelve 404** — el artículo no existe en esa ley (número fuera de rango). Sugerir `/lex:explorar-ley <law_id>` para ver la TOC.
- **Artículo existe pero está derogado** — devolver el texto igualmente + marcar el estado en la respuesta.
