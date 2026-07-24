from fastapi import FastAPI, UploadFile, File, Form
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
    result = await analyze_resume(
        resume,
        job_description
    )

    return result