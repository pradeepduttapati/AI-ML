from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_match_score(resume_text, job_description):

    resume_embedding = model.encode([resume_text])

    jd_embedding = model.encode([job_description])

    similarity = cosine_similarity(
        resume_embedding,
        jd_embedding
    )

    score = float(similarity[0][0])

    return int(score * 100)
