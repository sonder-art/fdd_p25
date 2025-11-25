# Introducción a las APIs

## ¿Qué es una API?

**API** = Application Programming Interface (Interfaz de Programación de Aplicaciones)

Una API es un **conjunto de reglas y definiciones** que permite que dos sistemas de software se comuniquen entre sí. Es como un **mesero en un restaurante**: tú (el cliente) no vas directamente a la cocina a preparar tu comida; le dices al mesero qué quieres, él va a la cocina, y te trae el resultado.

```
┌─────────────┐         ┌─────────┐         ┌─────────────┐
│   Cliente   │ ──────► │   API   │ ──────► │  Servidor   │
│  (Tú)       │         │ (Mesero)│         │  (Cocina)   │
└─────────────┘         └─────────┘         └─────────────┘
                              │
                              ▼
                        ┌─────────────┐
                        │  Respuesta  │
                        │  (Tu plato) │
                        └─────────────┘
```

### Analogía del Enchufe Eléctrico

Piensa en un enchufe eléctrico:
- No necesitas saber cómo funciona la red eléctrica
- Solo necesitas saber que si conectas un aparato al enchufe, recibirás electricidad
- El enchufe es la **interfaz** entre tu aparato y la red eléctrica

Una API funciona igual: no necesitas saber cómo funciona internamente el sistema, solo cómo interactuar con él.

---

## Conceptos Fundamentales

### 1. Contrato (Contract)

Un **contrato** en el contexto de APIs es un **acuerdo formal** entre el proveedor de la API y quien la consume. Define:

- **Qué datos puedes enviar** (formato, tipos, campos obligatorios)
- **Qué datos recibirás** (estructura de la respuesta)
- **Cómo debes hacer las peticiones** (métodos, headers, autenticación)
- **Qué errores pueden ocurrir** (códigos de error, mensajes)

```
┌─────────────────────────────────────────────────────────────┐
│                    CONTRATO DE API                          │
├─────────────────────────────────────────────────────────────┤
│  Petición:                                                  │
│    - Método: POST                                           │
│    - Ruta: /usuarios                                        │
│    - Cuerpo: { "nombre": string, "email": string }          │
│                                                             │
│  Respuesta Exitosa (201):                                   │
│    - { "id": number, "nombre": string, "email": string }    │
│                                                             │
│  Errores Posibles:                                          │
│    - 400: Datos inválidos                                   │
│    - 409: Email ya existe                                   │
└─────────────────────────────────────────────────────────────┘
```

**Analogía**: Es como un contrato de arrendamiento. Ambas partes saben qué esperar: el arrendador provee la vivienda, el arrendatario paga la renta. Si alguna parte incumple, hay consecuencias claras.

### 2. Boundary (Frontera/Límite)

Un **boundary** es la **línea divisoria** entre dos sistemas o componentes. La API actúa como el boundary entre:

- Tu aplicación y un servicio externo
- El frontend y el backend
- Un microservicio y otro

```
┌──────────────────────────────────────────────────────────────────┐
│                         SISTEMA A                                │
│    ┌──────────────┐                                              │
│    │  Lógica de   │                                              │
│    │  Negocio     │                                              │
│    └──────┬───────┘                                              │
│           │                                                      │
│    ┌──────▼───────┐         ┌ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│    │     API      │◄────────    B O U N D A R Y               │  │
│    │  (Interfaz)  │         └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│    └──────────────┘                                              │
└──────────────────────────────────────────────────────────────────┘
                                    │
                                    │  Comunicación
                                    ▼
┌──────────────────────────────────────────────────────────────────┐
│                         SISTEMA B                                │
│    ┌──────────────┐                                              │
│    │     API      │                                              │
│    │  (Interfaz)  │                                              │
│    └──────────────┘                                              │
└──────────────────────────────────────────────────────────────────┘
```

**¿Por qué es importante el boundary?**

1. **Encapsulamiento**: Oculta la complejidad interna
2. **Independencia**: Cada sistema puede evolucionar por separado
3. **Seguridad**: Controla qué puede y qué no puede hacer el mundo exterior
4. **Claridad**: Define responsabilidades claras

---

## Modelo Cliente-Servidor

Antes de profundizar en APIs, necesitas entender el modelo **cliente-servidor**:

```
┌────────────────┐                        ┌────────────────┐
│    CLIENTE     │                        │    SERVIDOR    │
│                │                        │                │
│  - Navegador   │   ───── Petición ────► │  - Aplicación  │
│  - App móvil   │                        │  - Base datos  │
│  - Otro server │   ◄─── Respuesta ───── │  - Lógica      │
│                │                        │                │
└────────────────┘                        └────────────────┘

     SOLICITA                                  PROVEE
     servicios                                servicios
```

### Características:

| Cliente | Servidor |
|---------|----------|
| Inicia la comunicación | Espera peticiones |
| Consume recursos | Provee recursos |
| Puede ser múltiples | Usualmente centralizado |
| No necesita estar siempre activo | Debe estar siempre disponible |

### Ejemplo cotidiano:

1. Abres Netflix en tu celular (cliente)
2. Tu celular pide al servidor de Netflix "dame la lista de películas"
3. El servidor busca las películas y te las envía
4. Tu celular las muestra en pantalla

---

## HTTPS: Comunicación Segura

### ¿Qué es HTTP?

**HTTP** (HyperText Transfer Protocol) es el protocolo que define **cómo se comunican** cliente y servidor en la web.

