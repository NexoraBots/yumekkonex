FROM python:3.10-slim-bookworm

# Install required system libraries for opencv and other packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copy project files
COPY . .

# Upgrade pip and install python dependencies
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Start bot + web process
CMD gunicorn app:app --bind 0.0.0.0:8000 & python3 -m Yumeko
