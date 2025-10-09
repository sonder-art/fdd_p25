FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get purge -y --auto-remove curl && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:${PATH}"

COPY requirements.txt .

RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install --no-cache -r requirements.txt

COPY main.py .

CMD [".venv/bin/python", "main.py"]






