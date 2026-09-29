from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import User

from ..schemas import (
    RegisterIn,
    LoginIn
)

from ..security import (
    hash_password,
    verify_password,
    create_token,
    COOKIE,
    user_id_from_request
)


router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)


@router.post("/register")
def register(
    data: RegisterIn,
    response: Response,
    db: Session = Depends(get_db)
):

    email = data.email.lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    user = User(
        name=data.name.strip(),
        email=email,
        password_hash=hash_password(
            data.password
        )
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    response.set_cookie(
        COOKIE,
        create_token(user.id),
        httponly=True,
        samesite="lax",
        max_age=43200
    )

    return {
        "message": "Registered",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/login")
def login(
    data: LoginIn,
    response: Response,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == data.email.lower()
        )
        .first()
    )

    if (
        not user
        or not verify_password(
            data.password,
            user.password_hash
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    response.set_cookie(
        COOKIE,
        create_token(user.id),
        httponly=True,
        samesite="lax",
        max_age=43200
    )

    return {
        "message": "Logged in",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


@router.post("/logout")
def logout(
    response: Response
):

    response.delete_cookie(COOKIE)

    return {
        "message": "Logged out"
    }


@router.get("/session")
def session(
    request: Request,
    db: Session = Depends(get_db)
):

    uid = user_id_from_request(request)

    user = db.get(
        User,
        uid
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return {
        "authenticated": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }