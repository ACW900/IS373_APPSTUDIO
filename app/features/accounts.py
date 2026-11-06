"""APP-002: signup, login, a private member space and logout.

The HTML forms and the JSON API call the same prepared security helpers, so both
paths get the same CSRF checks, throttles, password hashing and session rules.
"""

from typing import Annotated

from fastapi import APIRouter, Form, Header, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from app import security
from app.features import games
from app.features.pages import render
from app.schemas import LoginInput, PublicUser, SignupInput

router = APIRouter()

FormText = Annotated[str, Form()]
CsrfHeader = Annotated[str | None, Header()]

FRIENDLY_FIELD_HELP = {
    "username": "Usernames need at least 3 letters, numbers or underscores.",
    "password": "Passwords need at least 8 characters. A short phrase is stronger.",
    "password:string_too_long": "That password is too long. Keep it to 128 characters.",
    "username:string_too_long": "That username is too long. Keep it to 32 characters.",
}


def friendly_problem(error: ValidationError) -> str:
    """Explain the first rejected field without echoing what was typed."""
    if not error.errors():
        return "Check the form and try again."
    first = error.errors()[0]
    field = str(first["loc"][0])
    return FRIENDLY_FIELD_HELP.get(
        f"{field}:{first['type']}",
        FRIENDLY_FIELD_HELP.get(field, "Check the form and try again."),
    )


# ---------- JSON API ----------


@router.get("/api/csrf")
def api_csrf(request: Request, response: Response):
    """Start (or reuse) a session and hand back its CSRF token."""
    return {"csrf_token": security.csrf_token(request, response)}


@router.post("/api/signup", status_code=201, response_model=PublicUser)
def api_signup(payload: SignupInput, request: Request, x_csrf_token: CsrfHeader = None):
    """Create a member. Extra fields such as a role are rejected by the schema."""
    security.require_csrf(request, x_csrf_token)
    security.limit_signup(request)
    return security.signup(
        request.app.state.settings, payload.username, payload.password
    )


@router.post("/api/login", response_model=PublicUser)
def api_login(
    payload: LoginInput,
    request: Request,
    response: Response,
    x_csrf_token: CsrfHeader = None,
):
    """Check the password and set the HttpOnly session cookie; no token in JSON."""
    security.require_csrf(request, x_csrf_token)
    return security.login(request, response, payload.username, payload.password)


@router.get("/api/me", response_model=PublicUser)
def api_me(request: Request):
    """401 before login, 200 with public identity after."""
    return security.require_user(request)


@router.post("/api/logout")
def api_logout(request: Request, response: Response, x_csrf_token: CsrfHeader = None):
    """Revoke the session on the server, not just in this browser."""
    security.require_csrf(request, x_csrf_token)
    security.logout(request, response)
    return {"detail": "You're logged out."}


# ---------- HTML pages ----------


@router.get("/signup", include_in_schema=False)
def signup_page(request: Request):
    """Friendly signup form."""
    return render(request, "signup.html", {"username": ""})


@router.post("/signup", include_in_schema=False)
def signup_form(
    request: Request,
    username: FormText = "",
    password: FormText = "",
    csrf_token: FormText = "",
):
    """Same rules as the API; on success, send the new member to log in."""
    kept = ""
    try:
        security.require_csrf(request, csrf_token)
        credentials = SignupInput(username=username, password=password)
        kept = credentials.username
        security.limit_signup(request)
        security.signup(
            request.app.state.settings, credentials.username, credentials.password
        )
    except ValidationError as error:
        return render(
            request,
            "signup.html",
            {"username": "", "error": friendly_problem(error)},
            422,
        )
    except HTTPException as error:
        return render(
            request,
            "signup.html",
            {"username": kept, "error": error.detail},
            error.status_code,
        )
    return RedirectResponse("/login?welcome=1", status_code=303)


@router.get("/login", include_in_schema=False)
def login_page(request: Request, welcome: str = "", signed_out: str = ""):
    """Login form; also where logged-out dashboard visits land."""
    notice = ""
    if welcome:
        notice = "Your account is ready. Log in to start your list."
    elif signed_out:
        notice = "You're logged out. Your list will be right here when you're back."
    return render(request, "login.html", {"username": "", "notice": notice})


@router.post("/login", include_in_schema=False)
def login_form(
    request: Request,
    username: FormText = "",
    password: FormText = "",
    csrf_token: FormText = "",
):
    """On success, go to the member space; on failure, keep only the username."""
    kept = ""
    destination = RedirectResponse("/dashboard", status_code=303)
    try:
        security.require_csrf(request, csrf_token)
        credentials = LoginInput(username=username, password=password)
        kept = credentials.username
        security.login(request, destination, credentials.username, credentials.password)
    except ValidationError:
        return render(
            request,
            "login.html",
            {"username": "", "error": "Enter your username and password."},
            422,
        )
    except HTTPException as error:
        return render(
            request,
            "login.html",
            {"username": kept, "error": error.detail},
            error.status_code,
        )
    return destination


@router.get("/dashboard", include_in_schema=False)
def dashboard(request: Request):
    """Members see their saved games; everyone else is sent to log in."""
    user = security.authenticate(request)
    if user is None:
        return RedirectResponse("/login", status_code=303)
    return games.dashboard_page(request, user)


@router.post("/logout", include_in_schema=False)
def logout_form(request: Request, csrf_token: FormText = ""):
    """Revoke the session, then show a friendly goodbye on the login page."""
    try:
        security.require_csrf(request, csrf_token)
    except HTTPException as error:
        return render(
            request,
            "message.html",
            {"title": "That didn't go through", "message": error.detail},
            error.status_code,
        )
    destination = RedirectResponse("/login?signed_out=1", status_code=303)
    security.logout(request, destination)
    return destination
