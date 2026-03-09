FROM python:3.11-slim-bookworm

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

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD bash -c "gunicorn app:app --bind 0.0.0.0:8000 & python3 -m Yumeko"
