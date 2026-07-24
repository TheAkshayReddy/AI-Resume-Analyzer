import os
import json

from dotenv import load_dotenv
from google import genai

from app.prompt_builder import build_prompt

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


async def analyze_resume(resume, job_description):
    prompt = await build_prompt(resume, job_description)

    response = client.models.generate_content(
        model="models/gemini-3.6-flash",
        contents=prompt
    )

    return json.loads(response.text)