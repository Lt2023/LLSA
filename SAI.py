import requests
import hashlib
from datetime import date
import json
from typing import Generator
import tkinter as tk
from tkinter import filedialog
from time import sleep

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

def stream_chat(prompt: str) -> Generator[dict, None, None]:
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
            yield json.loads(line.decode("utf-8"))

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

if __name__ == "__main__":
    while True:
        print('''
SAI 命令列表：
-----------------
1. 聊天
2. 文本转语音
3. 文生图
4. 图片描述
5. 退出
-----------------
''', end="")
        cmd = input("请输入命令序号：")
        match cmd:
            case "1":
                mode = input("是否流式？[y/n]:")
                if mode == "y":
                    while True:
                        print("请输入内容(输入exit退出)")
                        text = input("> ")
                        if text == "exit":
                            break
                        res = stream_chat(text)
                        print("输出：", end="")
                        prev_text = ""
                        for i in res:
                            res_text = i["output"]
                            print(res_text.replace(prev_text, ""), end="", flush=True)
                            prev_text = res_text
                        print()
                else:
                    while True:
                        print("请输入内容(输入exit退出)")
                        text = input("> ")
                        if text == "exit":
                            break
                        res = stream_chat(text)
                        for i in res:
                            res_text = i["output"]
                        print(f"输出：{res_text}")

            case "2":
                text = input("请输入文本：")
                download = input("是否下载？[y/n]:")
                res = tts(text, download == "y")
                print(res)
                if download == "y":
                    print("下载成功！请到./output.wav查看")
                else:
                    print("访问链接:http://ai.coludai.cn" + res["dir"])
                sleep(5)

            case "3":
                text = input("请输入文本：")
                download = input("是否下载？[y/n]:")
                res = txt2img(text, download == "y")
                print(res)
                if download == "y":
                    print("下载成功！请到./output.png查看")
                else:
                    print("访问链接:http://ai.coludai.cn" + res["dir"])
                sleep(5)
            
            case "4":
                input("请选择一张图片,回车继续")
                files_path = open_files_dialog()[0]
                res = img_desc(files_path)
                print(res)
                sleep(5)
            
            case "5":
                exit()
            
            case _:
                print("无效命令")
                sleep(5)
