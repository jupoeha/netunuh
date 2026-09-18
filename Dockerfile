FROM python:3.11-slim
WORKDIR /srv
COPY _speedups*.so ./
COPY run.py .
COPY www ./www
EXPOSE 3000
CMD ["python3", "run.py"]
