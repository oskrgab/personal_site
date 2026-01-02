---
title: "Modern Stack for Python Projects Part 3: Robust Git Strategy"
lastmod: 2025-12-24
date: 2025-12-24
draft: true
topics: ["git", "python", "automation"]
summary: "Implementing branch protection, automated quality checks, and PR validation for open-source Python libraries."
---

In [Part 1]({{< ref "blog/4_modern_python_stack_part_1_setup" >}}) and [Part 2]({{< ref "blog/5_modern_python_stack_part_2_cicd" >}}), we built a modern Python project with automated CI/CD. Now, we need to protect it.

When building an open-source scientific Python library, maintaining code quality and a clean git history becomes crucial—especially when you're planning for community contributions. This post covers the git strategy I implemented for [Relperm](https://github.com/oskrgab/relperm).

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

## PR Validation Workflow (`pr-validation.yaml`)

This is the secret sauce that enforces the branching strategy. It validates that PRs follow the correct workflow.

**Rules enforced:**

**PRs to `main` - Only allow:**
- ✅ `dev` branch (normal releases)
- ✅ `hotfix/*` branches (emergency fixes)

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
```

This workflow **fails the PR** if the branching strategy is violated, preventing merge.

## Pre-commit Hooks: Local Protection Layer

While GitHub's branch protection is powerful, it only works when you push to remote. Pre-commit hooks provide **immediate local feedback** before you even create a commit.

### Setting Up Pre-commit Hooks

We already added pre-commit in Part 1. Now, let's configure it to protect our branches locally.

**Configuration (`.pre-commit-config.yaml`):**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: no-commit-to-branch
        args: ['--branch=main', '--branch=dev']  # ⭐ Prevents commits to protected branches
```

### How It Works

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
```

**Step 3: Run quality checks locally**
```bash
uv run pytest
uv run ruff check
```

**Step 4: Push and create PR to `dev`**
```bash
git push -u origin feature/add-let-model
gh pr create --base dev --title "Add LET correlation model"
```

**Step 5: Squash and merge**
When merged, all commits are squashed into one clean commit on `dev`.

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

**Step 4: After merge, sync to `dev`**
```bash
git checkout dev
git pull origin dev
git merge main
git push origin dev
```

This ensures `dev` gets the hotfix too!

## Conclusion

By combining **Modern Tooling** (Part 1), **Automated CI/CD** (Part 2), and **Robust Git Strategy** (Part 3), we have created a professional, scalable environment for Python development.

The complete system ensures:
- ✅ Quality is enforced automatically
- ✅ Contribution workflow is clear and documented
- ✅ Releases are fast and consistent
- ✅ Git history is clean and readable

You can find the full repository here: [oskrgab/relperm](https://github.com/oskrgab/relperm).