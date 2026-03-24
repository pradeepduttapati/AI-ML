import streamlit as st
import requests
import pdfplumber

st.set_page_config(page_title="AI Resume Analyzer")

st.title("🤖 AI Resume ATS Analyzer")

API_URL = "https://ai-ml-aj9f.onrender.com/analyze"


# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text


# Inputs
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")


if st.button("Analyze Resume"):

    if resume_file and job_description:

        with st.spinner("Analyzing..."):

            resume_text = extract_text_from_pdf(resume_file)

            payload = {
                "resume_text": resume_text,
                "job_description": job_description
            }

            try:
                response = requests.post(API_URL, json=payload, timeout=60)
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
        st.warning("Upload resume and enter job description")
