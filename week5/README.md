# Week 5

Minimal full‑stack starter for experimenting with autonomous coding agents.

- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Minimal tests (pytest)
- Pre-commit (black + ruff)
- Tasks to practice agent-driven workflows

## Quickstart

1) Install dependencies from the repository root

```bash
uv sync --group dev
```

2) (Optional) Install pre-commit hooks

```bash
uv run pre-commit install
```

3) Run the app (from `week5/`)

```bash
cd week5 && uv run make run
```

Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

## Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS for agent-driven workflows
```

## Tests

```bash
cd week5 && uv run make test
```

## Formatting/Linting

```bash
cd week5 && uv run make format
cd week5 && uv run make lint
```

## Configuration

Copy `.env.example` to `.env` (in `week5/`) to override defaults like the database path.
