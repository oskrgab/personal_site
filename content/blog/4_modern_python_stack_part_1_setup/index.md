---
title: "Modern Stack for Python Projects Part 1: Setup & Tooling"
lastmod: 2025-12-23
date: 2025-12-23
draft: false
topics: ["python", "uv", "tooling"]
summary: "A beginner-friendly guide to setting up a professional Python project with modern tooling: UV, Ruff, Ty, and Pre-commit. Written for engineers who code, not professional developers."
---

If you're an engineer who writes Python scripts to solve problems—whether it's calculating relative permeabilities, modeling heat transfer, or analyzing production data—this guide is for you.

I recently challenged myself to publish a Python package with some petroleum engineering functionality (specifically, relative permeabilities and capillary pressures). Along the way, I discovered how much the Python ecosystem has improved. Gone are the days of wrestling with `pip install` errors and virtual environment headaches.

This is **Part 1** of a three-part series. Here, we'll focus on *why* we set things up the way we do, and *what* this modern tooling enables. We won't dive into every terminal command—you'll be using VSCode for most of this anyway.

## Why Should You Care About Any of This?

Let me paint a picture you might recognize: You wrote a Python script six months ago. It worked perfectly. Now you need it again, and... nothing works. Python version mismatch. Missing packages. That one library updated and broke everything.

Or maybe: You're collaborating with a colleague. They send you their script. It doesn't run on your machine because they have different packages installed.

**Modern Python tooling solves these problems.** Here's what we're setting up and why:

| Tool | What It Does | Why You Care |
|------|--------------|--------------|
| **UV** | Manages Python versions and packages | "It just works" on any machine |
| **Git + GitHub** | Tracks changes, enables collaboration | Never lose your work, easy sharing |
| **Ruff** | Checks and formats your code | Catch bugs before they bite |
| **Ty** | Checks your types | Find mistakes before running code |
| **Pre-commit** | Runs checks automatically | Enforces quality without thinking |

## Version Control: Your Safety Net

Before we talk about Python tools, let's address something fundamental: **version control with Git**.

If you've ever had files named `script_v2_final_FINAL_actually_final.py`, you understand the problem Git solves.

### What Git Actually Does For You

Think of Git as an "infinite undo" for your entire project:

- **Track every change**: See exactly what you modified and when
- **Experiment freely**: Try new approaches without fear—you can always go back
- **Collaborate**: Multiple people can work on the same project without overwriting each other
- **Backup**: Your code lives on GitHub, not just your laptop

### GitHub: Git in the Cloud

GitHub is where your Git repository lives online. It provides:

- **Backup**: Your laptop could die tomorrow and your code survives
- **Sharing**: Send a link instead of a zip file
- **Automation**: Run tests and checks automatically (more on this in Part 2)
- **Publishing**: Host your documentation and release your package

**Screenshot suggestion 1**: GitHub repository page showing the relperm project with the green "Code" button and file listing.

## Installing UV: The Modern Python Manager

UV is a game-changer. It's a single tool that replaces the confusing mix of `pip`, `virtualenv`, `poetry`, and `conda` that used to be the Python experience.

### Why UV Over the Old Way?

Remember these frustrations?

- "Which Python version is installed?" (trick question—you probably have 5)
- "Is my virtual environment activated?"
- "Why does `pip install` take forever?"
- "Works on my machine..."

UV eliminates all of this:

```bash
# Install UV (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
```

That's it. UV now handles:
- **Python versions**: Automatically downloads the right Python for each project
- **Virtual environments**: Created and managed for you
- **Package installation**: 10-100x faster than pip (seriously)
- **Lock files**: Guarantees everyone uses identical package versions

**Screenshot suggestion 2**: Terminal showing `uv --version` output after successful installation.

## Creating Your Project

With UV installed, creating a new project is simple:

```bash
uv init relperm
cd relperm
```

UV creates your starter files:

```
relperm/
├── .python-version    # Which Python version to use
├── pyproject.toml     # Project configuration (we'll explore this)
├── README.md          # Description of your project
└── main.py            # A starter script
```

Here's what the initial `pyproject.toml` looks like—UV created this for us:

```toml
[project]
name = "relperm"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []
```

This one file defines your entire project. No more scattered `requirements.txt`, `setup.py`, and `setup.cfg` files.

## The Project Structure: Why It Matters

Now let's organize the project properly. Here's the structure we're building toward:

```
relperm/
├── src/
│   └── relperm/          # Your actual code lives here
│       ├── __init__.py
│       └── relperm.py
├── tests/                # Tests for your code
│   └── test_relperm.py
├── docs/                 # Documentation
│   └── index.md
├── .github/
│   └── workflows/        # Automation (Part 2)
├── pyproject.toml        # The single source of truth
└── README.md
```

### Why This Structure?

**The `src/` layout**: Your code goes inside `src/relperm/`, not at the root. This prevents a subtle but common bug where tests accidentally import from your local folder instead of the installed package. Trust me, this saves headaches.

