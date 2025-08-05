"""Language detection service"""

from typing import Dict, Any
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from app.config import LANGUAGE_NAMES, logger

# Ensure consistent language detection results
DetectorFactory.seed = 0


class LanguageDetectionService:
    """Service for language detection"""

    @staticmethod
    def detect_language(text: str) -> Dict[str, Any]:
        """Detects language of the given text"""
        try:
            if not text or len(text.strip()) < 3:
                return {
                    "language_code": "unknown",
                    "language_name": "Unknown",
                    "confidence": 0.0,
                }

            detected_lang = detect(text)
            language_name = LANGUAGE_NAMES.get(detected_lang, detected_lang.upper())

            return {
                "language_code": detected_lang,
                "language_name": language_name,
                "confidence": 0.99,  # langdetect doesn't provide confidence scores
            }
        except LangDetectException as e:
            logger.warning(f"Error during language detection: {str(e)}")
            return {
                "language_code": "unknown",
                "language_name": "Unknown",
                "confidence": 0.0,
            }

    @staticmethod
    def get_supported_languages() -> Dict[str, str]:
        """Returns list of supported languages"""
        return LANGUAGE_NAMES
