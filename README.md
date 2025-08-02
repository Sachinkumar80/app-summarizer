# Document Summarizer – Vertex AI Gemini (Cloud Run)

A web application to summarize PDF, DOCX, and TXT files using Google Cloud **Vertex AI Gemini model**.  
Hosted serverlessly on **Cloud Run**, supporting secure file uploads to **Cloud Storage** with signed URL downloads.

---

## Features
- Summarizes PDF, DOCX, and TXT documents using Vertex AI Gemini 2.0 Flash
- Secure file storage on Google Cloud Storage
- Signed URL generation for temporary, secure downloads
- Simple and responsive UI built with Streamlit
- Hosted on Cloud Run (auto-scaling, serverless)
- Developer credit displayed in footer

---

## Prerequisites

1. Google Cloud Project with **billing enabled**
2. Enable required APIs:
   ```bash
   gcloud services enable \
      aiplatform.googleapis.com \
      run.googleapis.com \
      artifactregistry.googleapis.com \
      cloudbuild.googleapis.com \
      storage.googleapis.com

Install:

Google Cloud SDK
Docker
Roles needed:
Vertex AI User
Cloud Run Admin
Storage Admin
Artifact Registry Admin

Setup Instructions
1. Clone the repository
git clone <repo-url>
cd <repo-folder>
2. Update app.py
Set your PROJECT_ID and BUCKET_NAME

Model: gemini-2.0-flash

3. Create Storage Bucket
gsutil mb -l us-central1 gs://doc-summarizer-streamlit
(Optional for testing: make public)
gsutil iam ch allUsers:objectViewer gs://doc-summarizer-streamlit

4. Create Artifact Registry
gcloud artifacts repositories create doc-summarizer-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repo for summarizer app"
  
5. Build & Push Docker Image
gcloud builds submit --tag us-central1-docker.pkg.dev/<PROJECT_ID>/doc-summarizer-repo/doc-summarizer

7. Deploy to Cloud Run
gcloud run deploy doc-summarizer \
  --image us-central1-docker.pkg.dev/<PROJECT_ID>/doc-summarizer-repo/doc-summarizer \
  --region us-central1 \
  --allow-unauthenticated

https://doc-summarizer-<PROJECT_NUMBER>.us-central1.run.app
Secure File Download (Signed URL)
Instead of making bucket public, signed URLs allow temporary access to files.


Developer
Created by Sachin Kumar
