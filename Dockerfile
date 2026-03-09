FROM python:3.11-slim-bookworm

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    git \
    ffmpeg \
    gcc \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/app

# Copy dependency file first (better docker caching)
COPY requirements.txt .

# Install python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose web port for gunicorn (if needed)
EXPOSE 8000

# Start bot + web server
CMD bash -c "gunicorn app:app --bind 0.0.0.0:8000 --workers 2 & python3 -m Yumeko"
