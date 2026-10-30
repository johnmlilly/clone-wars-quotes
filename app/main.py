from fastapi import FastAPI, HTTPException

from app.data import QUOTES, filter_quotes, get_quote, random_quote
from app.models import Quote

app = FastAPI(
    title="Clone Wars Quotes API",
    description="The opening morals from every episode of Star Wars: The Clone Wars.",
)


@app.get("/")
def root() -> dict:
    return {"message": "Hello there!", "docs": "/docs", "quote_count": len(QUOTES)}


@app.get("/quotes")
def list_quotes(season: int | None = None, search: str | None = None) -> list[Quote]:
    return filter_quotes(season=season, search=search)


# Must come BEFORE /quotes/{quote_id}, or "random" would be read as an id.
@app.get("/quotes/random")
def get_random_quote() -> Quote:
    return random_quote()


@app.get("/quotes/{quote_id}")
def get_quote_by_id(quote_id: int) -> Quote:
    quote = get_quote(quote_id)
    if quote is None:
        raise HTTPException(status_code=404, detail=f"No quote with id {quote_id}")
    return quote


@app.get("/seasons/{season}/episodes/{episode}")
def get_by_episode(season: int, episode: int) -> Quote:
    for quote in filter_quotes(season=season):
        if quote.episode == episode:
            return quote
    raise HTTPException(status_code=404, detail=f"No moral for S{season}E{episode}")

@app.get("/seasons/{season}")
def get_by_season(season: int) -> list[Quote]:
    quotes = filter_quotes(season=season)
    if not quotes:
        raise HTTPException(status_code=404, detail=f"No morals for season {season}")
    return quotes