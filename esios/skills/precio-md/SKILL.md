---
name: precio-md
description: "Devuelve el precio del Mercado Diario (precio MD) en €/MWh para España y/o Portugal, hora a hora. Soporta rango de fechas, agregación (horaria/diaria/semanal/mensual) y filtro por país. Use when the user says 'precio MD hoy', 'precio mercado diario última semana', 'evolución precio eléctrico', 'cuánto costó la luz en <fecha>', 'precio MIBEL en <periodo>', 'precio MD por hora ayer'. Llama al tool ESIOS para el indicador de precio MD (ID 600 oficial ESIOS, o nombre 'precio mercado diario')."
argument-hint: "<rango temporal> [agregación] [país]"
---

# Precio del Mercado Diario (MD)

Precio horario del mercado mayorista MIBEL — referencia base para la facturación de consumidores y para análisis de mercado.

## Pasos al ejecutarse

1. **Parsear el rango temporal**:
   - "hoy" → desde 00:00 de hoy hasta ahora
   - "ayer" → 00:00–23:59 del día anterior
   - "última semana" / "últimos 7 días" → desde -7d hasta hoy
   - "este mes" → desde día 1 del mes actual
   - "<fecha concreta>" → ese día completo
   - "<fecha-A> a <fecha-B>" → rango explícito
   - Sin fecha → preguntar al usuario antes de consultar (la serie histórica es muy larga, descargarla entera es desperdicio).
2. **Parsear agregación** (opcional, default horaria):
   - "por hora" / "horario" → resolución original (24 puntos/día)
   - "por día" / "media diaria" → agrupar a 1 punto/día (media o suma según métrica)
   - "por semana" / "por mes" → agrupar
3. **Parsear país** (opcional, default ES):
   - Si menciona "Portugal" → PT
   - Si menciona "ambos" / "MIBEL completo" → devolver ES y PT lado a lado
4. **Llamar el tool ESIOS** para el indicador `precio_md` con los parámetros derivados.
5. **Presentar**: tabla con timestamp + precio €/MWh, ordenada cronológicamente. Si la serie es larga (>50 puntos), proponer un resumen estadístico (min, max, media, mediana) en lugar de tabla completa.
6. **Añadir contexto**: el último precio publicado, la diferencia con el día anterior, si está por encima/debajo del precio medio del mes.

## Ejemplos esperados

<!-- TODO validate live cuando el MCP esté accesible en sesión -->

- *"precio MD hoy"* → tabla horaria de las 24 horas, hora actual marcada.
- *"precio MD ayer comparado con hace una semana"* → dos series superpuestas con diferencia horaria.
- *"media mensual del precio MD en 2025"* → agregación mensual, 12 puntos.
- *"precio MD máximo y mínimo del último año"* → resumen estadístico + las dos horas concretas donde se dio cada extremo.

## Caveats

- **Festivos y fines de semana**: el precio MD se subasta también esos días pero la dinámica es distinta. Si la pregunta es analítica, sugerir excluir/incluir explícitamente.
- **Cambios de hora (DST)**: días con 23 o 25 horas. Reportar el dato bruto sin "corregir" y comentar la anomalía.
- **Precios negativos** (raros pero reales en horas de alta renovable): devolver el valor literal sin filtrar.
- **Latencia del dato**: el precio MD del día D se publica el día D-1 a las 13:00. Si el usuario pide "precio MD mañana" y aún no se ha publicado, devolver "aún no disponible, publicación a las 13:00".
