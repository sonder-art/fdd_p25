# Guía rápida para recordar y entender Python (sin soluciones)

Esta guía resume fundamentos y patrones comunes de Python para orientarte mientras practicas. No explica banderas de ejecución ni resuelve las consignas del ejercicio; su objetivo es ayudarte a recordar conceptos clave con ejemplos mínimos.

---

## 1) Cómo ejecutar Python

- REPL (interactivo): ejecuta `python3` y escribe expresiones una por línea. Sal con `exit()` o `Ctrl+D`.
- Script: guarda código en un archivo `.py` y ejecútalo con `python3 nombre.py`.

Consejo: usa el REPL para probar ideas pequeñas y el archivo `.py` para guardar lo que quieras reutilizar.

---

## 2) Sintaxis esencial

- Indentación: define bloques. Usa la misma cantidad de espacios en un bloque.
- Comentarios: comienzan con `#` para una línea. Los docstrings van entre `"""` comillas triples `"""`.
- Nombres: usa `snake_case` para variables y funciones.

---

## 3) Tipos básicos y literales

- Numéricos: `int` (enteros), `float` (decimales)
- Booleanos: `bool` → `True` / `False`
- Texto: `str` → comillas simples o dobles
- Especial: `None` (ausencia de valor)

Conversión de tipos frecuentes: `int()`, `float()`, `str()`, `bool()`

---

## 4) Contenedores fundamentales

- Lista `list`: ordenada y mutable → `[1, 2, 3]`
- Tupla `tuple`: ordenada e inmutable → `(1, 2, 3)`
- Conjunto `set`: elementos únicos sin orden → `{1, 2, 3}`
- Diccionario `dict`: pares clave-valor → `{"k": 1, "z": 2}`

Operaciones útiles:
- Listas: `append`, `extend`, `insert`, `pop`, `slice` `a[b:c]`
- Diccionarios: `d["k"]`, `d.get("k")`, `keys()`, `values()`, `items()`
- Conjuntos: unión `|`, intersección `&`, diferencia `-`

---

## 5) Operadores y verdad

- Aritméticos: `+  -  *  /  //  %  **`
- Comparación: `==  !=  <  <=  >  >=`
- Lógicos: `and  or  not`
- Pertenencia y identidad: `in`, `is`

Verdad (truthiness): valores vacíos (`""`, `[]`, `{}`, `set()`, `0`, `None`) se consideran `False` en condiciones.

---

## 6) Cadenas (strings)

- Concatenación: `"hola " + "mundo"`
- Repetición: `"ha" * 3`
- Slicing: `s[ini:fin:paso]`
- F-strings: prefijo `f` para interpolar valores: `f"x={x}"`
- Métodos útiles: `lower()`, `upper()`, `strip()`, `split()`, `join()`

---

## 7) Control de flujo

- Condicionales: `if / elif / else`
- Bucle `for`: recorre elementos de una secuencia (`for x in secuencia:`)
- Bucle `while`: repite mientras una condición sea verdadera
- Atajos: `break` (sale), `continue` (salta a la siguiente iteración)

---

## 8) Funciones

- Definición: `def nombre(parametros): ...`
- Retorno: `return valor`
- Parámetros por defecto, argumentos por nombre, `*args` y `**kwargs` (para casos variables)
- Docstring: describe qué hace la función entre `""" ... """`
- Tipado opcional (anotaciones): `def suma(a: int, b: int) -> int: ...`

Reglas de ámbito (LEGB, simplificado):
1. Local (dentro de la función)
2. Enclosing (entornos externos a la función)
3. Global (módulo actual)
4. Builtins (funciones/nombres integrados)

---

## 9) Módulos e importación

- `import modulo`
- `from modulo import nombre`
- Alias: `import modulo as m`

Usa imports al inicio del archivo. Organiza estándar/biblioteca estándar, terceros y locales.

---

## 10) Errores y excepciones (manejo básico)

- Captura: `try: ... except TipoDeError: ...`
- Opcionales: `else:` (si no hubo error), `finally:` (siempre se ejecuta)
- Lanza una excepción: `raise TipoDeError("mensaje")`

En depuración, imprime el mensaje del error o usa herramientas como `traceback` cuando corresponda.

---

## 11) REPL: trucos útiles

- `help(obj)` muestra ayuda; en ayuda sal con `q`.
- `type(x)` para inspeccionar tipos.
- `dir(obj)` lista atributos/métodos disponibles.
- Importa tu módulo y prueba funciones/variables interactivamente.

---

## 12) Glosario mínimo

- Bytecode: instrucciones intermedias que ejecuta la VM de Python.
- `__pycache__/`: carpeta donde Python guarda bytecode compilado (`.pyc`).
- Módulo: archivo `.py` que se puede importar.
- Paquete: directorio con `__init__.py` (en versiones modernas puede omitirse en algunos casos).

---

## 13) Palabras reservadas (no usarlas como nombres)

`False`, `None`, `True`, `and`, `as`, `assert`, `async`, `await`, `break`, `class`, `continue`, `def`, `del`, `elif`, `else`, `except`, `finally`, `for`, `from`, `global`, `if`, `import`, `in`, `is`, `lambda`, `nonlocal`, `not`, `or`, `pass`, `raise`, `return`, `try`, `while`, `with`, `yield`, `match`, `case`

---

## 14) Buenas prácticas rápidas

- Escribe código claro y legible antes que “clever”.
- Nombra bien: que el nombre explique su intención.
- Prefiere funciones cortas y que hagan una sola cosa.
- Agrega docstrings en funciones públicas.
- Evita duplicación: extrae funciones si repites lógica.

---

## 15) Herramientas integradas que conviene recordar

- `print`, `len`, `range`, `enumerate`, `sum`, `min`, `max`, `sorted`
- `any`, `all`, `zip`, `map`, `filter` (útiles con iterables)
- Estructuras por comprensión (idea): `[expr for x in xs if cond]` y `{k: v for ...}`

Nota: estas herramientas son para escribir código más claro; no son parte de la consigna específica.



