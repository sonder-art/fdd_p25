# API con FastAPI + MongoDB en Docker

API REST simple construida con FastAPI y MongoDB, orquestada con Docker Compose.

## 🎯 Objetivo

Este proyecto implementa una API básica para gestionar items, demostrando:
- Uso de **FastAPI** como framework web
- Integración con **MongoDB** como base de datos
- Containerización con **Docker** y **Docker Compose**
- Operaciones CRUD básicas

## 📁 Estructura del Proyecto

```
ejercicio_api/
│
├── docker-compose.yml      # Orquestación de servicios
│
├── app/                    # Aplicación FastAPI
│   ├── Dockerfile          # Imagen Docker de la app
│   ├── requirements.txt    # Dependencias Python
│   ├── main.py             # Aplicación FastAPI principal
│   └── models.py            # Modelos Pydantic
│
└── README.md               # Este archivo
```

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker instalado
- Docker Compose instalado

### Pasos para levantar el proyecto

1. **Navega al directorio del proyecto:**
   ```bash
   cd ejercicio_api
   ```

2. **Construye y levanta los contenedores:**
   ```bash
   docker-compose up --build
   ```

3. **Espera a ver este mensaje en los logs:**
   ```
   app_1  | INFO:     Uvicorn running on http://0.0.0.0:8000
   app_1  | INFO:     Application startup complete.
   ```

4. **¡Listo!** La API está disponible en:
   - API: http://localhost:8000
   - Documentación Swagger: http://localhost:8000/docs
   - Documentación ReDoc: http://localhost:8000/redoc

## 📡 Endpoints Disponibles

### Health Check
```
GET /
```
**Respuesta:**
```json
{
  "status": "ok"
}
```

### Listar todos los items
```
GET /items
```
**Respuesta:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "nombre": "Laptop",
    "descripcion": "MacBook Pro"
  }
]
```

### Crear un nuevo item
```
POST /items
Content-Type: application/json

{
  "nombre": "Laptop",
  "descripcion": "MacBook Pro"
}
```
**Respuesta (201):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "nombre": "Laptop",
  "descripcion": "MacBook Pro"
}
```

### Obtener un item por ID
```
GET /items/{item_id}
```
**Respuesta:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "nombre": "Laptop",
  "descripcion": "MacBook Pro"
}
```

## 🧪 Probar la API

### Opción 1: Swagger UI (Recomendado)

1. Abre tu navegador en: http://localhost:8000/docs
2. Verás todos los endpoints listados
3. Haz clic en un endpoint para expandirlo
4. Haz clic en "Try it out"
5. Llena los parámetros si es necesario
6. Haz clic en "Execute"
7. Ve la respuesta abajo

### Opción 2: curl (Terminal)

**Health check:**
```bash
curl http://localhost:8000/
```

**Listar items:**
```bash
curl http://localhost:8000/items
```

**Crear un item:**
```bash
curl -X POST http://localhost:8000/items \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Laptop", "descripcion": "MacBook Pro"}'
```

**Obtener item por ID:**
```bash
curl http://localhost:8000/items/507f1f77bcf86cd799439011
```

**Ver respuesta formateada:**
```bash
curl http://localhost:8000/items | python -m json.tool
```

## 🛠️ Comandos Útiles

### Levantar los servicios
```bash
docker-compose up
```

### Levantar en background (detached)
```bash
docker-compose up -d
```

### Ver logs
```bash
docker-compose logs -f
```

### Ver logs de un servicio específico
```bash
docker-compose logs -f app
docker-compose logs -f db
```

### Detener los servicios
```bash
docker-compose down
```

### Detener y eliminar volúmenes (borra datos de MongoDB)
```bash
docker-compose down -v
```

### Reconstruir después de cambios
```bash
docker-compose up --build
```

### Ejecutar comandos dentro del contenedor
```bash
docker-compose exec app bash
```

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Compose                       │
│                                                         │
│   ┌─────────────────┐      ┌─────────────────┐          │
│   │                 │      │                 │          │
│   │    FastAPI      │─────►│    MongoDB      │          │
│   │    (app)        │      │    (db)         │          │
│   │                 │      │                 │          │
│   │   Puerto 8000   │      │   Puerto 27017  │          │
│   │                 │      │                 │          │
│   └────────┬────────┘      └─────────────────┘          │
│            │                                            │
└────────────┼────────────────────────────────────────────┘
             │
             ▼
   http://localhost:8000
```

## 📦 Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para Python
- **MongoDB**: Base de datos NoSQL
- **Pymongo**: Driver de Python para MongoDB
- **Pydantic**: Validación de datos y modelos
- **Uvicorn**: Servidor ASGI
- **Docker**: Containerización
- **Docker Compose**: Orquestación de contenedores

## 🔧 Configuración

### Variables de Entorno

El proyecto usa las siguientes variables de entorno (configuradas en `docker-compose.yml`):

- `MONGO_URL`: URL de conexión a MongoDB (por defecto: `mongodb://db:27017`)

**Importante:** Dentro de Docker, usa `db` como hostname (nombre del servicio), no `localhost`.

## ❓ Troubleshooting

### Error: "Connection refused" al conectar a MongoDB
**Solución:** Verifica que uses `db` como hostname en la URL de conexión, no `localhost`:
```
mongodb://db:27017  ✅ Correcto
mongodb://localhost:27017  ❌ Incorrecto
```

### Error: "Port already in use"
**Solución:** Otro servicio está usando el puerto. Opciones:
- Detén el otro servicio
- Cambia el puerto en `docker-compose.yml`

### Cambios en código no se reflejan
**Solución:** Reconstruye la imagen:
```bash
docker-compose up --build
```

### Error: "Module not found"
**Solución:** Verifica que `requirements.txt` tenga todas las dependencias y reconstruye:
```bash
docker-compose up --build
```

## ✅ Criterios de Éxito

- ✅ `docker-compose up --build` levanta sin errores
- ✅ http://localhost:8000/docs muestra Swagger UI
- ✅ `curl http://localhost:8000/` retorna `{"status":"ok"}`
- ✅ Puedo crear un item con `POST /items`
- ✅ Puedo ver items creados con `GET /items`
- ✅ Los items persisten en MongoDB (no se pierden al refrescar)

## 🎓 Aprendizajes

Este proyecto demuestra:
- Cómo estructurar una API REST con FastAPI
- Integración con MongoDB usando Pymongo
- Uso de modelos Pydantic para validación
- Containerización con Docker
- Orquestación con Docker Compose
- Comunicación entre contenedores en una red Docker

## 📝 Notas

- Los datos de MongoDB se persisten en un volumen Docker
- La documentación automática está disponible en `/docs` (Swagger) y `/redoc`
- El proyecto usa Python 3.11
- MongoDB versión 7

---

**Autor:** Lucas-G-A  
**Fecha:** 2024

