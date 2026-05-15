---
name: generacion-por-tecnologia
description: "Devuelve el reparto de generación eléctrica por tecnología (nuclear, ciclo combinado, eólica, fotovoltaica, hidráulica, térmica renovable, otras) en MWh agregado por hora/día/mes. Soporta rango temporal y filtros por tecnologías concretas. Use when the user says 'generación por tecnología', 'cuánta eólica generamos', 'mix energético', 'producción solar última semana', 'cuota renovable en <periodo>', 'reparto generación <fecha>'. Llama a varios tools ESIOS — uno por tecnología — y compone una matriz temporal."
argument-hint: "<rango temporal> [tecnologías] [agregación]"
---

# Generación por tecnología

Reparto de la producción eléctrica peninsular por fuente — útil para análisis de mix energético, cuota renovable, dependencia de gas, etc.

## Tecnologías cubiertas

Eólica, solar fotovoltaica, solar térmica, hidráulica, nuclear, ciclo combinado (gas), cogeneración, biomasa/residuos, carbón (residual), bombeo, intercambios internacionales. El conjunto exacto disponible depende del MCP — el primer paso es resolver vía discovery si el usuario no especifica tecnologías.

## Pasos al ejecutarse

1. **Parsear rango temporal** (mismas reglas que skills anteriores).
2. **Parsear tecnologías** pedidas:
   - "todo el mix" / "todas las tecnologías" → consultar todas
   - "renovables" → subconjunto: eólica + solar FV + solar térmica + hidráulica + biomasa
   - Tecnologías concretas mencionadas ("eólica", "nuclear") → solo esas
3. **Parsear agregación** (default diario para análisis multi-día; horario solo si rango ≤ 48h).
4. **Llamar el(los) tool(s) ESIOS** — uno por tecnología. Si son muchas, paralelizar.
5. **Componer matriz**: filas = timestamps, columnas = tecnologías, valor = MWh (o MW si agregación horaria).
6. **Añadir totales** y **cuota porcentual** por tecnología sobre el total del periodo.
7. **Presentar**:
   - Tabla pivot (técnicas × timestamps) si el rango es corto
   - Resumen por tecnología (MWh totales, % del mix) si el rango es largo
   - Línea adicional: "cuota renovable" agregada (eólica + solar + hidráulica + biomasa, sobre el total).

## Ejemplos esperados

<!-- TODO validate live cuando el MCP esté accesible en sesión -->

- *"reparto de generación ayer"* → mix horario de las 24 horas del día anterior.
- *"cuota renovable este mes"* → suma renovable / total, %, evolución diaria.
- *"cuánta eólica generamos en enero 2026"* → solo eólica, agregación diaria, total mensual.
- *"comparar generación solar 2024 vs 2025"* → solo fotovoltaica, agregación mensual, dos años superpuestos.

## Caveats

- **Definición de "renovable" no es única**: REE clasifica algunas tecnologías de forma específica (la biomasa va en "renovable"; la cogeneración generalmente no, aunque algunas formas sí). El plugin sigue la clasificación ESIOS oficial; si el usuario pide una clasificación distinta (p. ej. la europea NACE), advertirlo.
- **Bombeo aparece como generación (bombeo turbinación) y como consumo (bombeo bombeo)** — en agregaciones, decidir cuál usar y explicarlo al usuario.
- **Intercambios internacionales no son generación interna** — si el usuario pide "generación peninsular", excluir; si pide "balance energético", incluir.
