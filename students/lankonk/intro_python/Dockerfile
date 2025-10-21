# syntax=docker/dockerfile:1
FROM python:3.12-slim

RUN useradd -m appuser

WORKDIR /app

COPY entrega.py .
COPY notas.txt .

USER appuser

CMD ["python", "entrega.py"]