---
name: demanda-real
description: "Devuelve la demanda eléctrica real peninsular española (MW), hora a hora. Soporta rango temporal, agregación y comparativa contra demanda prevista. Use when the user says 'demanda eléctrica hoy', 'cuánta luz consumimos ayer', 'demanda peninsular última semana', 'pico de demanda en <periodo>', 'demanda real vs prevista'. Llama al tool ESIOS para el indicador de demanda real (ID ESIOS oficial; el MCP también acepta 'demanda real')."
argument-hint: "<rango temporal> [agregación] [vs-prevista]"
---

# Demanda eléctrica real peninsular

Demanda eléctrica horaria medida por REE en el sistema peninsular español. Útil para análisis de carga, picos, comparativas estacionales, y validación de modelos de previsión propios.

## Pasos al ejecutarse

1. **Parsear el rango temporal** — mismas reglas que `/esios:precio-md`. Sin rango → preguntar.
2. **Parsear agregación** (default horario): horario, diario (suma o media — preguntar cuál si no está claro; default suma porque la demanda en MW × horas = MWh diarios), mensual, anual.
3. **Detectar si el usuario pide comparativa con demanda prevista**:
   - "real vs prevista" / "desvío de previsión" / "qué tan bien predijimos" → activar modo comparativa, llamar también al indicador de demanda prevista
   - default solo demanda real
4. **Llamar tools** ESIOS para el(los) indicador(es) en el rango pedido.
5. **Presentar**:
   - Modo simple: tabla cronológica con MW por intervalo + pico horario en el rango con su timestamp.
   - Modo comparativa: tabla con tres columnas (timestamp, real, prevista, desvío_MW, desvío_%) + resumen final (MAPE — Mean Absolute Percentage Error — del periodo).
6. **Añadir contexto**: comparación con el mismo periodo del año anterior si el rango lo permite (señalar tendencia).

## Ejemplos esperados

<!-- TODO validate live cuando el MCP esté accesible en sesión -->

- *"demanda peninsular hoy"* → tabla horaria.
- *"pico de demanda del invierno 2025"* → encontrar el máximo horario en dic 2024–feb 2025 y devolverlo con su fecha/hora exacta.
- *"qué tan bien predijimos la demanda esta semana"* → modo comparativa real vs prevista, MAPE semanal.
- *"demanda media en agosto 2025"* → agregación mensual.

## Caveats

- **Datos provisionales vs definitivos**: la demanda en tiempo real es provisional las primeras 24-48h. Si el usuario pide algo de las últimas horas, marcar "provisional, sujeto a revisión". Para análisis serios sugerir esperar a la consolidación.
- **Cambios de hora (DST)**: igual que en precio-md, reportar dato bruto.
- **No incluye islas**: este indicador es peninsular. Si el usuario pregunta por Canarias o Baleares, advertir y sugerir el indicador específico de sistemas insulares (si está disponible en el MCP).
- **Anomalías históricas**: cortes generalizados, COVID, etc. — devolver el dato literal sin "suavizar" pero comentar si pasa por un periodo conocido de anomalía.
