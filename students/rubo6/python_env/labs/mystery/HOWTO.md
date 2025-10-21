# Mystery Lab (Docker + uv) – Reproducir
1) Desde la raíz del repo:
   docker build -t mystery-uv -f students/rubo6/python_env/labs/mystery/Dockerfile .
2) Ejecutar:
   docker run --rm mystery-uv
   # Debe imprimir la tabla y "OK – entorno configurado correctamente." (exit code 0)
3) Si aparece ImportError, añade el paquete a:
   students/rubo6/python_env/labs/mystery/requirements.txt
   y repite 1) y 2).
