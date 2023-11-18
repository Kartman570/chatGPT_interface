from fastapi import FastAPI, Request
from pydantic import BaseModel
from chatGPT import get_chatgpt_response

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str


@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    chatgpt_response = get_chatgpt_response(chat_request.message)
    return {"response": chatgpt_response}

@app.get("/chat_dialogue/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("item.html", {"request": request})
