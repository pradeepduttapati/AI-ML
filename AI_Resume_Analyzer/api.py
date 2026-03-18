from fastapi import FastAPI
from pydantic import BaseModel

from skill_extractor import extract_skills_with_llm
from scoring import calculate_skill_score
from embedding_matcher import semantic_match_score

app = FastAPI()


class RequestData(BaseModel):
    resume_text: str
    job_description: str


@app.post("/analyze")
def analyze(data: RequestData):

    resume_skills = extract_skills_with_llm(data.resume_text)
    jd_skills = extract_skills_with_llm(data.job_description)

    skill_score, matched, missing = calculate_skill_score(
        resume_skills,
        jd_skills
    )

    semantic_score = semantic_match_score(
        data.resume_text,
        data.job_description
    )

    final_score = int((skill_score * 0.6) + (semantic_score * 0.4))

    return {
        "score": final_score,
        "matched_skills": matched,
        "missing_skills": missing
    }
