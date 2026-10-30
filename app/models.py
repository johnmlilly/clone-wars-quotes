"""Pydantic models for the API."""

from pydantic import BaseModel


class Quote(BaseModel):
    """One episode's opening moral."""

    id: int
    season: int
    episode: int
    title: str
    quote: str
