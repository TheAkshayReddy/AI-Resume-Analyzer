from pydantic import BaseModel
from typing import List


class ResumeAnalysisResponse(BaseModel):
    match_score: int
    resume_summary: str
    job_summary: str
    matching_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    weaknesses: List[str]
    resume_improvements: List[str]
    final_recommendation: str