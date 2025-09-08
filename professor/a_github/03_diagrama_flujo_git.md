# Diagrama de Flujo: Entrega de Tareas en GitHub

> **🎯 Visualización completa del proceso** - Sigue el flujo paso a paso para una entrega exitosa

## 📊 Flujo Visual Completo

```mermaid
flowchart TD
    A["🏠 INICIO<br/>Repositorio Local"] --> B["📥 PASO 1: Sincronizar<br/>git fetch upstream<br/>git merge upstream/main<br/>git push origin main"]
    
    B --> C["🌿 PASO 2: Nueva Rama<br/>git checkout -B nombre-tarea<br/>git status"]
    
    C --> D["📝 PASO 3: Trabajar en tu Carpeta<br/>📁 students/tu-usuario/<br/>⚠️ Solo modificar TU carpeta<br/>touch .gitkeep (si carpeta vacía)"]
    
    D --> E["💾 PASO 4: Guardar Cambios<br/>git add students/tu-usuario/...<br/>❌ Evitar: git add .<br/>git commit -m 'Tarea: descripción'"]
    
    E --> F["☁️ PASO 5: Subir Rama<br/>git push origin nombre-tarea<br/>✅ Verificar en GitHub"]
    
    F --> G{"🔀 PASO 6: Fusionar<br/>¿Cómo prefieres?"}
    
    G -->|"🌐 GitHub (Recomendado)"| H["📋 Pull Request Interno<br/>tu-repo/main ← tu-repo/rama-tarea<br/>✅ Merge en GitHub<br/>📍 main actualizado en la nube"]
    
    G -->|"💻 Local"| I["🔄 Merge Local<br/>git checkout main<br/>git merge nombre-tarea<br/>git push origin main<br/>📍 main actualizado local → nube"]
    
    H --> J["🎯 PASO 7: Pull Request Final<br/>📤 sonder_art/main ← tu-repo/main<br/>📝 Título: 'Carpeta de Tareas {nombre}'<br/>🔍 Revisar SOLO tu carpeta afectada"]
    
    I --> J
    
    J --> K["⏳ PASO 8: Esperar Aprobación<br/>👨‍🏫 Profesor revisa y aprueba<br/>✅ Merge al repositorio principal"]
    
    K --> L["🔄 PASO 8b: Sincronizar Final<br/>git checkout main<br/>git pull upstream main<br/>git push origin main<br/>🎉 ¡Completado!"]
    
    L --> M["✅ ÉXITO<br/>Repositorio sincronizado<br/>Tarea entregada"]
    
    %% Estilos para mejor UX
    classDef startEnd fill:#e1f5fe,stroke:#01579b,stroke-width:3px,color:#000
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px,color:#000
    classDef decision fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef github fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef warning fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000
    classDef success fill:#e0f2f1,stroke:#00695c,stroke-width:3px,color:#000
    
    class A,M startEnd
    class B,C,D,E,F,H,I,J,K,L process
    class G decision
    class H,J github
    class D warning
    class M success
```

---

## 🎨 Código de Colores del Diagrama

| Color | Significado | Elementos |
|-------|-------------|-----------|
| 🔵 **Azul** | Inicio y Final | Puntos de entrada y salida |
| 🟣 **Morado** | Procesos Normales | Pasos regulares del flujo |
| 🟠 **Naranja** | Decisiones | Puntos donde eliges una opción |
| 🟢 **Verde** | Acciones en GitHub | Interacciones con la plataforma |
| 🔴 **Rojo** | Advertencias | Pasos críticos que requieren atención |
| 🟢 **Verde Oscuro** | Éxito | Completación exitosa |

---

## 📋 Información Clave por Paso

### 🔄 **Flujo Principal vs Alternativo**

| Aspecto | 🌐 **GitHub (Recomendado)** | 💻 **Local** |
|---------|---------------------------|---------------|
| **Dificultad** | ⭐⭐ Fácil | ⭐⭐⭐ Intermedio |
| **Visibilidad** | ✅ Clara en interfaz web | ❌ Solo en terminal |
| **Reversibilidad** | ✅ Fácil de deshacer | ⚠️ Requiere más comandos |
| **Aprendizaje** | 📚 Enseña GitHub UI | 🔧 Enseña Git puro |

### ⚠️ **Puntos Críticos de Atención**

#### 🎯 **Paso 3: Zona de Trabajo**
- **✅ Correcto:** `students/tu-usuario/mi-tarea/`
- **❌ Incorrecto:** Cualquier carpeta fuera de tu usuario
- **💡 Tip:** Usa `pwd` para verificar tu ubicación

#### 🎯 **Paso 4: Staging de Archivos**
- **✅ Correcto:** `git add students/tu-usuario/archivo.txt`
- **❌ Peligroso:** `git add .` (puede incluir archivos no deseados)
- **💡 Tip:** Usa `git status` antes de cada commit

#### 🎯 **Paso 7: Pull Request Final**
- **✅ Dirección correcta:** `sonder_art/main ← tu-repo/main`
- **❌ Dirección incorrecta:** `tu-repo/main ← sonder_art/main`
- **💡 Tip:** Revisa la dirección antes de crear el PR

---

## 🚀 Comandos Rápidos por Paso

### **Secuencia Completa Resumida**
```bash
# Paso 1: Sincronizar
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# Paso 2: Nueva rama
git checkout -b mi-tarea-nueva

# Paso 3-4: Trabajar y guardar
cd students/mi-usuario
# ... hacer cambios ...
git add students/mi-usuario/
git commit -m "Tarea: descripción clara"

# Paso 5: Subir
git push origin mi-tarea-nueva

# Paso 6: Fusionar (opción GitHub recomendada)
# → Ir a GitHub y crear PR interno

# Paso 7: PR final
# → Crear PR desde tu main al main del profesor

# Paso 8: Sincronizar final (después de aprobación)
git checkout main
git pull upstream main
git push origin main
```

---

## 💡 Tips de UX para el Flujo

### 🎯 **Antes de Empezar**
- [ ] Verifica que tienes configurado `upstream`
- [ ] Confirma tu identidad Git: `git config --list`
- [ ] Asegúrate de estar en la carpeta correcta: `pwd`

### 🎯 **Durante el Proceso**
- [ ] Usa `git status` frecuentemente
- [ ] Verifica cada comando antes de ejecutarlo
- [ ] Lee los mensajes de Git cuidadosamente

### 🎯 **Al Final**
- [ ] Revisa el PR antes de enviarlo
- [ ] Confirma que solo tu carpeta está afectada
- [ ] Espera confirmación del profesor antes de continuar

---

## 🔗 Enlaces Relacionados

- 📖 **[Flujo Detallado](01_flujo_git.md)** - Instrucciones paso a paso completas
- 📚 **[Cheatsheet](02_cheatsheet_git_github.md)** - Comandos básicos y referencia rápida
- 🌐 **GitHub Docs** - Documentación oficial de GitHub
- 📺 **Git Tutorials** - Videos tutoriales recomendados
