FROM python:3.13.5

RUN useradd -m usuarioPrueba
WORKDIR /app
COPY requirements.txt  .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY main.py .
USER usuarioPrueba
CMD ["python" , "main.py" ]
