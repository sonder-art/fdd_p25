# Ejercicio: API con FastAPI + MongoDB en Docker

## Objetivo

Montar el "Hello World" de una API usando:
- **FastAPI** como framework web
- **MongoDB** como base de datos
- **Docker Compose** para orquestar ambos contenedores

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA OBJETIVO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                         TU MÁQUINA                              │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                    Docker Compose                       │   │
│   │                                                         │   │
│   │   ┌─────────────────┐      ┌─────────────────┐          │   │
│   │   │                 │      │                 │          │   │
│   │   │    FastAPI      │─────►│    MongoDB      │          │   │
│   │   │    (app)        │      │    (db)         │          │   │
│   │   │                 │      │                 │          │   │
│   │   │   Puerto 8000   │      │   Puerto 27017  │          │   │
│   │   │                 │      │                 │          │   │
│   │   └────────┬────────┘      └─────────────────┘          │   │
│   │            │                                            │   │
│   └────────────┼────────────────────────────────────────────┘   │
│                │                                                │
│                ▼                                                │
│   http://localhost:8000                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Parte 1: Diseño de Infraestructura

### ¿Qué es Docker Compose?

Docker Compose permite definir y ejecutar **múltiples contenedores** como un solo servicio. En lugar de iniciar cada contenedor manualmente, defines todo en un archivo YAML.

```
┌─────────────────────────────────────────────────────────────────┐
│                 SIN DOCKER COMPOSE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Terminal 1:                                                    │
│  $ docker run -p 27017:27017 mongo                              │
│                                                                 │
│  Terminal 2:                                                    │
│  $ docker build -t mi-api .                                     │
│  $ docker run -p 8000:8000 --link mongo mi-api                  │
│                                                                 │
│  ❌ Tedioso, propenso a errores                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                 CON DOCKER COMPOSE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  $ docker-compose up                                            │
│                                                                 │
│  ✅ Un solo comando levanta todo                                │
│  ✅ Redes configuradas automáticamente                          │
│  ✅ Reproducible                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Estructura de Archivos a Crear

```
ejercicio_api/
│
├── docker-compose.yml      ← Orquestación de servicios
│
├── app/                    ← Tu aplicación FastAPI
│   ├── Dockerfile          ← Cómo construir la imagen
│   ├── requirements.txt    ← Dependencias Python
│   ├── main.py             ← Punto de entrada
│   └── models.py           ← Modelos Pydantic
│
└── README.md               ← Instrucciones
```

---

## Parte 2: Anatomía del docker-compose.yml

El archivo `docker-compose.yml` define los **servicios** (contenedores) que necesitas:

```
┌─────────────────────────────────────────────────────────────────┐
│               ESTRUCTURA DE DOCKER-COMPOSE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  version: "3.8"                                                 │
│  │                                                              │
│  └── Versión del formato de Docker Compose                      │
│                                                                 │
│  services:                                                      │
│  │                                                              │
│  ├── app:                  ← Servicio 1: Tu API                 │
│  │   ├── build: ./app      ← Construir desde Dockerfile         │
│  │   ├── ports:            ← Mapeo de puertos                   │
│  │   │   └── "8000:8000"   ← host:contenedor                    │
│  │   ├── depends_on:       ← Esperar a que db inicie            │
│  │   │   └── db                                                 │
│  │   └── environment:      ← Variables de entorno               │
│  │       └── MONGO_URL     ← Conexión a MongoDB                 │
│  │                                                              │
│  └── db:                   ← Servicio 2: MongoDB                │
│      ├── image: mongo      ← Usar imagen oficial                │
│      └── ports:                                                 │
│          └── "27017:27017"                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Comunicación entre Contenedores

