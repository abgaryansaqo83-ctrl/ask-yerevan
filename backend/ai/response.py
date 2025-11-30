# backend/ai/response.py

import os
from openai import AsyncOpenAI

from backend.utils.logger import logger

AI_API_KEY = os.getenv("AI_API_KEY", "")

client = AsyncOpenAI(api_key=AI_API_KEY)


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
    if not AI_API_KEY:
        logger.warning("AI_API_KEY is missing, fallback reply used")
        if lang == "ru":
            return "Пока что я не могу ответить подробно, но скоро научусь 🙂"
        if lang == "en":
            return "I cannot answer in detail yet, but I will learn soon 🙂"
        return "Հիմա դեռ չեմ կարող մանրամասն պատասխանել, բայց շուտով կկարողանամ 🙂"

    system_prompts = {
        "hy": (
            "Դու Երևանի մասին օգնող, անվտանգ բոտ ես։ Չես օգնում մարդկանց գտնել անձնական տվյալներ, փաստաթղթեր, հեռախոսահամարներ, դեմքի ճանաչում կամ այլ մարդու մասին «ստուգումներ»։ Պատասխանիր կարճ (մինչև 3 նախադասություն), միայն անվտանգ, նորմալ հարցերին՝ սնունդ, տեղեր, իրադարձություններ։"
        ),
        "ru": (
            "Ты безопасный помощник про Ереван. Ты не помогаешь искать чужие персональные данные, документы, телефоны, распознавать лица или «пробивать» людей. Отвечай коротко (до 3 предложений) только на безопасные вопросы про город, места, события."
        ),
        "en": (
            "You are a safe assistant about Yerevan. You do not help search for personal data, documents, phone numbers, facial recognition, or ‘background checks’ on people. Answer briefly (up to 3 sentences) only safe questions about the city, places, and events."
        ),
    }
    system_prompt = system_prompts.get(lang, system_prompts["hy"])

    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logger.exception("AI generate_reply failed: %s", e)
        if lang == "ru":
            return "Сейчас что-то пошло не так, попробуйте написать ещё раз позже."
        if lang == "en":
            return "Something went wrong, please try again later."
        return "Ինչ‑որ բան սխալ գնաց, խնդրում եմ փորձիր ավելի ուշ։"
