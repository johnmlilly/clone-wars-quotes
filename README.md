# Clone Wars Quotes API

[![Test](https://github.com/johnmlilly/clone-wars-quotes/actions/workflows/test.yml/badge.svg)](https://github.com/johnmlilly/clone-wars-quotes/actions/workflows/test.yml)
[![Pylint](https://github.com/johnmlilly/clone-wars-quotes/actions/workflows/pylint.yml/badge.svg)](https://github.com/johnmlilly/clone-wars-quotes/actions/workflows/pylint.yml)
[![Deploy](https://github.com/johnmlilly/clone-wars-quotes/actions/workflows/deploy.yml/badge.svg)](https://github.com/johnmlilly/clone-wars-quotes/actions/workflows/deploy.yml)
![Python](https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.162-009688?logo=fastapi&logoColor=white)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-F38020?logo=cloudflare&logoColor=white)

## Overview

This project is an API for the quotes from Star Wars: The Clone Wars animated series. It fetches the opening moral of every episode from Wookieepedia, stores them in a JSON file, and exposes several endpoints for consumption.

- 125 morals across Seasons 1–7
- Live at https://clone-wars-quotes.jm2lilly.workers.dev ([docs](https://clone-wars-quotes.jm2lilly.workers.dev/docs))
- Interactive docs at `/docs`

## Tech Stack

- **Python** – language
- **uv** – packages and virtualenv
- **FastAPI** – web framework
- **Pydantic** – data models and validation
- **Requests** – scraping the Wookieepedia (MediaWiki) API
- **pytest** – tests
- **Cloudflare Workers** – hosting

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

Run all commands from the project root.

**Scrape the quotes** (writes `src/data/quotes.json`):

```bash
uv run python scraper/scraper_quotes.py
```

**Run the API locally:**

```bash
uv run uvicorn app.main:app --app-dir src --reload
```

Then open http://127.0.0.1:8000/docs.

**Run on the Workers runtime locally** (http://localhost:8787):

```bash
uv run pywrangler dev
```

**Deploy to Cloudflare Workers:**

```bash
uv run pywrangler deploy
```

**Run the tests:**

```bash
uv run python -m pytest
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Home page (HTML) with a random quote |
| GET | `/api` | API info and quote count |
| GET | `/quotes` | All quotes. Optional `?season=` and `?search=` filters |
| GET | `/quotes/random` | A random quote |
| GET | `/quotes/{id}` | One quote by id |
| GET | `/seasons/{season}` | All quotes from a season |
| GET | `/seasons/{season}/episodes/{episode}` | The quote for one episode |

### Example

`GET /quotes/1`

```json
{
  "id": 1,
  "season": 1,
  "episode": 1,
  "title": "Ambush",
  "quote": "Great leaders inspire greatness in others."
}
```

## Data source

Quotes are sourced from [Wookieepedia](https://starwars.fandom.com), licensed under [CC BY-SA](https://creativecommons.org/licenses/by-sa/3.0/). Star Wars is a trademark of Lucasfilm Ltd.