```
┌─────────────────────────────────────────────────────────────────┐
│              RED INTERNA DE DOCKER COMPOSE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Docker Compose crea una RED INTERNA automáticamente            │
│                                                                 │
│   ┌─────────────────────────────────────────────────────┐       │
│   │                   Red: mi_app_default               │       │
│   │                                                     │       │
│   │   ┌─────────┐                    ┌─────────┐        │       │
│   │   │   app   │ ────────────────── │   db    │        │       │
│   │   │         │   mongodb://db:27017         │        │       │
│   │   └─────────┘        │           └─────────┘        │       │
│   │                      │                              │       │
│   │   Los contenedores se pueden encontrar              │       │
│   │   por su NOMBRE de servicio                         │       │
│   │                                                     │       │
│   └─────────────────────────────────────────────────────┘       │
│                                                                 │
│   Desde "app" puedes conectar a MongoDB usando:                 │
│   mongodb://db:27017                                            │
│            │                                                    │
│            └── "db" es el nombre del servicio                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Parte 3: Anatomía del Dockerfile

El Dockerfile define cómo construir la imagen de tu API:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCKERFILE EXPLICADO                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FROM python:3.11-slim                                          │
│  │                                                              │
│  └── Imagen base: Python 3.11 versión ligera                    │
│                                                                 │
│  WORKDIR /app                                                   │
│  │                                                              │
│  └── Directorio de trabajo dentro del contenedor                │
│                                                                 │
│  COPY requirements.txt .                                        │
│  │                                                              │
│  └── Copiar archivo de dependencias                             │
│                                                                 │
│  RUN pip install --no-cache-dir -r requirements.txt             │
│  │                                                              │
│  └── Instalar dependencias                                      │
│                                                                 │
│  COPY . .                                                       │
│  │                                                              │
│  └── Copiar todo el código                                      │
│                                                                 │
│  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
│  │                                                              │
│  └── Comando para iniciar la aplicación                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Dependencias Mínimas (requirements.txt)

```
fastapi          ← El framework
uvicorn          ← El servidor ASGI
pymongo          ← Driver para MongoDB
motor            ← Driver asíncrono para MongoDB (opcional)
```

---

## Parte 4: Especificación de la API

### Endpoints a Implementar

Para el ejercicio, implementa estos endpoints mínimos:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENDPOINTS DEL EJERCICIO                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GET  /                                                         │
│       └── Health check: { "status": "ok" }                      │
│                                                                 │
│  GET  /items                                                    │
│       └── Listar todos los items de MongoDB                     │
│                                                                 │
│  POST /items                                                    │
│       └── Crear un nuevo item                                   │
│       └── Body: { "nombre": "...", "descripcion": "..." }       │
│                                                                 │
│  GET  /items/{id}                                               │
│       └── Obtener un item por ID                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Modelos Pydantic Sugeridos

```
┌─────────────────────────────────────────────────────────────────┐
│                    MODELOS PYDANTIC                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Para CREAR un item (input):                                    │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ItemCreate                                             │    │
│  │  ├── nombre: str       (obligatorio)                    │    │
│  │  └── descripcion: str  (opcional, default vacío)        │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  Para RESPONDER con un item (output):                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ItemResponse                                           │    │
│  │  ├── id: str           (generado por MongoDB)           │    │
│  │  ├── nombre: str                                        │    │
│  │  └── descripcion: str                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Parte 5: Levantar el Proyecto

### Comandos Esenciales

```
┌─────────────────────────────────────────────────────────────────┐
│                 COMANDOS DOCKER COMPOSE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  # Construir y levantar (primera vez o después de cambios)      │
│  docker-compose up --build                                      │
│                                                                 │
│  # Levantar (si ya está construido)                             │
│  docker-compose up                                              │
│                                                                 │
│  # Levantar en background (no bloquea terminal)                 │
│  docker-compose up -d                                           │
│                                                                 │
│  # Ver logs                                                     │
│  docker-compose logs -f                                         │
│                                                                 │
│  # Detener todo                                                 │
│  docker-compose down                                            │
│                                                                 │
│  # Detener y eliminar volúmenes (borra datos de MongoDB)        │
│  docker-compose down -v                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ¿Cómo sé que funciona?

```
┌─────────────────────────────────────────────────────────────────┐
│                    VERIFICACIÓN                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Cuando veas esto en los logs, la API está lista:               │
│                                                                 │
│  app_1  | INFO:     Uvicorn running on http://0.0.0.0:8000      │
│  app_1  | INFO:     Application startup complete.               │
│                                                                 │
│  Ahora puedes acceder a:                                        │
│  • http://localhost:8000       → Tu API                         │
│  • http://localhost:8000/docs  → Documentación Swagger          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Parte 6: Probando la API

### Opción 1: Swagger UI (Navegador)

