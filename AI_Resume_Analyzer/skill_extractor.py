import requests
import os
import json

API_KEY = os.getenv("NVIDIA_API_KEY")

URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "google/gemma-3n-e4b-it"


def analyze_resume_with_llm(resume_text, job_description):

    if not API_KEY:
        return {"error": "API key not set"}

    prompt = f"""
You are an AI Resume Analyzer.

1. Extract technical skills from the RESUME.
2. Extract required skills from the JOB DESCRIPTION.
3. Identify missing skills.
4. Provide improvement feedback.

Return STRICT JSON like this:
{{
  "resume_skills": [],
  "jd_skills": [],
  "missing_skills": [],
  "feedback": ""
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 500
    }

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=15)
        data = response.json()

        if "choices" not in data:
            return {"error": str(data)}

        content = data["choices"][0]["message"]["content"]

        # Clean response
        content = content.replace("```json", "").replace("```", "")

        try:
            result = json.loads(content)
        except:
            return {"error": "Invalid JSON from LLM"}

        return result

    except Exception as e:
        return {"error": str(e)}
