from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_match_score(resume_text, job_description):

    embeddings = model.encode([resume_text, job_description])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    return int(similarity * 100)


def calculate_skill_score(resume_skills, jd_skills):

    matched = []
    missing = []

    for skill in jd_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(jd_skills) == 0:
        return 0, matched, missing

    score = int((len(matched) / len(jd_skills)) * 100)

    return score, matched, missing
