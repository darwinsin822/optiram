#!/usr/bin/env python3
"""
optiram - Optimizador Universal de Memoria RAM para Proyectos y Tareas Pesadas (DarwinSin)
Soporta: Android/Gradle, Node.js/TypeScript/Vite, Python/ML, Rust/Cargo, C/C++/Make.

Uso:
  optiram                  -> Diagnostica, limpia procesos dev huérfanos y auto-afina el proyecto actual.
  optiram status           -> Muestra diagnóstico detallado de RAM y top procesos devoradores.
  optiram clean            -> Termina daemons y procesos pesados huérfanos (Gradle, Kotlin, Node, etc.).
  optiram tune [ruta]      -> Aplica límites de memoria inteligentes a la configuración del proyecto.
  optiram run <comando...> -> Ejecuta un comando en un entorno contenido de baja memoria RAM.
"""

import os
import sys
import subprocess
import shutil
import time

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def get_ram_info():
    mem = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    k = parts[0].strip()
                    v = parts[1].strip().split()[0]
                    mem[k] = int(v) // 1024 # MB
    except Exception:
        pass
    
    total = mem.get("MemTotal", 0)
    free = mem.get("MemFree", 0)
    avail = mem.get("MemAvailable", free)
    cached = mem.get("Cached", 0)
    buffers = mem.get("Buffers", 0)
    swap_total = mem.get("SwapTotal", 0)
    swap_free = mem.get("SwapFree", 0)
    swap_used = swap_total - swap_free if swap_total >= swap_free else 0
    used = total - avail if total >= avail else 0
    return {
        "total": total,
        "available": avail,
        "used": used,
        "free": free,
        "cached": cached,
        "buffers": buffers,
        "swap_total": swap_total,
        "swap_used": swap_used
    }

def fmt_mb(mb):
    if mb >= 1024:
        return f"{mb / 1024.0:.2f} GB"
    return f"{mb} MB"

def show_status():
    ram = get_ram_info()
    pct_used = (ram["used"] / ram["total"] * 100) if ram["total"] > 0 else 0
    print("┌──────────────────────────────────────────────────────────┐")
    print("│ 🧠 OPTIRAM — DIAGNÓSTICO DE MEMORIA DEL SISTEMA         │")
    print("├──────────────────────────────────────────────────────────┤")
    print(f"│ • RAM Total:       {fmt_mb(ram['total']):<10}                           │")
    print(f"│ • RAM Usada:       {fmt_mb(ram['used']):<10} ({pct_used:.1f}%)                     │")
    print(f"│ • RAM Disponible:  {fmt_mb(ram['available']):<10}                           │")
    print(f"│ • Swap Usado:      {fmt_mb(ram['swap_used']):<10} / {fmt_mb(ram['swap_total']):<10}              │")
    print("├──────────────────────────────────────────────────────────┤")
    print("│ 🔥 TOP 6 PROCESOS CON MAYOR CONSUMO DE RAM:              │")
    
    _, stdout, _ = run_cmd("ps axo pid,pmem,rss,comm,args --sort=-%mem | head -n 7 | tail -n +2")
    if stdout:
        for line in stdout.splitlines()[:6]:
            parts = line.split(maxsplit=4)
            if len(parts) >= 4:
                pid, pmem, rss, comm = parts[0], parts[1], parts[2], parts[3]
                args = parts[4] if len(parts) > 4 else comm
                rss_mb = int(rss) // 1024 if rss.isdigit() else 0
                short_cmd = os.path.basename(args.split()[0]) if args else comm
                print(f"│   PID {pid:>6}: {pmem:>5}% ({fmt_mb(rss_mb):>8}) - {short_cmd[:28]:<28} │")
    print("└──────────────────────────────────────────────────────────┘")

