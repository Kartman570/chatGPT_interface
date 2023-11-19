from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel, Field
from chatGPT import get_chatgpt_response, OPENAI_API_KEY

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
import io
from fastapi import UploadFile


OPENAI_API_BASE_URL = "https://api.openai.com/v1"
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

conversation_log = [{"role": "system", "content": "You are an AI assistant. Keep your answers simple and short"}]


class ChatRequest(BaseModel):
    message: str


@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    if len(conversation_log) > 10:
        del conversation_log[1:3]
    conversation_log.append({"role": "user", "content": chat_request.message})
    chatgpt_response = get_chatgpt_response(conversation_log)
    conversation_log.append({"role": "assistant", "content": chatgpt_response})
    return {"response": chatgpt_response}


@app.get("/chat_dialogue/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})


class OpenAIRequest(BaseModel):
    data: dict = Field(default_factory=dict)
    headers: dict = Field(default_factory=dict)


@app.api_route("/api/{path:path}", methods=["POST"])
async def proxy_to_openai(path: str, request_body: OpenAIRequest):
    async with httpx.AsyncClient() as client:
        try:
            full_url = f"{OPENAI_API_BASE_URL}/{path}"

            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
            headers.update(request_body.headers)

            response = await client.post(full_url, json=request_body.data, headers=headers)

            return JSONResponse(status_code=response.status_code, content=response.json())
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))


@app.post("/audio/speech/")
async def create_speech(input: str, model: str = "tts-1", voice: str = "alloy", response_format: str = "mp3", speed: float = 1.0):
    data = {
        "model": model,
        "input": input,
        "voice": voice,
        "response_format": response_format,
        "speed": speed
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{OPENAI_API_BASE_URL}/audio/speech", json=data, headers=headers)

        if response.status_code == 200:
            return StreamingResponse(io.BytesIO(response.content), media_type=f"audio/{response_format}")
        else:
            return Response(content=response.text, status_code=response.status_code)


@app.post("/audio/transcriptions/")
async def create_transcription(file: UploadFile, model: str = "whisper-1", language: str = None, prompt: str = None,
                               response_format: str = "json", temperature: float = 0.0):
    files = {"file": (file.filename, await file.read())}
    data = {
        "model": model,
        "language": language,
        "prompt": prompt,
        "response_format": response_format,
        "temperature": temperature
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{OPENAI_API_BASE_URL}/audio/transcriptions", files=files, data=data,
                                     headers=headers)

        return JSONResponse(status_code=response.status_code, content=response.json())


@app.post("/audio/translations/")
async def create_translation(file: UploadFile, model: str = "whisper-1", prompt: str = None,
                             response_format: str = "json", temperature: float = 0.0):
    files = {"file": (file.filename, await file.read())}
    data = {
        "model": model,
        "prompt": prompt,
        "response_format": response_format,
        "temperature": temperature
    }
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{OPENAI_API_BASE_URL}/audio/translations", files=files, data=data,
                                     headers=headers)

        return JSONResponse(status_code=response.status_code, content=response.json())
