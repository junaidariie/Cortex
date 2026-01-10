import os
import shutil
from fastapi.responses import FileResponse
import asyncio
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from utils import STT, TTS
from data_ingestion import Ingest_Data 
from RAG import app as rag_app, Ragbot_State, reload_vector_store

app = FastAPI(title="LangGraph RAG Chatbot", version="1.0")

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    query: str
    thread_id: str = "default_user"
    use_rag: bool = False
    use_web: bool = False
    model_name: str = "gpt"

class TTSRequest(BaseModel):
    text: str
    voice: str = "en-US-AriaNeural"


# --- Endpoints ---

@app.get("/")
def health_check():
    return {"status": "running", "message": "Bot is ready"}

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...), 
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    try:
        temp_filename = f"temp_{file.filename}"

        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        def process_and_reload(path):
            try:
                result = Ingest_Data(path)
                print(f"Ingestion Result: {result}")
                reload_vector_store()
                
            except Exception as e:
                print(f"Error processing background task: {e}")
            finally:
                if os.path.exists(path):
                    os.remove(path)

        background_tasks.add_task(process_and_reload, temp_filename)

        return {
            "message": "File received. Processing started in background.", 
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Earlier i was using a function which was streaming fine on localhost but wasn't workng once i uploaded it on hf so i switched to non-streaming.
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    
    inputs = {
        "query": request.query,
        "RAG": request.use_rag,
        "web_search": request.use_web,
        "model_name": request.model_name,
        "context": [],
        "metadata": [],
        "web_context": "",
    }

    async def event_generator():
        async for event in rag_app.astream_events(inputs, config=config, version="v1"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                
                if content:
                    data = content.replace("\n", "\\n")
                    yield f"data: {data}\n\n"

    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ---------------- STT ---------------- #
@app.post("/stt")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        return await STT(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------- TTS ---------------- #
@app.post("/tts")
async def text_to_speech(req: TTSRequest):
    try:
        audio_path = await TTS(req.text, req.voice)
        return FileResponse(audio_path, media_type="audio/mpeg", filename="output.mp3")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

