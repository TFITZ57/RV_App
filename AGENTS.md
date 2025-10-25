# Repository Guidelines

## Project Structure & Module Organization
FastAPI services live in `backend/`, with routers under `backend/routers/` and long-running logic in `backend/services/`. Shared config and DB helpers are in `backend/config.py` and `backend/db.py`. Browser assets (`index.html`, `app.js`, `styles.css`) stay under `backend/static/` to keep the monitor UI self-contained. Automation utilities (`scripts/init_db.py`, `scripts/package_targets.py`) seed the SQLite database and seal target pools; run them before launching the server. Protocol docs, API references, and monitor prompts live in `docs/`. Targets and judging packs reside in `targets/`, while regression tests sit in `tests/` alongside fixtures.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` — standard environment used across the repo.
- `pip install -r requirements.txt` — installs FastAPI, Pydantic, and other runtime deps.
- `pip install -r requirements-dev.txt` — adds pytest + Ruff for local QA.
- `python scripts/init_db.py` — creates/updates the SQLite schema defined in `backend/schema.sql`.
- `python scripts/package_targets.py` — hashes media in `targets/` and emits `targets.yaml`.
- `uvicorn backend.app:app --reload` — launches the API plus static UI for local sessions.
- `pytest` or `pytest tests/test_scoring.py -k scoring` — runs the Pytest suite or focused modules.
- `make lint | make test` — wrappers for Ruff linting and the default pytest run.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation. Keep modules and functions in `snake_case`, classes and Pydantic models in `PascalCase`, and constants/env keys in `UPPER_SNAKE_CASE`. Use explicit type hints on service boundaries (e.g., scoring, guardrails) and prefer dependency-injected FastAPI routers over global state. Run `make lint` (Ruff check + import order) before pushing if you modify HTTP handlers or services.

## Testing Guidelines
Pytest is the supported harness; place new specs under `tests/` and name files `test_<area>.py`. Mirror the production module structure (e.g., `tests/test_tasker.py`). For features affecting scoring or protocol enforcement, add property-level assertions plus regression fixtures. Aim for coverage on database writes, monitor FSM transitions, and target sealing logic. Run `make test` (which invokes `pytest --maxfail=1`) before submitting.

## Commit & Pull Request Guidelines
History favors imperative Conventional-style summaries (`feat:`, `fix:`, `chore:`). Keep messages under 72 chars in the subject and include concise body details when touching scripts or schema. PRs must explain: purpose, key endpoints touched, schema or protocol changes, and any manual testing (commands + outcomes). Link tracking issues and attach screenshots/GIFs when UI assets change.

## Security & Configuration Notes
Never commit `.env` or real `RV_TASKER_SECRET` values; copy from `.env.example` and inject secrets locally. Treat packaged targets as sensitive—regenerate `targets.yaml` whenever media changes. Optional CLIP helpers require extra deps; isolate that install in a separate environment if you do not need GPU access.
