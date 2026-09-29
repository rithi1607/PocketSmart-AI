import json

from sqlalchemy.orm import Session

from ..models import Recommendation

from .gemini import recommend


def create_recommendation(
    db: Session,
    user_id: int,
    planner: str,
    request,
    image_bytes=None,
    mime=None
):

    result = recommend(
        planner,
        request,
        image_bytes,
        mime
    )

    row = Recommendation(
        user_id=user_id,
        planner=planner,
        budget=request.budget,
        request_json=request.model_dump_json(),
        result_json=json.dumps(
            result
        )
    )

    db.add(row)

    db.commit()

    db.refresh(row)

    return row, result