import os
import json
import logging

from dotenv import load_dotenv
from google import genai

from app.prompt_builder import build_prompt

load_dotenv()

logger = logging.getLogger(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


async def analyze_resume(resume, job_description):
    logger.info("Building prompt")

    prompt = await build_prompt(
        resume,
        job_description
    )

    logger.info("Calling Gemini API")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    logger.info("Analysis completed successfully")

    return json.loads(response.text)