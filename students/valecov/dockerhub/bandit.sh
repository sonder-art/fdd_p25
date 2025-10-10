#!/bin/bash

LEVEL=$BANDIT_LEVEL
PASSWORD=$BANDIT_PASSWORD

if [ -z "$LEVEL" ] || [ -z "$PASSWORD" ]; then
  echo "define nivel y contraseña."
  echo "así:"
  echo "docker run -e BANDIT_LEVEL=0 -e BANDIT_PASSWORD=bandit0 tuimagen"
  exit 1
fi

sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no bandit$LEVEL@bandit.labs.overthewire.org -p 2220

