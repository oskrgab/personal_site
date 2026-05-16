# Post Category — Ingredients & Workflow

This doc is loaded only when triaging an issue in the **post** category. It defines the issue template, the ingredient inventory, the source audit pattern, the Hugo conventions the agent must follow, and the handoff rules for `ready-for-human` and `ready-for-review`.

The state machine, AI disclaimer, "show what needs attention" view, and quick-state override all come from `SKILL.md` and apply unchanged.

## Modes

A post issue runs in one of two modes:

- **Migration mode** — issue contains a LinkedIn URL. Publish date is decoded from the URL's snowflake activity ID; title is seeded from the URL slug.
- **From-scratch mode** — no LinkedIn URL. The maintainer supplies title and date directly.

## Issue template

Issues should be created from `.github/ISSUE_TEMPLATE/post.md` (`gh issue create --template post.md`). The template has anchor sections the inventory step parses verbatim:

```markdown
## Ingredients

**LinkedIn URL:** <url, or leave blank for from-scratch>
**Date:** <YYYY-MM-DD; leave blank in migration mode (auto-decoded)>

**Thumbnail:**
<drop thumbnail.jpg here>

**Body text:**
<paste verbatim text with emojis here>

**Body images** (in order of appearance):
1. <drop image-1>
2. <drop image-2>

**First comment:**
<paste verbatim text from the LinkedIn post's pinned first comment — typically `Label: url` lines; leave blank if none>

**YouTube video ID:** <ID only, e.g. dQw4w9WgXcQ — leave blank if none>

**PDF:** <drop PDF here, or leave blank if none>

### Optional overrides (leave blank to let the agent derive)

**Title:** <force a specific title; otherwise the agent drafts one from body text>
**Topics:** <comma-separated; otherwise the agent picks from existing tags in `content/blog/*/index.md`>
```

## Ingredient checklist

Ingredients split into **raw inputs** (the maintainer must provide them — the agent can't) and **derived outputs** (the agent figures them out from raw inputs plus repo state). See ADR-0002.

### Raw inputs

| Ingredient | Required when | Source | Missing → |
|---|---|---|---|
| LinkedIn URL | migration mode | issue body | `needs-info` (or treat as from-scratch) |
| Publish date | from-scratch mode | `Date:` field (auto-decoded from snowflake in migration mode) | `needs-info` |
| Body text | always | maintainer paste (verbatim, with emojis) | `needs-info` |
| Thumbnail | always | issue attachment | `needs-info` |
| Body images | iff source had inline images | issue attachments | `needs-info` |
| First comment | iff source had a pinned first comment with useful links | `First comment:` field — verbatim `Label: url` text | optional; do not block on this |
| YouTube video ID | iff source had video | `YouTube video ID:` field | `ready-for-human` if not yet uploaded; `needs-info` once uploaded |
| PDF | only when explicitly called for | issue attachment OR repo path supplied by maintainer | `ready-for-human` until attached |

Once all required raw inputs are present, promote to `ready-for-agent`. Missing derived outputs never block — they're agent work.

### Single image → thumbnail only

A common case in migration mode: the maintainer provides exactly one image, and the original LinkedIn post had a single inline image. The first content line of every post is `![Post Image](thumbnail.jpg)` (see Hugo conventions below), so if that same image is also listed under "Body images" the post renders it twice in a row.

Default rule: **one image → thumbnail only, no body image entry.** Confirm with the maintainer if it's ambiguous (e.g. the image clearly belongs mid-body rather than at the top). The same rule applies in reverse — if the maintainer attaches the image only under "Body images" and leaves "Thumbnail" blank, ask whether that image should serve as the thumbnail; if yes, treat it as the thumbnail and drop it from the body-images list.

When this disambiguation happens during triage, record the decision in the needs-info / agent-brief comment ("The single attached image will serve as the thumbnail; no body images.") so the downstream agent doesn't re-introduce the duplicate.

### Derived outputs

The agent produces these from raw inputs + repo state; the maintainer reviews them at `ready-for-review`. The maintainer can pre-empt the agent's choice by filling in the corresponding optional override in the issue template.

| Output | Source | Override field |
|---|---|---|
| Title | Drafted from body text | `Title:` |
| Topics | Picked from existing tags in `content/blog/*/index.md` frontmatter; new tags only when no existing one fits (justify in PR description) | `Topics:` |
| Body subheadings | Added where post length / structure warrants; short LinkedIn-style migrations may have none | — |
| Resources section (heading + placement) | Derived from the **First comment** ingredient — see Hugo conventions below | — |
| Frontmatter `description` / `summary` | Drafted from the first paragraph | — |

## Migration mode: source audit

On first triage of a migration-mode issue, run a WebFetch on the LinkedIn URL and decode the publish date from the activity ID:

```python
# Snowflake decode for LinkedIn activity IDs
activity_id = int(<id from URL>)
timestamp_ms = activity_id >> 22
# Convert to UTC datetime; the result is the publish time.
```

Post a `needs-info` comment that begins with the AI disclaimer and includes a **Source audit** section. The audit is *paraphrased* — never present it as verbatim:

```markdown
> *This was generated by AI during triage.*

## Triage Notes

**Source audit** (auto-fetched from LinkedIn URL — paraphrased, not verbatim):

