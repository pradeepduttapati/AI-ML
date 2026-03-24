import streamlit as st
import requests

st.set_page_config(page_title="AI Resume ATS Analyzer")

st.title("🤖 AI Resume ATS Analyzer")

st.write("Upload your resume text and paste job description.")

# Inputs
resume_text = st.text_area("Paste Resume Text")
job_description = st.text_area("Paste Job Description")

# API URL
API_URL = "https://ai-ml-aj9f.onrender.com/analyze"

if st.button("Analyze Resume"):

    if resume_text and job_description:

        with st.spinner("Analyzing..."):

            payload = {
                "resume_text": resume_text,
                "job_description": job_description
            }

            try:
                response = requests.post(API_URL, json=payload)

                data = response.json()

                if "error" in data:
                    st.error(data["error"])

                else:
                    st.subheader("ATS Score")
                    st.progress(data["final_score"] / 100)
                    st.write(f"Score: {data['final_score']}%")

                    st.subheader("Matched Skills")
                    st.write(data["matched"])

                    st.subheader("Missing Skills")
                    st.write(data["missing"])

            except Exception as e:
                st.error(f"API Error: {str(e)}")

    else:
        st.warning("Please enter resume and job description")
