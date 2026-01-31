# backend/armenia/recommend.py

import aiohttp
from typing import List, Optional

from backend.config.settings import settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

# Classic Places API base (nearbysearch/json)
GOOGLE_PLACES_BASE = "https://maps.googleapis.com/maps/api/place"
YEREVAN_CENTER = "40.1811,44.5136"

# Փնտրման keywords-ները հայերեն/անգլերեն
CATEGORY_MAP = {
    "սնունդ": "restaurant",
    "սրճարան": "cafe",
    "ռեստորան": "restaurant",
    "բար": "bar",
    "փաբ": "bar",
    "ռոք": "night_club",
    "ջազ": "night_club",
    "ծնունդ": "restaurant",
    "հավաքույթ": "restaurant",
    "հանգիստ": "cafe",
    "ուտել": "restaurant",
    "food": "restaurant",
    "cafe": "cafe",
    "bar": "bar",
}

RECOMMEND_EMOJIS = {
    "restaurant": "🍽️",
    "cafe": "☕",
    "bar": "🍻",
    "night_club": "🎶",
}


async def get_recommendations(
    query: str,
    api_key: str = None,
    limit: int = 2,
    user_location: Optional[str] = None,  # "lat,lon"
) -> List[str]:
    """
    AI + Google Places recommendations.
    1-2 տարբերակ՝ rating > 4.0, open_now.
    Նախ փորձում է user_location-ից, հետո fallback է անում Երևանի կենտրոնից ավելի լայն շառավիղով։
    """
    api_key = api_key or settings.GOOGLE_MAPS_API_KEY

    if not api_key:
        return ["🍽️ Recommendation service temporarily unavailable 😅"]

    category = _detect_category(query)
    if not category:
        return [
            "🤔 Մոտիկ վայր առաջարկելու համար գրի՛, թե ինչ տեսակի տեղ ես փնտրում "
            "(սրճարան, ռեստորան, փաբ...)"
        ]

    emoji = RECOMMEND_EMOJIS.get(category, "📍")

    async with aiohttp.ClientSession() as session:
        try:
            places: List[dict] = []

            # 1) Նախ՝ user_location-ից, եթե ունենք
            if user_location:
                places = await _search_places(
                    session,
                    category=category,
                    api_key=api_key,
                    location=user_location,
                    radius=3000,
                    limit=limit,
                )

            # 2) Եթե չգտավ կամ user_location չունենք → fallback Երևանի կենտրոնից
            if not places:
                places = await _search_places(
                    session,
                    category=category,
                    api_key=api_key,
                    location=YEREVAN_CENTER,
                    radius=7000,  # մի քիչ ավելի լայն շրջան
                    limit=limit,
                )

            recommendations: List[str] = []
            for place in places[:limit]:
                rec_text = _format_recommendation(place, emoji)
                recommendations.append(rec_text)

            return (
                recommendations
                if recommendations
                else [f"{emoji} Այս պահին լավ {category}-ներ չգտնվեցին մոտակայքում։"]
            )

        except Exception as e:
            logger.error(f"Recommendations failed: {e}")
            return [f"{emoji} Ռեկոմենդացիաների սերվիսը ժամանակավոր անհասանելի է 😅"]


async def _search_places(
    session: aiohttp.ClientSession,
    category: str,
    api_key: str,
    location: str,
    radius: int = 3000,
    limit: int = 3,
) -> List[dict]:
    """
    Google Places Nearby Search arbitrary location-ից.
    location: "lat,lon"
    """
    url = (
        f"{GOOGLE_PLACES_BASE}/nearbysearch/json?"
        f"location={location}"
        f"&radius={radius}"
        f"&type={category}"
        f"&open_now=true"
        f"&key={api_key}"
    )

    async with session.get(url) as resp:
        data = await resp.json()
        places: List[dict] = []

        results = data.get("results", [])
        for place in results:
            rating = place.get("rating", 0)
            if rating >= 4.0:
                places.append(
                    {
                        "name": place.get("name", "Անվանումը բացակայում է"),
                        "rating": rating,
                        "address": place.get("vicinity", ""),
                        "price_level": place.get("price_level", 0),
                        "types": place.get("types", []),
                    }
                )

        return sorted(places, key=lambda x: x["rating"], reverse=True)[:limit]


def _detect_category(query: str) -> Optional[str]:
    """Հայերեն/անգլերեն keywords-եր detect անում ա։"""
    query_lower = query.lower()

    for keyword, category in CATEGORY_MAP.items():
        if keyword in query_lower:
            return category

    return None


def _format_recommendation(place: dict, emoji: str) -> str:
    """1 տեղի recommendation-ի ֆորմատ։"""
    name = place["name"]
    rating = place["rating"]
    address = place["address"]
    price_level = place["price_level"]

    # Price emoji (Google price_level 0–4)
    price_emojis = {
        0: "💸",          # unknown
        1: "💰",          # էժան
        2: "💰💰",
        3: "💰💰💰",
        4: "💰💰💰💰",
    }
    price_str = price_emojis.get(price_level, "💰")

    # Short description
    types = place.get("types", [])
    desc = _get_short_desc(types)

    return (
        f"{emoji} {name}\n"
        f"⭐ {rating:.1f} | {address}\n"
        f"{price_str} {desc}"
    )


def _get_short_desc(types: List[str]) -> str:
    """Types-ից կարճ նկարագրություն։"""
    if "restaurant" in types:
        return "համեղ խոհանոց + հարմար մթնոլորտ"
    elif "cafe" in types:
        return "համեղ սուրճ + հանգստյան վայր"
    elif "bar" in types or "night_club" in types:
        return "լավ երեկոյան + երաժշտություն"
    else:
        return "հիանալի ընտրություն"
