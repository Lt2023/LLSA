from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
from client import AIApiClient

# FastAPI 应用实例
app = FastAPI()

# 请求体定义
class ChatRequest(BaseModel):
    prompt: str

class TTSRequest(BaseModel):
    text: str
    download: bool = False

class TextToImageRequest(BaseModel):
    text: str
    download: bool = False

# 初始化 AIApiClient
ai_client = AIApiClient()

@app.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(ai_client.stream_chat(request.prompt))

@app.post("/tts")
async def text_to_speech(request: TTSRequest) -> JSONResponse:
    return JSONResponse(ai_client.tts(request.text, request.download))

@app.post("/txt2img")
async def text_to_image(request: TextToImageRequest) -> JSONResponse:
    return JSONResponse(ai_client.txt2img(request.text, request.download))

@app.post("/img_desc")
async def image_description(file: UploadFile = File()) -> JSONResponse:
    file_path = file.filename
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    return JSONResponse(ai_client.img_desc(file_path))


def logoPrint():
    logo = '''   ____           _               _      _      ___ 
  / ___|   ___   | |  _   _    __| |    / \\    |_ _|
 | |      / _ \\  | | | | | |  / _` |   / _ \\    | | 
 | |___  | (_) | | | | |_| | | (_| |  / ___ \\   | | 
  \\____|  \\___/  |_|  \\__,_|  \\__,_| /_/   \\_\\ |___|'''
    print(logo)


if __name__ == "__main__":
    logoPrint()
    config = ai_client.config
    uvicorn.run(app, host="0.0.0.0", port=config["Port"])
