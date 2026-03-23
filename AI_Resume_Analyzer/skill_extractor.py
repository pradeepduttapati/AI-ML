import requests
import os

API_KEY = os.getenv("NVIDIA_API_KEY")

URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "google/gemma-3n-e4b-it"


def extract_skills_with_llm(text):

    if not API_KEY:
        print("ERROR: NVIDIA_API_KEY not set")
        return []

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

    try:
        response = requests.post(
            URL,
            headers=headers,
            json=payload,
            timeout=10   
        )

        data = response.json()

        if "choices" not in data:
            print("API ERROR:", data)
            return []

        skills_text = data["choices"][0]["message"]["content"]

        skills = list(set([s.strip().lower() for s in skills_text.split(",")]))

        return skills

    except Exception as e:
        print("LLM ERROR:", str(e))
        return []
