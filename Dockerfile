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

# Install PDM
RUN pip install --no-cache-dir pdm

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies with PDM
RUN pdm install --prod

# Expose the Streamlit default port
EXPOSE 8501

# Set environment variables for Streamlit (optional)
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501

# Run Streamlit app
CMD ["streamlit", "run", "main.py"] 