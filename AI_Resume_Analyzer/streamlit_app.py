import streamlit as st
from resume_parser import extract_text_from_pdf
from skill_extractor import extract_skills_with_llm
from scoring import calculate_skill_score
from llm_feedback import get_ai_feedback 

st.title("AI Resume ATS Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):

    if uploaded_file and job_description:
        st.subheader("Analyzing Resume...")
        # Extract resume text
        resume_text = extract_text_from_pdf(uploaded_file)

        # Extract skills
        resume_skills = extract_skills_with_llm(resume_text)
        jd_skills = extract_skills_with_llm(job_description)

        # Scoring
        result = calculate_skill_score(
            resume_skills,
            jd_skills,
            resume_text,
            job_description
        )

        final_score = result["final_score"]
        strong = result["strong_matches"]
        partial = result["partial_matches"]
        missing = result["missing"]

        # UI Output
        st.subheader(f"ATS Score: {final_score}%")

        st.subheader("Strong Matches")
        st.write(strong)

        st.subheader("Partial Matches")
        st.write(partial)

        st.subheader(" Missing Skills")
        st.write(missing)

        # AI Feedback
        feedback = get_ai_feedback(resume_text, job_description)
        st.subheader("AI Feedback")
        st.write(feedback)

    else:
        st.warning("Please upload resume and enter job description")
