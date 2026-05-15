---
name: comparar-versiones
description: "Lista los cambios aplicados a una ley en una ventana temporal (qué artículos se modificaron, añadieron, derogaron, por qué normas modificadoras). Útil para regulatory monitoring y para entender el impacto de una reforma. Use when the user says 'qué cambió en la <ley/RD> de <año-A> a <año-B>', 'cambios en la Ley X desde <fecha>', 'qué modificó el RD <N> a la Ley X', 'reforma de <ley>', 'changelog del Real Decreto <X>'. Llama a `mcp__lex__compare_versions` en modo `changes` (por defecto) o `unit`/`law` cuando se pide diff específico."
argument-hint: "<ley o cita> [desde] [hasta]"
---

# Comparar versiones de una ley

Devuelve el inventario de cambios (additions, modifications, deletions) sobre una ley en un rango temporal.

## Tres modos del MCP tool, mapeados a tres patrones de pregunta del usuario

- **modo `changes` (defecto)** — *"¿qué cambios ha sufrido la Ley X?"*: lista todos los cambios con la norma modificadora, el `unit_type` y el `number` afectados. Útil para auditoría regulatoria.
- **modo `unit`** — *"¿qué cambió el art. 4 entre 2023 y 2024?"*: diff palabra-por-palabra de un artículo concreto entre dos fechas.
- **modo `law`** — *"diff completo entre la versión actual y la de hace un año"*: todos los artículos que cambiaron en la ventana, con sus diffs.

## Pasos al ejecutarse

1. **Resolver la ley al `law_id`** vía `mcp__lex__list_laws` si el usuario dio una cita textual. Si dio el `law_id` directo, usarlo.
2. **Inferir el modo** desde la pregunta:
   - "qué cambios", "changelog", "modificaciones" → `changes`
   - "qué cambió el art. X" → `unit` (requiere `unit_type`, `number`, `date1`, `date2`)
   - "diff entre versiones" sin artículo específico → `law` (requiere `since`, `until`)
3. **Inferir ventana temporal**:
   - "este año" → `since=YYYY-01-01`, `until=hoy`
   - "desde la última reforma" → buscar primero la fecha de última modificación con `explore_law` y usar esa como `since`
   - "todo el histórico" → omitir `since`/`until`
4. **Llamar** `mcp__lex__compare_versions(law_id=..., mode=..., since=..., until=..., min_change_chars=50)`. El filtro `min_change_chars=50` descarta typos y correcciones de erratas.
5. **Presentar** una tabla cronológica con: fecha del cambio; norma modificadora (cita + BOE id); unidad afectada (`unit_type` + `number`); tipo de cambio (added/modified/removed); número de caracteres cambiados (proxy de magnitud).
6. **Resumen al final** — número total de cambios en la ventana, normas modificadoras únicas (las "leyes que tocaron esta ley"), y % aproximado del articulado afectado.

## Ejemplos

- *"qué cambios ha sufrido el RD 244/2019 en 2025-2026"*: resolver a `es-royal-decree-2019-04-05-244` y llamar `compare_versions(law_id=..., mode='changes', since='2025-01-01', min_change_chars=50)`. Devuelve los cambios introducidos por RD-ley 7/2025, Ley 9/2025, RD-ley 7/2026 (vistos en validación del Art. 4).
- *"qué cambió el art. 4 entre 2024 y 2026"*: `compare_versions(law_id=..., mode='unit', unit_type='articulo', number='4', date1='20240101', date2='20260101')`.
- *"todo lo que cambió en la LSE desde la última reforma"*: primero `explore_law` para encontrar la fecha de última modificación, luego `compare_versions(mode='law', since=<esa-fecha>)`.

## Errores y caveats

- **Ley sin historial de versiones** (ley nueva, sin enmiendas) → devolver "Sin cambios registrados desde su publicación". Útil saberlo.
- **Ventana muy larga + ley muy modificada** (típico con la Ley del Sector Eléctrico) → puede devolver cientos de cambios. Sugerir filtrar por `keyword` o reducir ventana.
- **`mode='unit'` con `number` que no existe en una de las dos fechas** (artículo añadido o derogado entre fechas) → devolver el dato igualmente, marcando "creado en X" o "derogado en Y".
