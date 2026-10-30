"""Load quotes.json and look up quotes."""

import random
import json
from pathlib import Path

from app.models import Quote

DATA_FILE = Path(__file__).parent.parent / "data" / "quotes.json"


def load_quotes() -> list[Quote]:
    """Read quotes.json and turn each dict into a Quote."""
    raw = json.loads(DATA_FILE.read_text())
    return [Quote(**item) for item in raw]


# Loaded once, when this module is first imported.
QUOTES = load_quotes()


def get_quote(quote_id: int) -> Quote | None:
    """Find one quote by id, or None."""
    return next((q for q in QUOTES if q.id == quote_id), None)


def filter_quotes(season: int | None = None, search: str | None = None) -> list[Quote]:
    """Return quotes, optionally narrowed by season and/or a search word."""
    results = QUOTES
    if season is not None:
        results = [q for q in results if q.season == season]
    if search:
        word = search.lower()
        results = [q for q in results if word in q.quote.lower()]
    return results


def random_quote() -> Quote:
    """Pick one quote at random."""
    return random.choice(QUOTES)


if __name__ == "__main__":
    print(f"Loaded {len(QUOTES)} quotes")
    print(get_quote(1))
    print(get_quote(999))
    print(len(filter_quotes(season=2)), "quotes in season 2")
    for q in filter_quotes(search="fear"):
        print(f"  S{q.season}E{q.episode} {q.title}: {q.quote}")
    print(random_quote().model_dump())
