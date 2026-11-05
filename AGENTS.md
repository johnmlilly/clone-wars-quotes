# AGENTS.md

FastAPI API serving the opening morals of every *Star Wars: The Clone Wars* episode, built as a step-by-step Python learning project. Deployed on Cloudflare Workers (Python) at https://clone-wars-quotes.jm2lilly.workers.dev.

**Current work:** see [context/PLAN.md](context/PLAN.md) for the plan, current state and next step.

## How to work with the user
- The user is learning Python and already knows some programming. Teach one step at a time and pause for questions or "next".
- **The user types the code.** Give code with short explanations of the concepts, comparing to JS/npm where it helps. Edit their files only when they explicitly ask.
- Test code (in a scratch directory) before handing it over, and state the expected output.
- Keep responses short. The user makes git commits themselves.

## Layout
- `src/` is the Worker bundle root (Wrangler uploads every `.py` under the entry file's folder, so nothing else goes here)
  - `src/worker.py` is the Workers entry point (`Default = asgi.entrypoint(app)`)
  - `src/app/` holds the FastAPI app: `models.py` (Pydantic `Quote`), `data.py` (load + filter), `main.py` (routes)
  - `src/data/quotes.json` has 125 quotes: `id, season, episode, title, quote`
- `scraper/` scrapes the Wookieepedia MediaWiki API → `src/data/quotes.json`
- `tests/` contains pytest tests for the API and the parser (the parser tests use no network)
- `wrangler.jsonc` is the Worker config. Non-Python files read at runtime need a `Data` rule there or they aren't bundled.
- `context/` holds plans and session notes

## Commands (run from the project root)
```bash
uv sync                                              # install deps (≈ npm ci)
uv run python scraper/scraper_quotes.py              # regenerate src/data/quotes.json
uv run uvicorn app.main:app --app-dir src --reload   # local API at :8000, docs at /docs
uv run pywrangler dev                                # local Workers runtime at :8787
uv run pywrangler deploy                             # deploy to Cloudflare
uv run python -m pytest                              # tests
uv run pylint $(git ls-files '*.py')                 # lint (CI requires 10/10)
```

## Conventions
- Python 3.15 locally via uv (`pyproject.toml` + `uv.lock`). The Workers runtime is Pyodide (Python 3.14), so avoid 3.15-only features in `src/`.
- Keep the data in `src/data/quotes.json` (no database).
- Run `python -m pytest`, not bare `pytest`. `pyproject.toml` sets `pythonpath = ["src", "scraper"]`.
- CI (`.github/workflows/`) runs pytest and pylint through `astral-sh/setup-uv`, pinned by commit SHA.
