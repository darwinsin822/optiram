<div align="center">

# 🧠 OptiRAM
### Optimizador Universal de Memoria RAM y Procesos para Sistemas Linux

<img src="./assets/optiram.jpg" alt="OptiRAM Engine Banner" width="380px" style="border-radius: 12px; margin: 16px 0; box-shadow: 0 8px 24px rgba(0,0,0,0.5);" />

[![GitHub License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Environment](https://img.shields.io/badge/Environment-Universal_(Claude_Code_|_Codex_|_Antigravity_|_OpenCode)-blueviolet.svg)](#-compatibilidad-universal-multi-entorno)
[![Kernel Telemetry](https://img.shields.io/badge/Telemetry-Realtime_Diagnostics-cyan.svg)](#-evidencia-de-ejecución-en-vivo)
[![CI](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](scripts/ci.sh)

</div>

**OptiRAM** es la herramienta y skill universal de contención de memoria RAM, diagnóstico de procesos y afinamiento automático de entornos de desarrollo (Android/Gradle, Node.js/Next/Vite, Python/ML, Rust/Cargo y C/C++) para cualquier entorno asistido por Inteligencia Artificial (**Claude Code, OpenAI Codex, Google Antigravity 2.0, OpenCode CLI, Cursor, etc.**).

Previene la saturación del sistema, elimina procesos devoradores de RAM huérfanos y aplica presupuestos de memoria estrictos antes de que el kernel sufra congelamientos por swap.

---

## 🌐 Compatibilidad Universal Multi-Entorno

OptiRAM protege el entorno de ejecución en cualquier herramienta de desarrollo asistida por IA:

| Entorno / Plataforma | Integración y Despliegue |
| :--- | :--- |
| **🤖 Google Antigravity (AGY 2.0)** | Integración nativa como Skill en `~/.gemini/config/skills/optiram/` y comando global `optiram`. Activación por chat o subagentes. |
| **🧠 Claude Code (Anthropic)** | Compatible como skill de CLI en `~/.claude/skills/optiram` o ejecutando `optiram` directamente desde el terminal de Claude. |
| **⚡ OpenCode CLI** | Compatible con ejecución en terminal con OpenCode CLI (`opencode`) para salvaguardar la RAM durante builds pesados. |
| **⚙️ OpenAI Codex / ChatGPT** | Utilizable en sandboxes y sesiones con acceso a bash para limitar heaps de JVM y compiladores paralelos. |
| **💻 Cursor / VS Code / Windsurf** | Configurable en `.cursorrules` o terminal integrado para evitar que compiladores saturen el editor de código. |

---

## 📊 Evidencia de Ejecución en Vivo

A continuación se muestra la telemetría real obtenida por el motor de diagnóstico de OptiRAM en tiempo real:

<div align="center">
  <img src="./assets/optiram-execution.png" alt="OptiRAM Status Terminal Execution" width="90%" style="border-radius: 8px; border: 1px solid #282e3e; margin: 16px 0;" />
</div>

---

## 🛠️ Capacidades por Stack

| Stack / Proyecto | Acciones de OptiRAM |
| :--- | :--- |
| **Android / Gradle** | Reduce heap JVM de 4GB a 1536MB, activa G1GC, limita `workers.max=2`, desactiva daemons persistentes y paralelismo desmedido. |
| **Node.js / React / Vite** | Fija `NODE_OPTIONS="--max-old-space-size=2048"`, purga instancias de `tsserver` y watchers huérfanos. |
| **Python / ML** | Purgado de zombies de `multiprocessing` e `ipykernel`, configuración de `MALLOC_ARENA_MAX=2` y `OMP_NUM_THREADS=2`. |
| **Rust / Cargo** | Inyecta `.cargo/config.toml` con `jobs = 2` para evitar desbordes de memoria al compilar crates masivos. |
| **Linux Mint / Kernel** | Telemetría en vivo (RAM total, usada, disponible, swap) y Top de procesos acaparadores de recursos. |

---

## 🚀 Instalación y Despliegue Rápido

Para instalar OptiRAM globalmente en tu sistema (`~/.local/bin/optiram`) y como skill en Google Antigravity 2.0:

```bash
git clone https://github.com/darwinsin822/optiram.git
cd optiram
./scripts/install.sh
```

Para ejecutar las pruebas de integridad deterministas:
```bash
./scripts/ci.sh
```

---

## 💻 Uso de la CLI

```bash
# Diagnóstico en tiempo real y Top de procesos
optiram status

# Limpieza y purga de daemons huérfanos
optiram clean

# Auto-afinar presupuesto de memoria de un proyecto
optiram tune /ruta/al/proyecto

# Ejecutar una compilación con presupuesto acotado de RAM
optiram run ./gradlew assembleDebug
optiram run npm run build
optiram run cargo build --release
```

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.
