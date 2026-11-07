"""APP-003 patch-status list: only a current admin can change it; members see it."""

import re

from fastapi.testclient import TestClient

from app import database
from app.main import create_app

PASSWORD = "a disposable test password"


def csrf(client):
    """Fetch the current session's CSRF token through the public endpoint."""
    return {"X-CSRF-Token": client.get("/api/csrf").json()["csrf_token"]}


def login_as(client, username):
    """Sign up and log in a disposable member through the real API."""
    body = {"username": username, "password": PASSWORD}
    assert (
        client.post("/api/signup", json=body, headers=csrf(client)).status_code == 201
    )
    assert client.post("/api/login", json=body, headers=csrf(client)).status_code == 200


def test_anonymous_and_member_cannot_change_the_list(client, settings):
    """Negative cases: direct API calls and form posts are refused by role."""
    assert (
        client.post(
            "/api/admin/games", json={"name": "Old Game"}, headers=csrf(client)
        ).status_code
        == 401
    )
    login_as(client, "plain_member")
    headers = csrf(client)
    assert (
        client.post(
            "/api/admin/games", json={"name": "Old Game"}, headers=headers
        ).status_code
        == 403
    )
    dashboard = client.get("/dashboard")
    token = re.search(r'name="csrf_token" value="([^"]+)"', dashboard.text).group(1)
    form = client.post("/admin/games", data={"name": "Old Game", "csrf_token": token})
    assert form.status_code == 403
    assert "Admin access required" in form.text
    with database.connect(settings) as connection:
        assert (
            connection.execute("SELECT COUNT(*) FROM patch_status").fetchone()[0] == 0
        )


def test_admin_can_add_list_and_toggle(client, settings):
    """Positive case: a current admin manages the marker through the API."""
    login_as(client, "site_admin")
    assert database.set_role(settings, "site_admin", "admin")
    headers = csrf(client)
    added = client.post("/api/admin/games", json={"name": "Old Game"}, headers=headers)
    assert added.status_code == 201 and added.json()["no_longer_patched"] is True
    duplicate = client.post(
        "/api/admin/games", json={"name": "old game"}, headers=headers
    )
    assert duplicate.status_code == 409
    game_id = added.json()["id"]
    off = client.patch(
        f"/api/admin/games/{game_id}",
        json={"no_longer_patched": False},
        headers=headers,
    )
    assert off.status_code == 200
    assert client.get("/api/admin").json()["games"][0]["no_longer_patched"] is False
    assert (
        client.patch(
            f"/api/admin/games/{game_id}", json={"no_longer_patched": True}
        ).status_code
        == 403
    )


def test_member_sees_badge_but_cannot_toggle_it(settings):
    """The marker reaches members; a member's direct PATCH changes nothing."""
    app = create_app(settings)
    with (
        TestClient(app, base_url=settings.origin) as admin,
        TestClient(app, base_url=settings.origin) as player,
    ):
        login_as(admin, "site_admin")
        database.set_role(settings, "site_admin", "admin")
        game = admin.post(
            "/api/admin/games", json={"name": "Old Game"}, headers=csrf(admin)
        ).json()
        login_as(player, "player")
        player.post("/api/games", json={"name": "OLD   game"}, headers=csrf(player))
        assert player.get("/api/games").json()["games"][0]["no_longer_patched"] is True
        assert "No longer patched" in player.get("/dashboard").text
        attempt = player.patch(
            f"/api/admin/games/{game['id']}",
            json={"no_longer_patched": False},
            headers=csrf(player),
        )
        assert attempt.status_code == 403
        assert admin.get("/api/admin").json()["games"][0]["no_longer_patched"] is True


def test_admin_forms_and_downgrade_take_effect_immediately(client, settings):
    """The HTML forms work for an admin and stop working after a role downgrade."""
    login_as(client, "site_admin")
    database.set_role(settings, "site_admin", "admin")
    page = client.get("/admin")
    assert page.status_code == 200
    token = re.search(r'name="csrf_token" value="([^"]+)"', page.text).group(1)
    response = client.post(
        "/admin/games",
        data={"name": "Old Game", "csrf_token": token},
        follow_redirects=False,
    )
    assert response.status_code == 303
    game_id = client.get("/api/admin").json()["games"][0]["id"]
    response = client.post(
        f"/admin/games/{game_id}/toggle",
        data={"csrf_token": token},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert client.get("/api/admin").json()["games"][0]["no_longer_patched"] is False
    database.set_role(settings, "site_admin", "member")
    response = client.post(f"/admin/games/{game_id}/toggle", data={"csrf_token": token})
    assert response.status_code == 403
