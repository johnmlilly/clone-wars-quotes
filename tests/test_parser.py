import sys
from pathlib import Path

# The scraper files import each other as plain modules (`from explore import ...`),
# so put scraper/ on Python's import path before importing them.
sys.path.insert(0, str(Path(__file__).parent.parent / "scraper"))

from parser_episode import clean_markup, parse_episode  # noqa: E402

SAMPLE_WIKITEXT = """{{TelevisionEpisode
|season=[[The Clone Wars: Season One|One]]<ref name="Guide" />
|episode=1<ref name="Guide" />
}}
{{Quote|Great leaders inspire greatness in others.|Moral|<ref name="Ambush" />}}
"""


def test_parse_episode():
    result = parse_episode("Ambush", SAMPLE_WIKITEXT)
    assert result == {
        "title": "Ambush",
        "season": 1,
        "episode": 1,
        "quote": "Great leaders inspire greatness in others.",
    }


def test_parse_episode_strips_title_suffix():
    result = parse_episode("Blue Shadow Virus (episode)", SAMPLE_WIKITEXT)
    assert result["title"] == "Blue Shadow Virus"


def test_page_without_moral_returns_none():
    wikitext = SAMPLE_WIKITEXT.replace("|Moral|", "|Anakin Skywalker|")
    assert parse_episode("Some Episode", wikitext) is None


def test_clean_markup():
    assert clean_markup("[[Jedi Order|Jedi]] are ''wise''") == "Jedi are wise"

def test_seasons():
    assert parse_episode("Ambush", SAMPLE_WIKITEXT)["season"] == 1
    for word, number in {
        "One": 1, "Two": 2, "Three": 3, "Four": 4,
        "Five": 5, "Six": 6, "Seven": 7,
    }.items():
        wikitext = SAMPLE_WIKITEXT.replace("|season=[[The Clone Wars: Season One|One]]", f"|season=[[The Clone Wars: Season {word}|{word}]]")
        assert parse_episode("Some Episode", wikitext)["season"] == number