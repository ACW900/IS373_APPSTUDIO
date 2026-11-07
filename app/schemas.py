"""Explicit input and public output contracts exclude server-controlled fields."""

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SignupInput(BaseModel):
    """Only these two properties may arrive from a public signup."""

    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=3, max_length=32, strict=True)
    password: str = Field(min_length=8, max_length=128, strict=True)

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        """One normalized identity; keep email ownership out of this small exercise."""
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-z0-9_]{3,32}", normalized):
            raise ValueError(
                "Use 3–32 letters, numbers, or underscores for your username."
            )
        return normalized


class LoginInput(BaseModel):
    """Bound credentials before performing an expensive password verification."""

    model_config = ConfigDict(extra="forbid")
    username: str = Field(min_length=1, max_length=32, strict=True)
    password: str = Field(min_length=1, max_length=128, strict=True)

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        """Use the same identity normalization as signup."""
        return value.strip().lower()


class GameInput(BaseModel):
    """One saved game name; the owner always comes from the session, never input."""

    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=60, strict=True)

    @field_validator("name")
    @classmethod
    def tidy_name(cls, value: str) -> str:
        """Collapse spacing and refuse invisible control characters."""
        tidy = " ".join(value.split())
        if not tidy:
            raise ValueError("Type a game name first.")
        if any(not character.isprintable() for character in tidy):
            raise ValueError("Use ordinary letters, numbers and punctuation.")
        return tidy


class PatchToggle(BaseModel):
    """Admin-only change to one game's 'no longer getting patches' marker."""

    model_config = ConfigDict(extra="forbid")
    no_longer_patched: bool = Field(strict=True)


class PublicUser(BaseModel):
    """Never return a password hash or a session identifier."""

    id: str
    username: str
    role: str
