from datetime import (
    datetime,
    timedelta,
    timezone
)

from jose import (
    jwt,
    JWTError
)

from passlib.context import CryptContext

from fastapi import (
    Request,
    HTTPException,
    status
)

from .config import settings


pwd = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


ALGO = "HS256"

COOKIE = "pocketsmart_token"


def hash_password(value: str) -> str:
    return pwd.hash(value)


def verify_password(
    value: str,
    hashed: str
) -> bool:
    return pwd.verify(
        value,
        hashed
    )


def create_token(user_id: int) -> str:

    payload = {
        "sub": str(user_id),
        "exp": (
            datetime.now(timezone.utc)
            + timedelta(hours=12)
        )
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGO
    )


def user_id_from_request(
    request: Request
) -> int:

    token = request.cookies.get(COOKIE)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required"
        )

    try:

        data = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGO]
        )

        return int(data["sub"])

    except (
        JWTError,
        KeyError,
        ValueError
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session"
        )