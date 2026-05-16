## Agent skills

### Issue tracker

Issues live in GitHub Issues for `oskrgab/personal_site`, managed via the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Three category labels (`bug`, `enhancement`, `post`) and six state labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `ready-for-review`, `wontfix`). See `docs/agents/triage-labels.md`. The `post` category triggers a specialized ingredient-inventory flow — see `.claude/skills/triage/POST-INGREDIENTS.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
