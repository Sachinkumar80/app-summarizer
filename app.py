import streamlit as st
import vertexai
from vertexai.preview.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")

# Load Gemini model
model = GenerativeModel("gemini-1.5-flash")

def summarize_text(text):
    prompt = f"Summarize this document in simple, concise language:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("Document Summarizer - Vertex AI Gemini")

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    with st.spinner("Summarizing..."):
        summary = summarize_text(text)
    st.subheader("Summary")
    st.write(summary)
