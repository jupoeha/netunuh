FROM python:3.13-slim

WORKDIR /tmp
COPY main.py app_core.so requirements.txt index.html posts.html 404.html ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl bash curl && \
    rm -rf /var/lib/apt/lists/* &&\
    pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "main.py"]
