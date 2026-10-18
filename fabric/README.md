# fabric

Skill to work with a Microsoft Fabric lakehouse from Python on your own machine, with your own Microsoft identity. Fabric applies your existing permissions to every query; nothing is stored besides your Azure CLI session.

Unlike the other plugins in this marketplace, `fabric` has no MCP server: Claude writes plain Python against Microsoft's official libraries (`mssql-python` for the SQL analytics endpoint, `deltalake` for OneLake Delta tables).

## Install

Claude Code:

```
/plugin install fabric --marketplace datons/agent-plugins
```

Codex: `codex plugin marketplace add datons/agent-plugins`, then `codex plugin add fabric@datons`.

## Requirements

- Azure CLI, signed in with `az login --tenant <tenant-id>`.
- `uv`, to run scripts with inline dependencies.
- Read access to the lakehouse's SQL analytics endpoint, granted by your IT team.

## Project setup

Add a `fabric.toml` at the root of your project. Your IT team has the values:

```toml
[fabric]
tenant = "<tenant-id>"
sql_server = "<id>.datawarehouse.fabric.microsoft.com"
database = "<lakehouse name>"
workspace_id = "<workspace guid>"   # only for OneLake Delta reads
lakehouse_id = "<lakehouse guid>"   # only for OneLake Delta reads
tables_guide = "docs/tablas.md"     # optional
queries_dir = "consultas"           # optional
```

Then ask Claude to check your access (`/fabric:lakehouse comprueba mi acceso`) or just ask a question about the data.

## Validated queries

A team can keep its agreed queries as `.sql` files in `queries_dir`, each with a header (`description`, `params`, `example`, `grain`, `validated`, `reviewer`). The skill uses a validated query when one fits, labels anything else as not validated, and `scripts/validate.py` runs every query with its example parameters to catch empty results and duplicate rows. See `skills/lakehouse/SKILL.md`.

## Install it for a whole team

Put this in the team repository's `.claude/settings.json`; anyone who opens the repository in Claude Code and trusts it gets the plugin:

```json
{
  "extraKnownMarketplaces": {
    "datons": { "source": { "source": "github", "repo": "datons/agent-plugins" } }
  },
  "enabledPlugins": { "fabric@datons": true }
}
```

## Where it works

Claude Code (terminal, IDE, and the Code tab of Claude Desktop) and Codex. Not in claude.ai chat: its sandbox has no access to your Azure CLI session or your network.
