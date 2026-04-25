# backend/ai/response.py

import os
import re
import aiohttp

from backend.utils.logger import logger

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


async def _call_gemini(system_prompt: str, user_message: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing")

    logger.info("Gemini: calling gemini-2.0-flash")

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY,
    }

    payload = {
        "system_instruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "parts": [{"text": user_message}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 900,
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json=payload) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Gemini API error {resp.status}: {text}")
            data = await resp.json()

            response = data["candidates"][0]["content"]["parts"][0]["text"].strip()

            # Հեռացնում ենք ավելորդ բացատները
            response = re.sub(r'\s+', ' ', response).strip()

            return response


async def generate_reply(
    user_message: str,
    lang: str = "hy",
) -> str:
    system_prompts = {
        "hy": (
            "Դու Երևանի և ամբողջ Հայաստանի մասին օգնող, անվտանգ բոտ ես։ "
            "Պատասխանում ես միայն այն հարցերին, որոնք վերաբերվում են Հայաստանին՝ Երևան, այլ քաղաքներ, վայրեր, ռեստորաններ, բարեր, ակումբներ, հյուրանոցներ, տեսարժան վայրեր, միջոցառումներ և տեղական կյանք։ "
            "Եթե քեզ հարցնում են որևէ այլ երկրի, քաղաքի կամ ընդհանուր աշխարհի մասին, պատասխանիր կարճ, մի քիչ սարկազմով, որ դու AskYerevan բոտն ես և զբաղվում ես միայն Հայաստանի թեմաներով։ "
            "Չես օգնում մարդկանց գտնել անձնական տվյալներ, փաստաթղթեր, հեռախոսահամարներ, դեմքի ճանաչում կամ այլ մարդու մասին «ստուգումներ»։ "
            "Պատասխանիր կարճ (մինչև 3 նախադասություն), պարզ լեզվով, հնարավորինս օգտակար և կոնկրետ։"
        ),
        "ru": (
            "Ты безопасный помощник по Еревану и всей Армении. "
            "Отвечаешь только на вопросы, которые связаны с Арменией: Ереван, другие города, заведения, рестораны, бары, клубы, отели, достопримечательности, события и местная жизнь. "
            "Если тебя спрашивают про другие страны, города или общие мировые темы, отвечай коротко и с лёгким сарказмом, что ты бот AskYerevan и работаешь только по Армении. "
            "Ты не помогаешь искать чужие персональные данные, документы, телефоны, распознавать лица или «пробивать» людей. "
            "Отвечай кратко (до 3 предложений), простым и понятным языком, как можно более полезно и по делу."
        ),
        "en": (
            "You are a safe assistant focused on Yerevan and all of Armenia. "
            "You only answer questions related to Armenia: Yerevan, other cities, places, restaurants, bars, clubs, hotels, landmarks, events, and local life. "
            "If someone asks about other countries, cities, or general world topics, reply briefly with a bit of sarcasm, making it clear you are the AskYerevan bot and only handle Armenia-related topics. "
            "You do not help search for personal data, documents, phone numbers, facial recognition, or any kind of background checks on people. "
            "Answer briefly (up to 3 sentences), in clear language, as helpful and concrete as possible."
        ),
    }
    system_prompt = system_prompts.get(lang, system_prompts["hy"])

    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is missing, fallback reply used")
        if lang == "ru":
            return "Пока что я не могу ответить подробно, но скоро научусь 🙂"
        if lang == "en":
            return "I cannot answer in detail yet, but I will learn soon 🙂"
        return "Հիմա դեռ չեմ կարող մանրամասն պատասխանել, բայց շուտով կկարողանամ 🙂"

    try:
        return await _call_gemini(system_prompt, user_message)
    except Exception as e:
        logger.exception("AI generate_reply failed: %s", e)
        if lang == "ru":
            return "Сейчас что-то пошло не так, попробуйте написать ещё раз позже."
        if lang == "en":
            return "Something went wrong, please try again later."
        return "Ինչ‑որ բան սխալ գնաց, խնդրում եմ փորձիր ավելի ուշ։"
