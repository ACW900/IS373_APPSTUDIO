"""APP-003: an admin-only "no longer getting patches" list, enforced on the server.

Every admin request reads the current role from the database (through the
prepared security helpers), so a hidden link, a typed URL or an old token can
never stand in for permission.
"""

import sqlite3
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Form, Header, HTTPException, Path, Request
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app import security
from app.database import connect
from app.features.pages import render
from app.schemas import GameInput, PatchToggle
from app.settings import Settings

router = APIRouter()

GameId = Annotated[str, Path(min_length=1, max_length=64)]
CsrfHeader = Annotated[str | None, Header()]


def list_status(settings: Settings) -> list[dict]:
    """Every game an admin has added, alphabetically."""
    with connect(settings) as connection:
        rows = connection.execute(
            "SELECT id, name, no_longer_patched FROM patch_status ORDER BY name_key"
        ).fetchall()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "no_longer_patched": bool(row["no_longer_patched"]),
        }
        for row in rows
    ]


def add_status(settings: Settings, name: str) -> dict:
    """Add a game, marked as no longer getting patches."""
    game = {"id": str(uuid4()), "name": name, "no_longer_patched": True}
    try:
        with connect(settings) as connection:
            connection.execute(
                "INSERT INTO patch_status (id, name, name_key, no_longer_patched) "
                "VALUES (?, ?, ?, 1)",
                (game["id"], name, name.casefold()),
            )
    except sqlite3.IntegrityError as error:
        raise HTTPException(409, f"{name} is already on the admin list.") from error
    return game


def set_status(settings: Settings, game_id: str, value: bool | None) -> bool:
    """Set the marker, or flip it when no value is given."""
    with connect(settings) as connection:
        if value is None:
            result = connection.execute(
                "UPDATE patch_status SET no_longer_patched = 1 - no_longer_patched "
                "WHERE id = ?",
                (game_id,),
            )
        else:
            result = connection.execute(
                "UPDATE patch_status SET no_longer_patched = ? WHERE id = ?",
                (int(value), game_id),
            )
        return result.rowcount == 1


# ---------- JSON API: anonymous 401, member 403, admin allowed ----------


@router.get("/api/admin")
def api_admin(request: Request):
    """The admin list, only for a current admin."""
    security.require_admin(request)
    return {"games": list_status(request.app.state.settings)}


@router.post("/api/admin/games", status_code=201)
def api_add(payload: GameInput, request: Request, x_csrf_token: CsrfHeader = None):
    """Mark a game as no longer getting patches."""
    security.require_admin(request)
    security.require_csrf(request, x_csrf_token)
    return add_status(request.app.state.settings, payload.name)


@router.patch("/api/admin/games/{game_id}")
def api_toggle(
    game_id: GameId,
    payload: PatchToggle,
    request: Request,
    x_csrf_token: CsrfHeader = None,
):
    """Turn the marker on or off."""
    security.require_admin(request)
    security.require_csrf(request, x_csrf_token)
    if not set_status(request.app.state.settings, game_id, payload.no_longer_patched):
        raise HTTPException(404, "That game isn't on the admin list.")
    return {"id": game_id, "no_longer_patched": payload.no_longer_patched}


# ---------- HTML pages ----------


def _admin_or_response(request: Request):
    """Return (user, None) for an admin, or (None, the response to send instead)."""
    user = security.authenticate(request)
    if user is None:
        return None, RedirectResponse("/login", status_code=303)
    if user["role"] != "admin":
        return None, render(request, "admin_denied.html", {}, 403)
    return user, None


def admin_page(request: Request, error: str = "", status_code: int = 200):
    """The admin list with its add and toggle forms."""
    return render(
        request,
        "admin.html",
        {"games": list_status(request.app.state.settings), "error": error},
        status_code,
    )


@router.get("/admin", include_in_schema=False)
def admin(request: Request):
    """Logged out goes to login; members get a friendly 403."""
    _, denied = _admin_or_response(request)
    return denied or admin_page(request)


@router.post("/admin/games", include_in_schema=False)
def admin_add(
    request: Request,
    name: Annotated[str, Form()] = "",
    csrf_token: Annotated[str, Form()] = "",
):
    """Add from the admin form."""
    _, denied = _admin_or_response(request)
    if denied:
        return denied
    try:
        security.require_csrf(request, csrf_token)
        add_status(request.app.state.settings, GameInput(name=name).name)
    except ValidationError:
        return admin_page(request, "Game names use 1–60 characters.", 422)
    except HTTPException as error:
        return admin_page(request, error.detail, error.status_code)
    return RedirectResponse("/admin", status_code=303)


@router.post("/admin/games/{game_id}/toggle", include_in_schema=False)
def admin_toggle(
    game_id: GameId, request: Request, csrf_token: Annotated[str, Form()] = ""
):
    """Flip the marker from the admin form."""
    _, denied = _admin_or_response(request)
    if denied:
        return denied
    try:
        security.require_csrf(request, csrf_token)
    except HTTPException as error:
        return admin_page(request, error.detail, error.status_code)
    if not set_status(request.app.state.settings, game_id, None):
        return admin_page(request, "That game isn't on the admin list.", 404)
    return RedirectResponse("/admin", status_code=303)
