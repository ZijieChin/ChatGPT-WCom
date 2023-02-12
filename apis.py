import datetime
import uuid

import requests

from chatgpt import Chatbot
from conf import conf_reader

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from loguru import logger


# request body
class Request(BaseModel):
    uid: str
    text: str
    user: str


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chatbots = {str: Chatbot}

global access_token
access_token = {"access_token": "", "expires": datetime.datetime.now()}


def genchatbot():
    uid = str(uuid.uuid1())
    bot = Chatbot(api_key=conf_reader()["openai_key"])
    chatbots[uid] = bot
    return uid


def getanswer(req: Request):
    logger.info(f"{req.user} ASK: {req.text}")
    try:
        bot = chatbots[req.uid]
    except Exception:
        return "校验失败，请刷新页面后重试。"
    response = bot.ask_stream(req.text)
    # return response["choices"][0]["text"]
    return response


# get access token from wxwork
def get_access_token():
    global access_token
    accesstokenapi = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"  # method: get
    params = {"corpid": conf_reader()["corpid"], "corpsecret": conf_reader()["corpsecret"]}
    response = requests.get(accesstokenapi, params=params)
    access_token = {"access_token": response.json()["access_token"],
                    "expires": datetime.datetime.now() + datetime.timedelta(seconds=response.json()["expires_in"])}
    logger.info(f"Get ACCESS_TOKEN: {access_token}")


@app.get("/api")
def start():
    uid = genchatbot()
    return uid


@app.post("/api/chat")
async def chat(req: Request):
    res = getanswer(req)
    response = ""
    for word in res:
        response += word
    response = response.replace("<|im_end|>", "").strip()
    logger.info(f"ANSWER: {response}")
    return {
        "result": 0,
        "answer": response
    }


@app.get("/api/userinfo")
def userinfo(code: str):
    getuserapi = "https://oa.app.swirecocacola.com/OAuth/Work/GetUserId"  # method: get
    getuserinfoapi = "https://qyapi.weixin.qq.com/cgi-bin/user/get"  # method: get
    userid = ""
    responseid = requests.get(getuserapi, params={"code": code})
    if responseid.status_code != 200:
        return {
            "result": 1,
        }
    else:
        userid = responseid.json()["UserId"]
    if datetime.datetime.now() > access_token["expires"]:
        get_access_token()
    responseinfo = requests.get(getuserinfoapi, params={"access_token": access_token["access_token"], "userid": userid})
    if responseinfo.status_code != 200:
        return {
            "result": 1,
        }
    else:
        return {
            "result": 0,
            "avatar": responseinfo.json()["avatar"],
            "id": responseinfo.json()["userid"],
            "uid": genchatbot(),
        }


def launch():
    uvicorn.run(app="apis:app", host="127.0.0.1", port=8888, reload=True)
