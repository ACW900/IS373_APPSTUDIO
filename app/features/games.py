"""APP-002 extra agreed with the learner: each member keeps a short saved-games list.

The owner always comes from the server-side session, never from the request body,
so one member can neither read nor remove another member's games.
"""

import time
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Form, Header, HTTPException, Path, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app import security
from app.database import connect
from app.features.pages import render
from app.schemas import GameInput
from app.settings import Settings

router = APIRouter()

MAX_GAMES = 20
GameId = Annotated[str, Path(min_length=1, max_length=64)]
CsrfHeader = Annotated[str | None, Header()]


def list_games(settings: Settings, user_id: str) -> list[dict]:
    """Only this member's games, oldest first, with the admin patch marker."""
    with connect(settings) as connection:
        rows = connection.execute(
            """SELECT saved.id, saved.name,
                      COALESCE(status.no_longer_patched, 0) AS no_longer_patched
               FROM saved_games AS saved
               LEFT JOIN patch_status AS status ON status.name_key = saved.name_key
               WHERE saved.user_id = ? ORDER BY saved.rowid""",
            (user_id,),
        ).fetchall()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "no_longer_patched": bool(row["no_longer_patched"]),
        }
        for row in rows
    ]


def add_game(settings: Settings, user_id: str, name: str) -> dict[str, str]:
    """Save one game, refusing duplicates and anything past the slot limit."""
    game = {"id": str(uuid4()), "name": name}
    with connect(settings) as connection:
        connection.execute("BEGIN IMMEDIATE")
        count = connection.execute(
            "SELECT COUNT(*) FROM saved_games WHERE user_id = ?", (user_id,)
        ).fetchone()[0]
        if count >= MAX_GAMES:
            raise HTTPException(
                409,
                f"All {MAX_GAMES} slots are full. Remove a game to add another.",
            )
        exists = connection.execute(
            "SELECT 1 FROM saved_games WHERE user_id = ? AND name_key = ?",
            (user_id, name.casefold()),
        ).fetchone()
        if exists:
            raise HTTPException(409, f"{name} is already on your list.")
        connection.execute(
            "INSERT INTO saved_games (id, user_id, name, name_key, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (game["id"], user_id, name, name.casefold(), int(time.time())),
        )
    return game


def remove_game(settings: Settings, user_id: str, game_id: str) -> bool:
    """Delete only when the game belongs to this member."""
    with connect(settings) as connection:
        result = connection.execute(
            "DELETE FROM saved_games WHERE id = ? AND user_id = ?",
            (game_id, user_id),
        )
        return result.rowcount == 1


def dashboard_page(request: Request, user: dict, error: str = "", status_code=200):
    """The member space: greeting, saved games and the add/remove forms."""
    saved = list_games(request.app.state.settings, user["id"])
    return render(
        request,
        "dashboard.html",
        {"user": user, "games": saved, "limit": MAX_GAMES, "error": error},
        status_code,
    )


# ---------- JSON API ----------


@router.get("/api/games")
def api_list(request: Request):
    """401 when logged out; otherwise only your own list."""
    user = security.require_user(request)
    return {
        "games": list_games(request.app.state.settings, user["id"]),
        "limit": MAX_GAMES,
    }


@router.post("/api/games", status_code=201)
def api_add(payload: GameInput, request: Request, x_csrf_token: CsrfHeader = None):
    """Add a game to the logged-in member's list."""
    user = security.require_user(request)
    security.require_csrf(request, x_csrf_token)
    return add_game(request.app.state.settings, user["id"], payload.name)


@router.delete("/api/games/{game_id}", status_code=204)
def api_remove(game_id: GameId, request: Request, x_csrf_token: CsrfHeader = None):
    """404 for a game that is not yours, so other lists stay invisible."""
    user = security.require_user(request)
    security.require_csrf(request, x_csrf_token)
    if not remove_game(request.app.state.settings, user["id"], game_id):
        raise HTTPException(404, "That game isn't on your list.")
    return Response(status_code=204)


# ---------- HTML forms ----------


@router.post("/dashboard/games", include_in_schema=False)
def form_add(
    request: Request,
    name: Annotated[str, Form()] = "",
    csrf_token: Annotated[str, Form()] = "",
):
    """Add from the dashboard form, then show the updated list."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    try:
        security.require_csrf(request, csrf_token)
        game = GameInput(name=name)
        add_game(request.app.state.settings, user["id"], game.name)
    except ValidationError:
        return dashboard_page(request, user, "Game names use 1–60 characters.", 422)
    except HTTPException as error:
        return dashboard_page(request, user, error.detail, error.status_code)
    return RedirectResponse("/dashboard", status_code=303)


@router.post("/dashboard/games/{game_id}/remove", include_in_schema=False)
def form_remove(
    game_id: GameId, request: Request, csrf_token: Annotated[str, Form()] = ""
):
    """Remove from the dashboard form."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    try:
        security.require_csrf(request, csrf_token)
    except HTTPException as error:
        return dashboard_page(request, user, error.detail, error.status_code)
    if not remove_game(request.app.state.settings, user["id"], game_id):
        return dashboard_page(request, user, "That game isn't on your list.", 404)
    return RedirectResponse("/dashboard", status_code=303)
