# RV Monitor Agent (Solo Training)

A minimal, production‑minded starter repo to run solo Remote Viewing (RV) practice **with an AI “monitor”** that enforces protocol structure (CRV Stages I–VI), keeps the session blind, and performs **SRI‑style rank‑order judging** and **effect‑size** scoring.

## Why this exists
- Preserve **double‑blind**: the monitor does not know the target content; it only sees a **Target ID** (HMAC tag).
- Enforce **structure** (Stages I–VI: I/A/B, Stage‑II sensory, Stage‑III sketching, Stage‑IV matrix, Stage‑V reductions, Stage‑VI modeling).
- Produce **publishable, auditable packets** (clean transcripts, judging pools, average rank & effect size like AIR/SRI).

> This project ships with a working FastAPI backend, a minimal UI, schema, guardrails, scoring, and a Tasker that seals targets using a **keyed hash** (HMAC). It’s ready for you to wire into your preferred LLM or run fully offline with simple rule‑based monitoring.

---

## Quickstart

```bash
# 1) Python 3.11+ recommended
python -V

# 2) Create virtual env
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt

# 4) Initialize database
python scripts/init_db.py

# 5) Package your target pool (place images in targets/ first)
python scripts/package_targets.py

# 6) Run server
uvicorn backend.app:app --reload

# 7) Open the minimal UI
# Visit http://127.0.0.1:8000/static/index.html
```

### Contributor Guide
Review `AGENTS.md` for repository conventions (structure, linting, tests, and PR expectations) before sending changes.

### Environment
Copy `.env.example` to `.env` and set values.

- `RV_TASKER_SECRET` — secret key for HMAC Target IDs. **Change this!**
- `DB_PATH` — SQLite file path (default: `rvmonitor.db`).
- `USE_CLIP` — `1` to enable CLIP pre-ranking if you install the optional deps.
- `LLM_MONITOR_ENABLED` — set to `1` to let an external LLM drive monitor prompts.
- `LLM_API_KEY` — API key for your provider (OpenAI-compatible REST today).
- `LLM_MODEL` — chat completion model name (defaults to `gpt-4o-mini`).
- `LLM_BASE_URL` — override if you proxy or self-host an OpenAI-compatible stack.

---

## Wiring in your preferred LLM

The monitor now supports OpenAI-compatible chat completions for neutral prompts. Configure the env vars above, restart `uvicorn`, and every `/sessions/log` call will send the viewer text + stage label to your LLM. The system prompt constrains responses to the whitelist in `docs/MONITOR_PROMPTS.md`; if the request fails or returns invalid JSON, the app falls back to the deterministic FSM guardrails so sessions remain unblocked. Because the REST contract is OpenAI-style, you can point `LLM_BASE_URL` at hosted third parties (e.g., Together, Anyscale) or your own gateway that mimics `/chat/completions`.

---

## Repo structure

```
rv-monitor-agent/
  backend/
    app.py                  # FastAPI app & routers
    config.py               # env & settings
    db.py                   # sqlite helpers
    schema.sql              # DB schema
    services/
      tasker.py             # target selection + HMAC Target IDs
      monitor_fsm.py        # stage machine + monitor prompts
      guardrails.py         # no-leading validator (AOL handling)
      scoring.py            # rank-order & effect size
      judge.py              # judging pools + ranking
      clip_ranker.py        # optional CLIP ranking helper
    routers/
      sessions.py           # session lifecycle endpoints
      judging.py            # judging & feedback endpoints
      targets.py            # target packaging & admin
    static/
      index.html            # minimal web UI
      app.js
      styles.css
    lexicon/
      nouns_en_basic.txt    # coarse noun list for "leading" detection
  scripts/
    init_db.py              # create schema
    package_targets.py      # build targets.yaml with hashes
  targets/
    targets.yaml            # your sealed pool (add images into targets/ first)
  tests/
    test_scoring.py
    test_guardrails.py
    test_tasker.py
  docs/
    PROTOCOL.md             # stage rules & monitor script
    API.md                  # endpoint reference
    ARCHITECTURE.md         # three-role split & data flow
    MONITOR_PROMPTS.md      # verbatim monitor utterances (whitelist)
    DOD.md                  # definition of done for MVP
  .env.example
  requirements.txt
  LICENSE
  README.md
```

---

## Notes

- **Targets**: place `*.jpg/*.png` in `targets/` then run `package_targets.py`. The Tasker will compute SHA‑256 and produce **Target IDs** using HMAC so you can prove a target was fixed before the session.
- **Judging**: by default uses plain **rank‑order**; optional **CLIP** pre‑ranking available if you install extras.
- **Blind**: the Monitor never sees target metadata or files. Only `target_id` is provided to maintain double‑blind.

---

## Legal/ethics

- This is research/training software. No claims of operational utility. Keep sessions comfortable; no hypnosis/drugs; keep pristine records for judging.
- Licensed MIT – see `LICENSE`.
