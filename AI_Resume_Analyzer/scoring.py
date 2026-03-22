from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# Embeddings
def get_embeddings(text_list):
    return model.encode(text_list)


# Skill matching
def match_skill(jd_skill, resume_skills, resume_text,
                strong_threshold=0.65,
                partial_threshold=0.45):

    corpus = resume_skills + [resume_text]

    jd_emb = get_embeddings([jd_skill])
    corpus_emb = get_embeddings(corpus)

    similarities = cosine_similarity(jd_emb, corpus_emb)[0]
    best_score = float(np.max(similarities))

    if best_score >= strong_threshold:
        return "strong", best_score
    elif best_score >= partial_threshold:
        return "partial", best_score
    else:
        return "missing", best_score


# Semantic score (full context)
def calculate_semantic_score(resume_text, jd_text):
    embeddings = get_embeddings([resume_text, jd_text])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return similarity * 100


# Final scoring
def calculate_skill_score(resume_skills, jd_skills, resume_text, jd_text):

    strong_matches = []
    partial_matches = []
    missing = []

    score_sum = 0
    total = len(jd_skills)

    for jd_skill in jd_skills:

        match_type, score = match_skill(jd_skill, resume_skills, resume_text)

        if match_type == "strong":
            strong_matches.append(jd_skill)
            score_sum += 1.0

        elif match_type == "partial":
            partial_matches.append(jd_skill)
            score_sum += 0.7

        else:
            missing.append(jd_skill)

    # Skill score
    skill_score = (score_sum / total) * 100 if total > 0 else 0

    # Semantic score
    semantic_score = calculate_semantic_score(resume_text, jd_text)

    # Final balanced score
    final_score = (skill_score * 0.4) + (semantic_score * 0.6)

    final_score = int(min(final_score, 100))

    return {
        "final_score": final_score,
        "skill_score": int(skill_score),
        "semantic_score": int(semantic_score),
        "strong_matches": strong_matches,
        "partial_matches": partial_matches,
        "missing": missing
    }
