---
title: "Building a Robust Git Strategy for Scientific Python Projects"
lastmod: 2025-12-24
date: 2025-12-24
draft: false
topics: ["git", "python", "automation"]
summary: "A comprehensive guide to implementing branch protection, automated quality checks, and PR validation for open-source Python libraries"
---

## Introduction

When building an open-source scientific Python library, maintaining code quality and a clean git history becomes crucial—especially when you're planning for community contributions. In this post, I'll walk through the complete git strategy I implemented for [Relperm](https://github.com/oskrgab/relperm), a petroleum engineering library for relative permeability calculations.

This strategy balances simplicity for solo development with scalability for future contributors, ensuring that every change is tested, validated, and follows a consistent workflow.

## The Problem: Protecting Production While Enabling Development

Like many projects, I started with a simple workflow: work directly on `main`, commit frequently, and push. This works fine for solo development, but it creates several problems:

1. **No quality gates** - Broken code can land on the main branch
2. **Messy history** - "fix typo", "oops", "actually fix it" commits pile up
3. **No integration testing** - Features aren't tested together before release
4. **Risky releases** - Tagging happens on potentially untested code
5. **Contributor confusion** - No clear workflow for external contributors

The goal was to build a strategy that:
- ✅ Keeps `main` always releasable
- ✅ Enforces quality checks automatically
- ✅ Provides clear contribution guidelines
- ✅ Supports both regular development and emergency hotfixes
- ✅ Maintains a clean, readable git history

## The Solution: Three-Branch Strategy with Automated Validation

### Branch Model Overview

I implemented a three-tier branching strategy:

```
main (production, stable releases only)
  ↑
  └── dev (integration branch, latest development)
       ↑
       ├── feature/*   (new features)
       ├── bugfix/*    (bug fixes)
       ├── refactor/*  (code improvements)
       └── hotfix/*    (can also merge directly to main for emergencies)
```

**Branch purposes:**

- **`main`**: Production-ready code only. Every commit on main represents a potential or actual release.
- **`dev`**: Integration branch where features come together. Can be temporarily broken, but should stabilize before merging to main.
- **Feature branches**: Short-lived branches for individual features, bugs, or improvements. Deleted after merge.

### Why Three Branches?

You might ask: "Why not just use `main` and feature branches?" Here's the rationale:

**Two-branch model (main + features):**
- ✅ Simple
- ❌ No integration testing before release
- ❌ Can't batch features into versioned releases
- ❌ Hotfixes complicate unreleased work

**Three-branch model (main + dev + features):**
- ✅ Integration testing in `dev` before release
- ✅ Can batch multiple features into releases
- ✅ Hotfixes can bypass `dev` when needed
- ✅ `main` stays stable while `dev` can be experimental
- ⚠️ Slightly more complex (manageable with automation)

For a scientific library expecting community contributions and needing stable releases, the three-branch model wins.

## Setting Up Branch Protection

GitHub's branch protection is the foundation of this strategy, but there's a **critical gotcha**: branch protection is **remote-only**. Git will happily let you commit to your local `main` branch, but GitHub will reject the push.

![Screenshot: Branch protection settings for main](./screenshots/branch-protection-main.png)

### Branch Protection for `main`

**Settings → Branches → Add rule for `main`:**

- ✅ **Require a pull request before merging** - Forces PR workflow
- ✅ **Require status checks to pass before merging** - Enforces CI
  - Select: `test`, `lint`, `validate-source-branch`
- ✅ **Require branches to be up to date before merging** - Prevents stale PRs
- ✅ **Block force pushes** - Protects history
- ✅ **Restrict deletions** - Can't accidentally delete main
- ✅ **Require linear history** (optional) - Enforces squash/rebase
- ✅ **Allow squash merging only** - Clean history

![Screenshot: Status checks configuration](./screenshots/status-checks-main.png)

### Branch Protection for `dev`

Same settings as `main`, but:
- ✅ **Allow merge commits** (optional) - Can use different merge strategy
- ✅ Status checks: `test`, `lint`, `validate-source-branch`

![Screenshot: Branch protection settings for dev](./screenshots/branch-protection-dev.png)

### The Golden Rule

**Never commit to local `main` or `dev` branches!** Always work on feature branches, even for small changes.

If you accidentally commit to local `main`:
```bash
# Save your work
git checkout -b feature/recover-my-work

# Reset main to match remote
git checkout main
git reset --hard origin/main

# Continue on feature branch
git checkout feature/recover-my-work
```

## Pre-commit Hooks: Local Protection Layer

While GitHub's branch protection is powerful, it only works when you push to remote. Pre-commit hooks provide **immediate local feedback** before you even create a commit.

### Setting Up Pre-commit Hooks

**Install pre-commit:**
```bash
uv add --dev pre-commit
uv run pre-commit install
```

**Configuration (`.pre-commit-config.yaml`):**
```yaml
repos:
  # Standard checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
        exclude: ^mkdocs\.yml$  # MkDocs uses Python-specific YAML
      - id: check-toml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-merge-conflict
      - id: check-case-conflict
      - id: no-commit-to-branch
        args: ['--branch=main', '--branch=dev']  # ⭐ Prevents commits to protected branches

  # Ruff - Fast linting and formatting (Rust-based)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff-format
      - id: ruff
        args: [--fix]

  # Ty - Type checking
  - repo: local
    hooks:
      - id: ty
        name: ty type checker
        entry: uv run ty check
        language: system
        types: [python]
        pass_filenames: false

  # Codespell - Catch typos
  - repo: https://github.com/codespell-project/codespell
    rev: v2.3.0
    hooks:
      - id: codespell
```

### What Gets Checked

Every time you commit, pre-commit automatically runs:

1. **Branch protection** - Blocks commits to `main` and `dev`
2. **Code formatting** - Auto-formats with ruff
3. **Linting** - Auto-fixes issues with ruff
4. **Type checking** - Validates types with ty
5. **File hygiene** - Removes trailing whitespace, fixes line endings
6. **YAML/TOML validation** - Checks workflow files
7. **Spell checking** - Catches typos

### How It Works

```bash
git checkout -b feature/my-feature
# ... make changes ...
git add .
git commit -m "Add feature"

# Pre-commit runs automatically:
# trailing-whitespace.....Passed
# end-of-file-fixer.......Passed
# check-yaml..............Passed
# check-toml..............Passed
# no-commit-to-branch.....Passed
# ruff-format.............Passed
# ruff....................Passed
# ty......................Passed
# codespell...............Passed
# ✅ Commit succeeds
```

**Protection from mistakes:**
```bash
# Trying to commit on protected branch
git checkout main
git commit -m "oops"

# Output:
# no-commit-to-branch........Failed
# You're attempting to commit on branch 'main'
# ❌ Commit blocked immediately!
```

### Two Layers of Protection

| Layer | When It Runs | What It Prevents |
|-------|--------------|------------------|
| **Pre-commit hooks** | Before local commit | ✅ Commits to main/dev<br>✅ Linting issues<br>✅ Type errors<br>✅ Formatting problems |
| **GitHub branch protection** | When pushing to remote | ✅ Pushes to main/dev<br>✅ Merges without PR<br>✅ Merges without CI passing |

This **defense in depth** approach means mistakes are caught at the earliest possible point.

## GitHub Actions Workflows

I created three workflows to automate quality checks and releases:

### 1. Quality Workflow (`quality.yaml`)

Runs on **every pull request** to validate code quality before merge.

**Trigger:**
```yaml
on:
  pull_request:  # Only on PRs, not on pushes to main/dev
```

**Jobs:**

1. **`test`** - Runs pytest with coverage requirement (>90%)
2. **`lint`** - Runs code quality checks:
   - `ruff format --check` (code formatting)
   - `ruff check` (linting)
   - `ty check` (type checking)

Both jobs run in **parallel** for faster feedback.

![Screenshot: Quality workflow running on a PR](./screenshots/quality-workflow-pr.png)

**Why only on PRs?**

With branch protection, all changes go through PRs anyway. Running checks on push to `main` would be redundant and waste CI minutes. The quality workflow acts as a **gate-keeper** for both `dev` and `main`.

```yaml
name: quality

on:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
      - name: Set up Python
        run: uv python install
      - name: Install dependencies
        run: uv sync
      - name: Run tests
        run: uv run pytest

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
      - name: Set up Python
        run: uv python install
      - name: Install dependencies
        run: uv sync
      - name: Run ruff format check
        run: uv run ruff format --check .
      - name: Run ruff lint
        run: uv run ruff check .
      - name: Run ty
        run: uv run ty check
```

### 2. PR Validation Workflow (`pr-validation.yaml`)

This is the secret sauce that enforces the branching strategy. It validates that PRs follow the correct workflow.

**Rules enforced:**

**PRs to `main` - Only allow:**
- ✅ `dev` branch (normal releases)
- ✅ `hotfix/*` branches (emergency fixes)
- ✅ `release/*` branches (for resolving merge conflicts)

**PRs to `main` - Block:**
- ❌ `feature/*` branches
- ❌ `bugfix/*` branches
- ❌ Any other branches

**PRs to `dev` - Recommend:**
- ✅ `feature/*` branches
- ✅ `bugfix/*` branches
- ✅ `refactor/*` branches
- ⚠️ Other branches (warn but allow)

![Screenshot: PR validation blocking a feature→main PR](./screenshots/pr-validation-blocked.png)

**Example error message when trying to merge `feature/*` → `main`:**

```
❌ Error: Feature branches cannot merge directly to main
   Current: feature/add-let-model → main

Correct workflow:
   1. Create PR: feature/add-let-model → dev
   2. After testing in dev, create release PR: dev → main
```

![Screenshot: PR validation error message in GitHub](./screenshots/pr-validation-error-message.png)

**Implementation highlights:**

```yaml
name: PR Validation

on:
  pull_request:
    branches:
      - main
      - dev

jobs:
  validate-source-branch:
    runs-on: ubuntu-latest
    steps:
      - name: Validate PR source branch
        run: |
          TARGET_BRANCH="${{ github.base_ref }}"
          SOURCE_BRANCH="${{ github.head_ref }}"

          # Block feature/* → main
          if [ "$TARGET_BRANCH" = "main" ] && [[ "$SOURCE_BRANCH" =~ ^feature/ ]]; then
            echo "❌ Error: Feature branches cannot merge directly to main"
            exit 1
          fi

          # Allow hotfix/* → main (with reminder)
          if [ "$TARGET_BRANCH" = "main" ] && [[ "$SOURCE_BRANCH" =~ ^hotfix/ ]]; then
            echo "✅ Hotfix PR: $SOURCE_BRANCH → main"
            echo "⚠️  REMINDER: Sync hotfix back to dev after merging"
            exit 0
          fi

          # ... more validation logic
```

This workflow **fails the PR** if the branching strategy is violated, preventing merge.

![Screenshot: PR checks showing validate-source-branch status](./screenshots/pr-checks-status.png)

### 3. Release Workflow (`release.yaml`)

Fully automated release pipeline triggered by **git tags**.

**Trigger:**
```yaml
on:
  push:
    tags:
      - "[0-9]+.[0-9]+.[0-9]+"      # 0.1.0
      - "[0-9]+.[0-9]+.[0-9]+a[0-9]+"  # 0.1.0a1
      - "[0-9]+.[0-9]+.[0-9]+b[0-9]+"  # 0.1.0b1
      - "[0-9]+.[0-9]+.[0-9]+rc[0-9]+" # 0.1.0rc1
```

**Pipeline:**

1. **Extract version** from tag
2. **Check PyPI** - Ensure version is newer than what's published
3. **Build package** - `uv build`
4. **Publish to PyPI** - Using Trusted Publisher (no API tokens!)
5. **Create GitHub Release** - With auto-generated notes
6. **Deploy docs** - To GitHub Pages

![Screenshot: Release workflow successful run](./screenshots/release-workflow-success.png)

**Creating a release:**

```bash
# Ensure dev is merged to main and tested
gh pr create --base main --head dev --title "Release v0.2.0"
# ... wait for checks, merge ...

# Tag and push
git checkout main
git pull origin main
git tag 0.2.0
git push origin 0.2.0

# Release workflow runs automatically
```

![Screenshot: GitHub release created by workflow](./screenshots/github-release-page.png)

**Key feature**: No tests in the release workflow! Why? Because `main` can only receive code that passed quality checks via PRs. Release workflow assumes `main` is already validated and focuses on building/publishing.

## The Complete Development Workflow

### For Regular Features/Bugfixes

**Step 1: Start from `dev`**
```bash
git checkout dev
git pull origin dev
git checkout -b feature/add-let-model
```

**Step 2: Develop with frequent commits**
```bash
# ... code code code ...
git add .
git commit -m "wip: started let model"
git commit -m "added tests"
git commit -m "fixed lint issues"
# Commit message quality doesn't matter - we squash merge!
```

**Step 3: Run quality checks locally**
```bash
uv run ruff format .
uv run ruff check --fix .
uv run ty check
uv run pytest --cov=relperm
```

**Step 4: Push and create PR to `dev`**
```bash
git push -u origin feature/add-let-model
gh pr create --base dev --title "Add LET correlation model"
```

![Screenshot: Creating a PR with gh CLI](./screenshots/gh-pr-create.png)

**Step 5: Wait for CI checks**

![Screenshot: PR with passing checks](./screenshots/pr-checks-passing.png)

All three checks must pass:
- ✅ `test` (pytest)
- ✅ `lint` (ruff + ty)
- ✅ `validate-source-branch` (correct workflow)

**Step 6: Squash and merge**

When merged, all commits are squashed into one clean commit on `dev`:

![Screenshot: Squash and merge button](./screenshots/squash-merge-button.png)

Result on `dev`:
```
* feat: Add LET correlation model (#5)
```

Instead of:
```
* wip: started let model
* added tests
* fixed lint issues
* fixed typo
* actually fixed typo
```

**Step 7: Clean up**
```bash
git checkout dev
git pull origin dev
git branch -d feature/add-let-model
```

### For Emergency Hotfixes

**When production is broken and you can't wait for the next release:**

**Step 1: Start from `main`**
```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-patch
```

**Step 2: Fix and test thoroughly**
```bash
# ... fix the issue ...
uv run pytest
uv run ruff check .
```

**Step 3: Create PR directly to `main`**
```bash
git push -u origin hotfix/critical-security-patch
gh pr create --base main --title "Hotfix: Critical security patch"
```

PR validation allows this:
```
✅ Hotfix PR: hotfix/critical-security-patch → main
⚠️  REMINDER: Sync hotfix back to dev after merging
```

![Screenshot: Hotfix PR to main passing validation](./screenshots/hotfix-pr-validation.png)

**Step 4: After merge, sync to `dev`**
```bash
git checkout dev
git pull origin dev
git merge main
git push origin dev
```

This ensures `dev` gets the hotfix too!

### Release Process

**When `dev` has enough features and is stable:**

**Step 1: Create release PR**
```bash
git checkout dev
git pull origin dev
gh pr create --base main --head dev --title "Release v0.2.0"
```

![Screenshot: Release PR from dev to main](./screenshots/release-pr.png)

PR validation allows this:
```
✅ Release PR: dev → main
```

**Step 2: Wait for quality checks**

Even though `dev` was tested, the release PR runs checks on the merge commit to `main`.

**Step 3: Merge to `main`**

Use merge commit (not squash) for releases to preserve the dev history:

![Screenshot: Merge commit for release](./screenshots/release-merge-commit.png)

**Step 4: Tag and trigger release**
```bash
git checkout main
git pull origin main
git tag 0.2.0
git push origin 0.2.0
```

**Step 5: Watch the release workflow**

![Screenshot: Release workflow in progress](./screenshots/release-workflow-running.png)

Within minutes:
- ✅ Package built and published to PyPI
- ✅ GitHub Release created with auto-generated notes
- ✅ Documentation deployed to GitHub Pages

![Screenshot: PyPI package page](./screenshots/pypi-package-page.png)

![Screenshot: GitHub Pages documentation](./screenshots/github-pages-docs.png)

## Real-World Examples

### Example 1: Feature Development

**Scenario**: Adding a new correlation model (LET model)

```bash
# Start
git checkout dev
git pull origin dev
git checkout -b feature/add-let-model

# Develop (multiple commits over several days)
git commit -m "Initial LET equations"
git commit -m "Add validation"
git commit -m "Add tests"
git commit -m "Fix edge cases"
git commit -m "Add documentation"

# Quality check
uv run pytest --cov=relperm
# Coverage: 94% ✅

# Create PR
gh pr create --base dev --title "Add LET correlation model"

# CI runs: test ✅, lint ✅, validate-source-branch ✅
# Merge via GitHub UI (squash)

# Result on dev: Single clean commit
# * feat: Add LET correlation model (#7)
```

### Example 2: Blocked Incorrect Workflow

**Scenario**: Accidentally trying to merge feature directly to main

```bash
git checkout -b feature/quick-fix
# ... make changes ...
gh pr create --base main --title "Quick fix"
```

**Result**: PR validation FAILS

![Screenshot: PR validation failure](./screenshots/pr-validation-failed-example.png)

```
❌ Error: Feature branches cannot merge directly to main
   Current: feature/quick-fix → main

Correct workflow:
   1. Create PR: feature/quick-fix → dev
   2. After testing in dev, create release PR: dev → main
```

The PR cannot be merged until you change the base branch:

```bash
# Close incorrect PR
gh pr close

# Create correct PR
gh pr create --base dev --title "Quick fix"
```

### Example 3: Production Hotfix

**Scenario**: Critical bug discovered in production (main)

```bash
# Start from main
git checkout main
git pull origin main
git checkout -b hotfix/fix-division-by-zero

# Fix and test
# ... fix code ...
uv run pytest
uv run ruff check .

# Create PR to main (allowed for hotfix/*)
gh pr create --base main --title "Hotfix: Fix division by zero error"

# CI runs: test ✅, lint ✅, validate-source-branch ✅
# Merge to main
# Tag and release
git checkout main
git pull origin main
git tag 0.1.1
git push origin 0.1.1

# Sync to dev
git checkout dev
git merge main
git push origin dev
```

**Timeline**: Bug fix is live on PyPI within ~10 minutes of discovering the issue.

![Screenshot: Fast hotfix deployment timeline](./screenshots/hotfix-timeline.png)

## Lessons Learned

### What Works Well

**1. Automated PR validation is a game-changer**

Before implementing PR validation, I occasionally created PRs to the wrong branch. Now it's impossible to merge incorrectly. The validation workflow catches mistakes immediately and provides helpful error messages.

**2. Squash merging keeps history clean**

Instead of:
```
* feat: Add feature (#8)
* wip
* fix tests
* fix lint
* actually fix lint
* fix typo
* Merge pull request #8
```

You get:
```
* feat: Add feature (#8)
```

Much easier to understand the project history!

**3. Separating quality checks from release is efficient**

Running tests in the quality workflow (on PRs) and skipping them in the release workflow saves time. Release workflow focuses on packaging and publishing, not validation.

**4. Branch protection prevents accidents**

Even working solo, I've accidentally started typing commits on `main` instead of a feature branch. Branch protection caught it when I tried to push.

### Challenges and Solutions

**Challenge 1: Branch protection is remote-only**

Git allows committing to local `main`. You only find out when you try to push.

**Solution**: Pre-commit hooks + git aliases.

**Pre-commit hooks** provide local protection that catches mistakes immediately:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: no-commit-to-branch
        args: ['--branch=main', '--branch=dev']
```

When you try to commit to a protected branch:
```bash
git checkout main
git commit -m "oops"

# Output:
# no-commit-to-branch........Failed
# You're attempting to commit on branch 'main'
# Committing directly to 'main' is not allowed.
```

**Defense in depth** - Two layers of protection:
1. **Local (pre-commit)**: Blocks commits to main/dev immediately
2. **Remote (GitHub)**: Blocks pushes even if pre-commit is bypassed

Added helpful aliases to `~/.gitconfig`:
```ini
[alias]
    feature = "!f() { git checkout dev && git pull && git checkout -b feature/$1; }; f"
```

Now: `git feature my-feature` automatically creates a feature branch from updated `dev`.

**Challenge 2: Remembering to sync hotfixes to dev**

After merging a hotfix to `main`, it's easy to forget syncing to `dev`.

**Solution**: PR validation workflow includes a reminder:
```
✅ Hotfix PR: hotfix/security-patch → main
⚠️  REMINDER: Sync hotfix back to dev after merging
```

Could be further automated with a workflow that auto-creates a `main` → `dev` PR after hotfix merge.

**Challenge 3: Status checks need to be selected manually**

When adding a new workflow, you must manually add it to branch protection status checks.

![Screenshot: Adding status check to branch protection](./screenshots/add-status-check.png)

**Solution**: Document this clearly in CONTRIBUTING.md. GitHub doesn't auto-detect new required checks.

### What I'd Do Differently

**1. Consider trunk-based development for solo work**

The three-branch model adds complexity. For solo development, a simpler model might suffice:
- `main` as the integration branch
- Feature branches merge to `main`
- Tags on `main` for releases

I chose the three-branch model because I'm planning for contributors, but it's more complex than needed initially.

**2. Automate hotfix → dev syncing**

Currently manual. Could add a workflow:
```yaml
# Trigger: When hotfix/* PR is merged to main
# Action: Auto-create PR from main to dev
```

**3. Add conventional commit enforcement**

Could add a workflow to validate commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` for features
- `fix:` for bug fixes
- `docs:` for documentation
- etc.

This would enable automatic changelog generation.

## Conclusion

Building a robust git strategy takes upfront effort, but pays dividends as the project grows. The combination of:

- **Branch protection** (enforces PR workflow)
- **Quality checks** (automated testing and linting)
- **PR validation** (enforces branching strategy)
- **Automated releases** (tags → PyPI + GitHub Release + Docs)

Creates a system where:
- ✅ `main` is always stable and releasable
- ✅ Quality is enforced automatically
- ✅ Contribution workflow is clear and documented
- ✅ Releases are fast and consistent
- ✅ Git history is clean and readable

For scientific Python projects expecting community contributions, this setup provides a professional foundation that scales from solo development to team collaboration.

## Resources

- **Repository**: [oskrgab/relperm](https://github.com/oskrgab/relperm)
- **Workflow files**: [`.github/workflows/`](https://github.com/oskrgab/relperm/tree/main/.github/workflows)
- **Contributing guide**: [`CONTRIBUTING.md`](https://github.com/oskrgab/relperm/blob/main/CONTRIBUTING.md)
- **GitHub Branch Protection**: [Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- **GitHub Actions**: [Docs](https://docs.github.com/en/actions)
- **UV Package Manager**: [astral-sh/uv](https://github.com/astral-sh/uv)

---

*Have questions or suggestions? Open an issue on [GitHub](https://github.com/oskrgab/relperm/issues) or reach out!*
