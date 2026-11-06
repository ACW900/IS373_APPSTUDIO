"""Saved games (agreed APP-002 extra): each member sees and changes only their list."""

import re

from fastapi.testclient import TestClient

from app.main import create_app

PASSWORD = "a disposable test password"


def csrf(client):
    """Fetch the current session's CSRF token through the public endpoint."""
    return {"X-CSRF-Token": client.get("/api/csrf").json()["csrf_token"]}


def member(client, username):
    """Sign up and log in a disposable member through the real API."""
    body = {"username": username, "password": PASSWORD}
    assert (
        client.post("/api/signup", json=body, headers=csrf(client)).status_code == 201
    )
    assert client.post("/api/login", json=body, headers=csrf(client)).status_code == 200


def test_logged_out_requests_get_no_list(client):
    """Negative case: no session means 401 from the API and a login redirect."""
    assert client.get("/api/games").status_code == 401
    response = client.post("/api/games", json={"name": "Hades"}, headers=csrf(client))
    assert response.status_code == 401
    page = client.post(
        "/dashboard/games", data={"name": "Hades"}, follow_redirects=False
    )
    assert page.headers["location"] == "/login"


def test_member_can_add_list_and_remove_games(client):
    """Positive case through the API, including duplicate and CSRF rejection."""
    member(client, "player_one")
    assert client.post("/api/games", json={"name": "Hades"}).status_code == 403
    added = client.post("/api/games", json={"name": "  Hades  "}, headers=csrf(client))
    assert added.status_code == 201 and added.json()["name"] == "Hades"
    duplicate = client.post("/api/games", json={"name": "hades"}, headers=csrf(client))
    assert duplicate.status_code == 409
    for invalid in ({"name": ""}, {"name": "x" * 61}, {"name": "Ok", "owner": "x"}):
        response = client.post("/api/games", json=invalid, headers=csrf(client))
        assert response.status_code == 422
    listed = client.get("/api/games").json()
    assert [game["name"] for game in listed["games"]] == ["Hades"]
    game_id = listed["games"][0]["id"]
    removed = client.delete(f"/api/games/{game_id}", headers=csrf(client))
    assert removed.status_code == 204
    assert client.get("/api/games").json()["games"] == []


def test_slot_limit_is_enforced(client):
    """The twenty-first game is refused rather than growing the list without bound."""
    member(client, "collector")
    headers = csrf(client)
    for number in range(20):
        response = client.post(
            "/api/games", json={"name": f"Game {number}"}, headers=headers
        )
        assert response.status_code == 201
    response = client.post("/api/games", json={"name": "One more"}, headers=headers)
    assert response.status_code == 409


def test_members_cannot_see_or_remove_each_others_games(settings):
    """Ownership comes from the session, so another member's ID is simply not found."""
    app = create_app(settings)
    with (
        TestClient(app, base_url=settings.origin) as first,
        TestClient(app, base_url=settings.origin) as second,
    ):
        member(first, "first_player")
        member(second, "second_player")
        game = first.post(
            "/api/games", json={"name": "Celeste"}, headers=csrf(first)
        ).json()
        assert second.get("/api/games").json()["games"] == []
        assert "Celeste" not in second.get("/dashboard").text
        attempt = second.delete(f"/api/games/{game['id']}", headers=csrf(second))
        assert attempt.status_code == 404
        assert [g["name"] for g in first.get("/api/games").json()["games"]] == [
            "Celeste"
        ]


def test_dashboard_form_adds_and_removes_with_escaping(client):
    """The HTML form uses the same rules, and a typed name is shown as text."""
    member(client, "form_player")
    page = client.get("/dashboard")
    token = re.search(r'name="csrf_token" value="([^"]+)"', page.text).group(1)
    response = client.post(
        "/dashboard/games",
        data={"name": "<b>Bold</b> Game", "csrf_token": token},
        follow_redirects=False,
    )
    assert response.status_code == 303
    page = client.get("/dashboard")
    assert "&lt;b&gt;Bold&lt;/b&gt; Game" in page.text
    assert "<b>Bold</b>" not in page.text
    bad = client.post("/dashboard/games", data={"name": "Other", "csrf_token": "wrong"})
    assert bad.status_code == 403
    game_id = client.get("/api/games").json()["games"][0]["id"]
    response = client.post(
        f"/dashboard/games/{game_id}/remove",
        data={"csrf_token": token},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert client.get("/api/games").json()["games"] == []
