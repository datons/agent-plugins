---
title: Tutorial Plugin - Precio MD Demo
version: 0.1.0
author: Datons (tutorial)
---

# Tutorial: Plugin de ejemplo — `precio-md-demo`

Este skill es un plugin de ejemplo ficticio creado para un tutorial. Simula una consulta simple al precio del Mercado Diario (MD) y muestra cómo estructurar las entradas y la respuesta.

## Comportamiento

- Entrada esperada: `precio-md-demo <rango>` (p. ej. `precio-md-demo última semana`).
- Parseo sencillo de rango (hoy / ayer / últimos 7 días / fecha exacta).
- Llamada ficticia al servicio ESIOS para obtener `precio_md` (en un tutorial real, reemplazar por la llamada MCP correspondiente).
- Salida: tabla con `timestamp` y `precio €/MWh` + resumen estadístico (min, max, media).

## Ejemplo

- Usuario: `precio-md-demo última semana`
- Respuesta (ejemplo):
  - Tabla con 168 filas (24h × 7d) mostrando precios horarios.
  - Resumen: `min=10.2 €/MWh @ 2026-05-13T03:00`, `max=145.6 €/MWh @ 2026-05-15T19:00`, `media=52.3 €/MWh`.

## Nota para el tutorial

Este archivo es sólo un ejemplo pedagógico. Para implementarlo funcionalmente:

1. Añadir un controlador que traduzca el texto del usuario a parámetros de fecha.
2. Llamar `mcp_esios-data_query` o el tool ESIOS interno para `precio_md`.
3. Formatear y paginar la respuesta si es larga (>50 puntos).

---
