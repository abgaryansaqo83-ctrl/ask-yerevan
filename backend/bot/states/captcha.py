# backend/bot/states/captcha.py
# ============================================
#   FSM STATE — CAPTCHA VERIFICATION
# ============================================

from aiogram.fsm.state import StatesGroup, State


class CaptchaForm(StatesGroup):
    waiting_for_answer = State()
