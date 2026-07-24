from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.resume_analyzer import analyze_resume

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer API"
    }


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
    )

    result = await analyze_resume(
        resume,
        job_description
    )

    return result