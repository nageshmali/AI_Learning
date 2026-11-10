import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
import json
from tkinter import Tk, filedialog
from pypdf import PdfReader


class JobDescription(BaseModel):
    role: str
    education: str
    required_skills: list[str]
    experience_years: int | None = None
    responsibilities: list[str]

schemaJob = JobDescription.model_json_schema()

class CandidateResume(BaseModel):
    name: str
    education: list[str]
    skills: list[str]
    experience_years: float
    projects: list[str]
    work_experience: list[str]

schemaCandidate = CandidateResume.model_json_schema()

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("API key not found")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"

hr_job_description = f"""
SDE I Intern , Amazon University Talent Acquisition
Job ID: 10541345 | ADCI - Karnataka
Description
Software Development Engineer 6 months Internship – 2027 (In-Person)

Job location
By applying to this position your application will be considered for all locations we hire for in India. This includes but is not limited to Bengaluru, Chennai, Hyderabad, Delhi, Mumbai and Pune.

Duration and Timelines
Amazon internships are full-time (40 hours/week) for 24 - 26 consecutive weeks (six months) with start dates between January - June 2027

Key job responsibilities
• Collaborate with experienced cross-disciplinary Amazonians to conceive, design, and bring innovative products and services to market.
• Design and build innovative technologies in a large distributed computing environment, and help lead fundamental changes in the industry.
• Create solutions to run predictions on distributed systems with exposure to innovative
technologies at incredible scale and speed.
• Build distributed storage, index, and query systems that are scalable, fault-tolerant, low cost, and easy to manage/use.
• Ability to design and code the right solutions starting with broadly defined problems.
• Work in an agile environment to deliver high-quality software.

Basic qualifications
- Knowledge of computer science fundamentals such as object-oriented design, operating systems, algorithms, data structures, and complexity analysis
- Knowledge of programming languages such as C/C++, Python, Java or Perl
- Currently enrolled in a Bachelor’s or Master’s Degree in Computer Science, Computer Engineering, or related field at time of application -Year of Graduation 2027

Preferred qualifications
- Previous technical internship(s).
- Experience with distributed, multi-tiered systems, algorithms, and relational databases.
- Experience in optimization mathematics such as linear programming and nonlinear optimization.
- Effectively articulate technical challenges and solutions.
- Adept at handling ambiguous or undefined problems as well as ability to think abstractly.
"""

prompt = f"This is the Job description --> {hr_job_description}. Please extract information from this."

message = {
    "role":"user",
    "content" : prompt
}

system_prompt = f"Extract JD related information from the JobDescription strictly based on this schema -> {schemaJob} and give in json format.Extract individual skills separately.Don't combine multiple programming languages into one string.Keep technical concepts as individual skills.Don't invent requirements that aren't in the JD."

msgJob = {
    "role" : "system",
    "content" : system_prompt
}

response_format = {
    "type":"json_object"
}

messages = [msgJob, message]

response = client.chat.completions.create(model=model,messages=messages,response_format=response_format)
JobDescriptionJSON = response.choices[0].message.content

hrJD = json.loads(JobDescriptionJSON)

hrJDinJSON = JobDescription(**hrJD)
print(hrJDinJSON)



print("#########################################################")

choice = input("Do you want to upload a resume? (y/n): ").strip().lower()

if choice == "y":
    root = Tk()
    root.withdraw()

    pdf_path = filedialog.askopenfilename(
        title="Select Resume",
        filetypes=[("PDF Files", "*.pdf")]
    )

    root.destroy()

    if pdf_path:
        reader = PdfReader(pdf_path)
        resume_text = reader.pages[0].extract_text()
        # print(resume_text)
    else:
        print("No file selected.")

elif choice == "n":
    print("Resume upload cancelled.")

else:
    print("Invalid choice.")



prompt2 = f"This is the Candidate extracted text from resume --> {resume_text}. Please extract information from this."

message2 = {
    "role":"user",
    "content" : prompt2
}

system_prompt2 = f"Extract Candidate Job related information from the CandidateResume strictly based on this schema -> {schemaCandidate} and give in json format"

msgJob2 = {
    "role" : "system",
    "content" : system_prompt2
}

response_format2 = {
    "type":"json_object"
}

messages2 = [msgJob2, message2]

response2 = client.chat.completions.create(model=model,messages=messages2,response_format=response_format2)
CandidateJSON = response2.choices[0].message.content

candidateResumeJson = json.loads(CandidateJSON)

CandidateResumeinJSON = CandidateResume(**candidateResumeJson)
print(CandidateResumeinJSON)



print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

reqSkills = hrJDinJSON.required_skills
candidateSkills = CandidateResumeinJSON.skills

reqSkills = [skill.lower() for skill in reqSkills]
candidateSkills = [skill.lower() for skill in candidateSkills]

print(reqSkills)
print(candidateSkills)


matching_skills = set(reqSkills) & set(candidateSkills)

finalScore = (len(matching_skills)/len(reqSkills)) * 100

print("Candidate Skills Matching score in pecentage -->", finalScore)