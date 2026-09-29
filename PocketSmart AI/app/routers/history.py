import json

from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..models import Recommendation

from ..security import user_id_from_request


router = APIRouter(
    prefix="/api",
    tags=["history"]
)


@router.get("/history")
def history(
    request: Request,
    db: Session = Depends(get_db)
):

    uid = user_id_from_request(request)

    rows = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == uid
        )
        .order_by(
            Recommendation.created_at.desc()
        )
        .limit(50)
        .all()
    )

    return [
        {
            "id": row.id,
            "planner": row.planner,
            "budget": row.budget,
            "created_at": row.created_at.isoformat(),
            "result": json.loads(
                row.result_json
            )
        }
        for row in rows
    ]


@router.get(
    "/recommendations/{rid}"
)
def detail(
    rid: int,
    request: Request,
    db: Session = Depends(get_db)
):

    uid = user_id_from_request(request)

    row = db.get(
        Recommendation,
        rid
    )

    if (
        not row
        or row.user_id != uid
    ):

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found"
        )

    return {
        "id": row.id,
        "planner": row.planner,
        "budget": row.budget,
        "created_at": row.created_at.isoformat(),
        "request": json.loads(
            row.request_json
        ),
        "result": json.loads(
            row.result_json
        )
    }