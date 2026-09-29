import json

from typing import Any

from . import mock_ai

from ..config import settings


try:

    from google import genai

    from google.genai import types

except Exception:

    genai = None
    types = None


SYSTEM = """
You are PocketSmart AI, a budget-aware recommendation assistant.

Return ONLY valid JSON.

Never invent live availability.

Treat platform names as search destinations,
not proof of current stock or price.

Respect the user's total budget.

Explain estimates.

Use this schema:

{
    "summary": "string",
    "budget_allocation": {},
    "recommendations": [],
    "tips": []
}

Recommendations should include:

name,
category,
estimated_price or estimated_total,
platform,
reason

where relevant.
"""


def _client():

    if (
        not settings.gemini_api_key
        or settings.use_mock_ai
        or genai is None
    ):

        return None

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def _call(
    prompt: str,
    image_bytes: bytes | None = None,
    mime: str | None = None
) -> dict[str, Any] | None:

    client = _client()

    if not client:
        return None

    contents: list[Any] = [
        SYSTEM + "\n\n" + prompt
    ]

    if image_bytes and types:

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime or "image/jpeg"
            )
        )

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=contents
    )

    text = (
        response.text or ""
    ).strip()

    if text.startswith("```"):

        text = (
            text
            .split("\n", 1)[1]
            .rsplit("```", 1)[0]
        )

    return json.loads(text)


def recommend(
    planner: str,
    request: Any,
    image_bytes: bytes | None = None,
    mime: str | None = None
) -> dict[str, Any]:

    try:

        if planner == "home":

            prompt = (
                "Create recommendations for home interior. "
                f"Input JSON: {request.model_dump_json()}"
            )

            result = _call(prompt)

            return (
                result
                or mock_ai.home(request)
            )

        if planner == "party":

            prompt = (
                "Create recommendations for party planning. "
                f"Input JSON: {request.model_dump_json()}"
            )

            result = _call(prompt)

            return (
                result
                or mock_ai.party(request)
            )

        prompt = (
            "Create jewelry recommendations for this request. "
            f"Input JSON: {request.model_dump_json()}. "
            "Analyze the uploaded outfit image if present "
            "for color/style coordination, without identifying "
            "the person."
        )

        result = _call(
            prompt,
            image_bytes,
            mime
        )

        return (
            result
            or mock_ai.jewelry(
                request,
                image_seen=image_bytes is not None
            )
        )

    except Exception as exc:

        if planner == "home":

            fallback = mock_ai.home(
                request
            )

        elif planner == "party":

            fallback = mock_ai.party(
                request
            )

        else:

            fallback = mock_ai.jewelry(
                request,
                image_seen=image_bytes is not None
            )

        fallback["ai_note"] = (
            "AI service unavailable; "
            "showing safe demo recommendations. "
            f"Details: {type(exc).__name__}"
        )

        return fallback