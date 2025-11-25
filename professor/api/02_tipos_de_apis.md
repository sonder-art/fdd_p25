# Tipos de APIs

## Panorama General

```
┌─────────────────────────────────────────────────────────────────────┐
│                      TIPOS DE APIs                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Basadas en HTTP:              Otros protocolos:                   │
│   ┌─────────────┐               ┌─────────────┐                     │
│   │    REST     │               │    gRPC     │                     │
│   └─────────────┘               └─────────────┘                     │
│   ┌─────────────┐               ┌─────────────┐                     │
│   │  GraphQL    │               │  WebSocket  │                     │
│   └─────────────┘               └─────────────┘                     │
│   ┌─────────────┐               ┌─────────────┐                     │
│   │    SOAP     │               │     MCP     │                     │
│   └─────────────┘               └─────────────┘                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. REST (Representational State Transfer)

### ¿Qué es?

REST es un **estilo arquitectónico** (no un protocolo) para diseñar APIs web. Es el más común hoy en día.

### Principios Fundamentales

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRINCIPIOS REST                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CLIENTE-SERVIDOR                                            │
│     → Separación de responsabilidades                           │
│                                                                 │
│  2. SIN ESTADO (Stateless)                                      │
│     → Cada petición contiene TODA la información necesaria      │
│     → El servidor no recuerda peticiones anteriores             │
│                                                                 │
│  3. CACHEABLE                                                   │
│     → Las respuestas pueden guardarse para reutilizar           │
│                                                                 │
│  4. INTERFAZ UNIFORME                                           │
│     → Recursos identificados por URLs                           │
│     → Operaciones con métodos HTTP estándar                     │
│                                                                 │
│  5. SISTEMA EN CAPAS                                            │
│     → Cliente no sabe si habla directamente con el servidor     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Concepto de Recurso

En REST, todo es un **recurso**. Un recurso es cualquier cosa que puedas nombrar:
- Un usuario
- Una orden de compra
- Una foto
- Una lista de productos

Cada recurso tiene una **URL única**:

```
/usuarios           → Colección de usuarios
/usuarios/123       → Usuario específico con ID 123
/usuarios/123/fotos → Fotos del usuario 123
```

### Ejemplo de API REST

```
RECURSO: Libros de una biblioteca

┌─────────────────────────────────────────────────────────────────┐
│ Operación          │ Método │ Ruta              │ Descripción   │
├─────────────────────────────────────────────────────────────────┤
│ Listar libros      │ GET    │ /libros           │ Todos         │
│ Obtener un libro   │ GET    │ /libros/42        │ Solo el 42    │
│ Crear libro        │ POST   │ /libros           │ Nuevo libro   │
│ Actualizar libro   │ PUT    │ /libros/42        │ Reemplazar 42 │
│ Modificar libro    │ PATCH  │ /libros/42        │ Cambio parcial│
│ Eliminar libro     │ DELETE │ /libros/42        │ Borrar 42     │
└─────────────────────────────────────────────────────────────────┘
```

### Ejemplo de Petición y Respuesta

**Petición: Crear un nuevo libro**
```
POST /libros
Content-Type: application/json

{
  "titulo": "Cien años de soledad",
  "autor": "Gabriel García Márquez",
  "año": 1967,
  "isbn": "978-0060883287"
}
```

**Respuesta exitosa:**
```
HTTP/1.1 201 Created
Location: /libros/42