La forma más fácil de probar tu API:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SWAGGER UI                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Abre el navegador                                           │
│  2. Ve a: http://localhost:8000/docs                            │
│  3. Verás todos tus endpoints listados                          │
│  4. Click en un endpoint para expandirlo                        │
│  5. Click en "Try it out"                                       │
│  6. Llena los parámetros si los hay                             │
│  7. Click en "Execute"                                          │
│  8. Ve la respuesta abajo                                       │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  POST /items         [Try it out]                         │  │
│  │                                                           │  │
│  │  Request body:                                            │  │
│  │  ┌───────────────────────────────────────────────────┐    │  │
│  │  │ {                                                 │    │  │
│  │  │   "nombre": "Mi primer item",                     │    │  │
│  │  │   "descripcion": "Creado desde Swagger"           │    │  │
│  │  │ }                                                 │    │  │
│  │  └───────────────────────────────────────────────────┘    │  │
│  │                                                           │  │
│  │  [Execute]                                                │  │
│  │                                                           │  │
│  │  Response:                                                │  │
│  │  Code: 201                                                │  │
│  │  ┌───────────────────────────────────────────────────┐    │  │
│  │  │ {                                                 │    │  │
│  │  │   "id": "507f1f77bcf86cd799439011",               │    │  │
│  │  │   "nombre": "Mi primer item",                     │    │  │
│  │  │   "descripcion": "Creado desde Swagger"           │    │  │
│  │  │ }                                                 │    │  │
│  │  └───────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Opción 2: curl (Terminal)

`curl` es una herramienta de línea de comandos para hacer peticiones HTTP:

```
┌─────────────────────────────────────────────────────────────────┐
│                    EJEMPLOS CON CURL                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  # Health check                                                 │
│  curl http://localhost:8000/                                    │
│                                                                 │
│  Respuesta: {"status":"ok"}                                     │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  # Listar items                                                 │
│  curl http://localhost:8000/items                               │
│                                                                 │
│  Respuesta: []   (vacío al inicio)                              │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  # Crear un item (POST con JSON)                                │
│  curl -X POST http://localhost:8000/items \                     │
│       -H "Content-Type: application/json" \                     │
│       -d '{"nombre": "Laptop", "descripcion": "MacBook Pro"}'   │
│                                                                 │
│  Respuesta: {"id":"...","nombre":"Laptop","descripcion":"..."}  │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  # Obtener item por ID                                          │
│  curl http://localhost:8000/items/507f1f77bcf86cd799439011      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  # Ver respuesta formateada (pretty print)                      │
│  curl http://localhost:8000/items | python -m json.tool         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Anatomía de curl

```
curl -X POST http://localhost:8000/items \
     │   │                │
     │   │                └── URL del endpoint
     │   └── Método HTTP
     └── Ejecutar curl

     -H "Content-Type: application/json" \
     │       │
     │       └── Valor del header
     └── Header (cabecera)

     -d '{"nombre": "Test"}'
     │       │
     │       └── El JSON a enviar
     └── Data (cuerpo de la petición)
