# Building a Modern Python Library from Scratch

A comprehensive guide to setting up a professional Python project with modern tooling: UV, Ruff, Ty, GitHub workflows, and automated releases.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installing UV - The Modern Python Package Manager](#installing-uv)
3. [Creating the Project Structure](#creating-the-project-structure)
4. [Initializing the Python Project](#initializing-the-python-project)
5. [Setting Up Git and GitHub](#setting-up-git-and-github)
6. [Installing Development Tools](#installing-development-tools)
7. [Configuring Code Quality Tools](#configuring-code-quality-tools)
8. [Creating GitHub Workflows](#creating-github-workflows)
9. [Setting Up Documentation](#setting-up-documentation)
10. [Configuring Pre-commit Hooks](#configuring-pre-commit-hooks)
11. [Setting Up Branch Protection](#setting-up-branch-protection)
12. [Your First Feature](#your-first-feature)
13. [Creating Your First Release](#creating-your-first-release)

---

## Prerequisites

Before we begin, ensure you have:

- **Python 3.12+** installed ([python.org](https://python.org))
- **Git** installed ([git-scm.com](https://git-scm.com))
- **GitHub account** ([github.com](https://github.com))
- **GitHub CLI** (optional but recommended): `gh` ([cli.github.com](https://cli.github.com))

Verify your installations:

```bash
python --version  # Should show 3.12 or higher
git --version     # Should show git version
gh --version      # (optional) Should show gh version
```

[SCREENSHOT: Terminal showing version checks for python, git, and gh]

---

## Installing UV - The Modern Python Package Manager

### What is UV?

**UV** is a blazingly fast Python package manager written in Rust. It's a modern replacement for `pip`, `poetry`, and `virtualenv` combined. Think of it as "Cargo for Python" - it handles:

- 🚀 **Dependency management** (10-100x faster than pip)
- 📦 **Virtual environment creation**
- 🔧 **Project scaffolding**
- 🏗️ **Building and publishing packages**
- 🔒 **Lock files** for reproducible environments

### Why UV over pip/poetry?

| Feature | pip | poetry | UV |
|---------|-----|--------|-----|
| Speed | Slow | Medium | **Extremely Fast** |
| Lock files | ❌ | ✅ | ✅ |
| Build backend | ❌ | ✅ | ✅ |
| Virtual envs | Manual | Built-in | Built-in |
| Resolver | Sometimes fails | Good | **Excellent** |

### Installing UV

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Via pip (if you prefer):**
```bash
pip install uv
```

**Verify installation:**
```bash
uv --version
```

[SCREENSHOT: Terminal showing successful UV installation and version]

### Basic UV Commands (Quick Reference)

Before we dive in, here are the essential UV commands you'll use:

```bash
# Initialize a new project
uv init <project-name>

# Sync dependencies (install/update)
uv sync

# Add a dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Run a command in the project environment
uv run <command>

# Build the package
uv build

# Update dependencies
uv sync --upgrade
```

---

## Creating the Project Structure

### Step 1: Create Project Directory

Let's create a Python library called `relperm` (relative permeability calculations for petroleum engineering):

```bash
# Navigate to your projects directory
cd ~/Documents/code

# Initialize the project with UV
uv init relperm
cd relperm
```

UV creates this initial structure:

```
relperm/
├── .python-version    # Specifies Python version
├── README.md          # Project description
├── pyproject.toml     # Project configuration
└── hello.py           # Example file (we'll replace this)
```

[SCREENSHOT: File explorer showing the initial project structure created by UV]

### Step 2: Organize for a Library

We'll reorganize to follow Python packaging best practices:

```bash
# Create src layout (recommended for libraries)
mkdir -p src/relperm
mkdir -p tests
mkdir -p docs
mkdir -p .github/workflows

# Remove the example file
rm hello.py

# Create package files
touch src/relperm/__init__.py
touch src/relperm/relperm.py
touch tests/__init__.py
touch tests/test_relperm.py
```

Your structure should now look like:

```
relperm/
├── .github/
│   └── workflows/        # CI/CD workflows (we'll populate this)
├── .python-version       # Python version constraint
├── src/
│   └── relperm/          # Source code
│       ├── __init__.py
│       └── relperm.py
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_relperm.py
├── docs/                 # Documentation (we'll populate this)
├── pyproject.toml        # Project config
└── README.md
```

[SCREENSHOT: File tree showing the complete project structure]

---

## Initializing the Python Project

### Step 3: Configure pyproject.toml

The `pyproject.toml` file is the heart of your Python project. It defines:
- Project metadata
- Dependencies
- Build system
- Tool configurations

Open `pyproject.toml` and replace it with:

```toml
[project]
name = "relperm"
version = "0.1.0"
description = "Relative permeability correlations for petroleum engineering"
readme = "README.md"
requires-python = ">=3.12"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "numpy>=2.3.2",
]

[project.urls]
Homepage = "https://github.com/yourusername/relperm"
Repository = "https://github.com/yourusername/relperm"
Documentation = "https://yourusername.github.io/relperm"

[build-system]
requires = ["uv_build>=0.8.14,<0.9.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "pytest>=8.4.2",
    "pytest-cov>=6.0.0",
    "ruff>=0.14.10",
    "ty>=0.0.5",
    "pre-commit>=4.5.1",
    "mkdocs>=1.6.1",
    "mkdocs-material>=9.7.1",
    "mkdocstrings>=1.0.0",
    "mkdocstrings-python>=2.0.1",
]
```

**Key sections explained:**

- **`[project]`**: Metadata about your package
- **`dependencies`**: Runtime dependencies (only NumPy for our library)
- **`[dependency-groups]`**: Development dependencies (testing, linting, docs)
- **`[build-system]`**: Uses UV's build backend

### Step 4: Install Dependencies

```bash
# Sync all dependencies (creates virtual environment automatically)
uv sync

# This creates:
# - .venv/ directory with isolated Python environment
# - uv.lock file for reproducible builds
```

[SCREENSHOT: Terminal showing `uv sync` output with dependency installation]

**What just happened?**

1. UV created a virtual environment (`.venv/`)
2. Installed all `dependencies` and `dev` dependencies
3. Generated `uv.lock` - a lock file ensuring everyone gets the same versions

---

## Setting Up Git and GitHub

### Step 5: Initialize Git Repository

```bash
# Initialize git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Documentation
site/
docs/_build/

# OS
.DS_Store
Thumbs.db
EOF

# Initial commit
git add .
git commit -m "Initial project structure"
```

[SCREENSHOT: Terminal showing git init and initial commit]

### Step 6: Create GitHub Repository

**Option A: Using GitHub CLI (Recommended)**

```bash
# Login to GitHub (if not already)
gh auth login

# Create repository (public)
gh repo create relperm --public --source=. --remote=origin

# Push to GitHub
git push -u origin main
```

**Option B: Using GitHub Web Interface**

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `relperm`
3. Description: "Relative permeability correlations for petroleum engineering"
4. Select **Public**
5. **Do NOT initialize** with README (we already have one)
6. Click "Create repository"

Then connect your local repo:

```bash
git remote add origin https://github.com/yourusername/relperm.git
git branch -M main
git push -u origin main
```

[SCREENSHOT: GitHub repository page showing the newly created repository]

---

## Installing Development Tools

Now let's install and configure the tools that enforce code quality.

### Step 7: Understanding the Tool Stack

| Tool | Purpose | Why We Need It |
|------|---------|----------------|
| **pytest** | Testing framework | Write and run tests |
| **pytest-cov** | Coverage reporting | Measure test coverage |
| **ruff** | Linter & formatter | Enforce code style, catch bugs |
| **ty** | Type checker | Catch type errors (Pyright-based) |
| **pre-commit** | Git hooks | Run checks before commits |
| **mkdocs** | Documentation | Generate beautiful docs |

All these are already in our `pyproject.toml` under `[dependency-groups]` and were installed with `uv sync`.

### Verify Installation

```bash
# Run in project environment
uv run pytest --version
uv run ruff --version
uv run ty --version
uv run mkdocs --version
```

[SCREENSHOT: Terminal showing all tool versions]

---

## Configuring Code Quality Tools

### Step 8: Configure Ruff (Linter & Formatter)

**What is Ruff?**

Ruff is an extremely fast Python linter and formatter (written in Rust). It replaces:
- `black` (formatting)
- `flake8` (linting)
- `isort` (import sorting)
- `pyupgrade` (syntax modernization)

**Why Ruff?**

- ⚡ **10-100x faster** than existing tools
- 🔧 **Auto-fixes** many issues
- 📦 **All-in-one** tool (no need for multiple linters)
- 🎯 **Drop-in replacement** for existing tools

Add this configuration to your `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
# Enable comprehensive rule sets
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort (import sorting)
    "B",    # flake8-bugbear (catches subtle bugs)
    "UP",   # pyupgrade (modern Python syntax)
    "N",    # pep8-naming (naming conventions)
    "D",    # pydocstyle (docstring enforcement)
    "NPY",  # NumPy-specific rules
    "PT",   # flake8-pytest-style
    "RUF",  # Ruff-specific rules
    "SIM",  # flake8-simplify
]

# Ignore rules that might be too strict initially
ignore = [
    "D100",  # Missing docstring in public module
    "D104",  # Missing docstring in public package
]

[tool.ruff.lint.pydocstyle]
convention = "numpy"  # Use NumPy docstring style

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Test Ruff:**

```bash
# Format code
uv run ruff format .

# Check for issues
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .
```

[SCREENSHOT: Terminal showing ruff format and ruff check output]

### Step 9: Configure Ty (Type Checker)

**What is Ty?**

Ty is a fast type checker for Python based on Pyright. It catches type-related bugs before runtime.

**Why Type Checking?**

```python
# Without type checking - runtime error
def calculate(x):
    return x / 2

calculate("hello")  # Error at runtime!

# With type hints - caught by ty before running
def calculate(x: float) -> float:
    return x / 2

calculate("hello")  # ty catches this immediately!
```

Add this to `pyproject.toml`:

```toml
[tool.ty.environment]
python-version = "3.12"

[tool.ty.rules]
# Enforce type checking
# Start lenient, increase strictness over time
```

**Test Ty:**

```bash
uv run ty check
```

[SCREENSHOT: Terminal showing ty check output]

### Step 10: Configure Pytest

Add this to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=relperm",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.coverage.run]
source = ["src"]

[tool.coverage.report]
# Require at least 90% test coverage
fail_under = 90
```

**Test Pytest:**

```bash
uv run pytest
```

---

## Creating GitHub Workflows

GitHub Actions automate testing, linting, and releases. Let's create two workflows:

1. **Quality Checks** - Runs on every PR
2. **Release** - Publishes to PyPI on git tags

### Step 11: Quality Workflow

Create `.github/workflows/quality.yaml`:

```yaml
name: Quality Checks

on:
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"

      - name: Set up Python
        run: uv python install

      - name: Install dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest

  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"

      - name: Set up Python
        run: uv python install

      - name: Install dependencies
        run: uv sync

      - name: Check formatting
        run: uv run ruff format --check .

      - name: Lint code
        run: uv run ruff check .

      - name: Type check
        run: uv run ty check
```

**What this does:**

- ✅ Runs on every PR to `main`
- ✅ Tests in parallel: `test` job + `lint` job
- ✅ Blocks merge if checks fail

[SCREENSHOT: GitHub Actions workflow file in VS Code or text editor]

### Step 12: Release Workflow

Create `.github/workflows/release.yaml`:

```yaml
name: Release

on:
  push:
    tags:
      - '*'

permissions:
  contents: write
  id-token: write

jobs:
  pypi-publish:
    name: Publish to PyPI
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/p/relperm

    steps:
      - uses: actions/checkout@v4

      - name: Install UV
        uses: astral-sh/setup-uv@v5
        with:
          version: "latest"

      - name: Set up Python
        run: uv python install

      - name: Build package
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
```

**What this does:**

- 🏷️ Triggers when you push a git tag (e.g., `v0.1.0`)
- 📦 Builds the package with `uv build`
- 🚀 Publishes to PyPI (using Trusted Publisher)
- 📝 Creates GitHub release with auto-generated notes

**Commit workflows:**

```bash
git add .github/workflows/
git commit -m "Add CI/CD workflows"
git push
```

[SCREENSHOT: GitHub repository showing the two workflow files in .github/workflows/]

---

## Setting Up Documentation

### Step 13: Configure MkDocs

MkDocs generates beautiful documentation from Markdown files.

**Create `mkdocs.yml`:**

```yaml
site_name: Relperm Documentation
site_description: Relative permeability correlations for petroleum engineering
site_author: Your Name
site_url: https://yourusername.github.io/relperm

repo_url: https://github.com/yourusername/relperm
repo_name: yourusername/relperm

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
    - search.suggest

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: numpy
            show_source: true

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.arithmatex:
      generic: true

extra_javascript:
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

nav:
  - Home: index.md
  - API Reference: reference.md
```

**Create documentation files:**

```bash
# Create docs structure
cat > docs/index.md << 'EOF'
# Relperm

Relative permeability correlations for petroleum engineering.

## Installation

```bash
pip install relperm
```

## Quick Start

```python
import numpy as np
from relperm import corey_krw

sw = np.linspace(0.2, 0.8, 50)
krw = corey_krw(sw, swr=0.2, snwr=0.2, krw0=0.8, nw=2.0)
```
EOF

cat > docs/reference.md << 'EOF'
# API Reference

::: relperm
EOF
```

**Test documentation locally:**

```bash
uv run mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

[SCREENSHOT: MkDocs documentation site showing the homepage]

**Commit documentation:**

```bash
git add mkdocs.yml docs/
git commit -m "Add documentation configuration"
git push
```

---

## Configuring Pre-commit Hooks

Pre-commit hooks run checks **before** you commit, catching issues early.

### Step 14: Create Pre-commit Configuration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-toml
```

**Install hooks:**

```bash
uv run pre-commit install
```

**Test hooks manually:**

```bash
uv run pre-commit run --all-files
```

Now, every time you `git commit`, these checks run automatically!

[SCREENSHOT: Terminal showing pre-commit hooks running on commit]

**Commit configuration:**

```bash
git add .pre-commit-config.yaml
git commit -m "Add pre-commit hooks"
git push
```

---

## Setting Up Branch Protection

Branch protection prevents direct pushes to `main` and enforces code review.

### Step 15: Enable Branch Protection

**Via GitHub Web Interface:**

1. Go to your repository on GitHub
2. Click **Settings** → **Branches**
3. Under "Branch protection rules", click **Add rule**
4. Branch name pattern: `main`
5. Enable these settings:
   - ✅ **Require a pull request before merging**
   - ✅ **Require status checks to pass before merging**
     - Add required checks: `test`, `lint`
   - ✅ **Require branches to be up to date before merging**
   - ✅ **Do not allow bypassing the above settings**
6. Click **Create** or **Save changes**

[SCREENSHOT: GitHub branch protection rules configuration page]

**Via GitHub CLI:**

```bash
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_pull_request_reviews='{"required_approving_review_count":0}' \
  --field required_status_checks='{"strict":true,"contexts":["test","lint"]}' \
  --field enforce_admins=true \
  --field restrictions=null
```

**What this means:**

- ❌ You **cannot** push directly to `main`
- ✅ You **must** create a pull request
- ✅ PRs **must** pass `test` and `lint` checks
- ✅ Even admins follow these rules

---

## Your First Feature

Let's implement a simple function following best practices.

### Step 16: Create Feature Branch

**IMPORTANT:** Always work on feature branches!

```bash
# Make sure main is up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/corey-model
```

### Step 17: Write Code with Type Hints and Docstrings

Edit `src/relperm/relperm.py`:

```python
"""Relative permeability correlations."""

import numpy as np
import numpy.typing as npt


def corey_krw(
    sw: npt.NDArray[np.float64],
    swr: float,
    snwr: float,
    krw0: float,
    nw: float,
) -> npt.NDArray[np.float64]:
    r"""Calculate wetting phase relative permeability using Corey model.

    The Corey model is a simple power-law correlation widely used in
    petroleum engineering for relative permeability calculations.

    Parameters
    ----------
    sw : np.ndarray
        Wetting phase saturation, dimensionless [0, 1].
    swr : float
        Residual wetting phase saturation, dimensionless [0, 1).
    snwr : float
        Residual non-wetting phase saturation, dimensionless [0, 1).
    krw0 : float
        Endpoint relative permeability at Sw = 1 - Snwr, dimensionless (0, 1].
    nw : float
        Corey exponent for wetting phase, dimensionless (>0).

    Returns
    -------
    np.ndarray
        Relative permeability for wetting phase, same shape as `sw`.

    Notes
    -----
    The Corey model is defined as:

    $$k_{rw} = k_{rw}^0 \left(\frac{S_w - S_{wr}}{1 - S_{wr} - S_{nwr}}\right)^{n_w}$$

    where $S_w$ is the wetting phase saturation.

    Examples
    --------
    >>> import numpy as np
    >>> sw = np.array([0.2, 0.4, 0.6, 0.8])
    >>> krw = corey_krw(sw, swr=0.2, snwr=0.2, krw0=0.8, nw=2.0)
    >>> krw.shape
    (4,)

    References
    ----------
    .. [1] Corey, A.T., "The Interrelation Between Gas and Oil Relative
           Permeabilities", Producers Monthly, 1954.
    """
    # Calculate effective saturation
    s_eff = (sw - swr) / (1.0 - swr - snwr)

    # Corey correlation
    return krw0 * s_eff**nw
```

Update `src/relperm/__init__.py`:

```python
"""Relperm - Relative permeability correlations for petroleum engineering."""

from relperm.relperm import corey_krw

__all__ = ["corey_krw"]
__version__ = "0.1.0"
```

### Step 18: Write Tests

Edit `tests/test_relperm.py`:

```python
"""Tests for relative permeability correlations."""

import numpy as np
import pytest
from relperm import corey_krw


def test_corey_krw_basic():
    """Test basic Corey correlation calculation."""
    sw = np.array([0.2, 0.4, 0.6, 0.8])
    krw = corey_krw(sw, swr=0.2, snwr=0.2, krw0=0.8, nw=2.0)

    assert krw.shape == sw.shape
    assert np.all(krw >= 0)
    assert np.all(krw <= 0.8)


def test_corey_krw_endpoints():
    """Test Corey correlation at endpoints."""
    # At Sw = Swr, krw should be 0
    sw_min = np.array([0.2])
    krw_min = corey_krw(sw_min, swr=0.2, snwr=0.2, krw0=0.8, nw=2.0)
    assert np.isclose(krw_min[0], 0.0)

    # At Sw = 1 - Snwr, krw should be krw0
    sw_max = np.array([0.8])
    krw_max = corey_krw(sw_max, swr=0.2, snwr=0.2, krw0=0.8, nw=2.0)
    assert np.isclose(krw_max[0], 0.8)


def test_corey_krw_monotonic():
    """Test that krw increases monotonically with Sw."""
    sw = np.linspace(0.2, 0.8, 50)
    krw = corey_krw(sw, swr=0.2, snwr=0.2, krw0=0.8, nw=2.0)

    # Check monotonicity
    assert np.all(np.diff(krw) >= 0)
```

### Step 19: Run Quality Checks Locally

```bash
# Run tests
uv run pytest

# Format code
uv run ruff format .

# Lint code
uv run ruff check --fix .

# Type check
uv run ty check
```

All checks should pass!

[SCREENSHOT: Terminal showing all quality checks passing]

### Step 20: Commit and Push

```bash
git add .
git commit -m "Implement Corey relative permeability model

- Add corey_krw function with full type hints
- Include NumPy-style docstring with LaTeX equations
- Add comprehensive tests for basic behavior, endpoints, and monotonicity
- All quality checks passing (pytest, ruff, ty)"

git push -u origin feature/corey-model
```

### Step 21: Create Pull Request

**Using GitHub CLI:**

```bash
gh pr create \
  --title "Implement Corey relative permeability model" \
  --body "Adds the industry-standard Corey correlation for calculating wetting phase relative permeability.

## Changes
- Core implementation with type hints and validation
- Comprehensive test suite (>90% coverage)
- NumPy-style documentation with equations

## Testing
- ✅ All tests pass
- ✅ Code formatted with ruff
- ✅ Type checking passes with ty"
```

**Using GitHub Web:**

1. Go to your repository on GitHub
2. Click "Compare & pull request" button
3. Fill in title and description
4. Click "Create pull request"

[SCREENSHOT: GitHub pull request page showing quality checks running]

**Wait for checks to pass**, then merge!

[SCREENSHOT: GitHub pull request showing all checks passed with green checkmarks]

### Step 22: Merge and Clean Up

```bash
# Merge via GitHub interface (squash merge)
# Then update local main
git checkout main
git pull origin main
git branch -d feature/corey-model
```

---

## Creating Your First Release

### Step 23: Update Version

Edit `pyproject.toml`:

```toml
[project]
version = "0.1.0"  # Your first release version
```

Commit:

```bash
git add pyproject.toml
git commit -m "Bump version to 0.1.0"
git push
```

### Step 24: Set Up PyPI Trusted Publisher

Before creating a release, configure PyPI to trust your GitHub workflow:

1. Create account on [PyPI](https://pypi.org/account/register/)
2. Go to [Account Settings → Publishing](https://pypi.org/manage/account/publishing/)
3. Click "Add a new pending publisher"
4. Fill in:
   - **PyPI Project Name:** `relperm`
   - **Owner:** `yourusername`
   - **Repository:** `relperm`
   - **Workflow name:** `release.yaml`
   - **Environment name:** `pypi`
5. Click "Add"

[SCREENSHOT: PyPI trusted publisher configuration page]

### Step 25: Create and Push Tag

```bash
# Create annotated tag
git tag -a 0.1.0 -m "Release v0.1.0

- Initial release
- Corey relative permeability model
- Comprehensive documentation
- Full test coverage"

# Push tag to trigger release workflow
git push origin 0.1.0
```

### Step 26: Watch the Magic Happen

Go to your repository → **Actions** tab and watch the release workflow:

1. ✅ Build package
2. ✅ Publish to PyPI
3. ✅ Create GitHub Release

[SCREENSHOT: GitHub Actions showing successful release workflow]

After a few minutes, your package is live!

**Check PyPI:**
```bash
pip install relperm  # Available worldwide!
```

[SCREENSHOT: PyPI package page showing the published package]

---

## Summary

You've now set up a professional Python project with:

✅ **Modern tooling:** UV for blazing-fast dependency management
✅ **Code quality:** Ruff (linting/formatting) + Ty (type checking)
✅ **Testing:** Pytest with >90% coverage requirement
✅ **Documentation:** MkDocs with Material theme
✅ **CI/CD:** Automated testing and releases via GitHub Actions
✅ **Branch protection:** Enforced code review and quality gates
✅ **Pre-commit hooks:** Catch issues before they reach CI
✅ **Automated publishing:** One git tag = PyPI release

## Key Takeaways

1. **UV is fast** - 10-100x faster than pip for dependency resolution
2. **Ruff replaces many tools** - One tool for linting, formatting, import sorting
3. **Type hints catch bugs** - Use ty to catch type errors before runtime
4. **Branch protection is essential** - Prevents accidental direct pushes to main
5. **Automate everything** - Let CI/CD handle testing, linting, and releases
6. **Documentation matters** - MkDocs + mkdocstrings = beautiful auto-generated docs
7. **Pre-commit saves time** - Catch issues locally before pushing

## Next Steps

- Add more correlations (LET model, Brooks-Corey, etc.)
- Increase test coverage with property-based testing (hypothesis)
- Add example gallery with Jupyter notebooks
- Set up code coverage reporting (codecov.io)
- Add badges to README (tests, coverage, PyPI version)

## Useful Commands Reference

```bash
# UV commands
uv sync                    # Install/update dependencies
uv add <package>           # Add runtime dependency
uv add --dev <package>     # Add dev dependency
uv run <command>           # Run command in project env
uv build                   # Build package

# Quality checks
uv run pytest              # Run tests
uv run pytest --cov        # Run tests with coverage
uv run ruff format .       # Format code
uv run ruff check .        # Lint code
uv run ruff check --fix .  # Auto-fix issues
uv run ty check            # Type check

# Documentation
uv run mkdocs serve        # Preview docs locally
uv run mkdocs build        # Build docs

# Git workflow
git checkout main && git pull           # Sync main
git checkout -b feature/my-feature      # Create feature branch
git push -u origin feature/my-feature   # Push feature branch
gh pr create                            # Create pull request
git tag 0.1.0 && git push origin 0.1.0  # Create release
```

---

**Happy coding! 🚀**
