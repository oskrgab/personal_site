---
title: "Modern Stack for Python Projects Part 2: CI/CD & Releases"
lastmod: 2025-12-24
date: 2025-12-24
draft: false
topics: ["python", "cicd", "github-actions"]
summary: "Setting up automated workflows for quality checks, documentation with MkDocs, and automated PyPI releases."
---

In [Part 1]({{< ref "blog/4_modern_python_stack_part_1_setup" >}}), we set up our local development environment with UV, Ruff, and pre-commit hooks. Now, we'll automate everything using GitHub Actions and set up our documentation.

## Creating GitHub Workflows

GitHub Actions automate testing, linting, and releases. We'll create two workflows:

1. **Quality Checks** - Runs on every PR
2. **Release** - Publishes to PyPI on git tags

### Step 1: Quality Workflow

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

![Screenshot: GitHub Actions workflow file in VS Code or text editor]

### Step 2: Release Workflow

Create `.github/workflows/release.yaml`. This uses **Trusted Publishing** (configured later in PyPI) so we don't need to manage API tokens manually.

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

## Setting Up Documentation

We'll use **MkDocs** with the **Material** theme for beautiful, static documentation.

### Configure MkDocs

Create `mkdocs.yml` in the root directory:

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

![Screenshot: MkDocs documentation site showing the homepage]

**Commit documentation:**

```bash
git add mkdocs.yml docs/
git commit -m "Add documentation configuration"
git push
```

## Your First Feature

Let's verify our setup by implementing a simple feature.

### Step 1: Create Feature Branch

**IMPORTANT:** Always work on feature branches!

```bash
# Make sure main is up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/corey-model
```

### Step 2: Write Code with Type Hints and Docstrings

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

### Step 3: Write Tests

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

### Step 4: Run Quality Checks Locally

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

### Step 5: Commit, Push, and Create PR

```bash
git add .
git commit -m "Implement Corey relative permeability model"
git push -u origin feature/corey-model

gh pr create --title "Implement Corey relative permeability model" --body "..."
```

**Wait for checks to pass**, then merge!

![Screenshot: GitHub pull request showing all checks passed with green checkmarks]

## Creating Your First Release

### Step 1: Update Version

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

### Step 2: Set Up PyPI Trusted Publisher

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

### Step 3: Create and Push Tag

```bash
# Create annotated tag
git tag -a 0.1.0 -m "Release v0.1.0"

# Push tag to trigger release workflow
git push origin 0.1.0
```

### Step 4: Watch the Magic Happen

Go to your repository → **Actions** tab and watch the release workflow:

1. ✅ Build package
2. ✅ Publish to PyPI
3. ✅ Create GitHub Release

After a few minutes, your package is live!

**Check PyPI:**
```bash
pip install relperm  # Available worldwide!
```

![Screenshot: PyPI package page showing the published package]

## Conclusion

We now have a fully automated pipeline. But how do we ensure our repository stays clean and safe as we scale? In [Part 3]({{< ref "blog/6_modern_python_stack_part_3_git_strategy" >}}), we will cover the robust Git strategy and branch protection rules.