FROM python:3

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY labs/mystery/main.py /app/main.py

CMD ["python", "main.py"] 
