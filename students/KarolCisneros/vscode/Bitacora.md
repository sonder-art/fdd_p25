# Notas sobre VSCODE

### VS CODE, qué es?
Es un lector de código moderno, con interfaz gráfica, acceso a extensiones, etc.

Tabla de referencia de formatos usados en esta guía

| Tipo | Cómo lo verás | Ejemplo |
|---|---|---|
| Comando de Paleta | `Nombre: Subcomando` | `View: Toggle Terminal` |
| Atajo de teclado | `Ctrl+Tecla` (o `Ctrl+K Ctrl+S`) | `Ctrl+Shift+P` |
| Ruta de menú | `Menú → Submenú` | `View → Explorer` |
| Archivo/Carpeta | `ruta/o/archivo` | `students/{tu_carpeta}/vscode/` |


Cómo mostrar/ocultar cada parte (elige Menú o Paleta; atajos dependen del sistema):
- Explorer: Menú View → Explorer, o `Ctrl+Shift+P` → "View: Show Explorer".
- Terminal: Menú Terminal → New Terminal, o `Ctrl+Shift+P` → "View: Toggle Terminal".
- Problems: Menú View → Problems, o `Ctrl+Shift+P` → "View: Toggle Problems".
- Extensions: Menú View → Extensions, o `Ctrl+Shift+P` → "Extensions: View Extensions".
- Restablecer diseño: `Ctrl+Shift+P` → "View: Reset Workbench Layout".

## Diagramas

Diagrama del layout (simplificado)

```mermaid
flowchart LR
    A["Activity Bar"] --> B["Side Bar"]
    B --> C["Editor"]
    C --> D["Panel (Terminal/Problems)"]
    E["Status Bar"] --- C
```

---

Diagrama: crear entorno `venv` desde la Paleta

```mermaid
sequenceDiagram
    participant U as Usuario
    participant V as VS Code
    participant P as Python Ext
    U->>V: `Python: Create Environment`
    V->>P: Solicita tipo de entorno (venv)
    P-->>V: Lista intérpretes Python 3.x
    U->>V: Selecciona intérprete
    V->>P: Crea `.venv` y pregunta por `requirements.txt`
    U->>V: Selecciona `requirements.txt` (opcional)
    P-->>U: Instala dependencias y selecciona intérprete en Status Bar
```
---

Diagrama: flujo de actualización y PR GIT

```mermaid
sequenceDiagram
    participant U as Usuario
    participant VS as VS Code
    participant GH as GitHub
    U->>VS: `Git: Fetch From All Remotes`
    U->>VS: `Git: Checkout to...` main
    U->>VS: `Git: Merge Branch...` upstream/main
    U->>VS: Create Branch (feat/...)
    U->>VS: Stage + Commit
    U->>GH: Publish Branch
    U->>GH: Create Pull Request
    GH-->>U: PR abierto
```
