from fastapi import FastAPI
from pydantic import BaseModel
from chatGPT import get_chatgpt_response

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    chatgpt_response = get_chatgpt_response(chat_request.message)
    return {"response": chatgpt_response}
