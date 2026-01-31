def detect_lang(message):
    code = (message.from_user.language_code or "hy").lower()
    if code.startswith("ru"):
        return "ru"
    if code.startswith("en"):
        return "en"
    return "hy"
