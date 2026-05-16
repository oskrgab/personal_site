# Agent derives title, topics, and structural choices from raw post inputs

For **Post (category)** issues, the triage skill collects only the inputs the agent can't derive — body text, thumbnail, and optional source-specific items (LinkedIn URL, body images, first comment, video ID, PDF). The agent then derives the title, the topic tags, body subheadings, the `description`/`summary` frontmatter, and the **Resources section**'s heading and placement from those raw inputs plus repo state. The maintainer reviews the derived choices at `ready-for-review` (per ADR-0001) and can correct them with a delta brief.

## Why this is non-obvious

GitHub issue-template tradition is that the reporter supplies every structured field. A future contributor reading `POST-INGREDIENTS.md` will see title and topics conspicuously absent from the raw-inputs list and ask why. The answer: LinkedIn posts don't have titles, and most don't suggest one cleanly from the body; forcing the maintainer to invent one at issue-creation time is friction that the agent can absorb. Topics are similar — picking from an existing tag set is a mechanical task the agent does reliably, and it avoids tag-pollution when the maintainer reaches for a new label that already exists under a different spelling.

## How this is safe

The `ready-for-review` gate from ADR-0001 already requires the maintainer to eyeball the rendered post before closing the issue. Title and topic mistakes surface in the same review pass — no new failure mode. Revisions follow the existing delta-brief flow.

## Scope

This rule applies only to the **Post** category. **Bug** and **Enhancement** issues keep their conventional shape — the reporter supplies the structured fields.

The maintainer can pre-empt the agent's derivation by filling in the optional `Title:` or `Topics:` hint fields in the issue template; those fields are overrides, not required inputs.
