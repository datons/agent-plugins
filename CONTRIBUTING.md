# Contributing to datons agent-plugins

Guide for adding new plugins, new skills, or fixing existing ones.

## Repository conventions

- One plugin per integration (one MCP service = one plugin). Follow Anthropic's `claude-plugins-official` pattern.
- Plugin names are lowercase kebab-case, short, descriptive (`lex`, `esios`, not `legal-corpus` or `iberian-electricity-market`).
- Skills inside a plugin use the same casing. Full slash command becomes `/<plugin>:<skill>` (e.g. `/lex:resolver-cita`).
- Spanish for user-facing strings (skill descriptions, error messages). English for code-internal docs (this file, plugin READMEs at high level).

## Add a new skill

```
<plugin>/skills/<skill-name>/
└── SKILL.md            (required)
```

Minimum `SKILL.md` frontmatter:

```markdown
---
name: <skill-name>
description: "Verb-first one-sentence summary in Spanish. Include 2-4 concrete trigger phrases the user would type. End with 'Use when ...'."
argument-hint: "<positional-args>"
---
```

Rules:

- `description` ≤ 1024 chars; third person; verb-first; **must** contain real trigger phrases (Claude uses these for skill discovery).
- `argument-hint` is a single short string shown in the autocomplete UI.
- Body of `SKILL.md` documents:
  1. When the skill applies and when not.
  2. The MCP tool(s) it calls and how it maps arguments.
  3. Error / empty-result handling.
  4. 2-3 example invocations.

## Add a new plugin

1. Create folder `<plugin-name>/` at the repo root.
2. Add `<plugin-name>/.claude-plugin/plugin.json` with `name`, `version`, `description`, `author`.
3. Add `<plugin-name>/.mcp.json` if the plugin registers MCP servers.
4. Add `<plugin-name>/README.md` documenting tools, auth, and skill catalog.
5. Add the plugin to the `plugins` array in `.claude-plugin/marketplace.json`.
6. Skills live under `<plugin-name>/skills/<skill-name>/SKILL.md`.

## Version bumps

Plugins follow semver. Bump on every shipped change so consumer caches invalidate:

- Patch (`x.y.Z`) — content edits, new skills inside existing plugins.
- Minor (`x.Y.0`) — new MCP tools, new skills that change behavior of existing tools.
- Major (`X.0.0`) — renames, removals, breaking schema changes in `plugin.json`.

After editing a plugin, **bump the version in `<plugin>/.claude-plugin/plugin.json`** before commit. Consumers running `claude plugin update <plugin>@datons` only pick up new versions.

## Skill design philosophy

Skills are wrappers that add semantic value over raw MCP tools. Three properties to preserve:

1. **Route through the MCP** — skills always call the MCP tool, never embed cached or trained-data answers. This keeps responses fresh, timestamped, and traceable.
2. **Add domain context the user shouldn't have to learn** — facet syntax, jurisdiction defaults, common arg patterns. The user types "RD 244/2019 art. 4"; the skill knows to force `jurisdiction='es'` and call `list_laws` before `read_unit`.
3. **Be composable, not workflow-final** — skills produce structured datapoints with metadata (timestamp, official URL, version). They don't draft deliverables. Composition is the user's job, with Claude's help.

## Testing locally before pushing

Load a plugin from a working copy with `--plugin-dir`:

```bash
CLAUDE_CONFIG_DIR=/tmp/claude-dev claude --plugin-dir ./lex
```

Inside the session, invoke the skill manually (`/lex:resolver-cita Art. 4 RD 244/2019`) and verify the output is sensible.

## Reporting issues / requesting plugins

Open an issue at <https://github.com/datons/agent-plugins/issues>.
