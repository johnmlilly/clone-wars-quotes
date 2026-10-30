"""Parse an episode page's wikitext into a quote dict."""

import re
from typing import Optional

from explore import fetch_wikitext

# Wookieepedia writes season numbers as words.
SEASON_NUMBERS = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4,
    "Five": 5, "Six": 6, "Seven": 7,
}

# {{Quote|<text>|Moral|...}}  ->  captures <text>
MORAL_PATTERN = re.compile(r"\{\{Quote\|(.+?)\|Moral\|")

# |season=[[The Clone Wars: Season One|One]]  ->  captures "One"
SEASON_PATTERN = re.compile(r"^\|season=\[\[[^|\]]+\|(\w+)\]\]", re.MULTILINE)

# |episode=1<ref ... />  ->  captures "1"
EPISODE_PATTERN = re.compile(r"^\|episode=(\d+)", re.MULTILINE)


def clean_markup(text: str) -> str:
    """Strip common wiki markup: [[link|label]] -> label, [[link]] -> link, ''italics''."""
    text = re.sub(r"\[\[[^|\]]+\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    return text.replace("''", "").strip()


def parse_episode(title: str, wikitext: str) -> Optional[dict]:
    """Pull the moral, season and episode number out of one episode page.

    Returns None if the page has no moral (e.g. Season 7 episodes).
    """
    moral = MORAL_PATTERN.search(wikitext)
    season = SEASON_PATTERN.search(wikitext)
    episode = EPISODE_PATTERN.search(wikitext)

    if not (moral and season and episode):
        return None

    return {
        "title": re.sub(r" \(.*\)$", "", title),  # strip trailing "(episode)" from the title
        "season": SEASON_NUMBERS[season.group(1)],
        "episode": int(episode.group(1)),
        "quote": clean_markup(moral.group(1)),
    }


if __name__ == "__main__":
    examples = [
        "Ambush",
        "Lethal Trackdown",
        "The Phantom Apprentice",
        "Blue Shadow Virus (episode)",
    ]
    for page in examples:
        print(parse_episode(page, fetch_wikitext(page)))
