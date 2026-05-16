# Post-category issues require a maintainer review gate before closing

For **Post (category)** issues, the rendered Hugo output is what matters — not just the diff. Agents therefore must not auto-close these issues: their PRs reference the issue via `Refs #N` (never `Fixes #N`/`Closes #N`), and on PR open the agent flips the issue's state to `ready-for-review`. Only the maintainer closes the issue, after verifying the rendered post locally (`hugo server`).

## Why this is non-obvious

The GitHub-idiomatic default — `Fixes #N` so a PR merge auto-closes its issue — would close **Post** issues at merge time, before the maintainer has eyeballed the rendered result. We accepted the extra manual close step because for blog content, "diff looks right" and "page reads right" are different verifications.

## Scope

This rule applies only to the **Post** category. **Bug** and **Enhancement** issues continue to use the GitHub-idiomatic `Fixes #N` auto-close.
