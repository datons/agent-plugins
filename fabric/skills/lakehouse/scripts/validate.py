# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["mssql-python==1.6.0", "azure-identity"]
# ///
"""Ejecuta cada consulta de queries_dir con sus parámetros `example` y comprueba que devuelve filas y que no hay duplicados en el grano declarado. Uso: uv run validate.py [fabric.toml] [consulta.sql ...]"""

import sys
import tomllib
from pathlib import Path

import mssql_python

REQUIRED = ("description", "params", "example", "grain", "validated", "reviewer")


def header(sql: str) -> dict[str, str]:
    meta = {}
    for line in sql.splitlines():
        if not line.startswith("--"):
            break
        key, sep, value = line[2:].partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    return meta


cfg_path = Path(sys.argv[1] if len(sys.argv) > 1 else "fabric.toml")
cfg = tomllib.loads(cfg_path.read_text())["fabric"]
queries_dir = cfg_path.parent / cfg.get("queries_dir", "consultas")
files = [Path(f) for f in sys.argv[2:]] or sorted(queries_dir.glob("*.sql"))
conn_str = f"Server={cfg['sql_server']};Database={cfg['database']};Authentication=ActiveDirectoryDefault;Encrypt=yes"

failed = 0
with mssql_python.connect(conn_str) as conn:
    for f in files:
        sql = f.read_text()
        meta = header(sql)
        problems = [f"falta '{k}' en la cabecera" for k in REQUIRED if k not in meta]
        rows = cols = []
        if not problems:
            params = tuple(p.strip() for p in meta["example"].split(",")) if meta["example"] else ()
            if len(params) != sql.count("?"):
                problems.append(f"example tiene {len(params)} valores y la consulta {sql.count('?')} parámetros")
            else:
                try:
                    with conn.cursor() as cur:
                        cur.execute(sql, params) if params else cur.execute(sql)
                        cols = [c[0] for c in cur.description]
                        rows = [tuple(r) for r in cur.fetchall()]
                except Exception as e:  # noqa: BLE001 (report the driver error verbatim)
                    problems.append(f"{type(e).__name__}: {str(e)[:300]}")
        if not problems and not rows:
            problems.append("no devuelve filas con los parámetros de example")
        if not problems:
            # grain is "una fila por a y b": check those columns are unique when they exist in the result.
            keys = [c for c in cols if c in meta["grain"]]
            if keys and len({tuple(r[cols.index(k)] for k in keys) for r in rows}) != len(rows):
                problems.append(f"filas duplicadas para el grano ({', '.join(keys)})")
        status = "OK" if not problems else "FALLO"
        failed += bool(problems)
        print(f"[{status}] {f.name}" + (f" ({len(rows)} filas)" if not problems else "") + "".join(f"\n       {p}" for p in problems))

print(f"\n{len(files) - failed}/{len(files)} consultas válidas.")
sys.exit(1 if failed else 0)
