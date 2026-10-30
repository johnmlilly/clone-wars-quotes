# Plan: Lesson 7 — Deploy to Cloudflare Workers

## Context
A learning project: a FastAPI API serving the opening morals of *Star Wars: The Clone Wars* episodes, built as step-by-step Python lessons. Lessons 1–6 are done. Next is deploying to **Cloudflare Workers (Python)**. **Keep the data in `data/quotes.json`** (no D1/KV).

### How to teach (user preferences)
- User knows some programming but is new to Python. Teach one step at a time, and pause after each step for questions / "next".
- **The user types the code.** Give code and explain the concepts (compare to JS/npm where helpful). Only edit their files when they explicitly ask ("do it for me").
- Test everything in the scratchpad before handing it over, and tell them the expected output.
- Keep answers short. The user runs git commits themselves.
- No AI attribution in commits or PRs.

## Current state
- Repo: `~/Repos/clone-wars-quotes` (remote `github.com/johnmlilly/clone-wars-quotes`, branch `main`)
- Python 3.15.2 (Homebrew) venv in `.venv`; Node 24, uv 0.13.5, wrangler 4.156 installed
- Layout:
  ```
  app/__init__.py, app/models.py (Pydantic Quote), app/data.py (load JSON, get_quote, filter_quotes, random_quote), app/main.py (FastAPI, 6 GET routes)
  data/quotes.json        # 125 quotes: {id, season, episode, title, quote}
  scraper/explore.py, scraper/parser_episode.py, scraper/scraper_quotes.py
  tests/test_api.py, tests/test_parser.py   # 16 passing; run `python -m pytest` from root
  requirements.txt, README.md (badges added, uncommitted), .gitignore
  ```
- `app/data.py` loads data via `Path(__file__).parent.parent / "data" / "quotes.json"`
- Loose ends: `requirements.txt` still pins `httpx==0.28.1` (should be `httpx2==2.16.0`), and `beautifulsoup4` is unused. Add `.pytest_cache/` to `.gitignore`.

## Steps

### 1. Move to `pyproject.toml` + uv
- Run `uv init --bare` (or write it by hand). Runtime deps: `fastapi`. Dev group: `workers-py`, `workers-runtime-sdk`, `pytest`, `httpx2`, `requests`, `uvicorn`.
- Teach: pyproject vs requirements.txt vs package.json, `uv sync`, `uv.lock` (≈ package-lock.json), `uv run`, dependency groups (≈ devDependencies).
- Delete `requirements.txt` once `uv run python -m pytest` passes. Add `.venv` handling: uv uses `.venv` by default.

### 2. Workers entry point and config
- Add `wrangler.jsonc`: `name: "clone-wars-quotes"`, `main: "src/main.py"` (or point it at `app/main.py`; decide after checking whether imports resolve), `compatibility_date: today`, `compatibility_flags: ["python_workers"]`.
- Append to the FastAPI module:
  ```python
  from workers import asgi
  Default = asgi.entrypoint(app)
  ```
  Guard it so local `uvicorn`/pytest still work, since `workers` only exists in the Workers runtime (e.g. a separate `src/worker.py` that imports `app` and sets `Default`).
- Teach: ASGI, why there's no uvicorn on Workers, Pyodide/WebAssembly, memory snapshots at deploy.

### 3. Local run: `uv run pywrangler dev` → `curl localhost:8787/quotes/1`
- **Main risk: JSON loading.** Check that `data/quotes.json` is bundled and readable via `Path`. If it isn't:
  1. Move the JSON next to the Python modules inside the worker's source dir, and/or add a wrangler `rules` entry for `**/*.json`.
  2. Fallback that still keeps JSON as the source of truth: serve it via Workers Static Assets (`assets` binding) and fetch it at startup. Otherwise, as a last resort, have a build step that embeds the JSON into a `.py` module.
- Verify all 6 routes plus `/docs`.

### 4. Deploy: `uv run pywrangler deploy`
- First run opens a browser for Cloudflare login (free account).
- Hit `https://clone-wars-quotes.<subdomain>.workers.dev/quotes/random` and `/docs`.
- Add the live URL to the README.

### 5. Wrap-up
- Update README setup/usage for uv and the deploy commands.
- Optional: GitHub Action to run tests and deploy on push (teaches CI and secrets: `CLOUDFLARE_API_TOKEN`).

## Docs
- https://developers.cloudflare.com/workers/languages/python/
- https://developers.cloudflare.com/workers/languages/python/packages/fastapi/
- Examples: https://github.com/cloudflare/python-workers-examples (`fastapi/`)

## Verification
- `uv run python -m pytest`: 16 pass
- `uv run uvicorn app.main:app --reload` still works locally
- `uv run pywrangler dev`: all routes return correct JSON on :8787
- The live workers.dev URL returns quotes and `/docs` loads
