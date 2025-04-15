import re
from utils.env_loader import get_badword_percent
from rapidfuzz import process, fuzz

percent = get_badword_percent()

with open("resources/text/badwords.txt", "r", encoding="utf-8") as f:
    BAD_WORDS = [line.strip().lower() for line in f if line.strip()]
    BAD_WORDS_SET = set(BAD_WORDS)


def is_bad(word: str, threshold: int = percent):
    # Badword to‘liq mosligini tekshirish
    if word in BAD_WORDS_SET:
        return {'word': word, 'badword': word, 'percent': '100.0'}

    # So‘zning ichida substrat bo‘lsa, faqat to‘liq so‘z sifatida tekshiramiz
    substr_matches = [bad for bad in BAD_WORDS if re.search(rf'\b{re.escape(bad)}\b', word)]
    if substr_matches:
        longest = max(substr_matches, key=len)
        return {'word': word, 'badword': longest, 'percent': '100.0'}

    # Fuzz bilan eng yaqin mos so‘zni tekshiramiz
    result = process.extractOne(word, BAD_WORDS, scorer=fuzz.ratio)
    if result:
        match, score, _ = result
        score = float(score)
        if score >= threshold:
            return {'word': word, 'badword': match, 'percent': f"{score:.2f}"}

    return None


def check_message_for_badwords(message: str):
    words = message.lower().split()
    result = []
    for word in words:
        match = is_bad(word)
        if match:
            result.append(match)
    return result
