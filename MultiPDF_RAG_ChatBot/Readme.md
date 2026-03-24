# 📚 Multi-PDF RAG Chatbot

A **Retrieval-Augmented Generation (RAG)** chatbot that allows users to upload multiple PDF documents and ask questions about their content.

The application processes the PDFs, creates embeddings, retrieves relevant document chunks, and generates answers using an LLM.

Built with **Streamlit**, **LangChain**, and **Cohere**.

<img width="1227" height="570" alt="image" src="https://github.com/user-attachments/assets/32ef56a7-d827-4974-b356-ea733dbd6adb" />

---

# Features

* Upload **multiple PDFs**
* Ask questions about document content
* **Conversation memory** for follow-up questions
* Semantic search using **vector embeddings**
* Clean **chat interface with Streamlit**
* Works with **Cohere or OpenAI models**

---

# How It Works

The RAG pipeline follows these steps:

```
PDF Upload
   ↓
Document Loader
   ↓
Text Chunking
   ↓
Embeddings Generation
   ↓
Vector Store (FAISS)
   ↓
Retriever
   ↓
LLM
   ↓
Answer
```

Relevant document chunks are retrieved and passed to the language model to generate accurate answers.

---

# 📂 Project Structure

```
multi-pdf-rag-chatbot/
│
├── app.py              # Streamlit UI
├── rag_pipeline.py     # RAG pipeline logic
├── requirements.txt    # Dependencies
└── README.md
```

--

# Deployment

The app can be deployed easily using **Streamlit Community Cloud**.

Steps:

1. Push the repository to GitHub
2. Go to Streamlit Cloud
3. Create a new app
4. Select the repository
5. Choose `app.py` as the main file

After deployment, you will get a public URL for the chatbot.

---

# 🛠 Technologies Used

* Streamlit
* LangChain
* Cohere / OpenAI
* FAISS
* PyPDF

---

# Example Use Case

Upload documents such as:

* research papers
* manuals
* reports
* textbooks

Then ask questions like:

```
What is the main topic of the document?
Summarize chapter 3
What does the paper say about transformers?
```

The chatbot retrieves relevant sections and generates answers.

---

# License

This project is licensed under the MIT License.

---

# Author

Dhenuka Dudde
