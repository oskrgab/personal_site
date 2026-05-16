# Personal Site

A Hugo blog at `content/blog/` whose posts are often migrated from prior LinkedIn shares. Issue triage runs against the GitHub repo `oskrgab/personal_site`.

## Language

### Content

**Blog post**:
A published entry under `content/blog/<YYYY-MM-DD-slug>/`, consisting of an `index.md` with Hugo frontmatter and co-located assets (e.g. `thumbnail.jpg`).
_Avoid_: Article, entry.

**LinkedIn post**:
A share originally published to LinkedIn, identified by an activity URL whose embedded snowflake ID encodes the publish timestamp. Source material for migration into a **Blog post**.
_Avoid_: LinkedIn share (only as backup CSV terminology).

### Triage

**Category**:
The kind of work an issue represents. Exactly one of three mutually-exclusive values: **Bug**, **Enhancement**, **Post**.

**Post (category)**:
A triage category for issues whose purpose is producing a new **Blog post**. The source may be a **LinkedIn post** being migrated, or original content drafted from scratch. Distinct from **Blog post** (the artifact) and **LinkedIn post** (the source, when applicable).
_Avoid_: Migration, port, repost — those describe one *mode* of a **Post** issue, not the category itself.

**State**:
Where an issue sits in the triage workflow. One of: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `ready-for-review`, `wontfix`.

**ready-for-review**:
The agent has finished its work and opened a PR; the maintainer reviews the diff and the rendered output locally (`hugo server`) before merging and closing. The agent flips the label when opening the PR; the agent's PR must not use closing keywords (`Fixes #N`, `Closes #N`) — only the maintainer closes the issue. Revisions during review go back to `ready-for-agent` with a delta brief comment, not to a separate revisions label.

**Ingredient**:
An input needed to promote a **Post (category)** issue to `ready-for-agent`. Split into two kinds:

- **Raw inputs** — what the maintainer must provide because the agent can't derive them. Always: body text, thumbnail. Conditional: **LinkedIn URL** (migration mode), publish date (from-scratch mode only — auto-decoded in migration mode), body images (when the source had any), **First comment** (when the source had one), YouTube video ID (when the source had a video), PDF (only when explicitly called for).
- **Derived outputs** — what the agent figures out from raw inputs plus repo state, with the maintainer reviewing at `ready-for-review`: title, topics (picked from the existing set in `content/blog/*/index.md` frontmatter; new ones only when no existing tag fits), body subheadings, the **Resources section**'s heading and placement, and the frontmatter `description`/`summary`.

The maintainer can override any derived output by filling in the corresponding hint field in the issue template, but those fields are not required.

**First comment**:
Verbatim text the maintainer pastes from the **LinkedIn post**'s pinned first comment — typically `Label: url`-style lines with supplementary links (data, repos, references). On the blog it renders as the **Resources section**. Optional raw input; only present when the LinkedIn source had a useful first comment.

**Resources section**:
The end-of-post block that surfaces supplementary links — produced from the **First comment** ingredient (or written from scratch). The agent picks its heading text (e.g. `## Resources`, `## Links`) and placement relative to other end-of-post elements per post; the `{{< subscription >}}` shortcode is always last.

**Migration mode** / **From-scratch mode**:
Two modes of a **Post (category)** issue, distinguished by the presence or absence of a **LinkedIn URL**. Migration mode auto-derives publish date and seeds title from the URL's snowflake activity ID; from-scratch mode requires the maintainer to supply title and date directly.

**Source audit**:
A structured paraphrase of the **LinkedIn post** produced by the triage skill via WebFetch in migration mode, posted in the `needs-info` comment. Explicitly labeled as paraphrased — never used as a substitute for the verbatim body text the maintainer must paste.

## Relationships

- A **Blog post** is produced by triaging a **Post** (category) issue to `ready-for-agent` (or `ready-for-human`) and executing it.
- A **Post** (category) issue typically links to exactly one **LinkedIn post** as source.
- Every triaged issue carries exactly one **Category** and exactly one **State**.
- A **Post (category)** issue accrues **Ingredients** during triage; once complete, it moves to `ready-for-agent`.
- When the agent opens its PR for a **Post (category)** issue, the agent flips the issue to `ready-for-review`; only the maintainer closes it from there.

## Flagged ambiguities

- "Post" was overloaded: it could mean the LinkedIn source, the published blog entry, or the triage category. Resolved by reserving **Blog post** for the artifact, **LinkedIn post** for the source, and **Post (category)** for the triage label.
