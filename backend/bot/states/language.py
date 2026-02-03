# backend/bot/states/language.py
# ============================================
#   FSM STATE — LANGUAGE SELECTION
# ============================================

from aiogram.fsm.state import StatesGroup, State


class LanguageForm(StatesGroup):
    waiting_for_choice = State()
