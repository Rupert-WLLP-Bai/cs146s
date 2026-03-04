# Assignments for CS146S: The Modern Software Developer

This is the home of the assignments for [CS146S: The Modern Software Developer](https://themodernsoftware.dev), taught at Stanford University fall 2025.

## Repo Setup
These steps work with Python 3.12 (project supports `>=3.10,<4.0`).

1. Install `uv`
   - https://docs.astral.sh/uv/getting-started/installation/

2. Install project dependencies from the repository root
   ```bash
   uv sync --group dev
   ```

3. Run commands through `uv`
   ```bash
   uv run uvicorn week2.app.main:app --reload
   uv run pytest
   uv run ruff check .
   ```
