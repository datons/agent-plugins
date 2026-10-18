---
name: lakehouse
description: "Consulta un lakehouse de Microsoft Fabric desde Python en el ordenador del usuario y con su propia identidad de Microsoft: SQL analytics endpoint con mssql-python y tablas Delta de OneLake con deltalake. Prioriza las consultas validadas del equipo y comprueba el acceso. Use when the project has a fabric.toml, or the user says 'consulta el lakehouse', 'qué tablas hay en Fabric', 'lee la tabla X del datalake', 'comprueba mi acceso a Fabric', 'conéctate a OneLake', 'guarda esta consulta como validada'."
argument-hint: "[pregunta sobre los datos]"
---

# Lakehouse de Microsoft Fabric desde Python

Escribe Python normal sobre las librerías oficiales de Microsoft. No hay paquete intermedio: la conexión son cinco líneas y el usuario debe poder leerlas.

Las rutas `scripts/...` de esta skill son relativas a la carpeta de la skill.

## 1. Lee la configuración del proyecto

Busca `fabric.toml` en la raíz del proyecto. Si no existe, pide los valores al usuario (los tiene su equipo de IT) y créalo:

```toml
[fabric]
tenant = "<tenant-id>"
sql_server = "<id>.datawarehouse.fabric.microsoft.com"   # lakehouse > SQL analytics endpoint > cadena de conexión
database = "<nombre del lakehouse>"
workspace_id = "<guid del workspace>"   # solo para leer Delta desde OneLake
lakehouse_id = "<guid del lakehouse>"   # solo para leer Delta desde OneLake
tables_guide = "docs/tablas.md"         # opcional: qué significa cada tabla
queries_dir = "consultas"               # opcional: consultas validadas del equipo
```

Si hay `tables_guide`, léelo antes de escribir ninguna consulta: ahí están el significado, el grano y las unidades de las tablas.

`fabric.toml` no contiene secretos, pero describe la infraestructura del cliente: no copies sus valores en código, ejemplos ni repositorios compartidos. Léelos del fichero al ejecutar.

## 2. Comprueba el acceso primero

Ejecuta la comprobación una vez por equipo, o cuando falle una conexión:

```bash
uv run scripts/check.py fabric.toml
```

Informa OK/FALLO de: configuración, Azure CLI, conexión SQL (y con qué usuario) y tablas visibles. Si algo falla, muestra al usuario el arreglo exacto que imprime el script; no improvises atajos ni otras credenciales.

El inicio de sesión es `az login --tenant <tenant>` (con `--allow-no-subscriptions` si la cuenta no tiene suscripción de Azure). Fabric aplica a cada consulta los permisos del propio usuario.

## 3. Conecta y consulta (SQL analytics endpoint)

Los scripts declaran sus dependencias en la cabecera para que `uv run script.py` funcione sin instalar nada. Fija `mssql-python==1.6.0`: la 1.7.0 falla en macOS con Python 3.12.

```python
# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["mssql-python==1.6.0", "azure-identity", "pandas"]
# ///
import tomllib
from pathlib import Path

import mssql_python
import pandas as pd

cfg = tomllib.loads(Path("fabric.toml").read_text())["fabric"]


def query(sql: str, params: tuple = ()) -> pd.DataFrame:
    conn_str = f"Server={cfg['sql_server']};Database={cfg['database']};Authentication=ActiveDirectoryDefault;Encrypt=yes"
    with mssql_python.connect(conn_str) as conn, conn.cursor() as cur:
        cur.execute(sql, params) if params else cur.execute(sql)
        return pd.DataFrame.from_records([tuple(r) for r in cur.fetchall()], columns=[c[0] for c in cur.description])
```

`ActiveDirectoryDefault` usa la sesión de Azure CLI: no hace falta gestionar tokens ni instalar el driver ODBC.

## 4. Primero, las consultas validadas

Si hay `queries_dir`, busca ahí antes de escribir SQL. Una consulta validada es la respuesta acordada por el equipo a una pregunta: si encaja, ejecútala tal cual con `query(Path(fichero).read_text(), params)` y di qué fichero has usado. No cambies su SQL sobre la marcha; si necesita un cambio, propón el cambio en el fichero.

