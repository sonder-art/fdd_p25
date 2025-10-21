# Usamos una imagen oficial de Python como base. Es ligera y eficiente.
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor en /app.
WORKDIR /app

# El ejercicio exige usar 'uv', así que lo instalamos primero.
RUN pip install uv

# Copiamos SOLO la lista de requerimientos. Docker es inteligente y si este
# archivo no cambia, no volverá a ejecutar el siguiente paso en futuras builds.
COPY requirements.txt .

# Usamos 'uv' para instalar todas las dependencias listadas en requirements.txt.
RUN uv pip install -r requirements.txt --system

# Ahora copiamos el resto de nuestro código (la carpeta 'labs' con el script).
COPY . .

# Finalmente, definimos el comando que se ejecutará cuando el contenedor inicie.
CMD ["python", "labs/mystery/main.py"]
