from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RequestData(BaseModel):
    resume_text: str
    job_description: str


@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/analyze")
def analyze(data: RequestData):
    return {"status": "fast"}
    try:
        from skill_extractor import analyze_resume_with_llm
        from scoring import calculate_skill_score, semantic_match_score

        result = analyze_resume_with_llm(
            data.resume_text,
            data.job_description
        )

        if "error" in result:
            return result

        resume_skills = result["resume_skills"]
        jd_skills = result["jd_skills"]
        feedback = result["feedback"]

        # Scoring
        skill_score, matched, missing = calculate_skill_score(
            resume_skills,
            jd_skills
        )

        semantic_score = semantic_match_score(
            data.resume_text,
            data.job_description
        )

        final_score = int((skill_score * 0.3) + (semantic_score * 0.7))

        return {
            "final_score": final_score,
            "skill_score": skill_score,
            "semantic_score": semantic_score,
            "matched": matched,
            "missing": missing,
            "feedback": feedback
        }

    except Exception as e:
        return {"error": str(e)}
