
def get_text(key: str, lang: str = "hy") -> str:
    texts = {
        "start": {
            "hy": "Բարև՛, ես AskYerevan բոտն եմ 🙌\nԻնչի՞ կարիք ունես։",
            "ru": "Привет! Я бот AskYerevan 🙌",
            "en": "Hello! I’m AskYerevan bot 🙌"
        }
    }
    return texts.get(key, {}).get(lang, key)
