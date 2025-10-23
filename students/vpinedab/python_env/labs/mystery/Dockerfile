FROM python:3.12-slim

WORKDIR /app

COPY main.py .
COPY requirements.txt .

RUN pip install uv
RUN uv venv .venv

RUN uv pip install -r requirements.txt

CMD ["/app/.venv/bin/python3", "main.py"]
