import streamlit as st
import requests


API_KEY = st.secrets["NVIDIA_API_KEY"]

URL = "https://integrate.api.nvidia.com/v1/chat/completions"

MODEL = "google/gemma-3n-e4b-it"


def get_ai_feedback(resume_text, job_description):

    prompt = f"""
You are an expert recruiter.

Analyze the resume based on the job description.

Provide:
1. Resume strengths
2. Weaknesses


Resume:
{resume_text}

Job Description:
{job_description}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 600
    }

    response = requests.post(URL, headers=headers, json=payload)

    data = response.json()

    return data["choices"][0]["message"]["content"]