**The `tests/` directory**: Keeps your tests separate from your code. You write tests to verify your equations and calculations work correctly—especially important for engineering code where mistakes can be costly.

**The `docs/` directory**: Documentation lives here. We'll use a tool called MkDocs that turns simple markdown files into a beautiful website (for free!).

**The `.github/workflows/` directory**: Automation scripts that run on GitHub. Every time you push code, GitHub can automatically run your tests and check for errors. We'll set this up in Part 2.

**Screenshot suggestion 3**: VSCode Explorer panel showing the complete project structure with folders expanded.

## Adding Development Tools

Here's where it gets interesting. We're going to add tools that automatically catch bugs and format our code. First, let's add them to our project.

In VSCode, open `pyproject.toml` and add a `dependency-groups` section:

```toml
[project]
name = "relperm"
version = "0.1.0"
description = "Relative permeability correlations for petroleum engineering"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "numpy>=2.3.2",
]

[build-system]
requires = ["uv_build>=0.8.14,<0.9.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "pytest>=8.4.2",
    "ruff>=0.14.10",
    "ty>=0.0.5",
    "pre-commit>=4.5.1",
]
```

Then install everything:

```bash
uv sync
```

UV creates a virtual environment, downloads the right Python version if needed, and installs all dependencies. One command. No activation needed.

### What These Tools Do

**Pytest**: Runs your tests. You write small functions that verify your calculations are correct.

**Ruff**: This is like having a code reviewer looking over your shoulder. It catches:
- Unused imports and variables
- Common bugs and gotchas
- Style inconsistencies
- Missing documentation

**Ty**: Checks that your types make sense. If you pass a string where a number is expected, Ty catches it before you run the code.

**Pre-commit**: The enforcer. Runs Ruff and other checks automatically every time you commit. You literally cannot commit bad code.

## Configuring Ruff: The Linter

Add this configuration to your `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # Style errors
    "F",    # Logic errors
    "I",    # Import sorting
    "B",    # Common bugs
    "UP",   # Modern Python syntax
    "N",    # Naming conventions
    "D",    # Docstrings (documentation)
    "NPY",  # NumPy best practices
]
ignore = ["D100", "D104"]  # Don't require docstrings for modules

[tool.ruff.lint.pydocstyle]
convention = "numpy"  # Use NumPy-style docstrings

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

Now you can run:

```bash
uv run ruff check .      # Find issues
uv run ruff check --fix . # Auto-fix what it can
uv run ruff format .     # Format your code consistently
```

**Screenshot suggestion 4**: VSCode with a Python file open showing Ruff squiggly underlines highlighting issues, with the Problems panel open at the bottom.

## Configuring Ty: The Type Checker

Add this simple configuration:

```toml
[tool.ty.environment]
python-version = "3.12"
```

Run it with:

```bash
uv run ty check
```

Ty reads your type hints (like `def calculate(x: float) -> float:`) and verifies they're consistent throughout your code.

## Pre-commit: Automatic Quality Checks

Create a file called `.pre-commit-config.yaml` in your project root:

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
      - id: check-toml
```

Install the hooks:

```bash
uv run pre-commit install
```

Now, every time you try to commit code, these checks run automatically. If something fails, the commit is blocked until you fix it. This sounds strict, but it's actually liberating—you never have to worry about committing broken code.

**Screenshot suggestion 5**: Terminal showing pre-commit hooks running on a commit, with green "Passed" indicators for each check.

## Pushing to GitHub

If you have the GitHub CLI installed, creating your repository is simple:

```bash
git init
git add .
git commit -m "Initial project structure"
gh repo create relperm --public --source=. --push
```

Your code is now on GitHub, backed up and ready to share.

## What We've Accomplished

Let's step back and appreciate what we have:

1. **Reproducible environment**: Anyone can clone your repo, run `uv sync`, and get the exact same setup
2. **Automatic quality checks**: Ruff catches bugs, Ty catches type errors, pre-commit enforces both
3. **Professional structure**: Your code is organized in a way that scales and follows Python best practices
4. **Version control**: Every change is tracked, you can collaborate, and your work is backed up

This might seem like a lot of setup for "just a Python script." But this foundation pays dividends:

- Your code works months later
- Others can use and contribute to your work
- You catch bugs before they cause problems
- Publishing to PyPI becomes straightforward (Part 3)

## Coming Up in Part 2

In the next post, we'll set up:
- **GitHub Actions**: Automated testing on every push
- **MkDocs**: Turn your docstrings into a beautiful documentation website
- **Coverage reports**: See which parts of your code are tested

The goal is a fully automated pipeline: push code, tests run, documentation updates, and eventually, your package publishes to PyPI automatically.

See you in Part 2!

---

*This post is part of a series documenting the creation of [relperm](https://github.com/oskrgab/relperm), a Python library for petroleum engineering relative permeability calculations.*
