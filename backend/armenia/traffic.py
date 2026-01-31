# backend/armenia/traffic.py

import aiohttp
import asyncio
from typing import List, Dict, Any
from backend.config.settings import settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

GOOGLE_DIRECTIONS_BASE = "https://maps.googleapis.com/maps/v1/directions"
YEREVAN_CENTER = "40.1811,44.5136"

# Կենտրոնական փողոցներ/մայրուղիներ Երևանում՝ խցանում ստուգելու համար
KEY_ROUTES = [
    # Սպիտակաձի → Նաիրի → Կենտրոն
    ("40.2050,44.5220", "40.1770,44.5100"),  # Սպիտակաձի → Նաիրի
    # Բաղրամյան → Թումանյան → Կենտրոն
    ("40.1900,44.5050", "40.1800,44.5150"),  # Բաղրամյան → Թումանյան
    # Դավիթ Անհանգիստ → Կոմիտաս → Ֆիզիկայի
    ("40.1950,44.5200", "40.1850,44.5250"),  # Դավիթ Անհանգիստ → Ֆիզիկայի
    # Արամյան → Շարուր → Մարշալ Բաղրամյան
    ("40.1700,44.5000", "40.1900,44.5100"),  # Արամյան → Մարշալ Բաղրամյան
    # Պաշտպանության → Վազգեն Սարգսյան → Ֆիզիկայի
    ("40.2100,44.5300", "40.1850,44.5250"),  # Պաշտպանության → Ֆիզիկայի
]

ROUTE_NAMES = {
    0: "Սպիտակաձի → Նաիրի",
    1: "Բաղրամյան → Թումանյան",
    2: "Դավիթ Անհանգիստ → Ֆիզիկայի",
    3: "Արամյան → Մարշալ Բաղրամյան",
    4: "Պաշտպանության → Ֆիզիկայի",
}


async def get_traffic_status(api_key: str = None) -> str:
    """
    Երկուշաբթի–ուրբաթ 08:30 խցանումների հաղորդագրություն.
    Ստուգում ենք մի քանի հիմնական ուղղություններ դեպի կենտրոն։
    """
    api_key = api_key or settings.GOOGLE_DIRECTIONS_KEY

    if not api_key:
        return "🚗 Խցանումների տվյալները ժամանակավորապես անհասանելի են։"

    congested_routes: List[Dict[str, Any]] = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, (origin, destination) in enumerate(KEY_ROUTES):
            task = check_route_congestion(session, origin, destination, i, api_key)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, dict) and result.get("congested"):
                congested_routes.append(result)

    return _format_traffic_report(congested_routes)


async def check_route_congestion(
    session: aiohttp.ClientSession,
    origin: str,
    destination: str,
    route_id: int,
    api_key: str,
) -> dict:
    """
    Ստուգում է մեկ route-ի խցանումը Google Directions API-ով.
    Ավելի զգայուն շեմ՝ 1.05 (5%+ դանդաղելը արդեն խցանում ենք համարում)։
    """
    url = (
        f"{GOOGLE_DIRECTIONS_BASE}?"
        f"origin={origin}&destination={destination}"
        f"&travelMode=driving&departure_time=now&traffic_model=best_guess"
        f"&key={api_key}"
    )

    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                logger.warning(f"Route {route_id} HTTP {resp.status}")
                return {"route_id": route_id, "congested": False}

            data = await resp.json()

            if "routes" not in data or not data["routes"]:
                return {"route_id": route_id, "congested": False}

            route = data["routes"][0]
            if not route.get("legs"):
                return {"route_id": route_id, "congested": False}

            leg = route["legs"][0]

            if "duration_in_traffic" not in leg or "duration" not in leg:
                # Եթե traffic data չկա, չենք եզրակացնում, որ աշխարհում ամեն ինչ OK է,
                # ուղղակի skip ենք անում այս ուղին։
                return {"route_id": route_id, "congested": False}

            duration_traffic = leg["duration_in_traffic"]["value"]  # վայրկյան
            duration_typical = leg["duration"]["value"]  # վայրկյան

            if duration_typical <= 0:
                return {"route_id": route_id, "congested": False}

            ratio = duration_traffic / duration_typical

            # Ավելի զգայուն շեմ՝ 1.05 → 5%+ դանդաղը արդեն նշում ենք որպես խցանում
            congested = ratio >= 1.05

            return {
                "route_id": route_id,
                "congested": congested,
                "ratio": ratio,
                "duration_traffic": duration_traffic / 60,  # րոպե
                "duration_typical": duration_typical / 60,
                "name": ROUTE_NAMES.get(route_id, f"Route {route_id}"),
            }

    except Exception as e:
        logger.warning(f"Route {route_id} check failed: {e}")
        return {"route_id": route_id, "congested": False}


def _format_traffic_report(routes: List[dict]) -> str:
    """
    Խցանումների հաշվետվության ֆորմատ.
    3 մակարդակ՝ միջին / խիտ / գրեթե կանգնած։
    Վերնագիրն էլ փոխում ենք ըստ ընդհանուր իրավիճակի։
    """
    if not routes:
        return (
            "🚗 ✅ Երևանի հիմնական երթուղիներում զգալի խցանումներ չկան։\n"
            "Մաղթում եմ անխափան երթևեկություն։"
        )

    # Max ratio overall՝ հասկանալու համար ընդհանուր ծանրությունը
    max_ratio = max((r.get("ratio", 1.0) for r in routes), default=1.0)

    if max_ratio >= 1.7:
        header = "🚨 <b>Երևանում լուրջ խցանումներ են</b>\n"
    elif max_ratio >= 1.3:
        header = "⚠️ <b>Երևանում խիտ խցանումներ կան</b>\n"
    else:
        header = "ℹ️ <b>Երևանում միջին խցանումներ են</b>\n"

    lines = [header, "Հիմնական ուղղություններ դեպի կենտրոն.\n"]

    for route in routes:
        name = route["name"]
        ratio = route.get("ratio", 1.0)
        dur_t = route.get("duration_traffic")
        dur_n = route.get("duration_typical")

        if ratio >= 1.7:
            status = "գրեթե կանգնած է"
        elif ratio >= 1.3:
            status = "խիտ խցանում"
        else:
            status = "միջին խցանում"

        extra = ""
        if dur_t is not None and dur_n is not None:
            extra = f" ({dur_n:.0f} → {dur_t:.0f} րոպե)"

        line = f"📍 {name} — {status}{extra}\n"
        lines.append(line)

    lines.append(
        "\n💡 Խորհուրդ՝ օգտագործիր Google Maps-ը կամ Waze-ը "
        "իրական ժամանակի երթևեկությունը տեսնելու համար։"
    )

    return "\n".join(lines)
