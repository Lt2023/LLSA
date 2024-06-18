#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('iic/speech_sambert-hifigan_tts_zhiyan_emo_zh-cn_16k')
print(model_dir)