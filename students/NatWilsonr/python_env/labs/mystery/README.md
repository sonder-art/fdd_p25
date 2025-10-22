# Mystery Lab (Docker + uv)

Este pequeño ejercicio no lista dependencias. Tu objetivo es (entrega por Pull Request desde tu carpeta de estudiante):

1) Crear un contenedor que ejecute `python labs/mystery/main.py` correctamente.
2) Descubrir e instalar las dependencias necesarias usando `uv` dentro del contenedor.
3) Lograr que la ejecución termine con código 0 y muestre una tabla con un valor.

Reglas del juego:
- No se revelan nombres de paquetes ni versiones.
- Usa prueba y error leyendo los `ImportError`/`ModuleNotFoundError`.
- Mantén un `requirements.txt` con las dependencias que vayas descubriendo.

Pistas mínimas:
- El programa imprime con “estilo/colores” y hace una petición HTTP a un endpoint público.

Sugerencia de ciclo :

```bash
# 1) primera build & run (probablemente fallará con ImportError)
docker build -t mystery-uv .
docker run --rm mystery-uv

# 2) lee el error, agrega una dependencia a requirements.txt
echo '<descubierta>' >> requirements.txt

# 3) reconstruye y vuelve a correr
docker build -t mystery-uv .
docker run --rm mystery-uv
# repite hasta ver "OK — entorno configurado correctamente."
```

Entrega: crea tu rama, confirma tus cambios dentro de `students/{tu_carpeta}/python_env/` y abre tu Pull Request.

Happy debugging!

---

Referencia y entrega
- Para repasar entornos, PATH, `venv`, `pip` y `uv`, vuelve a `professor/python_env/README.md` (o a tu copia en `students/{tu_carpeta}/python_env/`).
- La entrega es por Pull Request desde tu carpeta de estudiante; sigue el flujo de Git/GitHub indicado en el README principal.


