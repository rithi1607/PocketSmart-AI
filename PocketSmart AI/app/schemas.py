from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)


class RegisterIn(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=120
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginIn(BaseModel):
    email: EmailStr

    password: str


class HomeItem(BaseModel):
    category: str = Field(
        min_length=2,
        max_length=80
    )

    quantity: int = Field(
        ge=1,
        le=100
    )

    notes: str = Field(
        default="",
        max_length=300
    )


class HomeRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    room: str = Field(
        min_length=2,
        max_length=80
    )

    style: str = Field(
        default="modern",
        max_length=80
    )

    items: list[HomeItem] = Field(
        min_length=1,
        max_length=30
    )


class PartyRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    event_type: str = Field(
        min_length=2,
        max_length=80
    )

    guests: int = Field(
        ge=1,
        le=5000
    )

    venue: str = Field(
        default="home",
        max_length=120
    )

    city: str = Field(
        default="",
        max_length=100
    )

    food_preference: str = Field(
        default="mixed",
        max_length=100
    )


class JewelryRequest(BaseModel):
    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = Field(
        min_length=2,
        max_length=100
    )

    style: str = Field(
        default="elegant",
        max_length=100
    )

    outfit_color: str = Field(
        default="",
        max_length=80
    )

    notes: str = Field(
        default="",
        max_length=500
    )


class RecommendationOut(BaseModel):
    id: int
    planner: str
    budget: float
    result: dict[str, Any]
    created_at: str