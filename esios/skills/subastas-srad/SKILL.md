---
name: subastas-srad
description: "Devuelve resultados de las subastas SRAD (Servicios de Reserva Adicional a Disposición) de Red Eléctrica: precio marginal, volumen asignado, participantes (cuando público), por horizonte horario. SRAD es el servicio de capacidad firme de respaldo del sistema eléctrico peninsular. Use when the user says 'subastas SRAD', 'precio SRAD <fecha>', 'volumen subasta capacidad', 'resultados servicios de reserva', 'asignación SRAD última semana'. Llama al tool ESIOS del indicador SRAD."
argument-hint: "<rango temporal> [tipo: precio | volumen | ambos]"
---

# Subastas SRAD (Servicios de Reserva Adicional a Disposición)

SRAD es un mecanismo de mercado que asigna capacidad firme de generación o demanda para garantizar la seguridad de suministro. Los resultados son públicos vía ESIOS.

## Datos típicamente disponibles por subasta

- **Precio marginal de casación** (€/MW)
- **Volumen asignado** (MW por horizonte horario)
- **Fecha de subasta** y **horizontes de entrega**
- **Tipo de producto** (anual, mensual, semanal, según subasta)

## Pasos al ejecutarse

1. **Parsear rango temporal** — fecha de SUBASTA o fecha de ENTREGA según contexto. Si ambiguo, preguntar al usuario "¿la subasta celebrada en <fecha> o el horizonte de entrega <fecha>?".
2. **Parsear tipo** (default ambos): "precios" / "volúmenes" / "ambos".
3. **Llamar tool ESIOS** del indicador SRAD correspondiente.
4. **Presentar**: tabla cronológica con fecha subasta, horizonte de entrega, precio €/MW, volumen MW. Si el rango cubre múltiples subastas, agregar resumen estadístico (precio medio, volumen total).
5. **Contexto regulatorio**: añadir nota breve "SRAD se regula por <Resolución CNMC>; consulta `/lex:buscar-norma SRAD` para la normativa vigente". Esta es la pieza que conecta verticalmente con `/lex`.

## Ejemplos esperados

<!-- TODO validate live cuando el MCP esté accesible en sesión -->

- *"subastas SRAD última semana"* → tabla con las celebradas en últimos 7 días.
- *"precio SRAD diciembre 2025"* → solo precios, agregación mensual.
- *"volumen total asignado en SRAD 2025"* → suma anual de MW asignados.
- *"precio marginal SRAD vs ciclo combinado mismo periodo"* → cross-skill con `/esios:generacion-por-tecnologia` (ciclo combinado) y este precio SRAD; Claude orquesta ambos.

## Caveats

- **Subastas con baja participación**: en algunos horizontes, la subasta no se ha celebrado o ha quedado desierta. Marcar al usuario "horizonte sin asignación" en lugar de devolver 0.
- **Reformas del mecanismo**: SRAD ha evolucionado en su diseño desde 2022. Si el rango temporal cruza una reforma, advertirlo y enlazar a `/lex:comparar-versiones` sobre la norma reguladora.
- **Volúmenes en MW vs MWh**: SRAD asigna capacidad (MW); la utilización efectiva es otro indicador distinto. No confundirlos.
