# Use a Debian Bullseye based image for better ARM support.
FROM python:3.9-bullseye

# Install system dependencies needed for building native extensions.
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    gfortran && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables to help BLIS avoid problematic auto-compilation.
ENV BLIS_DISABLE_AUTO_COMPILE=1
ENV BLIS_FORCE_CMAKE=1

# Upgrade pip.
RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Download required spaCy language models.
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]