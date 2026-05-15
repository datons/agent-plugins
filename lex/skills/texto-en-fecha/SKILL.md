---
name: texto-en-fecha
description: "Devuelve el texto literal de un artículo tal como estaba vigente en una fecha pasada. Útil para análisis retrospectivos: 'qué decía exactamente el art. 14 LSE en 2020' o 'cuál era la modalidad de autoconsumo aplicable cuando se firmó este contrato en 2021'. Use when the user says 'qué decía el art. X en <fecha>', 'versión de la Ley X a fecha Y', 'texto vigente de <cita> en <año>', 'cómo era el art. X en <fecha>', 'a fecha <X> qué pone el artículo Y'. Llama a `mcp__lex__read_unit` con el parámetro `date` para obtener la consolidación histórica."
argument-hint: "<cita> <fecha YYYY-MM-DD>"
---

# Texto de un artículo en una fecha pasada

Time-travel sobre artículos individuales. Diferencia clave con `/lex:resolver-cita` es que esta devuelve la versión consolidada vigente a la fecha indicada, no la actual.

## Cuándo usar esta vs `comparar-versiones`

- **Esta skill**: el usuario quiere **un punto temporal**. "¿Qué decía el art. 14 en 2020?"
- **`comparar-versiones`**: el usuario quiere **un diff entre dos puntos** o un inventario de cambios. "¿Qué cambió en la LSE entre 2020 y 2023?"

## Pasos al ejecutarse

1. **Resolver la cita al `law_id`** + extraer `unit_type` y `number` (mismas reglas que `/lex:resolver-cita`).
2. **Parsear la fecha del usuario** a formato YYYYMMDD (sin guiones; lo que pide la tool). Aceptar `2020-01-15`, `15 enero 2020`, `enero 2020` (primer día del mes), `2020` (1 de enero como aproximación, pero **avisar al usuario** que es interpretación).
3. **Llamar** `mcp__lex__read_unit(law_id=..., unit_type=..., number=..., date='YYYYMMDD', format='text')`.
4. **Presentar** la respuesta con cabecera explícita: cita estandarizada + "versión consolidada vigente a fecha <X>" + texto literal + `consolidated_date` que devuelve la tool (puede no coincidir con la fecha pedida si no hubo cambios entre fechas — explicar al usuario).
5. **Opcional**: ofrecer comparar con la versión actual usando `/lex:comparar-versiones` en modo `unit` (`date1=<fecha-pedida>`, `date2=hoy`).

## Ejemplos

- *"qué decía el art. 14 LSE en 2020"*: resolver `es-law-2013-12-26-24`, llamar `read_unit(law_id=..., unit_type='articulo', number='14', date='20200101')`. El `consolidated_date` que vuelva será la última fecha de modificación ANTES o EN 2020-01-01.
- *"texto vigente del Art. 4 RD 244/2019 a fecha 31 marzo 2022"*: `read_unit(law_id='es-royal-decree-2019-04-05-244', unit_type='articulo', number='4', date='20220331')`. Útil para entender la versión del artículo antes de la reforma del RD-ley 18/2022 (que añadió el apartado 7).
- *"versión de la Ley 24/2013 art. 6 a 1 enero 2021"*: `read_unit(law_id='es-law-2013-12-26-24', unit_type='articulo', number='6', date='20210101')`.

## Caveats

- **Fecha anterior a la publicación de la ley** → la tool puede devolver 404 o la versión original. Si el usuario pidió una fecha pre-vigencia, advertir.
- **Artículo no existía en esa fecha** (añadido por una reforma posterior) → tool devuelve 404. Marcar al usuario "el art. X se añadió en YYYY-MM-DD; no existía a la fecha que pediste".
- **Texto consolidado vs texto auténtico** — la consolidación de datons cruza modificaciones; siempre coincide con el texto BOE consolidado oficial pero los timestamps de versión pueden estar 1-2 días desfasados del BOE oficial. Para auditoría estricta, devolver siempre el `official_url` para verificación cruzada.
