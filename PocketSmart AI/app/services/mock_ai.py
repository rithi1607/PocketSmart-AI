from typing import Any


def money(value: float) -> str:
    return f"₹{value:,.0f}"


def home(req) -> dict[str, Any]:

    shares = {
        "furniture": 0.45,
        "lighting": 0.20,
        "decor": 0.20,
        "misc": 0.15
    }

    per_item_budget = (
        req.budget /
        max(len(req.items), 1)
    )

    products = []

    for item in req.items:

        category = item.category.lower()

        if "light" in category:
            platform = "IKEA"

        elif (
            "fan" in category
            or "furniture" in category
        ):
            platform = "Amazon"

        else:
            platform = "Flipkart"

        price = round(
            min(
                per_item_budget,
                req.budget * 0.35
            ),
            -1
        )

        products.append(
            {
                "name": (
                    f"{req.style.title()} "
                    f"{item.category.title()} Pick"
                ),

                "category": item.category,

                "quantity": item.quantity,

                "estimated_unit_price": price,

                "platform": platform,

                "search_url": (
                    f"https://www."
                    f"{platform.lower()}.com/"
                    f"search?q="
                    f"{item.category.replace(' ', '+')}"
                ),

                "reason": (
                    f"Fits a {req.style} "
                    f"{req.room} plan and stays "
                    f"within the allocated budget."
                )
            }
        )

    return {
        "summary": (
            f"A {req.style} plan for your "
            f"{req.room} within "
            f"{money(req.budget)}."
        ),

        "budget_allocation": {
            "furniture": (
                req.budget * shares["furniture"]
            ),
            "lighting": (
                req.budget * shares["lighting"]
            ),
            "decor": (
                req.budget * shares["decor"]
            ),
            "miscellaneous": (
                req.budget * shares["misc"]
            )
        },

        "recommendations": products,

        "tips": [
            "Compare final prices and delivery charges before buying.",
            "Keep a small contingency for installation or accessories."
        ]
    }


def party(req) -> dict[str, Any]:

    allocation = {
        "food": req.budget * 0.50,
        "decoration": req.budget * 0.15,
        "venue": req.budget * 0.20,
        "entertainment": req.budget * 0.10,
        "contingency": req.budget * 0.05
    }

    food_per_guest = (
        allocation["food"] /
        req.guests
    )

    return {
        "summary": (
            f"{req.event_type.title()} plan "
            f"for {req.guests} guests in "
            f"{req.city or 'your city'}."
        ),

        "budget_allocation": allocation,

        "recommendations": [

            {
                "category": "Food",

                "option": (
                    f"{req.food_preference.title()} "
                    "catering package"
                ),

                "estimated_total": round(
                    allocation["food"]
                ),

                "estimated_per_guest": round(
                    food_per_guest
                ),

                "platform": "Swiggy / Zomato"
            },

            {
                "category": "Venue",

                "option": (
                    f"{req.venue.title()} "
                    "venue shortlist"
                ),

                "estimated_total": round(
                    allocation["venue"]
                ),

                "platform": (
                    "Local venues / OYO where applicable"
                )
            },

            {
                "category": "Decoration",

                "option": (
                    "Theme decoration package"
                ),

                "estimated_total": round(
                    allocation["decoration"]
                ),

                "platform": "Local decorators"
            },

            {
                "category": "Entertainment",

                "option": (
                    "Music / games / host"
                ),

                "estimated_total": round(
                    allocation["entertainment"]
                ),

                "platform": "Local vendors"
            }
        ],

        "tips": [
            "Get at least two vendor quotes.",
            "Confirm taxes, service fees and minimum-order rules."
        ]
    }


def jewelry(
    req,
    image_seen: bool = False
) -> dict[str, Any]:

    return {

        "summary": (
            f"{req.style.title()} jewelry ideas "
            f"for {req.occasion} within "
            f"{money(req.budget)}."
        ),

        "image_analysis": (
            "The uploaded outfit image was received; "
            "use its visible colors and neckline as "
            "a styling reference."
            if image_seen
            else
            "No outfit image supplied; "
            "recommendations use your text preferences."
        ),

        "recommendations": [

            {
                "name": "Minimal statement necklace",
                "type": "Necklace",
                "estimated_price": round(
                    req.budget * 0.35
                ),
                "platform": "Amazon",
                "match": (
                    "Balances an elegant occasion look."
                )
            },

            {
                "name": "Matching earrings",
                "type": "Earrings",
                "estimated_price": round(
                    req.budget * 0.25
                ),
                "platform": "Flipkart",
                "match": (
                    "Coordinates with the necklace "
                    "without overpowering the outfit."
                )
            },

            {
                "name": "Bracelet / bangle set",
                "type": "Bracelet",
                "estimated_price": round(
                    req.budget * 0.20
                ),
                "platform": "Amazon / Flipkart",
                "match": (
                    "Adds a coordinated accent."
                )
            }
        ],

        "tips": [
            "Check material, hallmark/certification and seller reviews.",
            "Reserve the remaining budget for delivery or alterations."
        ]
    }