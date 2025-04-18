import re
from utils.env_loader import get_badword_percent
from rapidfuzz import process, fuzz

percent = get_badword_percent()

import re
import difflib
import os

BADWORDS_FILE = 'resources/text/badwords.txt'
SIMILARITY_THRESHOLD = percent


def load_bad_words(filepath):
    if not os.path.exists(filepath):
        print(f"Xato: '{filepath}' fayli topilmadi.")
        return set(), {}

    bad_words_set = set()
    normalized_to_original = {}

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()
                if word and not word.startswith('#'):
                    bad_words_set.add(word)
                    normalized_word = normalize_word(word)

                    if normalized_word not in normalized_to_original:
                        normalized_to_original[normalized_word] = word


    except Exception as e:
        print(f"Xato: '{filepath}' faylini o'qishda muammo: {e}")
        return set(), {}

    print(f"{len(bad_words_set)} ta nomaqbul so'z yuklandi.")
    return bad_words_set, normalized_to_original


def normalize_word(word):
    word = word.lower()

    word = re.sub(r'\s+', '', word)

    word = re.sub(r'(.)\1+', r'\1', word)
    return word


def find_bad_words_in_text(text, bad_words_set, normalized_to_original, threshold):
    found_matches = []
    normalized_bad_words_keys = list(normalized_to_original.keys())  # O'xshashlik uchun list

    words_in_text = re.findall(r'\b[\w\']+\b', text.lower())

    for word in words_in_text:
        normalized_input_word = normalize_word(word)

        if normalized_input_word in normalized_to_original:
            original_bad_word = normalized_to_original[normalized_input_word]
            found_matches.append({
                "input_word": word,
                "matched_bad_word": original_bad_word,
                "reason": f"Normallashtirilgan moslik ({normalized_input_word})"
            })
            continue

        close_matches = difflib.get_close_matches(normalized_input_word, normalized_bad_words_keys, n=1, cutoff=threshold)

        if close_matches:
            matched_normalized = close_matches[0]
            original_bad_word = normalized_to_original[matched_normalized]
            similarity = difflib.SequenceMatcher(None, normalized_input_word, matched_normalized).ratio()
            found_matches.append({
                "input_word": word,
                "matched_bad_word": original_bad_word,
                "reason": f"O'xshashlik ({similarity:.2f} > {threshold}) normallashtirilgan '{matched_normalized}' ga"
            })

    processed_text = text.lower()
    normalized_processed_text = normalize_word(processed_text)

    for bad_phrase in bad_words_set:
        if ' ' in bad_phrase:
            normalized_bad_phrase = normalize_word(bad_phrase)
            if normalized_bad_phrase in normalized_processed_text:
                already_found = False
                for match in found_matches:
                    if match['matched_bad_word'] in bad_phrase:
                        pass

                if not already_found:
                    found_matches.append({
                        "input_word": f"'{bad_phrase}' iborasiga o'xshash qism",
                        "matched_bad_word": bad_phrase,
                        "reason": f"Normallashtirilgan ibora mosligi ('{normalized_bad_phrase}')"
                    })

    return found_matches


bad_words, norm_to_orig_map = load_bad_words(BADWORDS_FILE)


def check_message_for_badwords(message: str):
    detected = find_bad_words_in_text(message, bad_words, norm_to_orig_map, SIMILARITY_THRESHOLD)
    return detected
