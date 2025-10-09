#!/bin/sh

# Salimos del script inmediatamente si un comando falla.
set -e

# 1. Validación de las variables de entorno
# Verificamos que las variables BANDIT_LEVEL y BANDIT_PASS existan y no estén vacías.
# El operador '-z' comprueba si una cadena tiene longitud cero.

if [ -z "$BANDIT_LEVEL" ]; then
  echo "Error: La variable de entorno BANDIT_LEVEL no está definida."
  exit 1
fi

if [ -z "$BANDIT_PASS" ]; then
  echo "Error: La variable de entorno BANDIT_PASS no está definida."
  exit 1
fi

# 2. Mensaje de conexión
# Informamos al usuario a qué nivel nos estamos conectando.
echo "🚀 Conectando a Bandit nivel $BANDIT_LEVEL..."
echo "Host: bandit.labs.overthewire.org | Puerto: 2220"

# 3. Ejecución de la conexión
# Usamos `exec` para que el proceso de `sshpass` reemplace al proceso del shell.
# Esto es una buena práctica, ya que el contenedor se detendrá en cuanto la sesión SSH termine.
# `sshpass` pasa la contraseña (variable $BANDIT_PASS) al comando ssh.
# Las opciones de ssh:
#   -o StrictHostKeyChecking=no : Evita la pregunta interactiva sobre la autenticidad del host.
exec sshpass -p "$BANDIT_PASS" ssh -o StrictHostKeyChecking=no bandit$BANDIT_LEVEL@bandit.labs.overthewire.org -p 2220
