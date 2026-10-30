"""Fetch raw wikitext from the Wookieepedia API."""

# Standard library imports (built into Python, no install needed)
import json

# Third-party import (installed with uv)
import requests

API_URL = "https://starwars.fandom.com/api.php"

# Some sites block requests that don't say who they are.
HEADERS = {"User-Agent": "clone-wars-quotes-learning-project/0.1"}


def fetch_wikitext(page_title: str) -> str:
    """Return the raw wikitext of a Wookieepedia page."""
    params = {
        "action": "parse",      # ask MediaWiki to parse a page
        "page": page_title,
        "prop": "wikitext",     # we only want the source text
        "format": "json",
    }
    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()   # raises an error on 404, 500, etc.

    data = response.json()        # JSON text -> Python dict
    try:
        return data["parse"]["wikitext"]["*"]
    except KeyError:
        # `data` is in scope here, so show what the API actually sent back
        print("Unexpected response shape:")
        print(json.dumps(data, indent=2)[:1000])
        raise                     # re-raise so the caller knows it failed


if __name__ == "__main__":
    try:
        text = fetch_wikitext("Ambush")
        print(text[:3000])        # first 3000 characters
    except requests.RequestException as error:
        print(f"Request failed: {error}")
    except KeyError:
        pass                      # details already printed in fetch_wikitext
