#!/usr/bin/env bash
set -eo pipefail

SCRIPT="labs/mystery/main.py"
if [ ! -f "$SCRIPT" ]; then
  echo "No se encontró $SCRIPT dentro del contenedor." >&2
  exit 2
fi

attempts=0
max=15

while true; do
  set +e
  out="$(python "$SCRIPT" 2>&1)"
  code=$?
  set -e

  # Muestra la salida siempre (para ver la tabla cuando ya corre)
  echo "$out"

  # Éxito
  if [ $code -eq 0 ]; then
    exit 0
  fi

  # Detectar módulo faltante (ModuleNotFoundError)
  if echo "$out" | grep -q "ModuleNotFoundError: No module named"; then
    mod="$(echo "$out" | sed -n "s/.*ModuleNotFoundError: No module named '\([^']\+\)'.*/\1/p" | head -n1)"
    if [ -z "$mod" ]; then
      echo "No se pudo detectar el módulo faltante." >&2
      exit $code
    fi

    attempts=$((attempts+1))
    if [ $attempts -gt $max ]; then
      echo "Demasiados intentos instalando dependencias." >&2
      exit 1
    fi

    # Mapear alias comunes de módulo -> paquete de PyPI
    case "$mod" in
      bs4)        pkg="beautifulsoup4" ;;
      PIL)        pkg="Pillow" ;;
      cv2)        pkg="opencv-python" ;;
      yaml)       pkg="PyYAML" ;;
      sklearn)    pkg="scikit-learn" ;;
      Crypto)     pkg="pycryptodome" ;;
      MySQLdb)    pkg="mysqlclient" ;;
      *)          pkg="$mod" ;;
    esac

    echo "Instalando dependencia faltante con uv: $pkg"
    uv pip install "$pkg"
    continue
  fi

  # Otros fallos: sal con el código para ver error real
  echo "Fallo no manejado (exit code $code)." >&2
  exit $code
done
