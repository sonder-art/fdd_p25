# Tarea 10: Docker Avanzado

Esta carpeta contiene la evidencia de la Tarea 10.

## Archivos
- `Dockerfile`: Definición de la imagen.
- `app.py`: Script de Python que imprime un mensaje y escribe en un volumen.

## Instrucciones de Ejecución

1.  **Construir la imagen**:
    ```bash
    docker build -t mi-python-app .
    ```

2.  **Ejecutar con volumen**:
    ```bash
    # Crear directorio local para datos
    mkdir data
    
    # Ejecutar montando el volumen
    docker run -v $(pwd)/data:/app/data mi-python-app
    ```

3.  **Verificar persistencia**:
    Revisar el archivo `data/log.txt` en el host. Debería contener la fecha y hora de ejecución.
