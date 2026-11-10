import os
from pathlib import Path
from groq import Groq
import re
from dotenv import load_dotenv
from time import sleep
from test_api import get_iphone_17_price


load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API KEY NOT FOUND")

model = "qwen/qwen3.8-27b"
client = Groq(api_key=my_api_key)


def get_product_price(product):
    if product.lower() == "iphone 17":
        return get_iphone_17_price()
    elif product.lower() == "iphone 15":
        return 500
    else:
        return 0

def calculate(expression):
    try:
        return eval(expression)
    except:
        return "calc error!"


tools = {
    "get_product_price": get_product_price,
    "calculate":calculate
}

system_prompt = """
You are a shopping assistant system who works for my company. We have only two products: Iphone17 and IPhone15

You have two tools:
get_product_price(product)
calculate(expression)

IMPORTANT:
Call tools exactly like these examples:

Action: get_product_price("iPhone 17")
Action: calculate("5000 - 1000")

Never write:
get_product_price(product="iPhone 17") or get_product_price('"iPhone 17"')

Never write:
calculate(expression="5000 - 1000")

Follow these rules:

1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer

#NOTE
If I dont have full money for the product i want to buy just tell me in Final Answer:Your budget is too low in first iteration itself.
"""

def run_agent(question):

    messages = [
        {
            "role":"system",
            "content":system_prompt
        },
        {
            "role":"user",
            "content":question
        }
    ]

    for step in range(5):

        print("\n------------------")
        print("STEP", step + 1)
        print("------------------")

        response = client.chat.completions.create(model=model,messages=messages)
        answer = response.choices[0].message.content
        print(answer)

        if "Final Answer:" in answer:
            break
    
        match = re.search(r"Action:\s*(\w+)\((.*?)\)", answer)

        if match:
                tool_name = match.group(1)
                tool_input = match.group(2)
                tool_input = tool_input.strip()
                tool_input = tool_input.strip('"')
        
                if tool_name in tools:
                    tool = tools[tool_name]
                    observation = tool(tool_input)
                else:
                    observation = "Tool not found"
        
                print("Observation:",observation)
        
                messages.append({
                    "role":"assistant",
                    "content":answer
                })
        
                messages.append({
                    "role":"user",
                    "content": "Observation:" + str(observation)
                })

                sleep(4)
        


prompt="""
I have 20 rupees. What is the price of an iphone 17?
and how much money will I have left?
"""
run_agent(prompt)