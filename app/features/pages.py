"""Shared page rendering for the account and saved-game forms."""

from fastapi import Request, Response

from app import security


def render(request: Request, name: str, context: dict, status_code: int = 200):
    """Render a page with a CSRF token, keeping any new pre-login session cookie."""
    holder = Response()
    token = security.csrf_token(request, holder)
    response = request.app.state.templates.TemplateResponse(
        request=request,
        name=name,
        context={**context, "csrf": token},
        status_code=status_code,
    )
    for key, value in holder.raw_headers:
        if key == b"set-cookie":
            response.headers.append("set-cookie", value.decode("latin-1"))
    return response
