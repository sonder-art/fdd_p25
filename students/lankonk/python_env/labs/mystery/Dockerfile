FROM python:3.12-slim

RUN useradd -m appuser

WORKDIR /app

RUN python -m venv .venv

COPY main.py .

COPY requirements.txt .
RUN .venv/bin/pip install --upgrade pip && .venv/bin/pip install -r requirements.txt


USER appuser

CMD ["/app/.venv/bin/python","main.py"]