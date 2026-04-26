"""Language detection and translation"""

import os
from typing import Dict, Tuple

# Try importing language detection libraries
try:
    from langdetect import detect, detect_langs, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False

try:
    from google.cloud import translate_v2
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

# Language code mappings
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ta": "Tamil",
    "bn": "Bengali",
    "gu": "Gujarati"
}

LANGUAGE_TO_CODE = {v.lower(): k for k, v in LANGUAGE_NAMES.items()}


def detect_language(text: str) -> str:
    """
    Detect input language.

    Args:
        text: Text to detect language from

    Returns:
        Language code (e.g., 'en', 'hi', 'te')
    """
    if not text or len(text) < 3:
        return "en"

    if LANGDETECT_AVAILABLE:
        try:
            # Get probabilities for all languages
            probs = detect_langs(text)
            # Return the most likely language
            if probs:
                lang = str(probs[0]).split(':')[0]
                # Map to supported languages
                if lang in LANGUAGE_NAMES:
                    return lang
                # If not supported, default to English
                return "en"
        except LangDetectException:
            return "en"
    else:
        # Fallback: simple heuristic based on common words
        text_lower = text.lower()
        if any(word in text_lower for word in ["namaste", "hello", "aap", "kya", "kaise"]):
            return "hi"
        elif any(word in text_lower for word in ["malli", "nuvvu", "vundee", "ekkada"]):
            return "te"

    return "en"


def get_language_name(lang_code: str) -> str:
    """Get full language name from code"""
    return LANGUAGE_NAMES.get(lang_code, "English")


def translate_to_language(text: str, target_lang: str) -> str:
    """
    Translate text to target language.

    Args:
        text: Text to translate
        target_lang: Target language code (e.g., 'hi', 'te')

    Returns:
        Translated text or original if translation fails
    """
    if target_lang == "en":
        return text

    # Try Google Cloud Translation API if available
    if GOOGLE_TRANSLATE_AVAILABLE and os.getenv("GOOGLE_TRANSLATE_API_KEY"):
        try:
            client = translate_v2.Client()
            result = client.translate_text(
                source_language="en",
                target_language=target_lang,
                text=text
            )
            return result["translatedText"]
        except Exception as e:
            print(f"Google Translate error: {e}")

    # Fallback: use googletrans library if available
    try:
        from googletrans import Translator
        translator = Translator()
        translation = translator.translate(text, src_language='en', dest_language=target_lang)
        return translation['text']
    except ImportError:
        print(f"⚠️ Translation libraries not available. Returning original text.")
        return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def translate_and_detect(text: str, target_lang: str = None) -> Tuple[str, str]:
    """
    Detect source language and optionally translate.

    Args:
        text: Text to process
        target_lang: Target language (optional)

    Returns:
        Tuple of (translated_text, detected_language)
    """
    detected_lang = detect_language(text)

    if target_lang and target_lang != detected_lang:
        # Translate if needed
        if detected_lang != "en":
            # First translate to English
            text = translate_to_language(text, "en")
        if target_lang != "en":
            # Then translate to target
            text = translate_to_language(text, target_lang)

    return text, detected_lang


def format_response_multilingual(
    response: Dict,
    target_language: str = "en"
) -> Dict:
    """
    Format response dict for multilingual output.

    Args:
        response: Response dict with explanation, answer, etc.
        target_language: Language to translate to

    Returns:
        Response dict with translated fields
    """
    if target_language == "en":
        return response

    translated = response.copy()

    # Fields to translate
    fields_to_translate = [
        "explanation", "answer", "analogy", "example", "question",
        "feedback"
    ]

    for field in fields_to_translate:
        if field in translated and translated[field]:
            translated[field] = translate_to_language(
                str(translated[field]),
                target_language
            )

    # Translate list items
    if "key_points" in translated and isinstance(translated["key_points"], list):
        translated["key_points"] = [
            translate_to_language(str(point), target_language)
            for point in translated["key_points"]
        ]

    translated["language"] = target_language

    return translated
