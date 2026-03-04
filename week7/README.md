# Week 7

Slightly enhanced full‑stack starter (copied from Week 5) with a few backend improvements.

- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Minimal tests (pytest)
- Pre-commit (black + ruff)
- Enhancements over Week 5:
  - Timestamps on models (`created_at`, `updated_at`)
  - Pagination and sorting for list endpoints
  - Optional filters (e.g., filter action items by completion)
  - PATCH endpoints for partial updates

## Quickstart

1) Install dependencies from the repository root

```bash
uv sync --group dev
```

2) (Optional) Install pre-commit hooks

```bash
uv run pre-commit install
```

3) Run the app (from `week7/`)

```bash
cd week7 && uv run make run
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
cd week7 && uv run make test
```

## Formatting/Linting

```bash
cd week7 && uv run make format
cd week7 && uv run make lint
```

## Configuration

Copy `.env.example` to `.env` (in `week7/`) to override defaults like the database path.

