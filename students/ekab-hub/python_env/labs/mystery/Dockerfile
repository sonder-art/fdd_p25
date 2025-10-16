FROM python:3.12-slim
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
  && ln -s /root/.local/bin/uv /usr/local/bin/uv

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN uv pip install --system -r requirements.txt

COPY . /app/

CMD ["python", "main.py"]

