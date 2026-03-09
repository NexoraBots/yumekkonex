FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required by many python libraries
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    git \
    ffmpeg \
    gcc \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copy requirements first (better caching)
COPY requirements.txt .

# Upgrade pip + install dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy rest of project
COPY . .

EXPOSE 8000

CMD bash -c "gunicorn app:app --bind 0.0.0.0:8000 --workers 2 & python3 -m Yumeko"
