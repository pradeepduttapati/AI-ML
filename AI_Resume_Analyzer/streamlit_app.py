import streamlit as st
import requests
import pdfplumber

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# Title
st.title("🤖 AI Resume ATS Analyzer")
st.caption("Get ATS score based on job description using AI")

# API URL
API_URL = "https://ai-ml-aj9f.onrender.com/analyze"


# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description", height=200)


if st.button("Analyze Resume"):

    if resume_file and job_description:

        with st.spinner("Analyzing resume.."):

            try:
                # Extract resume text
                resume_text = extract_text_from_pdf(resume_file)

                payload = {
                    "resume_text": resume_text,
                    "job_description": job_description
                }

                # Call API
                response = requests.post(API_URL, json=payload, timeout=120)
                data = response.json()

                if "error" in data:
                    st.error(data["error"])

                else:
                    st.subheader("ATS Score")
                    st.progress(data["final_score"] / 100)
                    st.success(f"Score: {data['final_score']}%")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("✅ Matched Skills")
                        st.write(data["matched"])

                    with col2:
                        st.subheader("❌ Missing Skills")
                        st.write(data["missing"])

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        st.warning("Please upload resume and enter job description")
