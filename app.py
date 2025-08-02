import streamlit as st
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from pypdf import PdfReader
from docx import Document
from google.cloud import storage
import os

# ------------------------
# Config
# ------------------------
PROJECT_ID = "YOUR_PROJECT_ID"
BUCKET_NAME = "your-bucket-name"

# Set credentials for Streamlit Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Init Vertex AI
vertexai.init(project=PROJECT_ID, location="us-central1")
model = GenerativeModel("gemini-1.5-flash")

# Init GCS client
storage_client = storage.Client()

# ------------------------
# Helper functions
# ------------------------
def upload_to_bucket(file_data, file_name):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    blob.upload_from_file(file_data)
    return f"gs://{BUCKET_NAME}/{file_name}"

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def summarize_text(text):
    prompt = f"Summarize this document in simple, concise language:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# ------------------------
# Streamlit UI
# ------------------------
st.title("Document Summarizer - Vertex AI Gemini (with GCS storage)")

uploaded_file = st.file_uploader("Upload document (TXT/PDF/DOCX)", type=["txt", "pdf", "docx"])

if uploaded_file:
    # Save uploaded file to GCS
    gcs_path = upload_to_bucket(uploaded_file, uploaded_file.name)
    st.success(f"File uploaded to: {gcs_path}")

    # Reset pointer to start reading
    uploaded_file.seek(0)

    # Extract text
    if uploaded_file.name.endswith(".pdf"):
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        text = extract_text_from_docx(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

    if not text.strip():
        st.error("No readable text found in the document.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarize_text(text)
        st.subheader("Summary")
        st.write(summary)
