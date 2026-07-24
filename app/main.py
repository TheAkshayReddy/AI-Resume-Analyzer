from fastapi import FastAPI
from pydantic import BaseModel
from app.resume_analyzer import analyze_resume

app = FastAPI()


class AnalyzeRequest(BaseModel):
    resume_path: str
    job_description: str


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer API"
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    result = analyze_resume(
        request.resume_path,
        request.job_description
    )

    return result