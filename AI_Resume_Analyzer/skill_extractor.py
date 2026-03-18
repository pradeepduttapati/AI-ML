import requests
import os

API_KEY = os.getenv("NVIDIA_API_KEY")

URL = "https://integrate.api.nvidia.com/v1/chat/completions"

MODEL = "google/gemma-3n-e4b-it"


def extract_skills_with_llm(text):

    prompt = f"""
Extract the technical skills from the following text.
Return only a comma-separated list.

Text:
{text}
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
        "temperature": 0.2,
        "max_tokens": 200
    }

    response = requests.post(URL, headers=headers, json=payload)

    data = response.json()

    skills_text = data["choices"][0]["message"]["content"]

    skills = list(set([s.strip().lower() for s in skills_text.split(",")]))

    return skills
