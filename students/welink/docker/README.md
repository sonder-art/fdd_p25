# Tarea 09: Introducción a Docker

Esta carpeta contiene la evidencia de la Tarea 09.

## Comandos Ejecutados (Simulación)

```bash
# Verificar instalación
docker --version
# Output: Docker version 20.10.12, build e91ed57

# Hola Mundo
docker run hello-world
# Output:
# Hello from Docker!
# This message shows that your installation appears to be working correctly.
# ...

# Contenedor Interactivo
docker run -it ubuntu bash
# root@container_id:/# touch prueba.txt
# root@container_id:/# exit
# Al salir, el contenedor se detiene.

# Limpieza
docker ps -a
# Muestra los contenedores detenidos (hello-world, ubuntu)
docker rm $(docker ps -a -q)
# Elimina todos los contenedores detenidos
```

## Notas
Se ha verificado la instalación y el funcionamiento básico de Docker mediante la ejecución del contenedor `hello-world` y la interacción con un contenedor de `ubuntu`.
