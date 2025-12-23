# Ejercicio API: FastAPI + MongoDB

Este proyecto implementa una API REST simple usando FastAPI y MongoDB con Docker Compose.

## Estructura

```
ejercicio_api/
├── docker-compose.yml      # Orquestación de servicios
├── app/                    # Aplicación FastAPI
│   ├── Dockerfile          # Imagen de la aplicación
│   ├── requirements.txt    # Dependencias Python
│   ├── main.py             # Punto de entrada FastAPI
│   └── models.py           # Modelos Pydantic
└── README.md               # Este archivo
```

## Comandos

### Levantar el proyecto

```bash
docker-compose up --build
```

### Levantar en background

```bash
docker-compose up -d
```

### Ver logs

```bash
docker-compose logs -f
```

### Detener

```bash
docker-compose down
```

### Detener y eliminar volúmenes

```bash
docker-compose down -v
```

## Endpoints

- `GET /` - Health check
- `GET /items` - Listar todos los items
- `POST /items` - Crear un nuevo item
- `GET /items/{id}` - Obtener un item por ID

## Documentación

Una vez levantado el proyecto, accede a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Ejemplos con curl

```bash
# Health check
curl http://localhost:8000/

# Listar items
curl http://localhost:8000/items

# Crear item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Laptop", "descripcion": "MacBook Pro"}'

# Obtener item por ID
curl http://localhost:8000/items/{id}
```

