# 📡 APIs - Guía Completa

## Contenido

Esta carpeta contiene una introducción detallada al mundo de las APIs (Application Programming Interfaces).

### Documentos

| Documento | Contenido |
|-----------|-----------|
| [01_introduccion_apis.md](./01_introduccion_apis.md) | Conceptos básicos, cliente-servidor, HTTPS, contratos y boundaries |
| [02_tipos_de_apis.md](./02_tipos_de_apis.md) | REST, GraphQL, gRPC, WebSockets, SOAP - comparativas y ejemplos |
| [03_mcp_y_patrones.md](./03_mcp_y_patrones.md) | Model Context Protocol, patrones de diseño, autenticación |
| [04_fastapi_fundamentos.md](./04_fastapi_fundamentos.md) | FastAPI, Uvicorn, Pydantic - conceptos y anatomía |
| [05_ejercicio_docker_fastapi.md](./05_ejercicio_docker_fastapi.md) | 🛠️ Ejercicio práctico: FastAPI + MongoDB con Docker Compose |

---

## Mapa Conceptual

```
                    ┌─────────────────────────────────────────────┐
                    │              CONCEPTOS API                  │
                    └─────────────────────────────────────────────┘
                                         │
         ┌───────────────────────────────┼───────────────────────────────┐
         │                               │                               │
         ▼                               ▼                               ▼
┌─────────────────┐             ┌─────────────────┐             ┌─────────────────┐
│   FUNDAMENTOS   │             │     TIPOS       │             │   PATRONES      │
├─────────────────┤             ├─────────────────┤             ├─────────────────┤
│ • Cliente/Serv  │             │ • REST          │             │ • Paginación    │
│ • HTTP/HTTPS    │             │ • GraphQL       │             │ • Versionado    │
│ • Contrato      │             │ • gRPC          │             │ • Rate Limiting │
│ • Boundary      │             │ • WebSocket     │             │ • Autenticación │
│ • Métodos HTTP  │             │ • SOAP          │             │ • Circuit Break │
│ • Status Codes  │             │ • MCP           │             │ • Idempotencia  │
└─────────────────┘             └─────────────────┘             └─────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    │                                         │
                    ▼                                         ▼
           ┌─────────────────┐                       ┌─────────────────┐
           │    FASTAPI      │                       │   EJERCICIO     │
           ├─────────────────┤                       ├─────────────────┤
           │ • Uvicorn       │                       │ • Docker Compose│
           │ • Decoradores   │                       │ • FastAPI + Mongo│
           │ • Pydantic      │                       │ • curl / Swagger│
           │ • Swagger UI    │                       │ • Práctica      │
           └─────────────────┘                       └─────────────────┘
```

---

## Prerrequisitos

Para aprovechar este material, es útil tener conocimientos básicos de:

- Conceptos de redes (qué es internet, URLs)
- Formatos de datos (JSON, XML)
- Programación básica (para entender pseudocódigo)

---

## Cómo usar este material

### Ruta de Aprendizaje

1. **Documento 01** - Establece las bases conceptuales (API, contratos, HTTP)
2. **Documento 02** - Explora los tipos de APIs (REST, GraphQL, gRPC, etc.)
3. **Documento 03** - Profundiza en patrones y MCP
4. **Documento 04** - Aprende los fundamentos de FastAPI
5. **Documento 05** - 🛠️ **Ejercicio práctico** con Docker Compose

### Sobre el Ejercicio (Documento 05)

El ejercicio está diseñado para completarse con ayuda de **Cursor**. El documento provee:
- Diseño de arquitectura (FastAPI + MongoDB)
- Especificación de endpoints
- Guía de Docker Compose
- Instrucciones de testing (curl + Swagger UI)

**No incluye código completo** - el objetivo es que uses Cursor para implementar siguiendo las especificaciones.

Cada documento incluye:
- 📝 Definiciones técnicas
- 🎯 Analogías para facilitar comprensión  
- 📊 Diagramas ASCII
- 💡 Ejemplos prácticos (JSON, YAML)
- ⚖️ Comparativas (pros/cons)

---

## Quick Reference

### ¿Qué tipo de API usar?

```
¿Necesitas...?                          → Usa...
────────────────────────────────────────────────────
API pública, simple                     → REST
Flexibilidad en queries del frontend    → GraphQL
Alto rendimiento entre servicios        → gRPC
Comunicación en tiempo real             → WebSocket
Conectar IA con herramientas            → MCP
Sistema enterprise legacy               → SOAP
```

### Códigos HTTP más importantes

```
200 OK          → Todo bien
201 Created     → Recurso creado
400 Bad Request → Error del cliente
401 Unauthorized→ No autenticado
403 Forbidden   → Sin permiso
404 Not Found   → No existe
429 Too Many    → Rate limit
500 Server Error→ Error del servidor
```

