---
name: precio-banda-secundaria
description: "Devuelve los precios horarios de banda secundaria (servicio de regulación a subir y a bajar) en €/MW, asignados por REE. La banda secundaria es uno de los componentes de los sobrecostes de servicios de ajuste que se repercuten en consumidores. Use when the user says 'precio banda secundaria', 'BS3', 'precio regulación secundaria', 'costes servicios ajuste', 'precio reserva potencia secundaria'. Llama al tool ESIOS del indicador de banda secundaria (precio a subir + precio a bajar)."
argument-hint: "<rango temporal> [direccion: subir | bajar | ambos]"
---

# Precio de banda secundaria

Servicio de ajuste del sistema eléctrico que cubre desviaciones a corto plazo entre generación y demanda. Tiene dos direcciones — banda a subir (asegurar capacidad de aumentar generación) y a bajar (asegurar capacidad de reducirla). El precio asignado se repercute proporcionalmente a las instalaciones de los consumidores via el componente BS3 de la factura.

## Por qué importa

Este precio se repercute proporcionalmente a las instalaciones del consumidor a través del componente BS3 de los servicios de ajuste, y entra en cualquier cálculo de sobrecostes de mercado por instalación. Útil para reconciliar valores reportados internamente contra la fuente oficial REE.

## Pasos al ejecutarse

1. **Parsear rango temporal**.
2. **Parsear dirección**: "subir" / "bajar" / "ambos" (default ambos).
3. **Llamar tool ESIOS** del indicador correspondiente — son dos indicadores distintos en ESIOS, uno por dirección.
4. **Presentar** tabla horaria con timestamp + precio_subir + precio_bajar (si ambos). Si rango largo, resumen estadístico (media, max, min).
5. **Contexto**: añadir cita rápida a la regulación — la banda secundaria está regulada por el P.O.7.2 del Procedimiento de Operación de REE. Sugerir `/lex:buscar-norma P.O.7.2 banda secundaria` para el texto vigente.

## Ejemplos esperados

<!-- TODO validate live cuando el MCP esté accesible en sesión -->

- *"precio banda secundaria ayer"* → tabla horaria con ambas direcciones.
- *"BS3 esta semana, solo a subir"* → solo dirección subir.
- *"comparar precios BS3 enero 2025 vs enero 2026"* → composición con `/esios:comparar-periodos`.

## Caveats

- **Asignación vs liquidación**: el precio asignado en subasta puede diferir del precio liquidado final si REE aplica cobertura ex-post. La skill devuelve el precio publicado oficial en ESIOS; para liquidaciones exactas hay que cruzar con otros datos.
- **Banda terciaria y desvíos** son servicios distintos con precios distintos. Esta skill cubre solo banda secundaria. Para terciaria → indicador RAD3 (otra skill futura, no en v0.1).