### ¿Y la "S" de HTTPS?

La **S** significa **Secure** (Seguro). HTTPS es HTTP + cifrado (encriptación).

```
HTTP (inseguro):
┌────────┐    "Hola, mi password es 1234"    ┌────────┐
│ Cliente│ ─────────────────────────────────►│Servidor│
└────────┘     🔓 Cualquiera puede leer      └────────┘

HTTPS (seguro):
┌────────┐    "X#k9$mP2@..." (cifrado)       ┌────────┐
│ Cliente│ ─────────────────────────────────►│Servidor│
└────────┘     🔒 Solo el servidor entiende  └────────┘
```

### ¿Cómo funciona HTTPS? (Simplificado)

```
┌────────────────────────────────────────────────────────────────┐
│                    HANDSHAKE TLS/SSL                           │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. Cliente: "Hola servidor, quiero comunicarme seguro"        │
│                         │                                      │
│                         ▼                                      │
│  2. Servidor: "Aquí está mi certificado (mi identidad)"        │
│                         │                                      │
│                         ▼                                      │
│  3. Cliente: Verifica certificado ✓                            │
│              "Ok, confío en ti. Aquí hay una clave secreta"    │
│                         │                                      │
│                         ▼                                      │
│  4. Ambos: Ahora usamos la clave para cifrar todo 🔐           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Anatomía de una URL HTTPS

```
https://api.ejemplo.com:443/usuarios/123?activo=true
  │       │              │      │         │
  │       │              │      │         └── Query params
  │       │              │      └── Ruta (path)
  │       │              └── Puerto (443 = HTTPS por defecto)
  │       └── Dominio/Host
  └── Protocolo (seguro)
```

---

## Componentes de una Petición HTTP

```
┌────────────────────────────────────────────────────────────────┐
│                     PETICIÓN HTTP                              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ LÍNEA DE PETICIÓN                                       │   │
│  │ POST /api/usuarios HTTP/1.1                             │   │
│  │  │         │          │                                 │   │
│  │  │         │          └── Versión del protocolo         │   │
│  │  │         └── Ruta del recurso                         │   │
│  │  └── Método HTTP                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ HEADERS (Metadatos)                                     │   │
│  │ Host: api.ejemplo.com                                   │   │
│  │ Content-Type: application/json                          │   │
│  │ Authorization: Bearer xyz123                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ BODY (Cuerpo - opcional)                                │   │
│  │ {                                                       │   │
│  │   "nombre": "Juan",                                     │   │
│  │   "email": "juan@correo.com"                            │   │
│  │ }                                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Métodos HTTP Principales

| Método | Propósito | ¿Tiene body? | Analogía |
|--------|-----------|--------------|----------|
| GET | Obtener datos | No | Leer un libro |
| POST | Crear recurso | Sí | Escribir una carta nueva |
| PUT | Reemplazar recurso | Sí | Reescribir todo el capítulo |
| PATCH | Modificar parcialmente | Sí | Corregir un párrafo |
| DELETE | Eliminar recurso | No | Tirar una carta a la basura |

---

## Códigos de Respuesta HTTP

```
┌─────────────────────────────────────────────────────────────┐
│                  CÓDIGOS DE ESTADO HTTP                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  2xx - ÉXITO ✅                                             │
│  ├── 200 OK: Todo bien, aquí está tu respuesta              │
│  ├── 201 Created: Se creó el recurso exitosamente           │
│  └── 204 No Content: Éxito, pero no hay nada que devolver   │
│                                                             │
│  3xx - REDIRECCIÓN 🔀                                       │
│  ├── 301 Moved Permanently: El recurso cambió de lugar      │
│  └── 304 Not Modified: Usa la versión en caché              │
│                                                             │
│  4xx - ERROR DEL CLIENTE ❌                                 │
│  ├── 400 Bad Request: Tu petición está mal formada          │
│  ├── 401 Unauthorized: No te has autenticado                │
│  ├── 403 Forbidden: No tienes permiso                       │
│  ├── 404 Not Found: El recurso no existe                    │
│  └── 429 Too Many Requests: Demasiadas peticiones           │
│                                                             │
│  5xx - ERROR DEL SERVIDOR 💥                                │
│  ├── 500 Internal Server Error: Algo falló en el servidor   │
│  ├── 502 Bad Gateway: Error de comunicación entre servers   │
│  └── 503 Service Unavailable: Servidor no disponible        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Resumen Visual

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│                        EL ECOSISTEMA API                            │
│                                                                     │
│   ┌──────────┐      CONTRATO        ┌──────────┐                    │
│   │          │  ◄──────────────────►│          │                    │
│   │ CLIENTE  │   "Así nos hablamos" │ SERVIDOR │                    │
│   │          │                      │          │                    │
│   └────┬─────┘                      └────┬─────┘                    │
│        │                                 │                          │
│        │         B O U N D A R Y         │                          │
│        │◄───────────────────────────────►│                          │
│        │            (API)                │                          │
│        │                                 │                          │
│        │     ┌─────────────────┐         │                          │
│        │     │     HTTPS       │         │                          │
│        └────►│   (Seguridad)   │◄────────┘                          │
│              └─────────────────┘                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Siguiente Documento

En el siguiente documento exploraremos los **tipos de APIs** más comunes: REST, GraphQL, gRPC, WebSockets, y más.

