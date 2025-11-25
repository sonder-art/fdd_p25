# Imagen base con Python 3
FROM python:3

# Definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar entrega.py y notas.txt al contenedor
COPY entrega.py notas.txt /app/

# Comando por defecto: ejecutar entrega.py
CMD ["python", "entrega.py"]