# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Streamlit port
EXPOSE 8080

# Run Streamlit on Cloud Run
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
