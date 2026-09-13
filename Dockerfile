FROM python:3.11-slim
COPY app.py /app/app.py
WORKDIR /app
EXPOSE 8080
CMD ["python3", "/app/app.py"]
