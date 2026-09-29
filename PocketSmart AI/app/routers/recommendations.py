from fastapi import (
    APIRouter,
    Depends,
    Request,
    UploadFile,
    File,
    HTTPException,
    Form
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest
)

from ..security import (
    user_id_from_request
)

from ..services.recommendations import (
    create_recommendation
)


router = APIRouter(
    prefix="/api/recommendations",
    tags=["recommendations"]
)


def auth_user(
    request: Request
):

    return user_id_from_request(
        request
    )


@router.post("/home")
def home(
    data: HomeRequest,
    request: Request,
    db: Session = Depends(get_db)
):

    user_id = auth_user(request)

    row, result = create_recommendation(
        db,
        user_id,
        "home",
        data
    )

    return {
        "id": row.id,
        "planner": "home",
        "budget": row.budget,
        "result": result
    }


@router.post("/party")
def party(
    data: PartyRequest,
    request: Request,
    db: Session = Depends(get_db)
):

    user_id = auth_user(request)

    row, result = create_recommendation(
        db,
        user_id,
        "party",
        data
    )

    return {
        "id": row.id,
        "planner": "party",
        "budget": row.budget,
        "result": result
    }


@router.post("/jewelry")
async def jewelry(
    request: Request,
    db: Session = Depends(get_db),
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("elegant"),
    outfit_color: str = Form(""),
    notes: str = Form(""),
    image: UploadFile | None = File(
        default=None
    )
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be greater than zero"
        )

    data = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        outfit_color=outfit_color,
        notes=notes
    )

    content = None
    mime = None

    if image:

        if (
            not image.content_type
            or not image.content_type.startswith(
                "image/"
            )
        ):

            raise HTTPException(
                status_code=400,
                detail="Only image uploads are supported"
            )

        content = await image.read()

        if len(content) > 5 * 1024 * 1024:

            raise HTTPException(
                status_code=413,
                detail="Image must be 5 MB or smaller"
            )

        mime = image.content_type

    user_id = auth_user(request)

    row, result = create_recommendation(
        db,
        user_id,
        "jewelry",
        data,
        content,
        mime
    )

    return {
        "id": row.id,
        "planner": "jewelry",
        "budget": row.budget,
        "result": result
    }