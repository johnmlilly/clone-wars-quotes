"""Cloudflare Workers entry point: wraps the FastAPI app."""

from workers import asgi

from app.main import app

Default = asgi.entrypoint(app)
