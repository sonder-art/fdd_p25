# Tarea 06: Introducción a Git

Esta carpeta contiene la evidencia de la Tarea 06.

## Comandos Ejecutados (Simulación)

```bash
# Configuración
git config --global user.name "welink"
git config --global user.email "welink@example.com"

# Inicialización (en un entorno separado)
mkdir tarea_git_basics
cd tarea_git_basics
git init

# Ciclo de vida
touch README.md
git status
git add .
git commit -m "Primer commit"
git log
```

## Notas
Como estamos trabajando dentro de un repositorio ya existente (`fdd_p25`), no se ejecutó `git init` aquí para evitar anidamiento de repositorios. Este archivo sirve como constancia de los pasos comprendidos.
