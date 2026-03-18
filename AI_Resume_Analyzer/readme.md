# 🤖 AI Resume ATS Analyzer

An AI-powered Resume Analyzer that evaluates resumes against job descriptions using **LLMs (NVIDIA Gemma)** and **semantic similarity (embeddings)** to generate an ATS (Applicant Tracking System) score.

---

##  Features

- 📄 Upload resume (PDF)
- 📝 Input job description
- 🧠 AI-based skill extraction (no hardcoded skills)
- 📊 ATS score calculation based on:
  - Skill matching
  - Semantic similarity (embeddings)
- ❗ Missing skills detection
- 💡 AI-powered resume feedback using LLM
- 🌐 Interactive UI using Streamlit

---

## 🧠 How It Works

1. Extract text from uploaded resume
2. Extract skills from:
   - Resume
   - Job description
   using NVIDIA Gemma LLM
3. Calculate:
   - Skill match score
   - Semantic similarity score (embeddings)
4. Combine scores to generate final ATS score
5. Generate improvement suggestions using AI

---

## 🏗️ Architecture
Resume (PDF) + Job Description
↓
Text Extraction
↓
LLM Skill Extraction
↓
Skill Matching + Missing Skills
↓
Embedding Similarity (MiniLM)
↓
ATS Score
↓
AI Feedback (Gemma)

---

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (UI)
- **NVIDIA API (Gemma-3n-e4b-it)** (LLM)
- **Sentence Transformers** (Embeddings)
- **Scikit-learn** (Cosine similarity)
- **pdfplumber** (PDF parsing)

---
## Author

Dhenuka Dudde
