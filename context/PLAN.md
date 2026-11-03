# Plan: Lesson 7 — Deploy to Cloudflare Workers

## Context
A learning project: a FastAPI API serving the opening morals of *Star Wars: The Clone Wars* episodes, built as step-by-step Python lessons. Lessons 1–6 are done. Next is deploying to **Cloudflare Workers (Python)**. **Keep the data in a JSON file** (no D1/KV).

### How to teach (user preferences)
- User knows some programming but is new to Python. Teach one step at a time, and pause after each step for questions / "next".
- **The user types the code.** Give code and explain the concepts (compare to JS/npm where helpful). Only edit their files when they explicitly ask ("do it for me").
- Test everything in the scratchpad before handing it over, and tell them the expected output.
- Keep answers short. The user runs git commits themselves.
- No AI attribution in commits or PRs.

## Current state
- Repo: `~/Repos/clone-wars-quotes` (remote `github.com/johnmlilly/clone-wars-quotes`, branch `main`)
- Python 3.15 via uv (`pyproject.toml` + `uv.lock`, `requirements.txt` removed); Node 24, uv 0.13.5, wrangler 4.156
- CI: `.github/workflows/test.yml` (pytest) and `pylint.yml` (pylint, 10/10), both using `astral-sh/setup-uv` pinned by SHA. Badges in the README.
- Steps 1 and 2 below are done or in progress; step 2 is tested in the scratchpad and handed to the user.
- Layout after step 2:
  ```
  src/worker.py           # Workers entry point (Default = asgi.entrypoint(app))
  src/app/                # models.py, data.py, main.py (FastAPI, 6 GET routes)
  src/data/quotes.json    # 125 quotes: {id, season, episode, title, quote}
  scraper/                # explore.py, parser_episode.py, scraper_quotes.py (writes src/data/quotes.json)
  tests/                  # test_api.py, test_parser.py, 16 passing
  wrangler.jsonc, pyproject.toml, uv.lock
  ```

## Steps

### 1. Move to `pyproject.toml` + uv ✅
- `uv init --bare --python 3.15`, `uv add fastapi`, `uv add --dev workers-py workers-runtime-sdk pytest httpx2 requests uvicorn pylint`
- Teach: pyproject vs requirements.txt vs package.json, `uv sync` (≈ `npm ci`), `uv.lock` (≈ package-lock.json), `uv run` (≈ npx, auto-syncs), dependency groups (≈ devDependencies).
- Gotcha: once `pyproject.toml` exists, pytest couldn't import `app`, so add `[tool.pytest.ini_options] pythonpath`.

### 1b. CI and lint fixes ✅
- `pylint.yml` failed because it only installed pylint (`E0401` import errors) and any message makes pylint exit non-zero (exit 30 = 2+4+8+16).
- Fix: `setup-uv` + `uv sync --locked` + `uv run pylint`. setup-uv has **no floating `v10` tag**, so pin the commit SHA (`68559e99cc807c1eb7e9238fd43a15bba460eec2 # v10.3.3`). Checkout is pinned to `3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`.
- Added `test.yml` (same pattern, runs `uv run pytest`), modeled on johnsblog `verify.yml` and francisroylilly `test.yml`.
- Lint: module/function docstrings, `no-docstring-rgx = "^(_|test_)"`, `@pytest.fixture(name="client") def fixture_client()`, narrowed `except` to `(requests.RequestException, KeyError)`, replaced the `sys.path` hack in `test_parser.py` with pytest `pythonpath` + pylint `init-hook`.

### 2. Workers entry point, config and local run (in progress)
**Findings (tested with `pywrangler dev`):**
- Wrangler uploads every `.py` under the entry file's directory. A root-level `worker.py` uploaded all of `.venv` and failed. Custom `PythonModule` rules are rejected (`rules` types are only ESModule, CommonJS, CompiledWasm, Text, Data). So the worker source goes in **`src/`**.
- Without a rule, `quotes.json` isn't bundled: `FileNotFoundError: /session/metadata/data/quotes.json`. A `Data` rule fixes it, and `Path(__file__)` reads work.
- The Workers runtime is **Python 3.14** (Pyodide), but FastAPI and Pydantic run fine there.
- Result: all 6 routes, `/docs` and `/openapi.json` return correctly. Tests 16 pass, pylint 10/10, uvicorn works.

**Teach:** ASGI (≈ Node's `(req, res)` handler contract; uvicorn is the server locally, `asgi.entrypoint` on Workers), Pyodide (CPython in WebAssembly in V8 isolates), memory snapshot at deploy (imports + JSON load run once), `Default` ≈ `export default`.

**User steps:**
1. Move the files (`app/data.py` path logic is unchanged because it's relative to itself):
   ```bash
   mkdir src
   git mv app src/app
   git mv data src/data
   ```
2. `src/worker.py`. It's separate because `workers` only exists on the runtime; locally it comes from `workers-runtime-sdk`.
   ```python
   """Cloudflare Workers entry point: wraps the FastAPI app."""

   from workers import asgi

   from app.main import app

   Default = asgi.entrypoint(app)
   ```
3. `wrangler.jsonc`:
   ```jsonc
   {
     "name": "clone-wars-quotes",
     "main": "src/worker.py",
     "compatibility_date": "2026-10-30",
     "compatibility_flags": ["python_workers"],
     // Bundle the quotes file so Path(...).read_text() can find it
     "rules": [{ "type": "Data", "globs": ["data/*.json"], "fallthrough": true }]
   }
   ```
4. `pyproject.toml`: `pythonpath = ["src", "scraper"]` and `init-hook = "import sys; sys.path += ['src', 'scraper']"`
5. `scraper/scraper_quotes.py`: `OUTPUT_FILE = Path(__file__).parent.parent / "src" / "data" / "quotes.json"`
6. `.gitignore`: add `python_modules/`, `pylock.toml`, `.wrangler/` (generated by `pywrangler sync`)
7. Run `uv run pywrangler dev` (the first start takes a minute or two), then:
   `curl localhost:8787/quotes/1` → `{"id":1,"season":1,"episode":1,"title":"Ambush","quote":"Great leaders inspire greatness in others."}`
- Local uvicorn is now `uv run uvicorn app.main:app --app-dir src --reload`.

### 3. Deploy: `uv run pywrangler deploy`
- First run opens a browser for Cloudflare login (free account).
- Hit `https://clone-wars-quotes.<subdomain>.workers.dev/quotes/random` and `/docs`.
- Add the live URL to the README.

### 4. Wrap-up
- Update README and AGENTS.md for uv, the `src/` layout, the new uvicorn command and the deploy commands.
- Optional: GitHub Action to deploy on push (teaches secrets: `CLOUDFLARE_API_TOKEN`).

## Docs
- https://developers.cloudflare.com/workers/languages/python/
- https://developers.cloudflare.com/workers/languages/python/packages/fastapi/
- Examples: https://github.com/cloudflare/python-workers-examples (`fastapi/`)

## Verification
- `uv run pytest`: 16 pass; `uv run pylint $(git ls-files '*.py')`: 10.00/10
- `uv run uvicorn app.main:app --app-dir src --reload` still works locally
- `uv run pywrangler dev`: all routes return correct JSON on :8787
- The live workers.dev URL returns quotes and `/docs` loads
