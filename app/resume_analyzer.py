import os
from dotenv import load_dotenv
from google import genai
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def load_prompt():
    with open("prompts/resume_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()

def load_resume():
    with open("sample_data/sample_resume.txt", "r", encoding="utf-8") as file:
        return file.read()

def build_prompt(resume_path, job_description):
    prompt = load_prompt()
    resume = load_resume_pdf(resume_path)

    return f"{prompt}\n\nJob Description:\n{job_description}\n\nResume:\n{resume}"


def analyze_resume(resume_path, job_description):
    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=build_prompt(resume_path, job_description)
    )

    return json.loads(response.text)

from pypdf import PdfReader


def load_resume_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text