```

---

## Parte 7: Instrucciones del Ejercicio

### Lo que debes hacer con Cursor

```
┌─────────────────────────────────────────────────────────────────┐
│                    TAREAS A COMPLETAR                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ESTRUCTURA                                                  │
│     □ Crear la carpeta del proyecto                             │
│     □ Crear los archivos necesarios                             │
│                                                                 │
│  2. DOCKER                                                      │
│     □ Escribir el Dockerfile para la app                        │
│     □ Escribir el docker-compose.yml                            │
│     □ Definir el requirements.txt                               │
│                                                                 │
│  3. CÓDIGO FASTAPI                                              │
│     □ Crear modelos Pydantic (ItemCreate, ItemResponse)         │
│     □ Implementar endpoint GET /                                │
│     □ Implementar endpoint GET /items                           │
│     □ Implementar endpoint POST /items                          │
│     □ Implementar endpoint GET /items/{id}                      │
│     □ Conectar con MongoDB                                      │
│                                                                 │
│  4. VERIFICACIÓN                                                │
│     □ Levantar con docker-compose up --build                    │
│     □ Probar endpoints con Swagger UI                           │
│     □ Probar endpoints con curl                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Tips para usar Cursor

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUGERENCIAS                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Puedes pedirle a Cursor cosas como:                            │
│                                                                 │
│  "Crea un Dockerfile para una aplicación FastAPI"               │
│                                                                 │
│  "Escribe un docker-compose con FastAPI y MongoDB"              │
│                                                                 │
│  "Crea un modelo Pydantic para un Item con nombre y descripcion"│
│                                                                 │
│  "Implementa un endpoint POST que guarde en MongoDB"            │
│                                                                 │
│  "¿Por qué no puedo conectar a MongoDB?" (si tienes errores)    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Parte 8: Troubleshooting Común

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROBLEMAS COMUNES                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ "Connection refused" al conectar a MongoDB                  │
│  ✅ Verifica que uses "db" como host, no "localhost"            │
│     mongodb://db:27017  (no mongodb://localhost:27017)          │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ❌ "Port already in use"                                       │
│  ✅ Otro servicio usa el puerto. Cambia el puerto en            │
│     docker-compose.yml o detén el otro servicio                 │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ❌ Cambios en código no se reflejan                            │
│  ✅ Reconstruye: docker-compose up --build                      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ❌ "Module not found" para pymongo/fastapi                     │
│  ✅ Verifica que requirements.txt tenga todas las dependencias  │
│     y reconstruye la imagen                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Diagrama de Flujo Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FLUJO COMPLETO DEL EJERCICIO                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   TÚ                                                                        │
│    │                                                                        │
│    │ curl -X POST /items -d '{"nombre":"Test"}'                             │
│    │                                                                        │
│    ▼                                                                        │
│ ┌─────────┐     ┌──────────────────────────────────────────────────────┐    │
│ │ Tu      │     │                  Docker Compose                      │    │
│ │Terminal │────►│                                                      │    │
│ └─────────┘     │  ┌────────────────────────────────────────────────┐  │    │
│                 │  │              Contenedor: app                   │  │    │
│    localhost    │  │                                                │  │    │
│    :8000        │  │  ┌─────────┐  ┌─────────┐  ┌─────────────┐     │  │    │
│       │         │  │  │ Uvicorn │─►│ FastAPI │─►│  Tu código  │     │  │    │
│       │         │  │  └─────────┘  └─────────┘  └──────┬──────┘     │  │    │
│       │         │  │       │                          │             │  │    │
│       └─────────│──│───────┘                          │             │  │    │
│                 │  └──────────────────────────────────┼─────────────┘  │    │
│                 │                                     │                │    │
│                 │                              mongodb://db:27017      │    │
│                 │                                     │                │    │
│                 │  ┌──────────────────────────────────▼─────────────┐  │    │
│                 │  │              Contenedor: db                    │  │    │
│                 │  │                                                │  │    │
│                 │  │              ┌──────────┐                      │  │    │
│                 │  │              │ MongoDB  │                      │  │    │
│                 │  │              │  :27017  │                      │  │    │
│                 │  │              └──────────┘                      │  │    │
│                 │  │                                                │  │    │
│                 │  └────────────────────────────────────────────────┘  │    │
│                 │                                                      │    │
│                 └──────────────────────────────────────────────────────┘    │
│                                                                             │
│   La respuesta viaja de regreso por el mismo camino                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Criterios de Éxito

```
┌─────────────────────────────────────────────────────────────────┐
│                    ¿CÓMO SÉ QUE TERMINÉ?                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ docker-compose up --build levanta sin errores               │
│                                                                 │
│  ✅ http://localhost:8000/docs muestra Swagger UI               │
│                                                                 │
│  ✅ curl http://localhost:8000/ retorna {"status":"ok"}         │
│                                                                 │
│  ✅ Puedo crear un item con POST /items                         │
│                                                                 │
│  ✅ Puedo ver items creados con GET /items                      │
│                                                                 │
│  ✅ Los items persisten en MongoDB (no se pierden al refrescar) │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Extensiones Opcionales

Si terminas temprano, puedes agregar:

- `DELETE /items/{id}` - Eliminar un item
- `PUT /items/{id}` - Actualizar un item completo
- Validaciones adicionales en Pydantic (longitud mínima, etc.)
- Variables de entorno para configuración
- Volúmenes para persistir datos de MongoDB

