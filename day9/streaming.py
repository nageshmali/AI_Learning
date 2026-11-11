import os
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("NO API KEY FOUND")

model = "qwen/qwen3.8-27b"
client = Groq(api_key=my_api_key)

prompt = "Explain me about Remote Jobs in India in detail"

message = {
    "role":"user",
    "content":prompt
}

messages = [message]

response = client.chat.completions.create(model=model,messages=messages,stream=True)
# answer = response.choices[0].message.content
# print(answer)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content:
        print(content,end="",flush=True)