import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
from time import sleep

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("NO API KEY FOUND")


model = "qwen/qwen3.8-27b"
client = Groq(api_key=my_api_key)


correctAnwers = """
Here is the list of correct answers
1.Apple
2.Banana
3.Carrot
4.Donkey
5.Elephant
"""

studentAnswers = """
Here is the list of Student answers
1.Air
2.Banana
3.Camel
4.Deer
5.Elephanta
"""


def call_llm(system_prompt,user_prompt):
    sys_msg = {
        "role":"system",
        "content":system_prompt
    }

    user_msg = {
        "role":"user",
        "content" : user_prompt
    }

    messages = [sys_msg,user_msg]
    response = client.chat.completions.create(model=model,messages=messages)
    answer = response.choices[0].message.content
    return answer


def step1_get_correct_answers(correct_answers):
    system_prompt = f"""
    You are professional Teacher in a school, took test for 5 questions and you responsible for to get correct answers.
    Output Format: Only provide correct answers seperated by commas.
    Dont Invent your own answers, stick to only what is given in user query.
    """

    user_prompt = f"""
    Give correct answers from this text: {correct_answers}
    """

    answer = call_llm(system_prompt,user_prompt)
    return answer


def step2_get_student_answers(student_answers):
    system_prompt = f"""
    You are professional parser and you responsible for to get answers of student.
    Output Format: Only provide answers given by student seperated by commas.
    Dont Invent your own answers, stick to only what is given in user query.
    """

    user_prompt = f"""
    Give answers from this text: {student_answers}
    """

    answer = call_llm(system_prompt,user_prompt)
    return answer

def step3_get_score(correct_answers,student_answers):
    system_prompt = f"""
    You are score generator, your task is to compare the correct answers and student answers and score in percentage.
    Output Format: Provide Percentage:percentage_score and Pass/Fail on condition(if percentage_score>35 pass else fail)
    In answer only show Match items - its number,Total Items and percentage calulation
    """

    user_prompt = f"""
    Compare the correct answers and student answers and score percentage: 
    Correct_Anwers : {correct_answers}
    Student_Answers : {student_answers}
    """

    answer = call_llm(system_prompt,user_prompt)
    return answer

crctAnsw = step1_get_correct_answers(correctAnwers)
print("Correct Answers: ",crctAnsw)
sleep(2)
studAnsw = step2_get_student_answers(studentAnswers)
print("Student Answers: ",studAnsw)
score = step3_get_score(crctAnsw,studAnsw)
print(score)
