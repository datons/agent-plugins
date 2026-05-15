---
name: citar-formato
description: "Estandariza una cita legal en formato canónico, devolviendo simultáneamente: cita BOE oficial, identificador ELI, URL pública del BOE, URL datons.com, y cita estilo Bluebook/APA para uso académico. Útil cuando un dev o abogado está redactando un documento y necesita una cita correcta y completa. Use when the user says 'formato canónico de <cita>', 'cómo cito el art. X correctamente', 'BOE id del Real Decreto Y', 'ELI de la Ley X', 'dame la URL oficial de <cita>'. Resuelve la cita vía `mcp__lex__list_laws` + `mcp__lex__read_unit` y devuelve los metadatos de identificación sin el contenido."
argument-hint: "<cita>"
---

# Formato canónico de una cita legal

A diferencia de `/lex:resolver-cita` (que devuelve TEXTO), esta skill devuelve **identificadores** — la información que necesita un documento para referenciar correctamente la norma.

## Por qué esta skill existe

Una cita legal correcta tiene cuatro componentes: cita textual estándar; URL oficial del BOE; identificador ELI (European Legislation Identifier, formato URI estable); identificador interno datons (`law_id`). Reunirlos todos requiere llamadas separadas. Esta skill las orquesta y devuelve un bloque copy-pasteable.

## Pasos al ejecutarse

1. **Resolver la cita** vía `mcp__lex__list_laws(jurisdiction=<inferida>, q='<número>/<año>')`.
2. **Si la cita incluye un artículo concreto**, llamar también `mcp__lex__read_unit(law_id=..., unit_type=..., number=..., format='text')` — pero solo para obtener metadatos (path, BOE oficial con anchor al artículo, fecha consolidada). El texto del artículo NO se incluye en la respuesta.
3. **Componer respuesta** con cinco bloques:
   - **Cita estándar BOE**: "Real Decreto 244/2019, de 5 de abril, art. 4."
   - **BOE id**: `BOE-A-2019-5089` (extraído del `official_url`).
   - **ELI**: `https://www.boe.es/eli/es/rd/2019/04/05/244` (campo `eli_url` del meta).
   - **URL oficial BOE con anchor**: `https://www.boe.es/buscar/act.php?id=BOE-A-2019-5089#a4`.
   - **URL datons.com**: `https://datons.com/apps/lex/es/es-royal-decree-2019-04-05-244/doc/<unit_id>`.
4. **Si el usuario pide estilo académico** (Bluebook, APA, ICCJ), añadir esa variante. Esto es opcional — el default es solo los identificadores oficiales.

## Ejemplo

Input: "cómo cito el art. 4 RD 244/2019".

Output esperado (estructura):

- Cita BOE: "Real Decreto 244/2019, de 5 de abril, por el que se regulan las condiciones administrativas, técnicas y económicas del autoconsumo de energía eléctrica, art. 4."
- BOE id: BOE-A-2019-5089
- ELI: https://www.boe.es/eli/es/rd/2019/04/05/244
- BOE oficial con anchor: https://www.boe.es/buscar/act.php?id=BOE-A-2019-5089#a4
- datons.com: https://datons.com/apps/lex/es/es-royal-decree-2019-04-05-244

## Caveats

- **Esta skill no es "solo formato" — llama al MCP para obtener los identificadores reales.** No inventar URLs ni IDs.
- Si la cita es ambigua (mis-resolución posible), aplicar las mismas reglas de jurisdicción forzada que `/lex:resolver-cita`.
- Si el `eli_url` no aparece en el meta de la ley (algunas resoluciones autonómicas no tienen ELI oficial), omitir esa línea y avisarlo: "ELI no disponible para esta norma".
