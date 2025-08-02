import streamlit as st
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from pypdf import PdfReader
from docx import Document

# ------------------------
# Initialize Vertex AI
# ------------------------
vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")

# Load Gemini model
model = GenerativeModel("gemini-1.5-flash")

# ------------------------
# Helper Functions
# ------------------------

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def summarize_text(text):
    """Send text to Gemini model for summarization."""
    prompt = f"Summarize this document in simple, concise language:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# ------------------------
# Streamlit UI
# ------------------------

st.title("Document Summarizer - Vertex AI Gemini")

uploaded_file = st.file_uploader("Upload your document", type=["txt", "pdf", "docx"])

if uploaded_file:
    # Handle different file types
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file)
    else:  # txt file
        text = uploaded_file.read().decode("utf-8")

    # Check file size or empty content
    if not text.strip():
        st.error("No readable text found in the document.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize_text(text)

        st.subheader("Summary")
        st.write(summary)
