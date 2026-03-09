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

# Clone your GitHub repository (includes .git for updates)
RUN git clone https://github.com/NexoraBots/yumekkonex 

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose web port
EXPOSE 8000

# Start web server + bot
CMD bash -c "gunicorn app:app --bind 0.0.0.0:8000 --workers 2 & python3 -m Yumeko"
