import hashlib
from datetime import date
import requests
from typing import Generator, Dict, List, Union
import tkinter as tk
from tkinter import filedialog
import json

def readConfigFile() -> dict:
    """读取配置文件"""
    with open("config.json", 'r', encoding='utf-8') as file:
        config_content = file.read()
    return json.loads(config_content)

class AIApiClient:
    def __init__(self, api_endpoint: str = 'https://ai.coludai.cn/'):
        """
        初始化 AIApiClient 类实例

        Args:
            api_endpoint (str): API 的基础 URL，默认为 'https://ai.coludai.cn/'。
        """
        self.api_endpoint = api_endpoint
        self.config = readConfigFile()
        self.headers = {"ca": self.config["ca"]}

    def md5(self, text: str) -> str:
        """生成字符串的 MD5 哈希值"""
        m = hashlib.md5()
        m.update(text.encode('utf-8'))
        return m.hexdigest()

    def gen_token(self, text: str) -> str:
        """生成基于当前日期和输入文本的 token"""
        now_date = date.today().strftime("%Y-%m-%d")
        date_md5 = self.md5(now_date)[:6]
        return self.md5(text + date_md5)

    def make_request(self, endpoint: str, data: dict, stream: bool = False, download: bool = False, file_key: str = None) -> Union[Dict[str, str], Generator[str, None, None]]:
        """
        通用的请求封装函数

        Args:
            endpoint (str): API 的具体端点（例如 '/api/tts'）。
            data (dict): 要发送的 JSON 数据。
            stream (bool, optional): 是否使用流式请求。默认为 False。
            download (bool, optional): 是否下载响应中的文件（如果存在）。默认为 False。
            file_key (str, optional): 如果要上传文件，请提供文件键名。默认为 None。

        Returns:
            Union[Dict[str, str], Generator[str, None, None]]: 返回 API 响应或生成器（用于流式响应）。
        """
        url = f"{self.api_endpoint}{endpoint}"
        headers = {"ca": self.config["ca"]}

        if file_key:
            files = {file_key: open(data[file_key], "rb")}
            res = requests.post(url, headers=headers, files=files).json()
        else:
            res = requests.post(url, json=data, headers=headers, stream=stream)
            if stream:
                return (line.decode("utf-8") for line in res.iter_lines() if line)
            res = res.json()

        if download:
            file_url = f"{self.api_endpoint}{res['dir']}"
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                file_name = "output" + (".wav" if endpoint == "/api/tts" else ".png")
                with open(file_name, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
        return res

    def stream_chat(self, prompt: str) -> Generator[str, None, None]:
        """流式聊天函数"""
        return self.make_request("/api/chat", data={"prompt": prompt, "token": self.gen_token(prompt), "stream": True})

    def tts(self, text: str, download: bool = False) -> Dict[str, str]:
        """文本转语音函数"""
        return self.make_request("/api/tts", data={"text": text, "token": self.gen_token(text)}, download=download)

    def txt2img(self, text: str, download: bool = False) -> Dict[str, str]:
        """文本转图像函数"""
        return self.make_request("/api/txt2img", data={"text": text, "token": self.gen_token(text)}, download=download)

    def img_desc(self, file_path: str) -> Dict[str, str]:
        """获取图像描述函数"""
        return self.make_request("/api/img_desc", data={"file": file_path}, file_key="file")

    @staticmethod
    def open_files_dialog() -> List[str]:
        """打开文件选择对话框函数"""
        root = tk.Tk()
        root.withdraw()
        files_paths = filedialog.askopenfilenames()
        return list(files_paths)
