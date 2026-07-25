from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
        logger.warning("Invalid file type uploaded")

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    result = await analyze_resume(
        resume,
        job_description
    )

    logger.info("Returning response")

    return result