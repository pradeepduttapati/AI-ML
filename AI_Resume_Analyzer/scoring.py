from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# Semantic Score 
def semantic_match_score(resume_text, jd_text):

    embeddings = model.encode([resume_text, jd_text])

    similarity = cosine_similarity(
        [embeddings[0]], [embeddings[1]]
    )[0][0]

    return similarity * 100


# Flexible Skill Matching 
def is_match(jd_skill, resume_skills):

    jd_skill = jd_skill.lower().strip()

    for res_skill in resume_skills:
        res_skill = res_skill.lower().strip()

        # Exact match
        if jd_skill == res_skill:
            return True

        # Substring match (both directions)
        if jd_skill in res_skill or res_skill in jd_skill:
            return True

        # Basic token overlap (handles multi-word cases)
        jd_tokens = jd_skill.split()
        res_tokens = res_skill.split()

        if any(token in res_tokens for token in jd_tokens):
            return True

    return False
    

# Skill Score 
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

