

# Instrucciones (entrega en `{tu_carpeta}/dockerhub/`)

1. **Dockerfile**

   * Crea un **Dockerfile completo** y funcional.
   * Debe **ejecutar un script de shell** al iniciar el contenedor.

2. **Script de shell**

   * El script debe **leer** (desde variables de entorno) **el nivel de Bandit** y **el password del nivel**.
   * Con esos datos, el script debe **conectarse** al nivel correspondiente de **Bandit**.

3. **Variables de entorno**

   * El contenedor debe aceptar las variables **tanto** con `-e` **como** con `--env-file` al usar `docker run`.

4. **Publicación en Docker Hub**

   * **Sube** la imagen resultante a **Docker Hub** (crea tu cuenta si no la tienes).

5. **Archivo con la URL**

   * En la misma carpeta, crea **`mi_dockerhub.txt`** que contenga **la URL de la imagen** publicada en Docker Hub (solo la URL).

6. **Pull Request**

   * Haz **pull request** al **repo mainstream de la clase** incluyendo:

     * `Dockerfile`
     * El **script de shell**
     * `mi_dockerhub.txt`

---
