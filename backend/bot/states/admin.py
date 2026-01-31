# backend/bot/states/admin.py
# ============================================
#   FSM STATE — ADMIN MESSAGE
# ============================================

from aiogram.fsm.state import StatesGroup, State

class AdminForm(StatesGroup):
    waiting_for_message = State()
