"""Password hashing, verification, and JWT token utilities."""

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from core.config import get_configs

configs = get_configs()


# --- Password ---


def hash_password(plain: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


# --- JWT ---


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a signed JWT access token.

    Args:
        data: Claims to encode (e.g. {"sub": user_id}).
        expires_delta: Custom expiry. Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (
        expires_delta or timedelta(minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, configs.SECRET_KEY, algorithm=configs.ALGORITHM
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decode and validate a JWT access token.

    Returns:
        The decoded claims dict, or None if the token is invalid/expired.
    """
    try:
        return jwt.decode(
            token, configs.SECRET_KEY, algorithms=[configs.ALGORITHM]
        )
    except JWTError:
        return None
