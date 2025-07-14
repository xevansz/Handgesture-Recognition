# Use an official Python base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libreoffice \
        poppler-utils \
        build-essential \
        wget \
        && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY config/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy the rest of the application code
COPY . .

# Expose the Streamlit default port
EXPOSE 8501

# Set environment variables for Streamlit (optional)
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501

# Run Streamlit app
CMD ["streamlit", "run", "main.py"] 