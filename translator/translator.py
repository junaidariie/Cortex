# translator.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from langdetect import detect

MODEL_NAME = "facebook/nllb-200-distilled-600M"

# ===============================
# LANGUAGE MAP
# ===============================
LANGUAGE_MAP = {
    "english": "eng_Latn", "french": "fra_Latn", "german": "deu_Latn", "spanish": "spa_Latn",
    "hindi": "hin_Deva", "marathi": "mar_Deva", "tamil": "tam_Taml", "telugu": "tel_Telu",
    "kannada": "kan_Knda", "bengali": "ben_Beng", "urdu": "urd_Arab", "arabic": "arb_Arab",
    "persian": "pes_Arab", "japanese": "jpn_Jpan", "chinese": "zho_Hans", "korean": "kor_Hang",
    "russian": "rus_Cyrl", "italian": "ita_Latn", "portuguese": "por_Latn", "dutch": "nld_Latn",
    "swedish": "swe_Latn", "norwegian": "nob_Latn", "danish": "dan_Latn", "finnish": "fin_Latn",
    "polish": "pol_Latn", "czech": "ces_Latn", "slovak": "slk_Latn", "hungarian": "hun_Latn",
    "romanian": "ron_Latn", "bulgarian": "bul_Cyrl", "ukrainian": "ukr_Cyrl", "greek": "ell_Grek",
    "gujarati": "guj_Gujr", "punjabi": "pan_Guru", "malayalam": "mal_Mlym",
    "thai": "tha_Thai", "vietnamese": "vie_Latn", "indonesian": "ind_Latn",
    "turkish": "tur_Latn", "hebrew": "heb_Hebr",
    "kurdish_kurmanji": "kmr_Latn",
    "kurdish_sorani": "ckb_Arab",
    "nepali": "npi_Deva",
    "sinhala": "sin_Sinh",
    "odia": "ory_Orya",
    "assamese": "asm_Beng",
    "maithili": "mai_Deva",
    "santali": "sat_Olck",
    "malay": "zsm_Latn",
    "filipino": "tgl_Latn",
    "khmer": "khm_Khmr",
    "lao": "lao_Laoo",
    "burmese": "mya_Mymr",
    "traditional_chinese": "zho_Hant",
    "mongolian": "mon_Cyrl",
    "kazakh": "kaz_Cyrl",
    "uzbek": "uzn_Latn",
    "tajik": "tgk_Cyrl",
    "kyrgyz": "kir_Cyrl",
    "turkmen": "tuk_Latn",
    "pashto": "pbt_Arab",
    "sindhi": "snd_Arab",
    "swahili": "swh_Latn",
    "amharic": "amh_Ethi",
    "yoruba": "yor_Latn",
    "igbo": "ibo_Latn",
    "hausa": "hau_Latn",
    "zulu": "zul_Latn",
    "xhosa": "xho_Latn",
    "somali": "som_Latn",
    "afrikaans": "afr_Latn",
    "estonian": "est_Latn",
    "latvian": "lav_Latn",
    "lithuanian": "lit_Latn",
    "icelandic": "isl_Latn",
    "irish": "gle_Latn",
    "welsh": "cym_Latn",
    "albanian": "sqi_Latn",
    "serbian": "srp_Cyrl",
    "croatian": "hrv_Latn",
    "slovenian": "slv_Latn",
    "latin": "lat_Latn",
    "esperanto": "epo_Latn"
}

ISO_TO_LANGUAGE_KEY = {
    "en": "english", "fr": "french", "de": "german", "es": "spanish", "hi": "hindi",
    "mr": "marathi", "ta": "tamil", "te": "telugu", "kn": "kannada", "bn": "bengali",
    "ur": "urdu", "ar": "arabic", "fa": "persian", "ja": "japanese", "zh": "chinese",
    "ko": "korean", "ru": "russian", "it": "italian", "pt": "portuguese", "nl": "dutch",
    "sv": "swedish", "no": "norwegian", "da": "danish", "fi": "finnish", "pl": "polish",
    "cs": "czech", "sk": "slovak", "hu": "hungarian", "ro": "romanian", "bg": "bulgarian",
    "uk": "ukrainian", "el": "greek", "gu": "gujarati", "pa": "punjabi", "ml": "malayalam",
    "th": "thai", "vi": "vietnamese", "id": "indonesian", "tr": "turkish", "he": "hebrew",
    "ku": "kurdish_kurmanji",
    "ckb": "kurdish_sorani",
    "ne": "nepali",
    "si": "sinhala",
    "or": "odia",
    "as": "assamese",
    "mai": "maithili",
    "sat": "santali",
    "ms": "malay",
    "tl": "filipino",
    "km": "khmer",
    "lo": "lao",
    "my": "burmese",
    "kk": "kazakh",
    "uz": "uzbek",
    "tg": "tajik",
    "ky": "kyrgyz",
    "tk": "turkmen",
    "ps": "pashto",
    "sd": "sindhi",
    "sw": "swahili",
    "am": "amharic",
    "yo": "yoruba",
    "ig": "igbo",
    "ha": "hausa",
    "zu": "zulu",
    "xh": "xhosa",
    "so": "somali",
    "af": "afrikaans",
    "et": "estonian",
    "lv": "latvian",
    "lt": "lithuanian",
    "is": "icelandic",
    "ga": "irish",
    "cy": "welsh",
    "sq": "albanian",
    "sr": "serbian",
    "hr": "croatian",
    "sl": "slovenian",
    "la": "latin",
    "eo": "esperanto"
}


# ===============================
# LOAD MODEL ONCE
# ===============================
print("Loading translation model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
print("Model loaded successfully.")

# ===============================
# HELPERS
# ===============================
def get_nllb_code(lang: str):
    lang = lang.lower().strip()

    if lang in LANGUAGE_MAP:
        return LANGUAGE_MAP[lang]

    if lang in ISO_TO_LANGUAGE_KEY:
        key = ISO_TO_LANGUAGE_KEY[lang]
        return LANGUAGE_MAP[key]

    return "eng_Latn"


# ===============================
# MANUAL TRANSLATOR
# ===============================
def standard_translator(text: str, src_lang: str, tgt_lang: str) -> str:
    src_code = get_nllb_code(src_lang)
    tgt_code = get_nllb_code(tgt_lang)

    tokenizer.src_lang = src_code
    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_code),
            max_length=512
        )

    return tokenizer.decode(output[0], skip_special_tokens=True)


# ===============================
# AUTO TRANSLATOR
# ===============================
def smart_auto_translator(text: str, target_lang: str):
    detected_iso = detect(text)
    detected_lang_key = ISO_TO_LANGUAGE_KEY.get(detected_iso, detected_iso)

    src_code = get_nllb_code(detected_iso)
    tgt_code = get_nllb_code(target_lang)

    tokenizer.src_lang = src_code
    inputs = tokenizer(text, return_tensors="pt")

    with torch.no_grad():
        output = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(tgt_code),
            max_length=512
        )

    translated_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return {
        "translated_text": translated_text,
        "detected_iso": detected_iso,
        "detected_language": detected_lang_key
    }

