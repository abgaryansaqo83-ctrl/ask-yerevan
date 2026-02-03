# backend/bot/states/language.py

from aiogram.fsm.state import StatesGroup, State

class LanguageForm(StatesGroup):
    waiting_for_choice = State()
