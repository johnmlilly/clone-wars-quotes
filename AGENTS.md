# AGENTS.md

FastAPI API serving the opening morals of every *Star Wars: The Clone Wars* episode, built as a step-by-step Python learning project.

**Current work:** Lesson 7, deploying to Cloudflare Workers. See [context/PLAN.md](context/PLAN.md) for the plan, current state and next step.

## How to work with the user
- The user is learning Python and already knows some programming. Teach one step at a time and pause for questions or "next".
- **The user types the code.** Give code with short explanations of the concepts, comparing to JS/npm where it helps. Edit their files only when they explicitly ask.
- Test code (in a scratch directory) before handing it over, and state the expected output.
- Keep responses short. The user makes git commits themselves.

## Layout
- `scraper/` scrapes the Wookieepedia MediaWiki API → `data/quotes.json` (125 quotes: `id, season, episode, title, quote`)
- `app/` holds the FastAPI app: `models.py` (Pydantic `Quote`), `data.py` (load + filter), `main.py` (routes)
- `tests/` contains pytest tests for the API and the parser (the parser tests use no network)
- `context/` holds plans and session notes

## Commands (run from the project root, with the venv active)
```bash
python scraper/scraper_quotes.py   # regenerate data/quotes.json
uvicorn app.main:app --reload      # local API at :8000, docs at /docs
python -m pytest                   # tests
```

## Conventions
- Python 3.15. Keep the data in `data/quotes.json` (no database).
- Run `python -m pytest`, not bare `pytest`, so `app` is importable.