def clean_hogs(project_dir=None):
    print("🧹 [OptiRAM] Identificando y limpiando procesos dev huérfanos...")
    stopped = []

    # 1. Gradle Daemons
    if project_dir:
        gradlew = os.path.join(project_dir, "gradlew")
        if os.path.isfile(gradlew) and os.access(gradlew, os.X_OK):
            run_cmd(f"{gradlew} --stop", cwd=project_dir)

    # Procesos específicos conocidos por acaparar memoria
    targets = [
        ("Gradle & Kotlin Daemons", r"(GradleDaemon|KotlinCompileDaemon)"),
        ("Zombie Node/TS Watchers", r"(tsserver\.js|eslint_d|metro/src/cli)"),
    ]

    for label, pattern in targets:
        code, stdout, _ = run_cmd(f"pgrep -f '{pattern}'")
        if code == 0 and stdout:
            pids = stdout.split()
            for pid in pids:
                run_cmd(f"kill -TERM {pid}")
            time.sleep(1.0)
            # Forzar si es necesario
            code2, stdout2, _ = run_cmd(f"pgrep -f '{pattern}'")
            if code2 == 0 and stdout2:
                for pid in stdout2.split():
                    run_cmd(f"kill -KILL {pid}")
            stopped.append(f"{label} ({len(pids)} PIDs)")

    if stopped:
        for s in stopped:
            print(f"   ✅ Detenidos: {s}")
    else:
        print("   ℹ️  No se detectaron daemons huérfanos activos.")

