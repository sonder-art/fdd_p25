# FastAPI con MongoDB - Docker Compose

Este proyecto contiene una configuración de Docker Compose con FastAPI y MongoDB.

## Estructura del Proyecto

```
ejercicio_api/
├── docker-compose.yml
├── README.md
└── app/
    ├── Dockerfile
    ├── requirements.txt
    └── main.py
```

## Características

- **FastAPI**: Framework web moderno y rápido para Python
- **MongoDB**: Base de datos NoSQL
- **Motor**: Driver asíncrono para MongoDB
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI de alto rendimiento

## Uso

### Iniciar los servicios

```bash
docker-compose up -d
```

### Ver los logs

```bash
docker-compose logs -f
```

### Detener los servicios

```bash
docker-compose down
```

### Detener y eliminar volúmenes

```bash
docker-compose down -v
```

## Acceso

- **API**: http://localhost:8000
- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc
- **MongoDB**: localhost:27017

## Credenciales MongoDB

- Usuario: `admin`
- Contraseña: `password123`
- Base de datos: `mydb`

## Endpoints de la API

- `GET /` - Página de bienvenida
- `GET /health` - Verificación de salud del servicio
- `POST /items` - Crear un nuevo item
- `GET /items` - Listar todos los items (con paginación)
- `GET /items/{item_id}` - Obtener un item por ID
- `DELETE /items/{item_id}` - Eliminar un item por ID

## Ejemplo de uso

### Crear un item

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto 1",
    "description": "Descripción del producto",
    "price": 29.99
  }'
```

### Listar items

```bash
curl "http://localhost:8000/items"
```

### Obtener un item específico

```bash
curl "http://localhost:8000/items/{item_id}"
```

## Notas

- Los datos de MongoDB se persisten en un volumen Docker
- El código de la aplicación se monta como volumen para desarrollo (hot-reload)
- Para producción, considera usar variables de entorno para las credenciales

