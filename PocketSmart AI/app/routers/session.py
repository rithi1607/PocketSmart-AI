from fastapi import (
    APIRouter,
    Request,
    Depends
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import User

from ..security import user_id_from_request


router = APIRouter(
    prefix="/api",
    tags=["session"]
)


@router.get("/session-info")
def session_info(
    request: Request,
    db: Session = Depends(get_db)
):

    uid = user_id_from_request(request)

    user = db.get(
        User,
        uid
    )

    return {
        "logged_in": True,
        "user_id": uid,
        "email": user.email if user else None
    }


@router.get("/session-data")
def session_data(
    request: Request,
    db: Session = Depends(get_db)
):

    uid = user_id_from_request(request)

    user = db.get(
        User,
        uid
    )

    count = (
        len(user.recommendations)
        if user
        else 0
    )

    return {
        "user_id": uid,
        "recommendation_count": count
    }