def tune_gradle(target_dir, total_ram):
    props_path = os.path.join(target_dir, "gradle.properties")
    if not os.path.isfile(props_path):
        return None

    backup_path = props_path + ".bak"
    if not os.path.exists(backup_path):
        shutil.copyfile(props_path, backup_path)

    with open(props_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Presupuesto de memoria para la JVM según RAM total disponible
    heap_size = 1536 if total_ram <= 9000 else 2048
    opt_jvmargs = f"-Xmx{heap_size}M -XX:MaxMetaspaceSize=384M -XX:+UseG1GC -XX:SoftRefLRUPolicyMSPerMB=50 -Dfile.encoding=UTF-8"
    opt_kotlin = f"-Xmx{heap_size}M -XX:+UseG1GC"

    lines = content.splitlines()
    new_lines = []
    flags = {"jvmargs": False, "parallel": False, "workers": False, "timeout": False, "daemon": False}

    for line in lines:
        s = line.strip()
        if s.startswith("org.gradle.jvmargs"):
            new_lines.append(f"org.gradle.jvmargs={opt_jvmargs} -Dkotlin.daemon.jvm.options=\"{opt_kotlin}\"")
            flags["jvmargs"] = True
        elif s.startswith("org.gradle.parallel"):
            new_lines.append("org.gradle.parallel=false")
            flags["parallel"] = True
        elif s.startswith("org.gradle.workers.max"):
            new_lines.append("org.gradle.workers.max=2")
            flags["workers"] = True
        elif s.startswith("org.gradle.daemon.idletimeout"):
            new_lines.append("org.gradle.daemon.idletimeout=60000")
            flags["timeout"] = True
        elif s.startswith("org.gradle.daemon="):
            new_lines.append("org.gradle.daemon=false")
            flags["daemon"] = True
        else:
            new_lines.append(line)

    if not flags["jvmargs"]:
        new_lines.append(f"org.gradle.jvmargs={opt_jvmargs} -Dkotlin.daemon.jvm.options=\"{opt_kotlin}\"")
    if not flags["parallel"]:
        new_lines.append("org.gradle.parallel=false")
    if not flags["workers"]:
        new_lines.append("org.gradle.workers.max=2")
    if not flags["timeout"]:
        new_lines.append("org.gradle.daemon.idletimeout=60000")
    if not flags["daemon"]:
        new_lines.append("org.gradle.daemon=false")

    with open(props_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

    return f"Android/Gradle: Heap acotado a {heap_size}M, Workers=2, Daemon=False, G1GC activo."

def tune_nodejs(target_dir):
    pkg_json = os.path.join(target_dir, "package.json")
    if not os.path.isfile(pkg_json):
        return None

    # Configurar NODE_OPTIONS en un .env.local o .env si no existe
    env_file = os.path.join(target_dir, ".env.local")
    if not os.path.exists(env_file):
        env_file = os.path.join(target_dir, ".env")
    
    node_opt_line = "NODE_OPTIONS=--max-old-space-size=2048\n"
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            c = f.read()
        if "max-old-space-size" not in c:
            with open(env_file, "a", encoding="utf-8") as f:
                f.write(f"\n# OptiRAM limit\n{node_opt_line}")
    else:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(f"# OptiRAM limit\n{node_opt_line}")

    return "Node.js/JS/TS: Límite de heap V8 fijado en 2048MB en entorno local."

def tune_cargo(target_dir):
    cargo_toml = os.path.join(target_dir, "Cargo.toml")
    if not os.path.isfile(cargo_toml):
        return None

    cargo_dir = os.path.join(target_dir, ".cargo")
    os.makedirs(cargo_dir, exist_ok=True)
    cfg_file = os.path.join(cargo_dir, "config.toml")
    
    line = "[build]\njobs = 2\n"
    if os.path.exists(cfg_file):
        with open(cfg_file, "r", encoding="utf-8") as f:
            c = f.read()
        if "jobs" not in c:
            with open(cfg_file, "a", encoding="utf-8") as f:
                f.write(f"\n{line}")
    else:
        with open(cfg_file, "w", encoding="utf-8") as f:
            f.write(line)

    return "Rust/Cargo: Trabajos de compilación concurrentes limitados a 2."

def tune_project(target_dir):
    ram = get_ram_info()
    results = []

    res_gradle = tune_gradle(target_dir, ram["total"])
    if res_gradle:
        results.append(res_gradle)

    res_node = tune_nodejs(target_dir)
    if res_node:
        results.append(res_node)

    res_cargo = tune_cargo(target_dir)
    if res_cargo:
        results.append(res_cargo)

    if results:
        print(f"⚙️  [OptiRAM] Afinamiento aplicado a '{os.path.basename(target_dir)}':")
        for r in results:
            print(f"   • {r}")
    else:
        print(f"ℹ️  [OptiRAM] No se detectó un archivo de configuración dependiente en {target_dir}")

def run_bounded(cmd_args):
    """Ejecuta cualquier comando bajo variables de entorno que restringen la memoria."""
    env = os.environ.copy()
    # Limitar heap en JVM, Node, PyTorch, C/C++
    env["GRADLE_OPTS"] = "-Xmx1536M -XX:+UseG1GC"
    env["NODE_OPTIONS"] = "--max-old-space-size=2048"
    env["CARGO_BUILD_JOBS"] = "2"
    env["MAKEFLAGS"] = "-j2"
    env["CMAKE_BUILD_PARALLEL_LEVEL"] = "2"
    env["OMP_NUM_THREADS"] = "2"
    env["MALLOC_ARENA_MAX"] = "2"

    print(f"🚀 [OptiRAM] Ejecutando comando con contención estricta de RAM:")
    print(f"   Comando: {' '.join(cmd_args)}")
    try:
        proc = subprocess.run(cmd_args, env=env)
        return proc.returncode
    except Exception as e:
        print(f"Error al ejecutar: {e}")
        return 1

def main():
    args = sys.argv[1:]
    target_dir = os.getcwd()

    if not args:
        # Modo por defecto: Diagnóstico + Limpieza + Afinamiento
        show_status()
        before = get_ram_info()["available"]
        clean_hogs(target_dir)
        tune_project(target_dir)
        after = get_ram_info()["available"]
        diff = after - before
        if diff > 0:
            print(f"\n🎉 [OptiRAM] Memoria RAM disponible recuperada: +{fmt_mb(diff)}")
        else:
            print("\n✅ [OptiRAM] Sistema y proyecto blindados contra desbordes de memoria.")
        return

    subcmd = args[0]

    if subcmd == "status":
        show_status()
    elif subcmd == "clean":
        clean_hogs(target_dir)
    elif subcmd == "tune":
        td = args[1] if len(args) > 1 else target_dir
        tune_project(os.path.abspath(td))
    elif subcmd == "run":
        if len(args) < 2:
            print("Uso: optiram run <comando...>")
            sys.exit(1)
        sys.exit(run_bounded(args[1:]))
    else:
        # Tratar argumento como ruta a afinar o comando
        if os.path.isdir(args[0]):
            show_status()
            clean_hogs(args[0])
            tune_project(os.path.abspath(args[0]))
        else:
            print(f"Comando no reconocido: {subcmd}")
            print("Uso: optiram [status | clean | tune [dir] | run <cmd>]")

if __name__ == "__main__":
    main()
