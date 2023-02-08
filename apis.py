import uuid

from chatgpt import Chatbot
from conf import conf_reader

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


# request body
class Request(BaseModel):
    uid: str
    text: str


app = FastAPI()

'''
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''


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
    response = bot.ask_stream(req.text)
    # return response["choices"][0]["text"]
    return response


@app.get("/api")
def start():
    uid = genchatbot()
    return uid


@app.post("/api/chat")
async def chat(req: Request):
    res = getanswer(req)
    response = ""
    for word in res:
        print(word, end="")
        response += word
    print("\n")
    return {
        "result": 0,
        "answer": response
    }


def launch():
    uvicorn.run(app="apis:app", host="127.0.0.1", port=8888, reload=True)
