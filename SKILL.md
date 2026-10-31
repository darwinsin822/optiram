---
name: optiram
description: >-
  Optimizador Universal de Memoria RAM y Procesos para TODOS los proyectos (Android/Gradle,
  Node.js/Next/Vite, Python/ML, Rust/Cargo, C/C++). Actívalo cuando el usuario diga "optiram",
  "optimizar ram", "liberar ram", "bajar consumo de ram", "optimiza la ram", "optimiza esta tarea",
  o cuando una tarea o compilación esté saturando la memoria del sistema. Detiene procesos
  y daemons devoradores de RAM huérfanos, auto-afina la configuración de proyectos para presupuestos
  de memoria seguros, y ejecuta tareas en un entorno contenido.
---

# 🧠 OptiRAM — Optimizador Universal de Memoria RAM (DarwinSin)

**OptiRAM** es la skill universal de gestión, contención y optimización de memoria RAM para cualquier tipo de proyecto y entorno en Linux Mint / Antigravity 2.0.

---

## ⚡ Cuándo Invocar OptiRAM
- Cuando el usuario mencione: `"optiram"`, `"optimizar ram"`, `"liberar ram"`, `"te estás llevando la ram"`, `"optimiza esta tarea"`.
- Cuando una compilación pesada o proceso esté elevando el consumo de memoria por encima del 75% o agotando la swap.
- Antes de iniciar compilaciones masivas (Android Studio/Gradle, Vite/Next.js, Rust `cargo build`, C++ `make/ninja`).

---

## 🛠️ Capacidades Universales por Stack

| Stack / Proyecto | Acciones de OptiRAM |
| :--- | :--- |
| **Android / Gradle / Kotlin** | Bajar heap de JVM de 4GB a 1536MB, activar `G1GC`, limitar `workers.max=2`, desactivar paralelismo saturante (`parallel=false`), desactivar daemons permanentes (`daemon=false`), timeout de 60s. |
| **Node.js / React / Next / Vite** | Fijar `NODE_OPTIONS="--max-old-space-size=2048"`, purgar procesos huérfanos de `tsserver` o watchers colgados. |
| **Python / ML / PyTorch** | Purgar zombies de `multiprocessing` e `ipykernel`, configurar `MALLOC_ARENA_MAX=2` y `OMP_NUM_THREADS=2`. |
| **Rust / Cargo** | Configurar `.cargo/config.toml` con `jobs = 2` para evitar desbordes al compilar crates paralelos. |
| **C / C++ / CMake / Ninja** | Inyectar `MAKEFLAGS="-j2"` y `CMAKE_BUILD_PARALLEL_LEVEL=2`. |
| **Sistema Operativo Linux Mint** | Diagnóstico en tiempo real (RAM total, usada, libre, disponible, swap) y Top de procesos acaparadores. |

---

## 🚀 Comandos y Uso de la CLI `optiram`

El script está vinculado globalmente en el `PATH` (`~/.local/bin/optiram`):

```bash
# 1. Diagnóstico completo + Limpieza de daemons huérfanos + Auto-afinamiento del proyecto actual
optiram

# 2. Solo diagnóstico de RAM y procesos pesados
optiram status

# 3. Solo limpieza y purga de daemons y servidores huérfanos
optiram clean

# 4. Auto-afinar un proyecto específico
optiram tune /ruta/al/proyecto

# 5. Ejecutar cualquier tarea o compilación en modo de bajo consumo (RAM acotada)
optiram run ./gradlew :app:assembleFossDebug
optiram run npm run build
optiram run cargo build --release
```

---

## 📋 Regla de Intervención de OptiRAM
1. **Medir:** Revisar `optiram status` antes de modificar o matar procesos.
2. **Contener:** No esperar a que el sistema empiece a congelarse por swap; aplicar límites de heap y threads tempranamente.
3. **Persistir:** Asegurar que los archivos de configuración (`gradle.properties`, `.env`, `.cargo/config.toml`) mantengan los parámetros optimizados para futuras ejecuciones.
