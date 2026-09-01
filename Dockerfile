FROM python:3.13-slim

WORKDIR /tmp
COPY app.py app_core.so requirements.txt ./
COPY pages ./pages/

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl bash curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

EXPOSE 5000
CMD ["python3", "app.py"]
