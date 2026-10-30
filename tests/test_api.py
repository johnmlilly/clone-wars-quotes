import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["quote_count"] == 125


def test_get_quote_by_id(client):
    response = client.get("/quotes/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "season": 1,
        "episode": 1,
        "title": "Ambush",
        "quote": "Great leaders inspire greatness in others.",
    }


def test_missing_quote_returns_404(client):
    response = client.get("/quotes/999")
    assert response.status_code == 404


def test_non_integer_id_returns_422(client):
    response = client.get("/quotes/abc")
    assert response.status_code == 422


def test_random_quote_has_all_fields(client):
    quote = client.get("/quotes/random").json()
    assert set(quote) == {"id", "season", "episode", "title", "quote"}


def test_filter_by_season(client):
    quotes = client.get("/quotes", params={"season": 2}).json()
    assert len(quotes) == 22
    assert all(q["season"] == 2 for q in quotes)


def test_search_is_case_insensitive(client):
    lower = client.get("/quotes", params={"search": "fear"}).json()
    upper = client.get("/quotes", params={"search": "FEAR"}).json()
    assert lower == upper
    assert len(lower) > 0


@pytest.mark.parametrize(
    "path, expected_status",
    [
        ("/seasons/2/episodes/22", 200),
        ("/seasons/7/episodes/1", 404),   # Season 7 premiere has no moral
        ("/seasons/1", 200),
        ("/seasons/8", 404),
    ],
)
def test_season_routes(client, path, expected_status):
    assert client.get(path).status_code == expected_status
