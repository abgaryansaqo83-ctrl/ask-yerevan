# backend/bot/handlers/captcha.py
# ============================================
#   CAPTCHA TEST + CHAT MEMBER RESTRICTIONS
# ============================================

import datetime
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    ChatPermissions,
    ChatMemberUpdated,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext

from backend.languages import get_text
from backend.utils.logger import logger

from ..states.captcha import CaptchaForm
from ..handlers.language import build_language_keyboard


router = Router()

# --------------------------------------------
# CAPTCHA correct answer
# --------------------------------------------
CAPTCHA_CORRECT = "lion"


# --------------------------------------------
# Build CAPTCHA keyboard
# --------------------------------------------
def build_captcha_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🦁 Առյուծ", callback_data="captcha:lion"),
                InlineKeyboardButton(text="🐶 Շուն", callback_data="captcha:dog"),
                InlineKeyboardButton(text="🐱 Կատու", callback_data="captcha:cat"),
            ]
        ]
    )


# --------------------------------------------
# Send CAPTCHA test to new user
# --------------------------------------------
async def send_captcha_test(chat_id: int, user_id: int, state: FSMContext, lang: str):
    """
    Sends the CAPTCHA test to a new member and restricts them until solved.
    """
    await state.set_state(CaptchaForm.waiting_for_answer)
    await state.update_data(captcha_attempts=0)

    text = {
        "hy": "Բարի գալուստ 👋\nԽնդրում եմ ընտրիր՝ ո՞ր կենդանին է առյուծը։",
        "ru": "Добро пожаловать 👋\nПожалуйста, выберите, где здесь лев.",
        "en": "Welcome 👋\nPlease choose which one is the lion.",
    }.get(lang, "Խնդրում եմ ընտրիր՝ ո՞ր կենդանին է առյուծը։")

    await state.update_data(captcha_next_allowed=None)

    await router.bot.send_message(
        chat_id,
        text,
        reply_markup=build_captcha_keyboard(),
    )


# --------------------------------------------
# CAPTCHA callback handler
# --------------------------------------------
@router.callback_query(F.data.startswith("captcha:"), CaptchaForm.waiting_for_answer)
async def handle_captcha_answer(callback: CallbackQuery, state: FSMContext):
    choice = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    data = await state.get_data()
    attempts = int(data.get("captcha_attempts", 0))
    next_allowed_str = data.get("captcha_next_allowed")

    now = datetime.datetime.now(datetime.timezone.utc)

    # Check cooldown
    if next_allowed_str:
        try:
            next_allowed = datetime.datetime.fromisoformat(next_allowed_str)
        except Exception:
            next_allowed = None

        if next_allowed and now < next_allowed:
            wait_hours = int((next_allowed - now).total_seconds() // 3600 + 1)
            await callback.answer(
                f"Հաջորդ փորձը հնարավոր կլինի մոտավորապես {wait_hours} ժամից։",
                show_alert=True,
            )
            return

    # Correct answer
    if choice == CAPTCHA_CORRECT:
        await state.update_data(captcha_passed=True)

        # Unrestrict user
        await callback.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
            ),
        )

        lang = "hy"
        welcome = get_text("welcome_new_member", lang).format(
            name=callback.from_user.full_name
        )

        combined = (
            "✅ Շնորհակալություն, թեստը հաջող անցար, հիմա կարող ես գրել խմբում։\n\n"
            + welcome
        )

        await callback.message.edit_text(combined)
        await callback.answer()

        # Ask language preference in private chat
        kb = build_language_keyboard()
        await callback.bot.send_message(
            callback.from_user.id,
            "Ընտրիր, թե որ լեզվով ես ուզում, որ բոտը քեզ հետ խոսի․",
            reply_markup=kb,
        )

        await state.clear()
        return

    # Wrong answer
    attempts += 1

    wait_hours = 0
    message_tail = ""

    if attempts == 1:
        message_tail = "Սա առաջին սխալ փորձն է, կարող ես նորից ընտրել։"
    elif attempts == 2:
        wait_hours = 8
        message_tail = "Սա երկրորդ սխալ փորձն է, հաջորդ հնարավորությունը կլինի 8 ժամից։"
    elif attempts == 3:
        wait_hours = 12
        message_tail = "Արդեն երեք սխալ փորձ կա, հաջորդ հնարավորությունը կլինի 12 ժամից։"
    elif attempts == 4:
        wait_hours = 24
        message_tail = "Սա չորրորդ սխալ փորձն է։ Հաջորդը կլինի վերջինը և հասանելի կլինի 24 ժամից։"
    else:
        # Blacklist
        await state.update_data(
            captcha_attempts=attempts,
            captcha_next_allowed=None,
            captcha_blacklisted=True,
        )
        await callback.answer(
            "Դու բազմակի անգամ սխալ ես ընտրել։ Հիմա խմբում կմնաս առանց գրելու հնարավորության։",
            show_alert=True,
        )
        return

    next_allowed = now + datetime.timedelta(hours=wait_hours) if wait_hours else None

    await state.update_data(
        captcha_attempts=attempts,
        captcha_next_allowed=next_allowed.isoformat() if next_allowed else None,
    )

    await callback.answer(
        f"Սխալ ընտրություն է։ {message_tail}",
        show_alert=True,
    )


# --------------------------------------------
# Chat member update — new member joins
# --------------------------------------------
@router.chat_member()
async def on_chat_member_update(event: ChatMemberUpdated, state: FSMContext):
    """
    When a new user joins the group:
    - Restrict them
    - Send CAPTCHA test
    """
    logger.info(
        "chat_member update: chat=%s user=%s old=%s new=%s",
        event.chat.id,
        event.new_chat_member.user.id,
        event.old_chat_member.status,
        event.new_chat_member.status,
    )

    old = event.old_chat_member
    new = event.new_chat_member
    user = new.user
    chat_id = event.chat.id

    # Detect language
    lang_code = (user.language_code or "hy").lower()
    if lang_code.startswith("ru"):
        lang = "ru"
    elif lang_code.startswith("en"):
        lang = "en"
    else:
        lang = "hy"

    # New member joined
    if new.status in ("member", "administrator") and old.status not in ("member", "administrator"):

        data = await state.get_data()
        if data.get("captcha_passed"):
            return

        # Restrict user until CAPTCHA is solved
        await event.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False),
        )

        await send_captcha_test(chat_id, user.id, state, lang=lang)
        return

    # Member left
    if old.status in ("member", "administrator") and new.status in ("left", "kicked"):
        text = get_text("goodbye_member", lang).format(name=user.full_name)
        await event.bot.send_message(chat_id, text)
