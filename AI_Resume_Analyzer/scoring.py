from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def is_match(jd_skill, resume_skills, threshold=0.6):

    if not resume_skills:
        return False

    jd_embedding = model.encode([jd_skill])
    res_embeddings = model.encode(resume_skills)
    similarities = cosine_similarity(jd_embedding, res_embeddings)
    return max(similarities[0]) >= threshold

def calculate_skill_score(resume_skills, jd_skills):

    if not jd_skills:
        return 0, [], []

    matched = []

    for jd_skill in jd_skills:
        if is_match(jd_skill, resume_skills):
            matched.append(jd_skill)

    score = int((len(matched) / len(jd_skills)) * 100)

    missing = [s for s in jd_skills if s not in matched]

    return score, matched, missing
