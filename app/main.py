from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from google.genai.errors import ServerError

from app.logger import logger
from app.resume_analyzer import analyze_resume
from app.models.response_models import ResumeAnalysisResponse

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer API"
    }


@app.post(
    "/analyze",
    response_model=ResumeAnalysisResponse
)
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    logger.info(f"Received file: {resume.filename}")

    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:

        result = await analyze_resume(
            resume,
            job_description
        )

        logger.info("Returning response")

        return result

    except ServerError:

        logger.error("Gemini service unavailable")

        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily busy. Please try again in a few moments."
        )

    except Exception as e:

        logger.exception(e)

        raise HTTPException(
            status_code=500,
            detail="Unexpected server error. Please try again later."
        )