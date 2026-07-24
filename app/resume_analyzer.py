import os
import json
import io

from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from fastapi import UploadFile

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def load_prompt():
    with open("prompts/resume_prompt.txt", "r", encoding="utf-8") as file:
        return file.read()


async def load_resume_pdf(resume: UploadFile):
    pdf_bytes = await resume.read()

    reader = PdfReader(io.BytesIO(pdf_bytes))

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text


async def build_prompt(resume: UploadFile, job_description: str):
    prompt = load_prompt()
    resume_text = await load_resume_pdf(resume)

    return f"""{prompt}

Job Description:
{job_description}

Resume:
{resume_text}
"""


async def analyze_resume(resume: UploadFile, job_description: str):
    prompt = await build_prompt(resume, job_description)

    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=prompt
    )

    return json.loads(response.text)