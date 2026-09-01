FROM python:3.13-slim

WORKDIR /tmp
COPY main.py app_core.so  ./
COPY www ./www/

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl bash curl && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000
CMD ["python3", "main.py"]
