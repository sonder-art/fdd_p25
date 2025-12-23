FROM python:3.12-slim

RUN pip install uv

WORKDIR /app

COPY labs/mystery/requirements.txt . 

RUN uv pip install --system -r requirements.txt

COPY labs/mystery/main.py .

CMD ["python", "main.py"]
