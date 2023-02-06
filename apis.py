import uuid

from chatgpt import Chatbot
from conf import conf_reader

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


# request body
class Request(BaseModel):
    uid: str
    text: str


app = FastAPI()

chatbots = {str: Chatbot}


def genchatbot():
    uid = str(uuid.uuid1())
    bot = Chatbot(api_key=conf_reader())
    chatbots[uid] = bot
    return uid


def getanswer(req: Request):
    try:
        bot = chatbots[req.uid]
    except Exception:
        return "failed"
    response = bot.ask(req.text)
    return response["choices"][0]["text"]


@app.get("/")
def start():
    uid = genchatbot()
    return uid


@app.post("/chat")
async def chat(req: Request):
    return {
        "result": 0,
        "answer": getanswer(req)
    }


def launch():
    uvicorn.run(app="apis:app", host="127.0.0.1", port=8888, reload=True)
