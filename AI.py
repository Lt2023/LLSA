import requests
import hashlib
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from datetime import date
import json
from typing import Generator
import tkinter as tk
from tkinter import filedialog
import uvicorn


# md5加密
def md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()

def gen_token(text):
    # 获取日期
    now_date = date.today().strftime("%Y-%m-%d")
    date_md5 = md5(now_date)[:6]
    return md5(text + date_md5)

def stream_chat(prompt: str) -> Generator[str, None, None]:
    res = requests.post(
        url="https://ai.coludai.cn/api/chat",
        json={
            "prompt": prompt,
            "token": gen_token(prompt),
            "stream": True
        },
        headers={
            "ca": ""
        },
        stream=True
    )
    for line in res.iter_lines():
        if line:
            (line.decode("utf-8"))

def tts(text: str, download: bool = False) -> dict:
    res = requests.post(
        url="https://ai.coludai.cn/api/tts",
        json={
            "text": text,
            "token": gen_token(text),
        },
        headers={
            "ca": ""
        }
    ).json()
    if download:
        with requests.get("http://ai.coludai.cn"+res["dir"], stream=True) as r:
            r.raise_for_status()
            with open("output.wav", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)
    return res

def txt2img(text: str, download: bool = False) -> dict:
    res = requests.post(
        url="https://ai.coludai.cn/api/txt2img",
        json={
            "text": text,
            "token": gen_token(text),
        },
        headers={
            "ca": ""
        }
    ).json()
    if download:
        file =requests.get("http://ai.coludai.cn" + res["dir"])
        with open("output.png", "wb") as f:
            f.write(file.content)
    return res

def open_files_dialog():
    root = tk.Tk()
    root.withdraw()
    files_paths = filedialog.askopenfilenames()
    return files_paths

def img_desc(file_path: str):
    res = requests.post(
        url="https://ai.coludai.cn/api/img_desc",
        headers={
            "ca": ""
        },
        files={
            "file": open(file_path, "rb")
        }
    ).json()
    return res

app = FastAPI()

# ... (保留原有的md5, gen_token, 等函数定义)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(stream_chat(request.prompt))

class TTSRequest(BaseModel):
    text: str
    download: bool = False

@app.post("/tts")
async def text_to_speech(request: TTSRequest) -> JSONResponse:
    return JSONResponse(tts(request.text, request.download))

class TextToImageRequest(BaseModel):
    text: str
    download: bool = False

@app.post("/txt2img")
async def text_to_image(request: TextToImageRequest) -> JSONResponse:
    return JSONResponse(txt2img(request.text, request.download))

@app.post("/img_desc")
async def image_description(file: UploadFile = File()) -> JSONResponse:
    file_path = file.filename
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    return JSONResponse(img_desc(file_path))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)