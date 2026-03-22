from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text_list):
    return model.encode(text_list)


def match_skill(jd_skill, resume_skills, resume_text,
                strong_threshold=0.65,
                partial_threshold=0.45):

    # Combine skills + full resume text
    corpus = resume_skills + [resume_text]

    jd_emb = get_embedding([jd_skill])
    corpus_emb = get_embedding(corpus)

    similarities = cosine_similarity(jd_emb, corpus_emb)[0]

    best_score = float(np.max(similarities))

    if best_score >= strong_threshold:
        return "strong", best_score
    elif best_score >= partial_threshold:
        return "partial", best_score
    else:
        return "missing", best_score


def calculate_skill_score(resume_skills, jd_skills, resume_text):

    strong_matches = []
    partial_matches = []
    missing = []

    total_weight = 0
    score_sum = 0

    for jd_skill in jd_skills:

        match_type, score = match_skill(jd_skill, resume_skills, resume_text)

        weight = 1.0  # can extend later

        if match_type == "strong":
            strong_matches.append(jd_skill)
            score_sum += 1.0 * weight

        elif match_type == "partial":
            partial_matches.append(jd_skill)
            score_sum += 0.6 * weight

        else:
            missing.append(jd_skill)

        total_weight += weight

    final_score = int((score_sum / total_weight) * 100)

    return final_score, strong_matches, partial_matches, missing
