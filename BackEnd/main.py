#STAART OF IMPORTS
import os
import requests

from fastapi import FastAPI, HTTPException, Response, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv

#END OF IMPORTS

app = FastAPI(title="CodeRed Orion API")

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "CodeRed Orion backend is running!"
        
    }

#START OF ELVENLABS LOAD
# Load our secret API key
load_dotenv("keys.env")

# Structure of a message sent by the frontend
class SpeechRequest(BaseModel):
    text: str


@app.post("/speak")
def speak(request: SpeechRequest):

    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ElevenLabs API key not found"
        )

    # Default ElevenLabs voice
    voice_id = "JBFqnCBsd6RMkjVDRZzb"

    url = (
        f"https://api.elevenlabs.io/v1/"
        f"text-to-speech/{voice_id}"
    )

    try:
        response = requests.post(
            url,
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg"
            },
            json={
                "text": request.text,
                "model_id": "eleven_multilingual_v2"
            },
            timeout=30
        )

        response.raise_for_status()

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="ElevenLabs speech generation failed"
        )

    return Response(
        content=response.content,
        media_type="audio/mpeg"
    )
#END OF ELVENLABS LOAD


# START OF SPEECH TO TEXT

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ElevenLabs API key not found"
        )

    if file.content_type not in [
        "audio/mpeg",
        "audio/mp3",
        "audio/wav",
        "audio/x-wav",
        "audio/webm",
        "audio/ogg",
        "audio/mp4"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format"
        )

    audio_data = await file.read()

    if not audio_data:
        raise HTTPException(
            status_code=400,
            detail="Audio file is empty"
        )

    try:
        response = requests.post(
            "https://api.elevenlabs.io/v1/speech-to-text",
            headers={
                "xi-api-key": api_key
            },
            data={
                "model_id": "scribe_v1"
            },
            files={
                "file": (
                    file.filename or "recording.wav",
                    audio_data,
                    file.content_type
                )
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="ElevenLabs transcription failed"
        )

    return {
        "status": "success",
        "transcription": result.get("text", "")
    }

# END OF SPEECH TO TEXT
