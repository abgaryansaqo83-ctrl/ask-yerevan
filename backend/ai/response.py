# backend/ai/response.py

import os
import aiohttp

from backend.utils.logger import logger

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "")

API_URL = "https://api.perplexity.ai/chat/completions"
MODEL_NAME = "sonar-small"

async def _call_perplexity(system_prompt: str, user_message: str) -> str:
    if not PERPLEXITY_API_KEY:
        raise RuntimeError("PERPLEXITY_API_KEY is missing")

    logger.info(f"Perplexity: using model={MODEL_NAME}")

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }
    ...

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Perplexity API error {resp.status}: {text}")
            data = await resp.json()
            return data["choices"][0]["message"]["content"].strip()


async def generate_reply(
    user_message: str,
    lang: str = "hy",
) -> str:
    """
    AskYerevan city-helper AI պատասխաններ:
    - Կենտրոնանում է Երևանի վրա
    - Պատասխանում է կարճ, 1–3 նախադասություն
    - Պահպանում է նշված լեզուն (hy/ru/en)
    """
    system_prompts = {
        "hy": (
            "Դու Երևանի մասին օգնող, անվտանգ բոտ ես։ Չես օգնում մարդկանց գտնել անձնական տվյալներ, "
            "փաստաթղթեր, հեռախոսահամարներ, դեմքի ճանաչում կամ այլ մարդու մասին «ստուգումներ»։ "
            "Պատասխանիր կարճ (մինչև 3 նախադասություն), միայն անվտանգ, նորմալ հարցերին՝ սնունդ, տեղեր, իրադարձություններ։"
        ),
        "ru": (
            "Ты безопасный помощник про Ереван. Ты не помогаешь искать чужие персональные данные, "
            "документы, телефоны, распознавать лица или «пробивать» людей. "
            "Отвечай кратко (до 3 предложений) только на безопасные вопросы про город, места, события."
        ),
        "en": (
            "You are a safe assistant about Yerevan. You do not help search for personal data, "
            "documents, phone numbers, facial recognition, or ‘background checks’ on people. "
            "Answer briefly (up to 3 sentences) only safe questions about the city, places, and events."
        ),
    }
    system_prompt = system_prompts.get(lang, system_prompts["hy"])

    if not PERPLEXITY_API_KEY:
        logger.warning("PERPLEXITY_API_KEY is missing, fallback reply used")
        if lang == "ru":
            return "Пока что я не могу ответить подробно, но скоро научусь 🙂"
        if lang == "en":
            return "I cannot answer in detail yet, but I will learn soon 🙂"
        return "Հիմա դեռ չեմ կարող մանրամասն պատասխանել, բայց շուտով կկարողանամ 🙂"

    try:
        return await _call_perplexity(system_prompt, user_message)
    except Exception as e:
        logger.exception("AI generate_reply failed: %s", e)
        if lang == "ru":
            return "Сейчас что-то пошло не так, попробуйте написать ещё раз позже."
        if lang == "en":
            return "Something went wrong, please try again later."
        return "Ինչ‑որ բան սխալ գնաց, խնդրում եմ փորձիր ավելի ուշ։"
