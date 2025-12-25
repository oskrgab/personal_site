---
title: "Modern Stack for Python Projects Part 1: Setup & Tooling"
lastmod: 2025-12-23
date: 2025-12-23
draft: false
topics: ["python", "uv", "tooling"]
summary: "A comprehensive guide to setting up a professional Python project with modern tooling: UV, Ruff, Ty, and Pre-commit."
---

The python package ecosystem has changed a lot since the last time I attempted to create a Python package.

I put myself the challenge for the past couple of weeks to publish a python package with some simple domain-knowledge functionality, in this case, relative permeabilities and capillary pressures in the context of the O&G industry.

The purpose of this exercise is to go from having nothing to creating a full project that can be published to PyPI, using a modern tech stack, CI/CD and testing. I want this to serve as a blueprint for future packages that I can build or to help somebody else in the same boat as me.

This is **Part 1** of a three-part series, focusing on the local development environment and tooling.

## Prerequisites

One of the best things about this modern stack is that you don't even need Python installed on your system to get started! **UV** can handle downloading and managing Python versions for you on a per-project basis.

Before we begin, ensure you have:

- **Git** installed ([git-scm.com](https://git-scm.com))
- **GitHub account** ([github.com](https://github.com))
- **GitHub CLI** (optional but recommended): `gh` ([cli.github.com](https://cli.github.com))

Verify your installations:

```bash
git --version     # Should show git version
gh --version      # (optional) Should show gh version
```

![Screenshot: Terminal showing version checks for git, and gh]

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

**Verify installation:**
```bash
uv --version
```

![Screenshot: Terminal showing successful UV installation and version]

### Basic UV Commands (Quick Reference)

Before we dive in, here are the essential UV commands you'll use:

```bash
# Initialize a new project
uv init <project-name>

# Sync dependencies (install/update)
# This will automatically download the required Python version!
uv sync

# Install a specific Python version manually
uv python install 3.12

# List available and installed Python versions
uv python list

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

![Screenshot: File explorer showing the initial project structure created by UV]

### Step 2: Organize for a Library

We'll reorganize to follow Python packaging best practices using the `src` layout:

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
│   └── workflows/        # CI/CD workflows (we'll populate this in Part 2)
├── .python-version       # Python version constraint
├── src/
│   └── relperm/          # Source code
│       ├── __init__.py
│       └── relperm.py
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_relperm.py
├── docs/                 # Documentation (we'll populate this in Part 2)
├── pyproject.toml        # Project config
└── README.md
```

![Screenshot: File tree showing the complete project structure]

## Initializing the Python Project

### Step 3: Configure pyproject.toml

The `pyproject.toml` file is the heart of your Python project. Open `pyproject.toml` and replace it with:

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
```

**Note:** If you don't have the required Python version (3.12+ as specified in our `pyproject.toml`), `uv` will automatically download it for you during this step! No more worrying about system-wide Python installations.

This creates the `.venv/` directory and `uv.lock` file, ensuring everyone works with the same versions.

![Screenshot: Terminal showing `uv sync` output with dependency installation]

## Setting Up Git and GitHub

### Initialize Git Repository

```bash
# Initialize git
git init

# Create .gitignore (make sure to exclude .venv, __pycache__, etc.)
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

![Screenshot: Terminal showing git init and initial commit]

### Create GitHub Repository

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

## Installing Development Tools

Now let's install and configure the tools that enforce code quality.

### Understanding the Tool Stack

| Tool | Purpose | Why We Need It |
|------|---------|----------------|
| **pytest** | Testing framework | Write and run tests |
| **pytest-cov** | Coverage reporting | Measure test coverage |
| **ruff** | Linter & formatter | Enforce code style, catch bugs |
| **ty** | Type checker | Catch type errors (Pyright-based) |
| **pre-commit** | Git hooks | Run checks before commits |
| **mkdocs** | Documentation | Generate beautiful docs |

All these are already in our `pyproject.toml` under `[dependency-groups]` and were installed with `uv sync`.

## Configuring Code Quality Tools

### Configure Ruff (Linter & Formatter)

**What is Ruff?**
Ruff is an extremely fast Python linter and formatter (written in Rust). It replaces `black` (formatting), `flake8` (linting), `isort` (import sorting), and `pyupgrade`.

Add this to `pyproject.toml`:

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
ignore = ["D100", "D104"]

[tool.ruff.lint.pydocstyle]
convention = "numpy"

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

### Configure Ty (Type Checker)

**What is Ty?**
Ty is a fast type checker for Python based on Pyright. It catches type-related bugs before runtime.

Add this to `pyproject.toml`:

```toml
[tool.ty.environment]
python-version = "3.12"

[tool.ty.rules]
# Enforce type checking
# Start lenient, increase strictness over time
```

### Configure Pytest

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

## Configuring Pre-commit Hooks

Pre-commit hooks run checks **before** you commit, catching issues early.

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

**Install and Run:**

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

Now, every time you `git commit`, these checks run automatically!

![Screenshot: Terminal showing pre-commit hooks running on commit]

## Conclusion

We now have a professional local development environment setup. In [Part 2]({{< ref "blog/5_modern_python_stack_part_2_cicd" >}}), we'll set up GitHub Actions for CI/CD, creating documentation, and publishing our first release.