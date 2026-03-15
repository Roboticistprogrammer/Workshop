# UV Setup Guide

## What is UV?

**UV** is a fast Python package installer and resolver written in Rust. It's designed to replace pip and poetry for dependency management with significantly improved performance.

### Key Benefits
- ⚡ **10-100x faster** than pip
- 🔒 Deterministic dependency resolution
- 📦 Works with `pyproject.toml` for dependency management
- 🎯 Minimal setup required

## Installation

UV comes pre-installed in this project. Check the version:
```bash
uv --version
```

## Important Commands

### Initialize a new project
```bash
uv init -n <project_name>
```

### Install dependencies from pyproject.toml
```bash
uv sync
```

### Add a new package
```bash
uv add <package_name>
```

### Add a dev dependency
```bash
uv add --dev <package_name>
```

### Run scripts in the virtual environment
```bash
uv run python script.py
```

### Remove a package
```bash
uv remove <package_name>
```

## Current Project Setup

**Dependencies installed:**
- `opencv-python` - For video processing

### View installed packages
```bash
uv pip list
```

## Project Structure
```
workshop/
├── pyproject.toml        # Project configuration and dependencies
├── .venv/                # Virtual environment (auto-created)
├── 01/                   # Project 1: FPS Threading Comparison
│   ├── no_threading.py
│   ├── cap_multithreading.py
│   ├── gui_utils.py
│   ├── comparison.py
│   └── Readme.md
└── data/
    └── sample.mp4        # Sample video file
```

## Quick Start

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run Project 1 - Single-threaded:**
   ```bash
   cd 01
   uv run python no_threading.py
   ```

3. **Run Project 1 - Multi-threaded:**
   ```bash
   cd 01
   uv run python cap_multithreading.py
   ```

4. **Run comparison:**
   ```bash
   cd 01
   uv run python comparison.py
   ```

## Troubleshooting

- **Virtual environment issues:** Delete `.venv/` and run `uv sync` again
- **Missing packages:** Run `uv sync` to ensure all dependencies are installed
- **Virtual environment not activating:** Use `uv run` prefix instead