{
  "id": 42,
  "titulo": "Cien años de soledad",
  "autor": "Gabriel García Márquez",
  "año": 1967,
  "isbn": "978-0060883287",
  "creado_en": "2024-01-15T10:30:00Z"
}
```

### Pros y Contras de REST

| ✅ Ventajas | ❌ Desventajas |
|-------------|----------------|
| Simple de entender | Over-fetching (traes más datos de los necesarios) |
| Usa estándares HTTP existentes | Under-fetching (necesitas múltiples peticiones) |
| Cacheable por defecto | No hay un estándar estricto (cada quien lo implementa diferente) |
| Escalable | Versionado puede ser problemático |
| Amplia adopción y herramientas | |

### Over-fetching y Under-fetching

```
OVER-FETCHING: Traes demasiado
┌─────────────────────────────────────────────────────────────┐
│  Solo quieres el nombre del usuario...                      │
│                                                             │
│  GET /usuarios/123                                          │
│                                                             │
│  Respuesta:                                                 │
│  {                                                          │
│    "id": 123,                                               │
│    "nombre": "Juan",        ← Solo necesitas esto           │
│    "email": "juan@...",     ← Datos extra                   │
│    "direccion": {...},      ← Datos extra                   │
│    "telefono": "...",       ← Datos extra                   │
│    "historial": [...]       ← Datos extra (pesado!)         │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘

UNDER-FETCHING: Necesitas hacer múltiples peticiones
┌─────────────────────────────────────────────────────────────┐
│  Quieres usuario + sus pedidos + sus reseñas                │
│                                                             │
│  1. GET /usuarios/123          ← Primera petición           │
│  2. GET /usuarios/123/pedidos  ← Segunda petición           │
│  3. GET /usuarios/123/reseñas  ← Tercera petición           │
│                                                             │
│  ¡3 roundtrips al servidor!                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. GraphQL

### ¿Qué es?

GraphQL es un **lenguaje de consulta para APIs** desarrollado por Facebook. Permite al cliente especificar exactamente qué datos necesita.

### Diferencia Clave con REST

```
REST: El servidor decide qué datos devolver
┌──────────┐                              ┌──────────┐
│ Cliente  │ ──── GET /usuario/123 ─────► │ Servidor │
└──────────┘                              └──────────┘
                     │
                     ▼
            Servidor decide: "Te mando TODO"

GraphQL: El cliente decide qué datos quiere
┌──────────┐                              ┌──────────┐
│ Cliente  │ ── "Quiero solo nombre" ───► │ Servidor │
└──────────┘                              └──────────┘
                     │
                     ▼
            Servidor: "Ok, solo el nombre"
```

### Anatomía de GraphQL

```
┌─────────────────────────────────────────────────────────────┐
│                      GRAPHQL                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  UN SOLO ENDPOINT: POST /graphql                            │
│                                                             │
│  TRES OPERACIONES:                                          │
│  ┌─────────────────┐                                        │
│  │ Query           │ → Leer datos (como GET)                │
│  └─────────────────┘                                        │
│  ┌─────────────────┐                                        │
│  │ Mutation        │ → Modificar datos (como POST/PUT)      │
│  └─────────────────┘                                        │
│  ┌─────────────────┐                                        │
│  │ Subscription    │ → Escuchar cambios en tiempo real      │
│  └─────────────────┘                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Ejemplo de Query GraphQL

**Petición:**
```
POST /graphql

{
  "query": "
    query {
      usuario(id: 123) {
        nombre
        email
        pedidos(limite: 5) {
          id
          total
          fecha
        }
      }
    }
  "
}
```

**Respuesta:**
```json
{
  "data": {
    "usuario": {
      "nombre": "Juan Pérez",
      "email": "juan@correo.com",
      "pedidos": [
        { "id": 1, "total": 150.00, "fecha": "2024-01-10" },
        { "id": 2, "total": 89.50, "fecha": "2024-01-08" }
      ]
    }
  }
}
```

### Schema: El Contrato de GraphQL

GraphQL usa un **schema** fuertemente tipado:

```
# Definición del schema (pseudocódigo)

type Usuario {
  id: ID!
  nombre: String!
  email: String!
  edad: Int
  pedidos: [Pedido!]!
}

type Pedido {
  id: ID!
  productos: [Producto!]!
  total: Float!
  fecha: String!
}

type Query {
  usuario(id: ID!): Usuario
  usuarios(limite: Int): [Usuario!]!
}

type Mutation {
  crearUsuario(nombre: String!, email: String!): Usuario!
  eliminarUsuario(id: ID!): Boolean!
}
```

### Pros y Contras de GraphQL

| ✅ Ventajas | ❌ Desventajas |
|-------------|----------------|
| Sin over-fetching ni under-fetching | Más complejo de implementar |
| Un solo endpoint | Difícil de cachear (todo es POST) |
| Tipado fuerte (schema) | Curva de aprendizaje |
| Excelente para frontends | Puede exponer demasiado si no hay control |
| Introspección (API auto-documentada) | Queries complejas pueden ser costosas |

---

## 3. gRPC (Google Remote Procedure Call)

### ¿Qué es?

gRPC es un framework de **llamadas a procedimientos remotos** de alto rendimiento. Permite que un programa llame funciones en otro programa como si fueran locales.

### Diferencia Conceptual

```
REST: "Dame el recurso /usuarios/123"
     → Piensas en DATOS

gRPC: "Ejecuta la función ObtenerUsuario(123)"
     → Piensas en ACCIONES
```

### Arquitectura gRPC

```
┌─────────────────────────────────────────────────────────────────┐
│                         gRPC                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Cliente                               Servidor                │
│   ┌──────────┐                         ┌──────────┐             │
│   │ Tu código│                         │ Tu código│             │
│   └────┬─────┘                         └────▲─────┘             │
│        │                                    │                   │
│   ┌────▼─────┐                         ┌────┴─────┐             │
│   │  Stub    │ ◄────── HTTP/2 ───────► │ Servidor │             │
│   │(generado)│     (Protocol Buffers)  │ gRPC     │             │
│   └──────────┘                         └──────────┘             │
│                                                                 │
│   El stub es código auto-generado que                           │
│   maneja la comunicación por ti                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Protocol Buffers (Protobuf)

gRPC usa Protocol Buffers como formato de serialización (en lugar de JSON):

```
// Archivo: usuario.proto

syntax = "proto3";

message Usuario {
  int32 id = 1;
  string nombre = 2;
  string email = 3;
}

message ObtenerUsuarioRequest {
  int32 id = 1;
}

service UsuarioService {
  rpc ObtenerUsuario(ObtenerUsuarioRequest) returns (Usuario);
  rpc ListarUsuarios(Empty) returns (stream Usuario);
}
```

### Tipos de Comunicación gRPC

```
┌─────────────────────────────────────────────────────────────────┐
│                 PATRONES DE COMUNICACIÓN                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. UNARY (uno a uno)                                           │
│     Cliente ──── Petición ────► Servidor                        │
│     Cliente ◄─── Respuesta ─── Servidor                         │
│                                                                 │
│  2. SERVER STREAMING                                            │
│     Cliente ──── Petición ────► Servidor                        │
│     Cliente ◄─── Mensaje 1 ─── Servidor                         │
│     Cliente ◄─── Mensaje 2 ─── Servidor                         │
│     Cliente ◄─── Mensaje N ─── Servidor                         │
│                                                                 │
│  3. CLIENT STREAMING                                            │
│     Cliente ──── Mensaje 1 ──► Servidor                         │
│     Cliente ──── Mensaje 2 ──► Servidor                         │
│     Cliente ──── Mensaje N ──► Servidor                         │
│     Cliente ◄─── Respuesta ─── Servidor                         │
│                                                                 │
│  4. BIDIRECTIONAL STREAMING                                     │
│     Cliente ◄───────────────► Servidor                          │
│          (mensajes en ambas direcciones)                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Pros y Contras de gRPC

| ✅ Ventajas | ❌ Desventajas |
|-------------|----------------|
| Muy rápido (binario, HTTP/2) | No funciona en browsers directamente |
| Contrato estricto (protobuf) | Más complejo de debuggear |
| Streaming bidireccional | Menos legible que JSON |
| Generación de código | Menor ecosistema que REST |
| Ideal para microservicios | Requiere tooling específico |

### ¿Cuándo usar gRPC?

```
USA gRPC cuando:
├── Comunicación entre microservicios
├── Necesitas alto rendimiento
├── Streaming de datos
└── Control estricto del contrato

USA REST cuando:
├── APIs públicas
├── Integración con browsers
├── Simplicidad es prioritaria
└── Equipo no familiarizado con gRPC
```

---

## 4. WebSockets

### ¿Qué es?

WebSocket es un protocolo que permite **comunicación bidireccional persistente** entre cliente y servidor.

### Diferencia con HTTP

```
HTTP (Petición-Respuesta):
┌────────┐                         ┌────────┐
│Cliente │ ──── Petición ────────► │Servidor│
│        │ ◄─── Respuesta ──────── │        │
│        │                         │        │
│        │ ──── Petición ────────► │        │
│        │ ◄─── Respuesta ──────── │        │
└────────┘     (conexión cerrada)  └────────┘


WebSocket (Conexión Persistente):
┌────────┐                         ┌────────┐
│Cliente │ ════════════════════════│Servidor│
│        │      Conexión abierta   │        │
│        │ ──── Mensaje ─────────► │        │
│        │ ◄─── Mensaje ────────── │        │
│        │ ◄─── Mensaje ────────── │        │
│        │ ──── Mensaje ─────────► │        │
│        │      ... continua ...   │        │
└────────┘                         └────────┘
```

### Handshake de WebSocket

```
1. Cliente inicia con HTTP normal:
   GET /chat HTTP/1.1
   Upgrade: websocket
   Connection: Upgrade

2. Servidor acepta:
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade

3. ¡Conexión WebSocket establecida!
   → Ahora ambos pueden enviar mensajes cuando quieran
```

### Casos de Uso

```
┌─────────────────────────────────────────────────────────────────┐
│                  USOS IDEALES DE WEBSOCKET                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🎮 Juegos en línea          → Actualizaciones en tiempo real   │
│  💬 Chat                     → Mensajes instantáneos            │
│  📈 Trading/Finanzas         → Precios en vivo                  │
│  📊 Dashboards               → Métricas que cambian             │
│  🔔 Notificaciones           → Push instantáneo                 │
│  👥 Colaboración             → Google Docs, Figma               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Pros y Contras de WebSocket

| ✅ Ventajas | ❌ Desventajas |
|-------------|----------------|
| Comunicación en tiempo real | Más complejo de implementar |
| Baja latencia | Mantener conexiones consume recursos |
| Bidireccional | Más difícil de escalar |
| Eficiente (sin overhead HTTP) | Sin cache |
| | Reconexión debe manejarse manualmente |

---

## 5. SOAP (Simple Object Access Protocol)

### ¿Qué es?

SOAP es un **protocolo** (no un estilo como REST) más antiguo y formal para intercambiar información estructurada.

### Características

```
┌─────────────────────────────────────────────────────────────────┐
│                          SOAP                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  • Usa XML exclusivamente                                       │
│  • Protocolo estricto con especificación formal                 │
│  • WSDL (Web Services Description Language) define el contrato  │
│  • Independiente del transporte (HTTP, SMTP, etc.)              │
│  • Muy usado en empresas grandes y sistemas legacy              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Estructura de un Mensaje SOAP

```xml
<?xml version="1.0"?>
<soap:Envelope 
  xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  
  <soap:Header>
    <!-- Metadatos opcionales -->
    <autenticacion>
      <token>abc123</token>
    </autenticacion>
  </soap:Header>
  
  <soap:Body>
    <!-- El contenido real -->
    <ObtenerUsuario>
      <id>123</id>
    </ObtenerUsuario>
  </soap:Body>
  
</soap:Envelope>
```

### Comparación Visual: SOAP vs REST

```
SOAP (verbose, estructurado):
┌─────────────────────────────────────────┐
│ <?xml version="1.0"?>                   │
│ <soap:Envelope>                         │
│   <soap:Body>                           │
│     <ObtenerUsuarioRequest>             │
│       <id>123</id>                      │
│     </ObtenerUsuarioRequest>            │
│   </soap:Body>                          │
│ </soap:Envelope>                        │
└─────────────────────────────────────────┘

REST (simple, ligero):
┌─────────────────────────────────────────┐
│ GET /usuarios/123                       │
└─────────────────────────────────────────┘
```

### Pros y Contras de SOAP

| ✅ Ventajas | ❌ Desventajas |
|-------------|----------------|
| Contrato estricto (WSDL) | Verbose (mucho XML) |
| Seguridad incorporada (WS-Security) | Complejo |
| Transacciones ACID | Lento comparado con REST |
| Ideal para sistemas empresariales | Difícil de debuggear |
| Independiente del transporte | Menos flexible |

### ¿Cuándo encontrarás SOAP?

```
Típicamente en:
├── Bancos y sistemas financieros
├── Sistemas de gobierno
├── Aplicaciones empresariales legacy
├── Integraciones B2B formales
└── Cuando se necesita WS-* (WS-Security, WS-Transaction)
```

---

## Tabla Comparativa

```
┌──────────────┬─────────┬─────────┬─────────┬───────────┬────────┐
│              │  REST   │ GraphQL │  gRPC   │ WebSocket │  SOAP  │
├──────────────┼─────────┼─────────┼─────────┼───────────┼────────┤
│ Formato      │  JSON   │  JSON   │ Protobuf│  Cualq.   │  XML   │
├──────────────┼─────────┼─────────┼─────────┼───────────┼────────┤
│ Transporte   │  HTTP   │  HTTP   │  HTTP/2 │    WS     │ HTTP++ │
├──────────────┼─────────┼─────────┼─────────┼───────────┼────────┤
│ Estilo       │ Recurso │ Query   │  RPC    │  Mensaje  │  RPC   │
├──────────────┼─────────┼─────────┼─────────┼───────────┼────────┤
│ Rendimiento  │  Medio  │  Medio  │  Alto   │   Alto    │  Bajo  │
├──────────────┼─────────┼─────────┼─────────┼───────────┼────────┤
│ Complejidad  │  Baja   │  Media  │  Alta   │   Media   │  Alta  │
├──────────────┼─────────┼─────────┼─────────┼───────────┼────────┤
│ Caché        │   Sí    │ Difícil │   No    │    No     │   No   │
├──────────────┼─────────┼─────────┼─────────┼───────────┼────────┤
│ Browser      │   Sí    │   Sí    │ Con lib │    Sí     │Con lib │
└──────────────┴─────────┴─────────┴─────────┴───────────┴────────┘
```

---

## ¿Cuál elegir?

```
┌─────────────────────────────────────────────────────────────────┐
│                    GUÍA DE DECISIÓN                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ¿API pública, simple, amplia adopción?                         │
│  └──► REST                                                      │
│                                                                 │
│  ¿Frontend complejo, necesitas flexibilidad en queries?         │
│  └──► GraphQL                                                   │
│                                                                 │
│  ¿Microservicios internos, alto rendimiento?                    │
│  └──► gRPC                                                      │
│                                                                 │
│  ¿Comunicación en tiempo real, bidireccional?                   │
│  └──► WebSocket                                                 │
│                                                                 │
│  ¿Sistema empresarial legacy, requisitos estrictos?             │
│  └──► SOAP                                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Siguiente Documento

En el siguiente documento exploraremos el **Model Context Protocol (MCP)** y patrones de diseño de APIs.

