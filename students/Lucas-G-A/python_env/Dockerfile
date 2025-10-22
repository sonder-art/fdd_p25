FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY . /app

RUN uv pip install --system -r requirements.txt

ENV MYSTERY_URL="https://jsonplaceholder.typicode.com/todos/1"

CMD ["python", "labs/mystery/main.py"]

