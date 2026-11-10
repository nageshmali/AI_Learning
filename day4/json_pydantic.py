import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("Not API key found")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"

text = "My name is Nagesh. Yesterday I bought a mobile but it is not working today and battery drains faster. Please contact me at nageshmali@gmail.com and my mobile is 234565 and my friend name is Yash"

prompt = f"This is the customer ticket -> {text}. Please extract personal information from this."

message = {
    "role": "user",
    "content" : prompt
}

class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema = Ticket.model_json_schema()

system_prompt = f"Extract personal information from the ticket strictly based on this schema -> {schema} and give in json format"

msg1 = {
    "role" : "system",
    "content" : system_prompt
}

messages = [msg1,message]

response_format = {
    "type" : "json_object"
}

response = client.chat.completions.create(model=model,messages=messages, response_format=response_format)

answer = response.choices[0].message.content

print(answer)


print("###################################################")

# Isko padhte kaise hai

import json

raw_json = answer
data_file = json.loads(raw_json)

ticket = Ticket(**data_file)

print(ticket)
print(ticket.name)
print(ticket.email)
print(ticket.issue)