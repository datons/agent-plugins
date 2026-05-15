# datons agent-plugins

Plugins for Claude Code, Claude Desktop, VSCode Copilot Chat, and other agent-plugin-compatible clients. Each plugin bundles an MCP server hosted at `mcp.datons.com` plus skills that exercise it from natural-language prompts.

## Plugins

- **`lex`** — Spanish, Italian and Chilean legislation. 101K+ laws, 700K+ legal units from BOE (Spain), Gazzetta Ufficiale (Italy), Diario Oficial (Chile). Citation resolution, full-text and faceted search, version comparison, time-travel queries to any historical version of an article.
- **`esios`** — Iberian electricity market (MIBEL) data via the ESIOS API of REE (Spanish system operator). Daily market prices, demand, generation by technology, balancing services (SRAD), historical comparisons.

## Install

### Claude Code (CLI or VSCode extension)

```
/plugin marketplace add github:datons/agent-plugins
/plugin install lex@datons
/plugin install esios@datons
```

Or via terminal:

```bash
claude plugin marketplace add github:datons/agent-plugins
claude plugin install lex@datons
```

### VSCode Copilot Chat (agent mode)

Command Palette → **Chat: Install Plugin From Source** → enter `https://github.com/datons/agent-plugins`.

Requires `chat.plugins.enabled` (org-managed setting, currently in preview).

## Authentication

Both MCPs use OAuth. The first time a skill invokes a tool, your agent client opens a browser to `mcp.datons.com` for authentication. Subsequent calls reuse the cached token.

A datons.com account is required. Sign up at <https://datons.com>.

## Repository structure

```
agent-plugins/
├── .claude-plugin/marketplace.json
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── lex/
│   ├── .claude-plugin/plugin.json
│   ├── .mcp.json                            (MCP server registration)
│   ├── README.md                            (plugin-specific doc)
│   └── skills/<skill-name>/SKILL.md         (one folder per skill)
└── esios/
    └── (same structure)
```

## Trust

These plugins register MCP servers hosted by datons. Review each plugin's `.mcp.json` and `README.md` before installing. The skills documented here always route through the MCP — they don't ship cached or hardcoded data. This means responses are live, timestamped and traceable to the official source (BOE, REE, etc.).

## License

[MIT](./LICENSE).
