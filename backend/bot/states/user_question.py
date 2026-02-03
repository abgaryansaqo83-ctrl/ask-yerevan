# backend/bot/states/user_question.py
# ============================================
#   FSM STATE — USER QUESTION
# ============================================

from aiogram.fsm.state import StatesGroup, State


class UserQuestion(StatesGroup):
    waiting_for_question = State()
