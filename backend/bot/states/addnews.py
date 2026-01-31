# backend/bot/states/news.py
# ============================================
#   FSM STATE — ADD NEWS (OWNER ONLY)
# ============================================

from aiogram.fsm.state import StatesGroup, State

class AddNewsForm(StatesGroup):
    waiting_for_title_hy = State()
    waiting_for_title_en = State()
    waiting_for_content_hy = State()
    waiting_for_content_en = State()
    waiting_for_image = State()
    waiting_for_category = State()
