import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("No Api key found")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"
role = "user"
prompt = "Suggest me a brand name for our shoe company. Just give only one name"


sys_message = {
    "role" : "system",
    "content" : "You are a marketing guy, working for my company."
}

message = {
    "role" : role,
    "content" : prompt
}

messages = [sys_message, message]

response = client.chat.completions.create(model=model,messages=messages,temperature=2)

print(response.choices[0].message.content)