# ===============================
# VOICE MAP
# ===============================
VOICE_MAP = {
    # ===== EXISTING (UNCHANGED) =====
    "english": "en-US-AriaNeural",
    "french": "fr-FR-DeniseNeural",
    "german": "de-DE-KatjaNeural",
    "spanish": "es-ES-ElviraNeural",
    "hindi": "hi-IN-SwaraNeural",
    "arabic": "ar-SA-ZariyahNeural",
    "japanese": "ja-JP-NanamiNeural",
    "korean": "ko-KR-SunHiNeural",
    "chinese": "zh-CN-XiaoxiaoNeural",
    "russian": "ru-RU-SvetlanaNeural",
    "marathi": "mr-IN-AarohiNeural",
    "tamil": "ta-IN-PallaviNeural",
    "telugu": "te-IN-ShrutiNeural",
    "kannada": "kn-IN-SapnaNeural",
    "bengali": "bn-IN-TanishaaNeural",
    "urdu": "ur-PK-UzmaNeural",
    "gujarati": "gu-IN-DhwaniNeural",
    "punjabi": "pa-IN-GurpreetNeural",
    "malayalam": "ml-IN-SobhanaNeural",
    "italian": "it-IT-ElsaNeural",
    "portuguese": "pt-PT-RaquelNeural",
    "dutch": "nl-NL-ColetteNeural",
    "swedish": "sv-SE-SofieNeural",
    "norwegian": "nb-NO-IselinNeural",
    "danish": "da-DK-ChristelNeural",
    "finnish": "fi-FI-NooraNeural",
    "polish": "pl-PL-ZofiaNeural",
    "czech": "cs-CZ-VlastaNeural",
    "slovak": "sk-SK-ViktoriaNeural",
    "hungarian": "hu-HU-NoemiNeural",
    "romanian": "ro-RO-AlinaNeural",
    "bulgarian": "bg-BG-KalinaNeural",
    "ukrainian": "uk-UA-PolinaNeural",
    "greek": "el-GR-AthinaNeural",
    "thai": "th-TH-PremwadeeNeural",
    "vietnamese": "vi-VN-HoaiMyNeural",
    "indonesian": "id-ID-GadisNeural",
    "turkish": "tr-TR-EmelNeural",
    "hebrew": "he-IL-HilaNeural",

    # ===== NEW – Edge TTS Supported =====

    # South Asia
    "nepali": "ne-NP-HemkalaNeural",
    "sinhala": "si-LK-ThiliniNeural",

    # Southeast Asia
    "malay": "ms-MY-YasminNeural",
    "filipino": "fil-PH-BlessicaNeural",
    "khmer": "km-KH-SreymomNeural",
    "lao": "lo-LA-KeomanyNeural",
    "burmese": "my-MM-NilarNeural",

    # Central Asia
    "kazakh": "kk-KZ-AigulNeural",
    "uzbek": "uz-UZ-MadinaNeural",

    # Africa
    "swahili": "sw-KE-ZuriNeural",
    "amharic": "am-ET-MekdesNeural",
    "zulu": "zu-ZA-ThandoNeural",
    "xhosa": "xh-ZA-NolwaziNeural",
    "afrikaans": "af-ZA-AdriNeural",

    # Middle East
    "azerbaijani": "az-AZ-BanuNeural",
    "persian": "fa-IR-DilaraNeural",

    # Europe Extra
    "estonian": "et-EE-AnuNeural",
    "latvian": "lv-LV-NeveraNeural",
    "lithuanian": "lt-LT-OnaNeural",
    "icelandic": "is-IS-GudrunNeural",
    "irish": "ga-IE-OrlaNeural",
    "welsh": "cy-GB-NiaNeural",
    "albanian": "sq-AL-AnilaNeural",
    "serbian": "sr-RS-SophieNeural",
    "croatian": "hr-HR-GabrijelaNeural",
    "slovenian": "sl-SI-PetraNeural"
}
ISO_TO_LANGUAGE_KEY = {
    # ===== EXISTING =====
    "en": "english", "fr": "french", "de": "german", "es": "spanish", "hi": "hindi",
    "mr": "marathi", "ta": "tamil", "te": "telugu", "kn": "kannada", "bn": "bengali",
    "ur": "urdu", "ar": "arabic", "fa": "persian", "ja": "japanese", "zh": "chinese",
    "ko": "korean", "ru": "russian", "it": "italian", "pt": "portuguese", "nl": "dutch",
    "sv": "swedish", "no": "norwegian", "da": "danish", "fi": "finnish", "pl": "polish",
    "cs": "czech", "sk": "slovak", "hu": "hungarian", "ro": "romanian", "bg": "bulgarian",
    "uk": "ukrainian", "el": "greek", "gu": "gujarati", "pa": "punjabi", "ml": "malayalam",
    "th": "thai", "vi": "vietnamese", "id": "indonesian", "tr": "turkish", "he": "hebrew",

    # ===== NEW =====
    "ne": "nepali",
    "si": "sinhala",
    "ms": "malay",
    "tl": "filipino",
    "km": "khmer",
    "lo": "lao",
    "my": "burmese",
    "kk": "kazakh",
    "uz": "uzbek",
    "sw": "swahili",
    "am": "amharic",
    "zu": "zulu",
    "xh": "xhosa",
    "af": "afrikaans",
    "az": "azerbaijani",
    "et": "estonian",
    "lv": "latvian",
    "lt": "lithuanian",
    "is": "icelandic",
    "ga": "irish",
    "cy": "welsh",
    "sq": "albanian",
    "sr": "serbian",
    "hr": "croatian",
    "sl": "slovenian"
}


import os
import time
from uuid import uuid4
import edge_tts
from langdetect import detect, LangDetectException
from groq import Groq
from dotenv import load_dotenv
import base64

load_dotenv()
client = Groq()

# ===============================
# CONFIGURATION
# ===============================
STATIC_DIR = "static"
DELETE_AFTER_SECONDS = 300 

# ===============================
# MEMORY TTS (Base64)
# ===============================
async def TTS(text: str, voice: str):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    b64_string = base64.b64encode(audio_data).decode('utf-8')
    return b64_string

# ===============================
# HANDLERS
# ===============================
async def source_tts_handler(text: str):
    if not text or not text.strip():
        return None
    try:
        iso = detect(text)
        lang_key = ISO_TO_LANGUAGE_KEY.get(iso, "english")
        voice = VOICE_MAP.get(lang_key, "en-US-AriaNeural")
    except LangDetectException:
        voice = "en-US-AriaNeural"

    return await TTS(text, voice)

async def target_tts_handler(text: str, target_lang: str):
    if not text:
        return None
    clean_lang = target_lang.lower().strip()
    voice = VOICE_MAP.get(clean_lang, "en-US-AriaNeural")
    return await TTS(text, voice)