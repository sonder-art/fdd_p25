# FastAPI: Fundamentos

## ¿Qué es FastAPI?

**FastAPI** es un framework moderno de Python para construir APIs. Su nombre viene de dos características principales:

1. **Fast** (Rápido): Alto rendimiento, comparable con Node.js y Go
2. **API**: Diseñado específicamente para crear APIs

```
┌─────────────────────────────────────────────────────────────────┐
│                    ¿Por qué FastAPI?                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ Fácil de aprender                                           │
│  ✅ Documentación automática (Swagger UI)                       │
│  ✅ Validación automática de datos                              │
│  ✅ Tipado estático con Python type hints                       │
│  ✅ Asíncrono por defecto                                       │
│  ✅ Basado en estándares (OpenAPI, JSON Schema)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Analogía: FastAPI como un Restaurante

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Cliente (Browser/App)                                         │
│        │                                                        │
│        │ "Quiero ordenar"                                       │
│        ▼                                                        │
│   ┌─────────────┐                                               │
│   │   Uvicorn   │  ← El HOST/Recepcionista                      │
│   │  (Servidor) │    Recibe a los clientes                      │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌─────────────┐                                               │
│   │   FastAPI   │  ← El MESERO                                  │
│   │ (Framework) │    Toma tu orden, te la trae                  │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌─────────────┐                                               │
│   │  Pydantic   │  ← El MENÚ                                    │
│   │  (Modelos)  │    Define qué puedes pedir y cómo             │
│   └──────┬──────┘                                               │
│          │                                                      │
│          ▼                                                      │
│   ┌─────────────┐                                               │
│   │  Tu código  │  ← La COCINA                                  │
│   │  (Lógica)   │    Prepara lo que pediste                     │
│   └─────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Los Tres Componentes Clave

### 1. Uvicorn - El Servidor

**Uvicorn** es un servidor ASGI (Asynchronous Server Gateway Interface). Es quien realmente "escucha" las peticiones HTTP y las pasa a FastAPI.

```
┌─────────────────────────────────────────────────────────────────┐
│                      UVICORN                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Internet ────► Puerto 8000 ────► Uvicorn ────► FastAPI         │
│                                                                 │
│  • Escucha en un puerto (ej: 8000)                              │
│  • Recibe conexiones HTTP                                       │
│  • Pasa las peticiones a tu aplicación FastAPI                  │
│  • Devuelve las respuestas al cliente                           │
│                                                                 │
│  Comando típico:                                                │
│  uvicorn main:app --host 0.0.0.0 --port 8000                    │
│           │   │                                                 │
│           │   └── nombre de la variable FastAPI                 │
│           └── nombre del archivo (main.py)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Analogía**: Uvicorn es como el edificio del restaurante. Sin edificio, no hay donde poner el restaurante (FastAPI).

### 2. FastAPI - El Framework

FastAPI es el framework que define **cómo manejar** cada petición. Usa **decoradores** para asociar funciones con rutas HTTP.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECORADORES EN FASTAPI                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Un decorador es una "etiqueta" que le pones a una función      │
│  para decirle a FastAPI: "cuando llegue una petición a esta     │
│  ruta, ejecuta esta función"                                    │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │                                                        │     │
│  │   @app.get("/usuarios")      ← Decorador               │     │
│  │   def obtener_usuarios():    ← Función                 │     │
│  │       return [...]           ← Lo que devuelve         │     │
│  │                                                        │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                 │
│  Cuando alguien hace GET /usuarios, se ejecuta esa función      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Decoradores disponibles (corresponden a métodos HTTP):**

```
@app.get("/ruta")      → Para leer datos
@app.post("/ruta")     → Para crear datos
@app.put("/ruta")      → Para reemplazar datos
@app.patch("/ruta")    → Para modificar parcialmente
@app.delete("/ruta")   → Para eliminar datos
```

### 3. Pydantic - Los Modelos de Datos

**Pydantic** es una librería que valida y serializa datos. En FastAPI, defines **modelos** que describen la estructura de tus datos.

```
┌─────────────────────────────────────────────────────────────────┐
│                       PYDANTIC                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Define la FORMA de tus datos:                                  │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐     │
│  │                                                        │     │
│  │   class Usuario(BaseModel):                            │     │
│  │       nombre: str           ← Debe ser texto           │     │
│  │       edad: int             ← Debe ser número entero   │     │
│  │       email: str            ← Debe ser texto           │     │
│  │       activo: bool = True   ← Opcional, default True   │     │
│  │                                                        │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                 │
│  Pydantic automáticamente:                                      │
│  • Valida que los datos tengan el tipo correcto                 │
│  • Convierte tipos cuando es posible ("123" → 123)              │
│  • Retorna errores claros si algo está mal                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Ejemplo de validación automática:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDACIÓN AUTOMÁTICA                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Petición válida:                                               │
│  {                                                              │
│    "nombre": "Juan",                                            │
│    "edad": 25,               ✅ Pasa validación                 │
│    "email": "juan@mail.com"                                     │
│  }                                                              │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Petición inválida:                                             │
│  {                                                              │
│    "nombre": "Juan",                                            │
│    "edad": "veinticinco",    ❌ Error: edad debe ser int        │
│    "email": "juan@mail.com"                                     │
│  }                                                              │
│                                                                 │
│  FastAPI responde automáticamente con:                          │
│  {                                                              │
│    "detail": [                                                  │
│      {                                                          │
│        "loc": ["body", "edad"],                                 │
│        "msg": "value is not a valid integer",                   │
│        "type": "type_error.integer"                             │
│      }                                                          │
│    ]                                                            │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Anatomía de un Endpoint

```
┌─────────────────────────────────────────────────────────────────┐
│                  ESTRUCTURA DE UN ENDPOINT                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                                                                 │
│   @app.post("/usuarios")                                        │
│   │    │        │                                               │
│   │    │        └── RUTA: dónde escuchar                        │
│   │    └── MÉTODO: qué tipo de petición                         │
│   └── app: tu instancia de FastAPI                              │
│                                                                 │
│   def crear_usuario(usuario: Usuario) -> UsuarioResponse:       │
│   │        │              │                    │                │
│   │        │              │                    └── SALIDA       │
│   │        │              └── ENTRADA (Pydantic model)          │
│   │        └── NOMBRE de la función (para documentación)        │
│   └── Definición de función                                     │
│                                                                 │
│       # ... lógica aquí ...                                     │
│       return UsuarioResponse(...)                               │
│              │                                                  │
│              └── Lo que devuelves al cliente                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tipos de Parámetros

