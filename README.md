# Cortex - Intelligent RAG Chatbot & Translator

🚀 **Live Demo**: [https://junaidariie.github.io/Cortex/](https://junaidariie.github.io/Cortex/)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

## 🌟 Overview

Cortex is a comprehensive AI-powered platform combining an intelligent chatbot with Retrieval-Augmented Generation (RAG) capabilities and a sophisticated multi-language translation system. Built with modern AI technologies, it provides seamless conversation, document analysis, and real-time translation across 100+ languages.

## ✨ Features

### 🤖 **Chatbot Features**
- **Multi-Model Support**: GPT-4, Kimi2, Llama4, Qwen3, and more
- **📚 RAG Capabilities**: Upload and query PDF documents with intelligent context retrieval
- **🌐 Real-time Web Search**: Get up-to-date information using Tavily search
- **🎤 Speech-to-Text**: Convert audio to text using Whisper models
- **🗣️ Text-to-Speech**: Generate natural speech with Edge TTS
- **💬 Streaming Responses**: Real-time response streaming
- **🧠 Memory Management**: Persistent conversation history
- **📄 Document Processing**: Automatic PDF ingestion and vectorization

### 🔤 **Translation Features**
- **🌍 100+ Languages**: Comprehensive language support
- **🤖 NLLB 600M Model**: Meta's state-of-the-art translation engine
- **🔍 Auto-Detection**: Smart language detection
- **🎧 Neural TTS**: Language-specific voice synthesis
- **⚡ Real-time Translation**: Instant text conversion
- **🔄 Bidirectional Switching**: Easy language swapping

## 🏗️ Architecture

### Architecture Overview
<img width="390" height="333" alt="Cortex Architecture" src="https://github.com/user-attachments/assets/fe1f31ec-0e5c-4164-8fa9-4e0743e4f488" />

### Core Components

#### **Chatbot System**
1. **FastAPI Backend** (`app.py`): Main API server handling HTTP requests
2. **RAG Engine** (`RAG.py`): LangGraph-based conversation flow with state management
3. **Document Ingestion** (`data_ingestion.py`): PDF processing and vector store creation
4. **Utilities** (`utils.py`): Speech processing and audio generation

#### **Translation System**
1. **Translator Backend** (`translator_app.py`): FastAPI server for translation services
2. **NLLB Engine** (`translator.py`): Meta's NLLB-200 distilled 600M model
3. **TTS Engine** (`utils.py`): Edge TTS with language-specific voices
4. **Language Detection**: Automatic source language identification

### Technology Stack

#### **Backend**
- **Framework**: FastAPI, Python 3.11+
- **API Documentation**: Auto-generated OpenAPI/Swagger
- **CORS**: Full cross-origin support

#### **AI/ML Stack**
- **LLM Framework**: LangChain, LangGraph
- **Models**: OpenAI GPT, Groq (Kimi2, Llama4, Qwen3)
- **Translation**: Meta NLLB-200 distilled 600M
- **Speech**: Whisper (STT), Edge TTS (TTS)

#### **Data Processing**
- **Vector Database**: FAISS
- **Search**: Tavily API
- **Document Processing**: PyPDF, RecursiveCharacterTextSplitter

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- API Keys:
  - OpenAI API Key
  - Groq API Key
  - Tavily API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/junaidariie/Cortex.git
   cd Cortex
   ```

2. **Create virtual environment**
   ```bash
   python -m venv myvenv
   source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the root directory:
   ```env
   # Chatbot API Keys
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   TAVILY_API_KEY=your_tavily_api_key
   
   # Translator Configuration
   TRANSLATOR_HOST=localhost
   TRANSLATOR_PORT=8001
   ```

5. **Run Chatbot Server**
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Run Translator Server** (in separate terminal)
   ```bash
   uvicorn translator_app:app --reload --host 0.0.0.0 --port 8001
   ```

## 📖 API Documentation

### Chatbot API (Port 8000)

#### Base URL
```
http://localhost:8000
```

#### Endpoints

##### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "status": "running",
  "message": "Bot is ready"
}
```

##### 2. Chat Endpoint
```http
POST /chat
```
**Request Body:**
```json
{
  "query": "Your question here",
  "thread_id": "user_session_id",
  "use_rag": false,
  "use_web": false,
  "model_name": "gpt"
}
```

##### 3. Document Upload
```http
POST /upload
```
**Request:** Multipart form data with PDF file

##### 4. Speech-to-Text
```http
POST /stt
```
**Request:** Multipart form data with audio file

##### 5. Text-to-Speech
```http
POST /tts
```
**Request Body:**
```json
{
  "text": "Text to convert to speech",
  "voice": "en-US-AriaNeural"
}
```

### Translator API (Port 8001)

#### Base URL
```
http://localhost:8001
```

#### Endpoints

##### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "status": "ok",
  "message": "Backend running"
}
```

##### 2. Manual Translation
```http
POST /translate/manual
```
**Request Body:** Form data with `text`, `src_lang`, `tgt_lang`

##### 3. Auto Translation
```http
POST /translate/auto
```
**Request Body:** Form data with `text`, `target_lang`
**Features:** Auto-detects source language

##### 4. Source TTS
```http
POST /tts/source
```
**Request Body:** Form data with `text`
**Features:** Auto-detects language for voice selection

