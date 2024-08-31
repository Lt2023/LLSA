from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from datetime import date
import hashlib
import requests
import tkinter as tk
from tkinter import filedialog
import uvicorn
from typing import Generator, List, Dict, Union
import json


class AIApiClient:
    """AI API 客户端"""

    def __init__(self, config_path: str = "config.json", api_endpoint: str = 'https://ai.coludai.cn/'):
        self.api_endpoint = api_endpoint
        self.config = self._read_config_file(config_path)

    def _read_config_file(self, config_path: str) -> Dict[str, Union[str, int]]:
        """读取配置文件"""
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.loads(file.read())

    @staticmethod
    def _md5(text: str) -> str:
        """生成字符串的 MD5 哈希值"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def _gen_token(self, text: str) -> str:
        """生成基于当前日期和输入文本的 token"""
        now_date = date.today().strftime("%Y-%m-%d")
        date_md5 = self._md5(now_date)[:6]
        return self._md5(text + date_md5)

    def _make_request(self, endpoint: str, data: dict, headers: Dict[str, str] = None, download: bool = False, file_key: str = None) -> Union[Dict[str, str], Generator[str, None, None]]:
        """
        通用的请求封装函数

        Args:
            endpoint (str): API 的具体端点（例如 '/api/tts'）。
            data (dict): 要发送的 JSON 数据。
            headers (dict, optional): 请求头。会自动包含或覆盖 "ca" 参数。默认为 None。
            download (bool, optional): 是否下载响应中的文件（如果存在）。默认为 False。
            file_key (str, optional): 如果要上传文件，请提供文件键名。默认为 None。

        Returns:
            Union[Dict[str, str], Generator[str, None, None]]: 返回 API 响应或生成器（用于流式响应）。
        """
        headers = headers or {}
        headers["ca"] = self.config["ca"]

        url = f"{self.api_endpoint}{endpoint}"
        if file_key:
            files = {file_key: open(data[file_key], "rb")}
            res = requests.post(url, headers=headers, files=files).json()
        else:
            res = requests.post(url, json=data, headers=headers, stream=data.get("stream", False))
            if data.get("stream"):
                return (line.decode("utf-8") for line in res.iter_lines() if line)
            res = res.json()

        if download:
            self._download_file(res, endpoint)

        return res

    def _download_file(self, response: Dict[str, str], endpoint: str):
        """下载文件"""
        file_url = f"{self.api_endpoint}{response['dir']}"
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            file_name = "output" + (".wav" if endpoint == "/api/tts" else ".png")
            with open(file_name, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

    def stream_chat(self, prompt: str) -> Generator[str, None, None]:
        """流式聊天函数"""
        return self._make_request("/api/chat", data={"prompt": prompt, "token": self._gen_token(prompt), "stream": True})

    def tts(self, text: str, download: bool = False) -> Dict[str, str]:
        """文本转语音函数"""
        return self._make_request("/api/tts", data={"text": text, "token": self._gen_token(text)}, download=download)

    def txt2img(self, text: str, download: bool = False) -> Dict[str, str]:
        """文本转图像函数"""
        return self._make_request("/api/txt2img", data={"text": text, "token": self._gen_token(text)}, download=download)

    def img_desc(self, file_path: str) -> Dict[str, str]:
        """获取图像描述函数"""
        return self._make_request("/api/img_desc", data={"file": file_path}, file_key="file")

    def open_files_dialog(self) -> List[str]:
        """打开文件选择对话框函数"""
        root = tk.Tk()
        root.withdraw()
        files_paths = filedialog.askopenfilenames()
        return list(files_paths)

    def logo_print(self):
        """打印程序Logo"""
        logo = (
            "   ____           _               _      _      ___ \n"
            "  / ___|   ___   | |  _   _    __| |    / \\    |_ _|\n"
            " | |      / _ \\  | | | | | |  / _` |   / _ \\    | | \n"
            " | |___  | (_) | | | | |_| | | (_| |  / ___ \\   | | \n"
            "  \\____|  \\___/  |_|  \\__,_|  \\__,_| /_/   \\_\\ |___|\n"
        )
        print(logo)


# 创建FastAPI应用实例
app = FastAPI()

class ChatRequest(BaseModel):
    prompt: str

class TTSRequest(BaseModel):
    text: str
    download: bool = False

class TextToImageRequest(BaseModel):
    text: str
    download: bool = False

# 初始化AIApiClient对象
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


if __name__ == "__main__":
    ai_client.logo_print()
    uvicorn.run(app, host="0.0.0.0", port=ai_client.config["Port"])
