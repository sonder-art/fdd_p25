# Tarea 12: Entornos Virtuales

Esta carpeta contiene la evidencia de la Tarea 12.

## Archivos
- `requirements.txt`: Lista de dependencias (requests).
- `main.py`: Script que utiliza la librería `requests`.

## Instrucciones (Simulación)

```bash
# 1. Crear entorno virtual
python3 -m venv .venv

# 2. Activar entorno
source .venv/bin/activate

# 3. Instalar dependencias
pip install requests
# O desde el archivo:
pip install -r requirements.txt

# 4. Verificar instalación
pip list
# Debe mostrar requests

# 5. Ejecutar script
python3 main.py

# 6. Generar requirements (si se instaló manual)
pip freeze > requirements.txt

# 7. Desactivar
deactivate
```