Si ninguna encaja, escribe una consulta a medida (pasos 5 y 6) y marca el resultado como **no validado**. Si el usuario la va a reutilizar, ofrece guardarla en `queries_dir` como borrador con `validated: pendiente`; la valida el revisor del equipo mediante la revisión del repositorio.

Cada consulta es un fichero `.sql` con una cabecera de comentarios. Todas las claves son obligatorias salvo `notes`:

```sql
-- description: qué pregunta responde, en una frase
-- params: nombre (significado/formato), en el orden de los ?
-- example: valor1, valor2
-- grain: una fila por <col> y <col>
-- validated: AAAA-MM-DD o pendiente
-- reviewer: equipo o rol que la valida
-- notes: trampas que resuelve
SELECT ...
```

Comprueba todas las consultas, o las que hayas tocado, con:

```bash
uv run scripts/validate.py fabric.toml [fichero.sql ...]
```

Ejecuta cada una con sus valores de `example` y falla si falta una clave de la cabecera, si no cuadra el número de parámetros, si no devuelve filas o si hay filas duplicadas para las columnas de `grain`. Pasar el validador no hace válida una consulta: solo el revisor pone la fecha en `validated`.

## 5. Explora antes de consultar

No inventes nombres de tablas ni de columnas. Lista y describe primero:

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, '[' + TABLE_SCHEMA + '].[' + TABLE_NAME + ']' AS sql_name
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA NOT IN ('sys', 'INFORMATION_SCHEMA', 'queryinsights', '_mlv_system');

SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? ORDER BY ORDINAL_POSITION;
```

Mira unas filas (`SELECT TOP 5 *`) y, antes de agregar, el rango de fechas de cada valor de las columnas de categoría (resolución, versión, sesión). Las categorías que se solapan cuentan dos veces al sumar, y las versiones acumuladas (una foto completa por sesión) no se suman nunca. Lo que aprendas de una tabla va al `tables_guide` del proyecto, no a comentarios en el código.

## 6. Reglas de SQL (T-SQL en el SQL analytics endpoint)

- Los nombres de tabla pueden llevar puntos (`origen.tabla` dentro del esquema `dbo`). Usa siempre el `sql_name` entre corchetes: `[dbo].[origen.tabla]`.
- `TOP n`, no `LIMIT n`.
- Filtra por fecha y agrega en SQL; no traigas tablas enteras a pandas.
- Los valores van como parámetros `?`, nunca formateados dentro del SQL.
- Hay columnas guardadas como texto (fechas, cuartos de hora): mira `DATA_TYPE` y convierte explícitamente.
- El endpoint es de solo lectura: solo SELECT.
- En tablas que son accesos directos, `INFORMATION_SCHEMA.COLUMNS` puede venir vacío; entonces usa `SELECT TOP 5 *` para ver las columnas.

## 7. Tablas que el endpoint SQL no puede leer: Delta en OneLake

El endpoint SQL no transporta NaN ni Infinity en columnas decimales: la lectura entera falla con un error de conversión. Para esas tablas lee los ficheros Delta directamente; los NaN llegan intactos y los limpias en pandas:

```python
# dependencies = ["deltalake", "pandas", "pyarrow"]
from deltalake import DeltaTable

url = f"abfss://{cfg['workspace_id']}@onelake.dfs.fabric.microsoft.com/{cfg['lakehouse_id']}/Tables/dbo/<tabla>"
df = DeltaTable(url, storage_options={"use_azure_cli": "true", "use_fabric_endpoint": "true"}).to_pandas()
```

Un 403 `User is not authorized ... for workspace` en un acceso directo significa que el usuario no tiene lectura en OneLake sobre el workspace *de origen*. Es un permiso que da su equipo de IT, no un problema del código.

## 8. Errores

| Error | Qué significa | Arreglo |
|---|---|---|
| `DefaultAzureCredential failed` / sin sesión de Azure CLI | No ha iniciado sesión, o la tiene en otro tenant | `az login --tenant <tenant>` |
| `Login failed` / `Cannot open database` | Sesión correcta, pero sin acceso a ese lakehouse | Pedir a IT lectura sobre el SQL analytics endpoint |
| `Invalid object name` | Esquema equivocado o nombre con puntos sin corchetes | Usar el `sql_name` del paso 5 |
| Error de conversión / NaN en una columna decimal | El endpoint SQL no transporta NaN | Leerla desde OneLake (paso 7) |
