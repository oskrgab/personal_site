# Writing Agent Briefs

An agent brief is a structured comment posted on a GitHub issue when it moves to `ready-for-agent`. It is the authoritative specification that an AFK agent will work from. The original issue body and discussion are context — the agent brief is the contract.

## Principles

### Durability over precision

The issue may sit in `ready-for-agent` for days or weeks. The codebase will change in the meantime. Write the brief so it stays useful even as files are renamed, moved, or refactored.

- **Do** describe interfaces, types, and behavioral contracts
- **Do** name specific types, function signatures, or config shapes that the agent should look for or modify
- **Don't** reference file paths — they go stale
- **Don't** reference line numbers
- **Don't** assume the current implementation structure will remain the same

### Behavioral, not procedural

Describe **what** the system should do, not **how** to implement it. The agent will explore the codebase fresh and make its own implementation decisions.

- **Good:** "The `SkillConfig` type should accept an optional `schedule` field of type `CronExpression`"
- **Bad:** "Open src/types/skill.ts and add a schedule field on line 42"
- **Good:** "When a user runs `/triage` with no arguments, they should see a summary of issues needing attention"
- **Bad:** "Add a switch statement in the main handler function"

### Complete acceptance criteria

The agent needs to know when it's done. Every agent brief must have concrete, testable acceptance criteria. Each criterion should be independently verifiable.

- **Good:** "Running `gh issue list --label needs-triage` returns issues that have been through initial classification"
- **Bad:** "Triage should work correctly"

### Explicit scope boundaries

State what is out of scope. This prevents the agent from gold-plating or making assumptions about adjacent features.

## Template

```markdown
## Agent Brief

**Category:** bug / enhancement / post
**Summary:** one-line description of what needs to happen

**Current behavior:**
Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.

**Desired behavior:**
Describe what should happen after the agent's work is complete.
Be specific about edge cases and error conditions.

**Key interfaces:**
- `TypeName` — what needs to change and why
- `functionName()` return type — what it currently returns vs what it should return
- Config shape — any new configuration options needed

**Acceptance criteria:**
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3

**Out of scope:**
- Thing that should NOT be changed or addressed in this issue
- Adjacent feature that might seem related but is separate
```

## Examples

### Good agent brief (bug)

```markdown
## Agent Brief

**Category:** bug
**Summary:** Skill description truncation drops mid-word, producing broken output

**Current behavior:**
When a skill description exceeds 1024 characters, it is truncated at exactly
1024 characters regardless of word boundaries. This produces descriptions
that end mid-word (e.g. "Use when the user wants to confi").

**Desired behavior:**
Truncation should break at the last word boundary before 1024 characters
and append "..." to indicate truncation.

**Key interfaces:**
- The `SkillMetadata` type's `description` field — no type change needed,
  but the validation/processing logic that populates it needs to respect
  word boundaries
- Any function that reads SKILL.md frontmatter and extracts the description

**Acceptance criteria:**
- [ ] Descriptions under 1024 chars are unchanged
- [ ] Descriptions over 1024 chars are truncated at the last word boundary
      before 1024 chars
- [ ] Truncated descriptions end with "..."
- [ ] The total length including "..." does not exceed 1024 chars

**Out of scope:**
- Changing the 1024 char limit itself
- Multi-line description support
```

### Good agent brief (enhancement)

```markdown
## Agent Brief

**Category:** enhancement
**Summary:** Add `.out-of-scope/` directory support for tracking rejected feature requests

**Current behavior:**
When a feature request is rejected, the issue is closed with a `wontfix` label
and a comment. There is no persistent record of the decision or reasoning.
Future similar requests require the maintainer to recall or search for the
prior discussion.

**Desired behavior:**
Rejected feature requests should be documented in `.out-of-scope/<concept>.md`
files that capture the decision, reasoning, and links to all issues that
requested the feature. When triaging new issues, these files should be
checked for matches.

**Key interfaces:**
- Markdown file format in `.out-of-scope/` — each file should have a
  `# Concept Name` heading, a `**Decision:**` line, a `**Reason:**` line,
  and a `**Prior requests:**` list with issue links
- The triage workflow should read all `.out-of-scope/*.md` files early
  and match incoming issues against them by concept similarity

**Acceptance criteria:**
- [ ] Closing a feature as wontfix creates/updates a file in `.out-of-scope/`
- [ ] The file includes the decision, reasoning, and link to the closed issue
- [ ] If a matching `.out-of-scope/` file already exists, the new issue is
      appended to its "Prior requests" list rather than creating a duplicate
- [ ] During triage, existing `.out-of-scope/` files are checked and surfaced
      when a new issue matches a prior rejection

**Out of scope:**
- Automated matching (human confirms the match)
- Reopening previously rejected features
- Bug reports (only enhancement rejections go to `.out-of-scope/`)
```

### Good agent brief (post — migration)

```markdown
## Agent Brief

**Category:** post
**Summary:** Migrate the 2026-01-20 LinkedIn post on agentic AI in upstream O&G into a Hugo blog post anchored on the Hamming quote.

**Current behavior:**
The content exists only as a LinkedIn share (URL in the issue body). The
blog has no entry under `content/blog/2026-01-20-*`.

**Desired behavior:**
A new Hugo blog post is created at `content/blog/2026-01-20-<slug>/`
containing the verbatim LinkedIn body text (emojis preserved), the
thumbnail attached to the issue, body images in order, and the YouTube
shortcode for the embedded video. Frontmatter, intro thumbnail image,
and the `{{< subscription >}}` shortcode follow the conventions in
[POST-INGREDIENTS.md](POST-INGREDIENTS.md).

**Ingredients (from the issue template):**
- LinkedIn URL — see issue body
- Title — "<title>"
- Publish date — 2026-01-20 (decoded from activity ID)
- Topics — `oil-and-gas`, `ai`, `agentic-ai`
- Body text — pasted verbatim in the issue's "Body text:" section
- Thumbnail — attached in "Thumbnail:" section
- Body images — 2 attached, in order
- YouTube video ID — `<id>`

**Acceptance criteria:**
- [ ] New directory `content/blog/2026-01-20-<slug>/` with `index.md` and co-located media
- [ ] Frontmatter: `title`, `date` (with time), `draft: false`, `description`, `topics`
- [ ] First content line is `![Post Image](thumbnail.jpg)`
- [ ] Body text matches the issue's "Body text:" section verbatim (emojis preserved)
- [ ] Body images placed in document order; YouTube embedded via `{{< youtube <id> >}}`
- [ ] Final content line (before any trailing blank lines) is `{{< subscription >}}`
- [ ] Branch off `dev`, named `post/<issue-number>-<short-slug>`
- [ ] PR title equals the post title; PR body uses `Refs #<issue-number>` (not `Fixes`/`Closes`)
- [ ] On PR open, agent applies `ready-for-review` and removes `ready-for-agent`

**Out of scope:**
- Editing other posts or the homepage
- Adjusting Hugo theme / layouts
- Closing the issue (the maintainer closes after rendered review)
```

### Bad agent brief

```markdown
## Agent Brief

**Summary:** Fix the triage bug

**What to do:**
The triage thing is broken. Look at the main file and fix it.
The function around line 150 has the issue.

**Files to change:**
- src/triage/handler.ts (line 150)
- src/types.ts (line 42)
```

This is bad because:
- No category
- Vague description ("the triage thing is broken")
- References file paths and line numbers that will go stale
- No acceptance criteria
- No scope boundaries
- No description of current vs desired behavior
