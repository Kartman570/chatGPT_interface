from fastapi import FastAPI, Request
from pydantic import BaseModel
from chatGPT import get_chatgpt_response

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
