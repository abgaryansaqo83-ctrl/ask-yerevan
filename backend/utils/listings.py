# backend/utils/listings.py

from __future__ import annotations
from typing import Literal

ListingCategory = Literal[
    "sell",          # իրերի վաճառք
    "rent",          # վարձով
    "job_offer",     # աշխատանքի / ծառայության առաջարկ
    "search",        # փնտրում եմ
]


SELL_KEYWORDS = [
    "վաճառվում է", "վաճառք", "վաճառքի", "ծախսում եմ",
    "продам", "продаю", "продажа",
]

RENT_KEYWORDS = [
    "վարձով է տրվում", "վարձով է տալիս", "վարձով", "վարձակալություն",
    "сдаётся", "сдается", "аренда",
]

JOB_OFFER_KEYWORDS = [
    "աշխատանք է առաջարկվում", "աշխատանքի առաջարկ", "պետք է աշխատակից",
    "վերցնում ենք աշխատանքի", "ищем сотрудника", "вакансия", "работа предлагается",
    "услуги оказываю", "предлагаю услуги",
]

SEARCH_KEYWORDS = [
    "փնտրում եմ", "պետք է գտնեմ", "պետք է բնակարան", "քիրա եմ փնտրում",
    "ищу", "нужна работа", "нужен человек", "нужна квартира",
]


def detect_listing_category(text: str) -> tuple[bool, ListingCategory | None]:
    """
    Վերադարձնում է (is_listing, category)՝ եթե տեքստը նման է հայտարարության։
    """
    if not text:
        return False, None

    lower = text.lower()

    for kw in SEARCH_KEYWORDS:
        if kw in lower:
            return True, "search"

    for kw in SELL_KEYWORDS:
        if kw in lower:
            return True, "sell"

    for kw in RENT_KEYWORDS:
        if kw in lower:
            return True, "rent"

    for kw in JOB_OFFER_KEYWORDS:
        if kw in lower:
            return True, "job_offer"

    return False, None
