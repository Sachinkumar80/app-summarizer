import streamlit as st
from google.cloud import aiplatform

# Initialize Vertex AI
aiplatform.init(project="trai-project", location="us-central1")
model = aiplatform.GenerativeModel("gemini-1.5-flash")

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