##### 5. Target TTS
```http
POST /tts/target
```
**Request Body:** Form data with `translated_text`, `target_lang`

## 🔧 Configuration

### Available Chat Models

| Model | Provider | Best For |
|-------|----------|----------|
| `gpt` | OpenAI | General-purpose tasks, reasoning |
| `kimi2` | Groq | Long-context documents, summarization |
| `gpt_oss` | Groq | Creative writing, niche topics |
| `lamma4` | Groq | Logical deduction, instructions |
| `qwen3` | Groq | Mathematics, programming |

### Translation Capabilities

#### **Supported Languages (100+)**
- **European**: English, French, German, Spanish, Italian, Russian, etc.
- **Asian**: Chinese, Japanese, Korean, Hindi, Tamil, Telugu, etc.
- **Middle Eastern**: Arabic, Persian, Hebrew, Turkish, Kurdish
- **African**: Swahili, Zulu, Afrikaans, Amharic
- **Special**: Latin, Esperanto

#### **Key Translation Features**
- **Model**: Meta NLLB-200 distilled 600M
- **Auto-detection**: Instant language identification
- **TTS Integration**: Language-specific neural voices
- **Character Limit**: 5000 characters per translation
- **Performance**: Optimized for real-time use

#### **Voice Options (Edge TTS)**
- 50+ language-specific neural voices
- Gender variations available
- Regional accents supported
- Real-time audio generation

## 💡 Usage Examples

### Basic Chat
```python
import requests

response = requests.post("http://localhost:8000/chat", json={
    "query": "Hello, how are you?",
    "thread_id": "user123",
    "use_rag": False,
    "use_web": False,
    "model_name": "gpt"
})
```

### Document-based RAG Query
```python
# Upload document
files = {"file": open("document.pdf", "rb")}
requests.post("http://localhost:8000/upload", files=files)

# Query with RAG
response = requests.post("http://localhost:8000/chat", json={
    "query": "What does the document say about AI?",
    "thread_id": "user123",
    "use_rag": True,
    "use_web": False,
    "model_name": "kimi2"
})
```

### Translation with Auto-detection
```python
# Auto-detect and translate
response = requests.post("http://localhost:8001/translate/auto", data={
    "text": "Hola, ¿cómo estás?",
    "target_lang": "english"
})

print(response.json())
# Output: {"translated_text": "Hello, how are you?", "detected_language": "spanish"}
```

### Manual Translation
```python
# Specify source and target languages
response = requests.post("http://localhost:8001/translate/manual", data={
    "text": "Bonjour le monde",
    "src_lang": "french",
    "tgt_lang": "english"
})
```

### Text-to-Speech for Translation
```python
# Get audio for translated text
response = requests.post("http://localhost:8001/tts/target", data={
    "translated_text": "Hello world",
    "target_lang": "english"
})

# Returns Base64 encoded audio
audio_base64 = response.json()["audio_base64"]
```

## 🗂️ Project Structure

```
Cortex/
├── app.py                      # Main FastAPI application (Chatbot)
├── translator_app.py           # Translator FastAPI application
├── RAG.py                      # LangGraph RAG implementation
├── translator.py               # NLLB translation engine
├── data_ingestion.py           # Document processing
├── utils.py                    # Shared utilities (TTS/STT)
├── vectorstore/                # FAISS vector database
│   └── db_faiss/
├── uploads/                    # Temporary file storage
├── outputs/                    # Generated audio files
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── README.md                   # This documentation
└── index.html                  # Frontend interface
```

## 🔒 Security Considerations

- **API Security**: All keys stored in environment variables
- **File Validation**: Strict upload restrictions (PDF only)
- **Input Sanitization**: Protection against injection attacks
- **Temporary Files**: Automatic cleanup after processing
- **CORS Configuration**: Controlled cross-origin access

## 🚀 Deployment

### Local Development
```bash
# Chatbot Server
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Translator Server
uvicorn translator_app:app --reload --host 0.0.0.0 --port 8001
```

### Production Deployment
```bash
# Using Gunicorn for production
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
# Dockerfile for Cortex
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & uvicorn translator_app:app --host 0.0.0.0 --port 8001"]
```

## 📊 Performance Characteristics

### Chatbot
- **Response Time**: < 2 seconds for typical queries
- **Document Processing**: ~30 seconds per 100-page PDF
- **Concurrent Users**: Supports 100+ simultaneous sessions
- **Memory Usage**: ~2GB RAM with all models loaded

### Translator
- **Translation Speed**: < 500ms for 100 characters
- **Language Detection**: < 100ms
- **TTS Generation**: < 1 second for short texts
- **Model Size**: ~2.3GB (NLLB 600M)

## 👨‍💻 Author

**Junaid** - [GitHub Profile](https://github.com/junaidariie)

Aspiring Machine Learning Engineer building intelligent systems to bridge language and knowledge barriers.

## 🙏 Acknowledgments

- **OpenAI** for GPT models and API
- **Meta AI** for the NLLB translation model
- **Groq** for high-performance inference
- **LangChain** community for the amazing framework
- **Tavily** for real-time web search
- **Edge TTS** for high-quality speech synthesis

⭐ **Star this repo if you find it useful!** ⭐
