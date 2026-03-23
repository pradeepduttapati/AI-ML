import streamlit as st

from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills_with_llm
from scoring import calculate_skill_score, semantic_match_score
from llm_feedback import get_ai_feedback


st.set_page_config(page_title="AI Resume ATS Analyzer")

st.title("🤖 AI Resume ATS Analyzer")
st.write("Upload your resume and paste the job description.")


resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")


if st.button("Analyze Resume"):

    if resume_file and job_description:

        st.subheader("Analyzing Resume...")

        # Extract text
        resume_text = extract_text_from_pdf(resume_file)

        # Extract skills
        resume_skills = extract_skills_with_llm(resume_text)
        jd_skills = extract_skills_with_llm(job_description)


        skill_score, matched, missing = calculate_skill_score(
            resume_skills,
            jd_skills
        )

        semantic_score = semantic_match_score(
            resume_text,
            job_description
        )

        final_score = int((skill_score * 0.3) + (semantic_score * 0.7))

         # UI
        st.subheader("ATS Score")
        st.progress(final_score / 100)
        st.write(f"Final Score: {final_score}%")

        st.write(f"Skill Score: {skill_score}%")
        st.write(f"Semantic Score: {semantic_score}%")

        st.subheader("Matched Skills")
        st.write(matched)

        st.subheader("Missing Skills")
        st.write(missing)

        # Feedback
        st.subheader("AI Resume Feedback")
        feedback = get_ai_feedback(resume_text, job_description)
        st.write(feedback)

    else:
        st.warning("Please upload resume and enter job description")
