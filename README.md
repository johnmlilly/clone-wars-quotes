# Clone Wars Quotes API

![Python](https://img.shields.io/badge/Python-3.15-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.162-009688?logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2-E92063?logo=pydantic&logoColor=white)
![pytest](https://img.shields.io/badge/tested_with-pytest-0A9EDC?logo=pytest&logoColor=white)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-F38020?logo=cloudflare&logoColor=white)

## Overview

This project is an API for the quotes from Star Wars: The Clone Wars animated series. It fetches the opening moral of every episode from Wookieepedia, stores them in a JSON file, and exposes several endpoints for consumption.

- 125 morals across Seasons 1–7
- Interactive docs at `/docs`

## Tech Stack

- **Python** – language
- **FastAPI** – web framework
- **Pydantic** – data models and validation
- **Requests** – scraping the Wookieepedia (MediaWiki) API
- **pytest** – tests
- **Cloudflare Workers** – hosting

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run all commands from the project root.

**Scrape the quotes** (writes `data/quotes.json`):

```bash
python scraper/scraper_quotes.py
```

**Run the API:**

```bash
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs.

**Run the tests:**

```bash
python -m pytest
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | API info and quote count |
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