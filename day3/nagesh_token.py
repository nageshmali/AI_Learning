import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("No Api key found")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"

p1 = "Hi"
p2 = "Give me essay on Global warming in 100 words"
p3 = "Explain in detail Tensors in Deep learning"

prompts = [p1,p2,p3]

for prompt in prompts:
    message = {
        "role" : "user",
        "content" : prompt
    }

    messages = [message]

    response = client.chat.completions.create(model=model,messages=messages, max_tokens=1000)

    usage = response.usage

    print(f"Prompt --> {prompt}, Input tokens={usage.prompt_tokens}. Output tokens={usage.completion_tokens}, Total tokens={usage.total_tokens}, Finish Reason={response.choices[0].finish_reason}")