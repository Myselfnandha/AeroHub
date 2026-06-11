# Multi-stage Dockerfile for MovieSongDownloader
FROM python:3.12-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential ffmpeg curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m compileall MovieSongDownloader

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
EXPOSE 8555
ENTRYPOINT ["python", "MovieSongDownloader/main.py", "--env", "prod"]
