# Flujo de Trabajo Detallado para Entregar Tareas en GitHub

## Paso 1: Actualizar tu repositorio local y rama `main` con los últimos cambios del repositorio de la clase (upstream)

1. Abre tu terminal
2. Navega a la carpeta de tu repositorio local:
   ```bash
   cd [ruta_a_tu_repositorio]
   ```
3. Asegúrate de estar en la rama `main`:
   ```bash
   git checkout main
   ```
4. Si es la primera vez, agrega el repositorio de la clase como "upstream":
   ```bash
   git remote add upstream [URL_del_repositorio_de_la_clase]
   ```
   Verifica con:
   ```bash
   git remote -v
   ```
5. Trae los últimos cambios del repositorio original:
   ```bash
   git fetch upstream
   ```
6. Fusiona estos cambios con tu rama `main` local:
   ```bash
   git merge upstream/main
   ```
7. Sube estos cambios a tu repositorio remoto (tu fork en GitHub) para que tu `main` en la nube esté sincronizado:
   ```bash
   git push origin main
   ```

## Paso 2: Crear una nueva rama para tu tarea

1. Desde tu rama `main` (asegúrate de estar en ella), crea una nueva rama con el nombre de tu tarea:
   ```bash
   git checkout -B [nombre_de_tu_rama_de_tarea]
   ```
2. Confirma que estás en la rama correcta:
   ```bash
   git status
   ```

## Paso 3: Realizar los cambios de tu tarea en tu carpeta asignada

> **⚠️ ¡Importante!** Asegúrate de estar dentro de tu carpeta personal (`students/[tu_usuario_de_github]`) en el repositorio.

1. Verifica tu ubicación:
   ```bash
   pwd
   ```
   Navega si es necesario:
   ```bash
   cd students/[tu_usuario_de_github]
   ```
2. Dentro de tu carpeta, crea los archivos y subcarpetas necesarios para tu tarea
3. Si creas una nueva carpeta vacía, añade un archivo `.gitkeep` dentro de ella:
   ```bash
   touch .gitkeep
   ```
   Esto permite que Git rastree la carpeta.

## Paso 4: Añadir y confirmar tus cambios (commit)

1. Añade **solo** los archivos modificados o nuevos dentro de tu carpeta a la zona de preparación (staging area). 
   
   > **⚠️ Evita `git add .`** para no incluir archivos no deseados.
   
   **Ejemplos:**
   ```bash
   git add students/[tu_usuario_de_github]/[nombre_del_archivo_o_carpeta]
   ```
   
   Para el `.gitkeep` inicial:
   ```bash
   git add students/[tu_usuario_de_github]/.gitkeep
   ```

2. Confirma tus cambios con un mensaje claro y descriptivo:
   ```bash
   git commit -m "Tarea: [Descripción breve de tu tarea]"
   ```

## Paso 5: Subir tus cambios a tu repositorio (fork) en GitHub

1. Sube los cambios de tu rama de tarea a tu fork en GitHub:
   ```bash
   git push origin [nombre_de_tu_rama_de_tarea]
   ```
2. Verifica en GitHub que la nueva rama y tus cambios estén visibles en tu fork

## Paso 6: Fusionar tu rama de tarea con tu rama `main` en GitHub

> **Opción recomendada para el Pull Request final**

### Método Principal (Recomendado):
1. Dirígete a tu repositorio (fork) en GitHub en tu navegador web
2. Ve a la pestaña "Pull requests" o "Branches". Deberías ver una opción para crear un Pull Request desde tu rama de tarea a tu rama `main` en tu fork
3. Crea este Pull Request: `[tu_repositorio]/main ← [tu_repositorio]/[nombre_de_tu_rama_de_tarea]`
4. Revisa los cambios y, si todo es correcto, fusiona (merge) este Pull Request

**Resultado:** Ahora, tu rama `main` en tu fork de GitHub contiene los cambios de tu tarea. Tu `main` local estará desactualizado con respecto a este, lo cual corregiremos en el último paso.

### Alternativa (Merge local):
Si prefieres fusionar localmente:
1. Vuelve a tu `main`:
   ```bash
   git checkout main
   ```
2. Fusiona tu rama de tarea:
   ```bash
   git merge [nombre_de_tu_rama_de_tarea]
   ```
3. Sube los cambios:
   ```bash
   git push origin main
   ```

En este caso, tu `main` local se actualizará primero, y luego lo sincronizas con la nube.

## Paso 7: Crear el Pull Request final desde tu fork al repositorio de la clase (upstream)

1. Una vez que tu rama `main` en tu fork de GitHub tiene los cambios de tu tarea (después del Paso 6), ve a tu repositorio (fork) en GitHub
2. Haz clic en "Contribute" y luego en "Open pull request" (o busca la opción de "New pull request")
3. **Asegúrate de que la dirección del Pull Request sea correcta:**
   ```
   sonder_art/main ← [tu_repositorio]/main
   ```
4. Asigna un título al Pull Request con el formato:
   - **Primera tarea:** "Carpeta de Tareas {nombre de tu carpeta}"
   - **Tareas posteriores:** "[Tarea X]: [Descripción breve de la tarea]"
5. Añade una descripción clara de tu tarea

> **⚠️ ¡Revisa cuidadosamente los cambios propuestos!** 
> 
> Asegúrate de que:
> - Solo tu carpeta personal esté afectada
> - No haya archivos no deseados (como `.DS_Store`)
> - **Cualquier modificación fuera de tu carpeta resultará en una calificación de cero**

6. Crea el Pull Request

## Paso 8: Esperar la aprobación y sincronizar tu repositorio local después del merge final

1. Una vez que tu Pull Request sea aceptado y fusionado en el repositorio de la clase (mi `main`), tu rama `main` local (y tu `main` en tu fork, si lo fusionaste en el Paso 6 Alternativo) estará desactualizada

2. **Para obtener los cambios finales:**
   
   a. Asegúrate de estar en tu rama `main` local:
   ```bash
   git checkout main
   ```
   
   b. Trae y fusiona los cambios del repositorio de la clase (upstream):
   ```bash
   git pull upstream main
   ```
   
   c. Finalmente, sube estos cambios a tu fork en GitHub para que tu `main` en la nube esté completamente actualizado:
   ```bash
   git push origin main
   ```

3. **¡Listo!** Ahora, tu repositorio local y tu fork en GitHub están completamente sincronizados con el repositorio de la clase.
