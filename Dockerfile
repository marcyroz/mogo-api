# Dockerfile
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# ✅ INSTALAR TODAS AS LIBS DE UMA VEZ (CACHE!)
RUN apt-get update && apt-get install -y \
    # GDAL
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    # PostgreSQL
    postgresql-client \
    # Build tools
    build-essential \
    gcc \
    g++ \
    python3-dev \
    # Utils
    netcat-openbsd \
    # OpenCV dependencies
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgthread-2.0-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    # FFmpeg
    ffmpeg \
    # Image libs
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# GDAL environment
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /app

# ✅ COPIAR E INSTALAR REQUIREMENTS (CACHE!)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY ./mogo /app/mogo

WORKDIR /app/mogo

CMD ["celery", "-A", "mogo", "worker", "-l", "info"]
