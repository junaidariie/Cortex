import os
from uuid import uuid4
import edge_tts
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

# ==================================================
# 🎧 SPEECH TO TEXT
# ==================================================

async def STT(audio_file):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{uuid4().hex}.wav"

    with open(file_path, "wb") as f:
        f.write(await audio_file.read())

    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
            temperature=0.0
        )
    
    # Optional: cleanup the uploaded file after processing
    # os.remove(file_path)

    return {
        "text": transcription.text,
        "segments": transcription.segments,
        "language": transcription.language
    }


# ==================================================
# 🗣️ TEXT TO SPEECH
# ==================================================

async def TTS(text: str, voice: str = "en-US-AriaNeural") -> str:
    """
    Converts text to speech and saves it to a file.
    Returns the path to the generated audio file.
    """
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/{uuid4().hex}.mp3"
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)
    
    return filename