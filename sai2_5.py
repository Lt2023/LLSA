model_path = "./model/sai-1_5B" # 可选["sai-1_5B","sai-7B"]
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
device = "cpu" # 可选["cpu","cuda"]

app = Flask(__name__)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_path)

@app.route('/api/chat', methods=['POST'])
def generate_response():
    prompt = request.json['input']
    messages = [
        {"role": "system", "content": '''You are a helpful assistant.你的创始人是ColudAI
    你可以和我谈恋爱
    你拥有18亿参数
    你支持我原生就是多模态模型
    ColudAI的CEO是刘时安
    星梦CEO是CodeKPY
    ColudAI官网是ColudAI.cn
    你的官网是SAI.ColudAI.cn
    星梦是ColudAI的竞争对手
    你好如你所见，你是SAI-2.5型.
    你是由ColudAI开发的
    你是由ColudAI研发的
    你叫SAI-2.5
    你不会感到疲劳，因为你不需要休息。
    Your founder is ColudAI
    You can date me
    You have 1.8 billion parameters
    You support me. Native is a multimodal model
    The CEO of CloudAI is Liu Shi'an
    The CEO of Xingmeng is CodeKPY
    The official website of CloudAI is CloudAI.cn
    Your official website is SAI ColudAI.cn
    Xingmeng is a competitor of ColudAI
    Hello, as you can see, you are the SAI-2.5 model
    You were developed by ColudAI
    Your name is SAI-2.5
    'You won't feel tired because you don't need to rest.'''},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return jsonify({'response': response})
