#STAART OF IMPORTS
import os
import requests
from google import genai

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


# START OF GEMINI PHRASE SUGGESTIONS

class SuggestionRequest(BaseModel):
    text: str


@app.post("/suggest")
def suggest(request: SuggestionRequest):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not found"
        )

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a phrase"
        )

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=(
                "You are helping someone use an AAC communication app. "
                "The user has entered a partial phrase. "
                "Suggest exactly three short, natural, first-person "
                "sentences that could complete their phrase. "
                "Preserve the user's original meaning when possible. "
                "Do not assume a disability, emotion, or personal situation. "
                "Return ONLY the three suggestions, one per line, "
                "without numbering or explanations.\n\n"
                f"Partial phrase: {request.text}"
            )
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="Gemini returned no suggestions"
            )

        suggestions = [
            line.strip().lstrip("123.-) ")
            for line in response.text.splitlines()
            if line.strip()
        ]

        return {
            "status": "success",
            "original_text": request.text,
            "suggestions": suggestions[:3]
        }
    except HTTPException:
        raise
    except Exception as e:
        print("GEMINI ERROR:", repr(e))
        raise HTTPException(
            status_code=502,
            detail="Gemini suggestion generation failed"
        )

# END OF GEMINI PHRASE SUGGESTIONS
