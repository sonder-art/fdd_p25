# 213620- Bitácora de VSCODE 

Cositas rápidas para mi misma: 
- Comando de Markdown (por si se cierra el archivo)
ctrl+shift+v
- Paleta de comandos: F1
- Cambiar de rama: esquina inferior izquierda

¿Qué es VSCODE?
un IDE que permite la instalación de extensiones aunado al uso de una terminal "propia". 

- Layout (las más relevantes desde mi pov)
status bar (raya de color al pie de la ventana): rama Git, escoger intérprete de python, zoom
- Command Palette: F1 sí funciona en mi compu

Ejercicio guiado:
- El comando Ctrl+Shift+P sí funciona en mi compu, pero resulta más conveniente utilizar F1. 
- Extensions es bastante intuitivo 
- la terminal funciona casi completamente igual a la de mi OS


# Terminal integrado vs terminal del sistema
la terminal que nos muestra VSCODE es la misma que la que trae nuestro OS por defecto, solo que aquí la personalizan para que sea más "cómodo" trabajar con ella
La prueba de la terminal me ayudó a darme cuenta de que hasta el momento tengo todo bien instalado

# Post-intalación general
Ctrl+ NO abré Settings UI para mi, simplemente hace un zoom inmediato a toda la interfaz

# Post-instalación para Python
#### ¿Qué es un intérprete?
Es el programa que traduce nuestro código a instrucciones que la compu sí entiende (lo traduce a lenguaje de máquina, i.e. 1s y 0s)

#### ¿Cómo crear/escoger un venv? 
F1 -> → “Python: Select Interpreter” → elige el .venv con el que vas a trabajar
- “Use Existing Environment”: selecciona un .venv ya creado en tu carpeta.
- “Create New Venv”: crea uno nuevo si no existe o si quieres empezar de cero.
##### ¿Cuándo borrar y crear uno nuevo? Si el entorno quedó roto o las dependencias están en conflicto; elimina la carpeta .venv/ y vuelve a crear.

*Otra opción:*
F1→ “Python: Create Environment” → venv → Python 3.x → VS Code propondrá seleccionar ese intérprete automáticamente.
- Si tienes requirements.txt, VS Code te preguntará si lo usas para instalar deps. Selecciona el archivo y acepta para instalar automáticamente.
- Si no tienes requirements.txt, puedes añadirlo después y usar la acción “Install from Requirements File”.

# Configuración de formato, lint y estilo
>**Nota:** Los 3 cositos (black, ruffus, pylance) ya quedaron bien cofiguradas en mi git.

Formatter: reescribe el código automáticamente siguiendo un estilo
Linter: Detecta errores o malas prácticas sin ejecutarlo
Type checker: analiza si los tipos de datos son coherentes

##### Dónde se guarda
User Settings → afecta todos tus proyectos (ideal si quieres siempre el mismo estilo).
📍Se guarda en `~/.config/Code/User/settings.json` (en Linux).

Workspace Settings → afecta solo ese proyecto, guardándose dentro de:
` tu_proyecto/.vscode/settings.json` 

Esto es útil cuando un equipo quiere que todos sigan el mismo formato.
