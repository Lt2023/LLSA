import requests

# res = requests.post("http://127.0.0.1:8000/api/chat", json={"input": "你好"}, timeout=600)

res = requests.post("http://127.0.0.1:8000/api/tts", json={"text": ''' 潜力无限，塑造ColudAI'''})
print(res.json())

