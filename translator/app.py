from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from translator import standard_translator, smart_auto_translator
from utils import source_tts_handler, target_tts_handler

app = FastAPI(title="Cortext Translator", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Backend running"}

@app.post("/translate/manual")
async def manual_translate(text: str = Form(...), src_lang: str = Form(...), tgt_lang: str = Form(...)):
    translated = standard_translator(text, src_lang, tgt_lang)
    return {"mode": "manual", "source_text": text, "translated_text": translated}

@app.post("/translate/auto")
async def auto_translate(text: str = Form(...), target_lang: str = Form(...)):
    result = smart_auto_translator(text, target_lang)
    return result


@app.post("/tts/source")
async def source_tts(text: str = Form(...)):
    b64_audio = await source_tts_handler(text)
    if not b64_audio:
        return {"error": "Could not generate audio"}
    return {"audio_base64": b64_audio}

@app.post("/tts/target")
async def target_tts(translated_text: str = Form(...), target_lang: str = Form(...)):
    b64_audio = await target_tts_handler(translated_text, target_lang)
    if not b64_audio:
        return {"error": "Could not generate audio"}
    return {"audio_base64": b64_audio}