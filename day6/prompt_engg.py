import os
from groq import Groq
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("No API key found")


model = "openai/gpt-oss-20b"

client = Groq(api_key=my_api_key)

def callLLM(prompt):

    message = {
        "role": "user",
        "content" : prompt
    }

    messages = [message]

    response = client.chat.completions.create(model=model,messages=messages)

    ans = response.choices[0].message.content

    print(ans)


prompt = """
# ROLE
You are a Issue Classifier System for my company which is a mobile/laptop selling company.
# Task
Classify the user query
# Constraints
Classify the customer issue among only these three namely: Technical, Billing, Return
# Output format
Just give one word category which is provided in constraints.
# Example
If user query is My device is not working - ans is Technical
If user has some issue with bill, money, want to avail bank offers - ans is Billing
If user want to return, exchange, replace, - ans is Return
# Fallback
If user query is unrelated, vague - ans is OTHER
This is user query:
I bought new phone but screen in very blur
"""

callLLM(prompt)