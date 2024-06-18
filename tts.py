from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import flask
import random
import string
import os
import config
import time
import threading

app = flask.Flask(__name__)

lock = threading.Lock()

output_config = config.Config("./output_data.json")

def generate_random_string_simple(length):
    """生成一个指定长度的随机字符串（非安全场景）"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

model_id = "/home/SAI/model/sai-tts"
sambert_hifigan_tts = pipeline(task=Tasks.text_to_speech, model=model_id)

@app.route('/api/tts', methods=['POST'])
def tts():
    text = flask.request.json['text']
    output = sambert_hifigan_tts(input=text)
    wav = output[OutputKeys.OUTPUT_WAV]
    file_name = generate_random_string_simple(8) 

    with open(f'./outputs/{file_name}.wav', 'wb') as f:
        f.write(wav)

    # 设置到期时间
    add_expire_and_path(int(round(time.time() * 1000)) + 1000 * 60 * 10, f'./outputs/{file_name}.wav')

    return flask.jsonify({'status': 'success', 'dir': f'/api/outputs/{file_name}.wav'})

@app.route('/api/outputs/<path:path>')
def get_output(path):
    return flask.send_from_directory("./outputs", path, as_attachment=True)

def add_expire_and_path(expire_time, path):
    with lock:
        item = {"path": path, "expire_time": expire_time}
        output_config["expire_at"].append(item)
        output_config.save()

def check_expire():
    while True:
        with lock:
            for i in output_config["expire_at"]:
                if i["expire_time"] < int(round(time.time() * 1000)):
                    os.remove(i["path"])
                    output_config["expire_at"].remove(i)
                    output_config.save()
        time.sleep(10)

# 启动子线程
threading.Thread(target=check_expire).start()