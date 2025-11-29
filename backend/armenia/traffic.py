# backend/armenia/traffic.py

import aiohttp
import asyncio
from typing import List
from config.settings import settings
from .utils.logger import setup_logger

logger = setup_logger(__name__)

GOOGLE_DIRECTIONS_BASE = "https://maps.googleapis.com/maps/v1/directions"
YEREVAN_CENTER = "40.1811,44.5136"

# Կենտրոնական փողոցներ/մայրուղիներ Երևանում՝ խցանում ստուգելու համար
KEY_ROUTES = [
    # Սպիտակաձի → Նաիրի → Կենտրոն
    ("40.2050,44.5220", "40.1770,44.5100"),  # Սպիտակաձի → Նաիրի
    # Բաղրամյան → Թումանյան → Կենտրոն
    ("40.1900,44.5050", "40.1800,44.5150"),  # Բաղրամյան → Թումանյան
    # Դավիթ Անհհանգիստ → Կոմիտաս → Ֆիզիկայի
    ("40.1950,44.5200", "40.1850,44.5250"),  # Դավիթ Անհհանգիստ → Ֆիզիկայի
    # Արամյան → Շարուր → Մարշալ Բաղրամյան
    ("40.1700,44.5000", "40.1900,44.5100"),  # Արամյան → Մարշալ Բաղրամյան
    # Պաշտպանության → Վազգեն Սարգսյան → Ֆիզիկայի
    ("40.2100,44.5300", "40.1850,44.5250"),  # Պաշտպանության → Ֆիզիկայի
]


ROUTE_NAMES = {
    0: "Սպիտակաձի → Նաիրի",
    1: "Բաղրամյան → Թումանյան", 
    2: "Դավիթ Անհհանգիստ → Ֆիզիկայի",
    3: "Արամյան → Մարշալ Բաղրամյան",
    4: "Պաշտպանության → Ֆիզիկայի",
}


async def get_traffic_status(api_key: str = None) -> str:
    """
    Երկուշաբթի–ուրբաթ 08:30 խցանումների հաղորդագրություն.
    Կենտրոն գնացող փողոցներ, որտեղ խցանում կա.
    """
    api_key = api_key or settings.GOOGLE_DIRECTIONS_KEY
    
    if not api_key:
        return "🚗 Խցանումների տվյալները ժամանակավորապես անհասանելի են։"

    congested_routes = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, (origin, destination) in enumerate(KEY_ROUTES):
            task = check_route_congestion(session, origin, destination, i, api_key)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, dict) and result["congested"]:
                congested_routes.append(result)

    return _format_traffic_report(congested_routes)


async def check_route_congestion(
    session: aiohttp.ClientSession, 
    origin: str, 
    destination: str, 
    route_id: int, 
    api_key: str
) -> dict:
    """Ստուգում է մեկ route-ի խցանումը."""
    url = (
        f"{GOOGLE_DIRECTIONS_BASE}?"
        f"origin={origin}&destination={destination}"
        f"&travelMode=driving&departure_time=now&traffic_model=best_guess"
        f"&key={api_key}"
    )
    
    try:
        async with session.get(url) as resp:
            if resp.status != 200:
                return {"route_id": route_id, "congested": False}
            
            data = await resp.json()
            
            # Ստուգում ենք duration_in_traffic vs duration (typical)
            if "routes" not in data or not data["routes"]:
                return {"route_id": route_id, "congested": False}
            
            route = data["routes"][0]
            if not route["legs"]:
                return {"route_id": route_id, "congested": False}
            
            leg = route["legs"][0]
            duration_traffic = leg["duration_in_traffic"]["value"] if "duration_in_traffic" in leg else 0
            duration_typical = leg["duration"]["value"]
            
            # Եթե traffic duration > 120% typical, խցանում կա
            congested = duration_traffic > (duration_typical * 1.2)
            
            return {
                "route_id": route_id,
                "congested": congested,
                "duration_traffic": duration_traffic / 60,  # minutes
                "duration_typical": duration_typical / 60,
                "name": ROUTE_NAMES.get(route_id, f"Route {route_id}")
            }
            
    except Exception as e:
        logger.warning(f"Route {route_id} check failed: {e}")
        return {"route_id": route_id, "congested": False}


def _format_traffic_report(routes: List[dict]) -> str:
    """Խցանումների հաշվետվության ֆորմատ."""
    if not routes:
        return "🚗 ✅ Երևանի կենտրոնական փողոցներում խցանումներ չկան։ Բարի ճանապարհ։"
    
    lines = ["🚨 <b>Խցանումներ դեպի կենտրոն</b>\n\n"]
    
    for route in routes:
        name = route["name"]
        if route["duration_traffic"] > route["duration_typical"] * 1.5:
            status = "կանգնացել է"
        else:
            status = "խցանում կա"
        
        line = f"📍 {name} — {status}\n"
        lines.append(line)
    
    lines.append("\n💡 Խորհուրդ՝ օգտագործիր Google Maps-ը իրական ժամանակի տվյալների համար։")
    
    return "\n".join(lines)

