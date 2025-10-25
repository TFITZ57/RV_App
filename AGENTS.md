# Repository Guidelines

## Project Structure & Module Organization
FastAPI APIs are under `backend/` with request routers in `backend/routers/` and business logic services in `backend/services/`. Shared config and DB helpers live in `backend/config.py` and `backend/db.py`. Static browser assets (`index.html`, `app.js`, `styles.css`) stay in `backend/static/` so the monitor UI deploys with the API. Database schemas and automation helpers run from `scripts/`. Targets and packaging outputs are stored in `targets/`, while docs, protocol references, and prompts sit in `docs/`. Tests mirror the runtime modules inside `tests/`.

## Build, Test, and Development Commands
`python -m venv .venv && source .venv/bin/activate` creates the shared virtualenv. Install runtime deps via `pip install -r requirements.txt` and add QA tooling with `pip install -r requirements-dev.txt`. Seed or upgrade the SQLite database using `python scripts/init_db.py`, and regenerate sealed targets with `python scripts/package_targets.py`. Run the API plus static UI locally using `uvicorn backend.app:app --reload`. Execute `make lint` for Ruff checks/import order and `make test` (pytest `--maxfail=1`) for regression coverage.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation. Modules and functions use `snake_case`, classes and Pydantic models use `PascalCase`, and config keys or constants stay `UPPER_SNAKE_CASE`. Keep FastAPI routers dependency-injected—avoid global state. Add explicit type hints at service boundaries and prefer meaningful docstrings over inline comments. Run Ruff before committing to catch formatting or import-order drift.

## Testing Guidelines
Pytest is the canonical harness; add new specs under `tests/` named `test_<area>.py` mirroring the production package layout. Target scoring logic, guardrails, and DB writes need regression coverage plus property-style assertions when possible. Use focused runs such as `pytest tests/test_scoring.py -k scoring` when iterating, then finish with `make test`.

## Commit & Pull Request Guidelines
Use Conventional-style subjects (e.g., `feat: add guardrail voting`) under 72 characters, with optional bodies explaining scripts or schema shifts. PRs should describe the purpose, list endpoints or services touched, note schema/protocol deltas, and capture manual verification commands. Link tracking issues and share screenshots or GIFs whenever UI assets under `backend/static/` change.

## Security & Configuration Tips
Never commit `.env` or real `RV_TASKER_SECRET` values—copy from `.env.example` and inject locally. Treat media in `targets/` as sensitive; regenerate `targets.yaml` whenever assets shift. Optional CLIP helpers need extra dependencies, so isolate them in a separate env if GPU tooling is unnecessary.

## LLM Monitor Integration
Set `LLM_MONITOR_ENABLED=1`, provide `LLM_API_KEY`, and choose `LLM_MODEL`/`LLM_BASE_URL` to let an OpenAI-compatible chat model drive monitor prompts. The backend enforces the utterance whitelist and falls back to the finite-state prompts automatically when credentials are missing or the provider errors.
