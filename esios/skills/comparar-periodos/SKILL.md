---
name: comparar-periodos
description: "Compara cualquier indicador ESIOS (precio MD, demanda, generación por tecnología, banda secundaria, SRAD) entre dos rangos temporales y devuelve el delta absoluto y porcentual. Use when the user says 'compara precio MD enero 2025 vs enero 2026', 'cómo cambió la demanda este invierno vs el anterior', 'diferencia generación eólica Q1 vs Q4', 'evolución year-over-year de <indicador>'. Llama dos veces al tool ESIOS del indicador con los dos rangos y compone el resultado."
argument-hint: "<indicador> <periodo-A> <periodo-B>"
---

# Comparar dos periodos del mercado eléctrico

Year-over-year (o cualquier comparativa de dos rangos) sobre las series temporales que cubren las otras skills del plugin.

## Cuándo usar esta skill vs llamar dos veces a las otras

- **Usar esta skill** cuando el usuario pide explícitamente comparativa o delta: "diferencia de X entre A y B", "cómo cambió X de A a B", "year-over-year".
- **Usar las otras** (precio-md, demanda-real, etc.) cuando el usuario solo pide la serie de un periodo.

## Pasos al ejecutarse

1. **Parsear el indicador** del input:
   - "precio MD" / "precio mercado" → llamar el tool de precio MD
   - "demanda" → demanda real
   - "eólica" / "fotovoltaica" / "nuclear" / cualquier tecnología → generación por tecnología
   - "banda secundaria" / "BS3" → precio banda secundaria
   - "SRAD" → subastas SRAD
2. **Parsear los dos rangos temporales** (Periodo A, Periodo B):
   - Mismas reglas de parseo que skills anteriores
   - Si periodos son de longitud distinta, advertir al usuario que el % delta puede ser engañoso
3. **Llamar el tool ESIOS dos veces** con cada rango. En paralelo si el cliente lo permite.
4. **Calcular agregados** para cada periodo: media (para precios), suma (para volumen demanda/generación).
5. **Componer respuesta**: tabla con valor_A, valor_B, delta_absoluto, delta_porcentual, junto con un comentario interpretativo (en lenguaje natural) — *"el precio MD ha subido un X% en enero 2026 respecto a enero 2025, lo cual es consistente con/atípico para el contexto..."*.
6. **Sugerir profundizar**: si la diferencia es grande, ofrecer skills relacionadas — p. ej., para una subida de precio MD ofrecer cruzar con `/esios:generacion-por-tecnologia` para ver si fue por menos renovable.

## Ejemplos esperados

<!-- TODO validate live cuando el MCP esté accesible en sesión -->

- *"precio MD enero 2025 vs enero 2026"* → comparativa mensual.
- *"demanda peninsular Q1 2024 vs Q1 2025"* → suma Q1 cada año.
- *"generación eólica enero 2025 vs enero 2026"* → solo eólica, dos meses.
- *"BS3 invierno 2024-25 vs invierno 2025-26"* → media estacional.

## Caveats

- **Periodos de longitud distinta**: el % es engañoso. Sugerir normalizar (p. ej. "media diaria" en lugar de "total").
- **Estacionalidad**: comparar enero vs julio no tiene sentido para demanda. La skill debe detectar y avisar.
- **Reformas regulatorias mid-periodo** (p. ej. cambio del mecanismo SRAD): el delta puede reflejar el cambio de mecanismo, no del mercado per se. Si la skill detecta una norma modificadora entre las dos fechas (cruce con `/lex:comparar-versiones` sobre la norma reguladora del indicador), advertir.
