FROM python:3.14-alpine
WORKDIR /tmp
COPY main.py app_core.so requirements.txt index.html posts.html 404.html ./
RUN apk add --no-cache openssl bash curl && \
    pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python3", "main.py"]