- **Publish date:** <YYYY-MM-DD> (decoded from activity ID)
- **Subject summary:** <one or two sentences from the WebFetch summary>
- **Likely media:** <what the summary suggests — images, video, PDF — flag uncertainty>

**What we still need from you (@reporter):**

- [ ] **Body text** — paste the verbatim LinkedIn text with emojis into the issue body's "Body text:" section
- [ ] **Thumbnail** — drop a `thumbnail.jpg` into the "Thumbnail:" section
- [ ] **Body images** — if the original had any, drop them into "Body images:" in order
- [ ] **First comment** — if the LinkedIn post has a pinned first comment with useful links (data, repos, references), paste it verbatim into "First comment:". Format is typically `Label: url` per line; the agent converts to markdown
- [ ] **Video** — if the original had a video, upload to YouTube and paste the ID into "YouTube video ID:"
- [ ] **PDF** — only if you want one attached
```

Trim the checkboxes to ingredients that aren't already present in the issue body. Do not list title or topics in the checklist — those are derived outputs (see ADR-0002); the maintainer reviews them at `ready-for-review`, or pre-empts via the optional override fields.

## From-scratch mode: needs-info template

Skip the source audit. Use the original `SKILL.md` needs-info template, listing only the missing ingredient anchors from the template.

## Hugo conventions the agent must follow

The agent brief for a post issue must enforce all of these:

- Directory: `content/blog/<YYYY-MM-DD>-<kebab-slug>/`
- File: `index.md` with frontmatter:

  ```yaml
  ---
  title: "<title>"
  date: <YYYY-MM-DD>T<HH:MM:SS>
  draft: false
  description: "<one-sentence summary the agent drafts from the first paragraph>"
  topics: ["<topic-1>", "<topic-2>"]
  ---
  ```
- **Title and topics** are derived (see ADR-0002): the agent drafts the title from the body text, and picks topics from the existing tags found in `content/blog/*/index.md` frontmatter. New topics are allowed only when no existing tag fits, and must be justified in the PR description. If the issue's optional `Title:` or `Topics:` override fields are filled in, use those verbatim.
- First content line: `![Post Image](thumbnail.jpg)` — the thumbnail file is co-located in the post directory.
- Body images: co-located in the post directory; referenced as `![alt](image-N.jpg)` (or appropriate extension) at the paragraph positions implied by the maintainer's ordering.
- YouTube embeds: `{{< youtube VIDEO_ID >}}` shortcode (just the ID, not a URL).
- PDFs: place under `static/docs/<slug>/<filename>.pdf` and link from the post with a relative `/docs/<slug>/<filename>.pdf` path.
- **Resources section** (when the `First comment:` field is non-empty):
  - Convert each `Label: url` line in the first-comment text into a markdown bullet: `- [Label](url)`. Preserve any leading emojis verbatim — e.g. `🌐 Live app: https://...` becomes `- 🌐 [Live app](https://...)`.
  - The agent picks the section heading per post (e.g. `## Resources`, `## Links`, or omits a heading entirely on short posts where a bare bullet list reads better). Match the tone of the post.
  - Skip the section if the `First comment:` field is empty.
- **End-of-post ordering**: the only fixed rule is that `{{< subscription >}}` is the last content line (before any trailing blank lines). The Resources section, YouTube embed, and PDF link can appear in whatever order reads best for the post — the agent decides.
- Preserve emojis verbatim from the body text.

## Ready-for-human triggers

Move to `ready-for-human` (not `needs-info`) when the missing input requires the maintainer to *do something* before they can provide data:

- The post has a video, but it isn't on YouTube yet — the maintainer must upload it first.
- The post needs a PDF, but the PDF hasn't been prepared yet — the maintainer must finalize the file before attaching.

The handoff comment should:

- Start with the AI disclaimer.
- Use the same body structure as an agent brief (`AGENT-BRIEF.md`) but addressed to the maintainer.
- Be explicit about what's blocked and what the next action is.

Once the maintainer reports the work is done (on a later `/triage` invocation), the issue moves back to `needs-info` (so the now-available data can be inventoried) and then to `ready-for-agent`.

## Ready-for-review handoff

The agent flips the issue to `ready-for-review` **when it opens the PR**, not before and not after merge. The agent brief for a post issue must include:

- Branch from `dev`, name `post/<issue-number>-<short-slug>`.
- PR title = the post title verbatim.
- PR body uses `Refs #<issue-number>` — **never** `Fixes #N` or `Closes #N` (see `docs/adr/0001-post-review-gate.md`).
- After opening the PR, the agent applies `ready-for-review` and removes `ready-for-agent`. The agent posts a comment with the PR link and a short instruction: *"Pull `dev` (after merge) and run `hugo server`; visit `/blog/<slug>/` to verify."*

Only the maintainer closes the issue, after verifying the rendered output locally.

## Revisions during review

If the maintainer wants changes during review, the issue returns to `ready-for-agent` with a **delta brief** comment listing the asks. The original agent brief still applies; the delta brief supersedes it where they conflict. If a revision reveals a missing ingredient (e.g. "we need a second image"), use `needs-info` instead until the ingredient arrives.

No separate `needs-revisions` label.
