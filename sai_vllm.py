from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

model_dir = "./model/sai-1_5B"


tokenizer = AutoTokenizer.from_pretrained(model_dir)


sampling_params = SamplingParams(temperature=0.7, top_p=0.8, repetition_penalty=1.05, max_tokens=512)


llm = LLM(model=model_dir)

system_prompt = '''You are a helpful assistant.你的创始人是ColudAI
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
    'You won't feel tired because you don't need to rest.'''

# Prepare your prompts
prompt = "Tell me something about large language models."
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# generate outputs
outputs = llm.generate([text], sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")