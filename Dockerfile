FROM python:3.14-slim
WORKDIR /srv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=3000
EXPOSE 3000
COPY _speedups*.so ./
COPY run.py .
COPY www ./www
CMD ["python3", "web.py"]