FastAPI obtiene parámetros de diferentes lugares:

```
┌─────────────────────────────────────────────────────────────────┐
│                 FUENTES DE PARÁMETROS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. PATH PARAMETERS (en la URL)                                 │
│     GET /usuarios/123                                           │
│                  │                                              │
│                  └── id = 123                                   │
│                                                                 │
│     @app.get("/usuarios/{id}")                                  │
│     def obtener_usuario(id: int):                               │
│         ...                                                     │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  2. QUERY PARAMETERS (después del ?)                            │
│     GET /usuarios?limite=10&pagina=2                            │
│                   │          │                                  │
│                   │          └── pagina = 2                     │
│                   └── limite = 10                               │
│                                                                 │
│     @app.get("/usuarios")                                       │
│     def listar_usuarios(limite: int = 10, pagina: int = 1):     │
│         ...                                                     │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  3. REQUEST BODY (en el cuerpo, para POST/PUT)                  │
│     POST /usuarios                                              │
│     Body: { "nombre": "Juan", "edad": 25 }                      │
│                                                                 │
│     @app.post("/usuarios")                                      │
│     def crear_usuario(usuario: UsuarioCreate):                  │
│         ...                    │                                │
│                                └── Pydantic model               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Documentación Automática (Swagger UI)

Una de las características más poderosas de FastAPI es la **documentación automática**.

```
┌─────────────────────────────────────────────────────────────────┐
│              DOCUMENTACIÓN AUTOMÁTICA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  FastAPI genera automáticamente:                                │
│                                                                 │
│  http://localhost:8000/docs      ← Swagger UI (interactiva)     │
│  http://localhost:8000/redoc     ← ReDoc (documentación)        │
│  http://localhost:8000/openapi.json ← Especificación OpenAPI    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    SWAGGER UI                           │    │
│  │                                                         │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │ GET    /usuarios        Listar usuarios         │    │    │
│  │  ├─────────────────────────────────────────────────┤    │    │
│  │  │ POST   /usuarios        Crear usuario           │    │    │
│  │  ├─────────────────────────────────────────────────┤    │    │
│  │  │ GET    /usuarios/{id}   Obtener usuario         │    │    │
│  │  ├─────────────────────────────────────────────────┤    │    │
│  │  │ DELETE /usuarios/{id}   Eliminar usuario        │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  │                                                         │    │
│  │  Cada endpoint se puede probar directamente desde       │    │
│  │  el navegador con el botón "Try it out"                 │    │
│  │                                                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Estructura Mínima de un Proyecto FastAPI

```
mi_proyecto/
│
├── main.py              ← Punto de entrada, define la app
├── models.py            ← Modelos Pydantic (schemas)
├── requirements.txt     ← Dependencias
└── Dockerfile           ← Para containerización
```

### Flujo de una Petición

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     FLUJO DE UNA PETICIÓN                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Cliente                                                                │
│     │                                                                   │
│     │  POST /usuarios                                                   │
│     │  { "nombre": "Ana", "edad": 30 }                                  │
│     │                                                                   │
│     ▼                                                                   │
│  ┌─────────┐                                                            │
│  │ Uvicorn │ ─── Recibe HTTP ───┐                                       │
│  └─────────┘                    │                                       │
│                                 ▼                                       │
│                          ┌───────────┐                                  │
│                          │  FastAPI  │                                  │
│                          └─────┬─────┘                                  │
│                                │                                        │
│         ┌──────────────────────┼──────────────────────┐                 │
│         ▼                      ▼                      ▼                 │
│   ┌───────────┐         ┌───────────┐         ┌───────────┐             │
│   │  Routing  │         │ Pydantic  │         │ Tu función│             │
│   │           │         │           │         │           │             │
│   │ ¿Cuál     │ ──────► │ Validar   │ ──────► │ Ejecutar  │             │
│   │ endpoint? │         │ datos     │         │ lógica    │             │
│   └───────────┘         └───────────┘         └─────┬─────┘             │
│                                                     │                   │
│                                                     ▼                   │
│                                              ┌───────────┐              │
│                                              │ Respuesta │              │
│                                              │   JSON    │              │
│                                              └─────┬─────┘              │
│                                                    │                    │
│     ◄──────────────────────────────────────────────┘                    │
│  Cliente recibe respuesta                                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Resumen de Conceptos

| Componente | Qué es | Responsabilidad |
|------------|--------|-----------------|
| **Uvicorn** | Servidor ASGI | Escuchar puerto, manejar conexiones |
| **FastAPI** | Framework web | Routing, manejar peticiones/respuestas |
| **Pydantic** | Validación de datos | Definir esquemas, validar entrada/salida |
| **Decorador** | @app.get, @app.post... | Asociar función con ruta HTTP |
| **Swagger UI** | Documentación | Probar API desde el navegador |

---

## Siguiente Documento

En el siguiente documento verás el **diseño de infraestructura** para montar FastAPI con MongoDB usando Docker Compose.

