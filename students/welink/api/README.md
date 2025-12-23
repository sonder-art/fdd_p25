# Tarea Extra: API con FastAPI y MongoDB

Esta carpeta contiene la implementación de una API REST básica utilizando FastAPI y MongoDB, orquestados con Docker Compose.

## Estructura

- `docker-compose.yml`: Define los servicios `app` (FastAPI) y `db` (MongoDB).
- `app/`:
    - `Dockerfile`: Construcción de la imagen de la API.
    - `requirements.txt`: Dependencias (fastapi, uvicorn, pymongo).
    - `main.py`: Lógica de la aplicación y endpoints.
    - `models.py`: Modelos Pydantic para validación de datos.

## Ejecución

1.  **Levantar servicios**:
    ```bash
    docker-compose up --build
    ```

2.  **Verificar**:
    - API: [http://localhost:8000](http://localhost:8000) -> `{"status": "ok"}`
    - Documentación (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints

- `GET /`: Health check.
- `GET /items`: Listar todos los items.
- `POST /items`: Crear un nuevo item.
- `GET /items/{id}`: Obtener un item por su ID.
