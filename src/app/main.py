"""FastAPI routes for the Clone Wars Quotes API."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.data import QUOTES, filter_quotes, get_quote, random_quote
from app.models import Quote

app = FastAPI(
    title="Clone Wars Quotes API",
    description="The opening morals from every episode of Star Wars: The Clone Wars.",
)


# Read once at import, like QUOTES, so it's part of the Workers memory snapshot.
HOME_PAGE = (Path(__file__).parent / "static" / "index.html").read_text()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home() -> str:
    """Serve the HTML home page."""
    return HOME_PAGE


@app.get("/api")
def api_info() -> dict:
    """Welcome message with a link to the docs."""
    return {"message": "Hello there!", "docs": "/docs", "quote_count": len(QUOTES)}


@app.get("/quotes")
def list_quotes(season: int | None = None, search: str | None = None) -> list[Quote]:
    """List quotes, optionally filtered by season and/or search word."""
    return filter_quotes(season=season, search=search)


# Must come BEFORE /quotes/{quote_id}, or "random" would be read as an id.
@app.get("/quotes/random")
def get_random_quote() -> Quote:
    """Return one random quote."""
    return random_quote()


@app.get("/quotes/{quote_id}")
def get_quote_by_id(quote_id: int) -> Quote:
    """Return one quote by id, or 404."""
    quote = get_quote(quote_id)
    if quote is None:
        raise HTTPException(status_code=404, detail=f"No quote with id {quote_id}")
    return quote


@app.get("/seasons/{season}/episodes/{episode}")
def get_by_episode(season: int, episode: int) -> Quote:
    """Return the moral for one episode, or 404."""
    for quote in filter_quotes(season=season):
        if quote.episode == episode:
            return quote
    raise HTTPException(status_code=404, detail=f"No moral for S{season}E{episode}")

@app.get("/seasons/{season}")
def get_by_season(season: int) -> list[Quote]:
    """Return every moral in a season, or 404."""
    quotes = filter_quotes(season=season)
    if not quotes:
        raise HTTPException(status_code=404, detail=f"No morals for season {season}")
    return quotes
