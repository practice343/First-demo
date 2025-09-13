FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DISPLAY=:0 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

WORKDIR /app

# System dependencies for tkinter, matplotlib, X virtual display and noVNC
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    tk \
    tcl \
    xvfb \
    x11vnc \
    fluxbox \
    websockify \
    novnc \
    libfreetype6 \
    libpng16-16 \
    fonts-dejavu \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Startup script to run Xvfb, window manager, VNC and noVNC, then the app
RUN chmod +x scripts/start.sh || true

EXPOSE 8080

CMD ["/bin/bash", "-lc", "scripts/start.sh"]


