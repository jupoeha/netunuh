FROM python:3.14-alpine
WORKDIR /srv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=3000
EXPOSE 3000
COPY web.py .
COPY www ./www
CMD ["python3", "web.py"]
