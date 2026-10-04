from .arabic import extract_arabic_signals
from .english import extract_english_signals


def detect_language(text: str) -> str:
    for character in str(text):
        if "\u0600" <= character <= "\u06FF":
            return "ar"

    return "en"


def extract_signals(text: str) -> dict:
    language = detect_language(text)

    if language == "ar":
        return extract_arabic_signals(text)

    return extract_english_signals(text)