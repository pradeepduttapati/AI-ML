from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")


# Semantic Score
def semantic_match_score(resume_text, jd_text):

    embeddings = model.encode([resume_text, jd_text])
    similarity = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]

    return similarity * 100


# Skill Matching 
def calculate_skill_score(resume_skills, jd_skills):

    if not jd_skills:
        return 0, [], []

    matched = []

    for jd_skill in jd_skills:
        if jd_skill in resume_skills:
            matched.append(jd_skill)

    score = int((len(matched) / len(jd_skills)) * 100)

    missing = [s for s in jd_skills if s not in matched]

    return score, matched, missing

