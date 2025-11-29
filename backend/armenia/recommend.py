# backend/armenia/recommend.py

import aiohttp
import re
from typing import List, Optional
from config.settings import settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

GOOGLE_PLACES_BASE = "https://maps.googleapis.com/maps/v1/places"
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
    limit: int = 2
) -> List[str]:
    """
    AI + Google Places recommendations.
    1-2 տարբերակ՝ rating > 4.0, open_now, near center.
    """
    api_key = api_key or settings.GOOGLE_MAPS_API_KEY
    
    if not api_key:
        return ["🍽️ Recommendation service temporarily unavailable 😅"]
    
    category = _detect_category(query)
    if not category:
        return ["🤔 Ճշտիր, ինչ տեսակի վայր ես փնտրում (սնունդ, սրճարան, բար, ռոք...)"]
    
    emoji = RECOMMEND_EMOJIS.get(category, "📍")
    
    async with aiohttp.ClientSession() as session:
        try:
            places = await _search_places(session, category, api_key)
            recommendations = []
            
            for place in places[:limit]:
                rec_text = _format_recommendation(place, emoji)
                recommendations.append(rec_text)
            
            return recommendations if recommendations else [
                f"{emoji} Ցավակցություն, {category}-ի լավ տարբերակներ չգտնվեցին։"
            ]
            
        except Exception as e:
            logger.error(f"Recommendations failed: {e}")
            return [f"{emoji} Ռեկոմենդացիաների սերվիսը ժամանակավոր անհասանելի ա 😅"]


async def _search_places(
    session: aiohttp.ClientSession, 
    category: str, 
    api_key: str
) -> List[dict]:
    """Google Places Nearby Search."""
    url = (
        f"{GOOGLE_PLACES_BASE}/nearbysearch/json?"
        f"location={YEREVAN_CENTER}"
        f"&radius=3000"
        f"&type={category}"
        f"&keyword=yer&open_now=true"
        f"&key={api_key}"
    )
    
    async with session.get(url) as resp:
        data = await resp.json()
        places = []
        
        if "results" in data:
            for place in data["results"]:
                rating = place.get("rating", 0)
                if rating >= 4.0:
                    places.append({
                        "name": place["name"],
                        "rating": rating,
                        "address": place.get("vicinity", ""),
                        "price_level": place.get("price_level", 1),
                        "types": place.get("types", []),
                    })
        
        # Sort by rating desc
        return sorted(places, key=lambda x: x["rating"], reverse=True)[:3]


def _detect_category(query: str) -> Optional[str]:
    """Հայերեն/անգլերեն keywords-եր detect անում ա."""
    query_lower = query.lower()
    
    for keyword, category in CATEGORY_MAP.items():
        if keyword in query_lower:
            return category
    
    return None


def _format_recommendation(place: dict, emoji: str) -> str:
    """1 տեղի recommendation-ի ֆորմատ."""
    name = place["name"]
    rating = place["rating"]
    address = place["address"]
    price_level = place["price_level"]
    
    # Price emoji
    price_emojis = {0: "💸💸💸", 1: "💰💰", 2: "💰", 3: "🆓"}
    price_str = price_emojis.get(price_level, "💰")
    
    # Short description
    types = place["types"]
    desc = _get_short_desc(types)
    
    return (
        f"{emoji} {name}"
        f"⭐ {rating:.1f} | {address}\n"
        f"{price_str} {desc}"
    )


def _get_short_desc(types: List[str]) -> str:
    """Types-ից կարճ նկարագրություն."""
    if "restaurant" in types:
        return "համեղ խոհանոց + հարմար մթնոլորտ"
    elif "cafe" in types:
        return "համեղ սուրճ + հանգստյան վայր"
    elif "bar" in types or "night_club" in types:
        return "լավ երեկոյան + երաժշտություն"
    else:
        return "հիանալի ընտրություն"

