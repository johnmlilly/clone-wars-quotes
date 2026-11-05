"""Scrape every episode's moral and save them to data/quotes.json."""

import json
import time
from pathlib import Path

import requests

from explore import API_URL, HEADERS, fetch_wikitext
from parser_episode import parse_episode

CATEGORY = "Category:Star_Wars:_The_Clone_Wars_episodes"

# Path(__file__) is this file. .parent is scraper/, .parent.parent is the project root.
OUTPUT_FILE = Path(__file__).parent.parent / "src" / "data" / "quotes.json"


def fetch_episode_titles() -> list[str]:
    """Ask the wiki for every page in the episodes category."""
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": CATEGORY,
        "cmlimit": 500,          # max per request;
        "format": "json",
    }
    response = requests.get(API_URL, params=params, headers=HEADERS, timeout=10)
    response.raise_for_status()
    members = response.json()["query"]["categorymembers"]
    return [member["title"] for member in members]


def main() -> None:
    """Fetch all episodes, parse their morals and write quotes.json."""
    titles = fetch_episode_titles()
    print(f"Found {len(titles)} episode pages")

    quotes = []
    skipped = []

    for number, title in enumerate(titles, start=1):
        print(f"[{number}/{len(titles)}] {title}")
        try:
            episode = parse_episode(title, fetch_wikitext(title))
        except (requests.RequestException, KeyError) as error:
            # One bad page shouldn't kill the whole run: note it and move on.
            skipped.append(f"{title} ({type(error).__name__}: {error})")
            continue

        if episode is None:
            skipped.append(title)
        else:
            quotes.append(episode)

        time.sleep(0.3)          # be polite: don't

    # Sort by season, then episode. The lambda retu
    quotes.sort(key=lambda q: (q["season"], q["episode"]))

    # Give each quote an id, 1..N, in that order.
    for index, quote in enumerate(quotes, start=1):
        quote["id"] = index

    OUTPUT_FILE.parent.mkdir(exist_ok=True)   # create data/ if it's missing
    OUTPUT_FILE.write_text(json.dumps(quotes, indent=2))

    print(f"\nSaved {len(quotes)} quotes to {OUTPUT_FILE}")
    print(f"Skipped {len(skipped)}: {skipped}")


if __name__ == "__main__":
    main()
