#!/usr/bin/env bash
# ==============================================================================
# OptiRAM — Suite de Verificación Determinista e Integración Continua Local
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 [1/4] Validando sintaxis de scripts Bash y Python..."
bash -n "$REPO_DIR/scripts/install.sh"
python3 -c "import ast; ast.parse(open('$REPO_DIR/scripts/optiram.py').read()); print('  ✔ [PASS] optiram.py AST sintácticamente válido.')"

echo "🧪 [2/4] Probando instalación en limpio hermética (Clean-Room)..."
TMP_HOME=$(mktemp -d)
HOME="$TMP_HOME" bash "$REPO_DIR/scripts/install.sh" >/dev/null
if [ -f "$TMP_HOME/.gemini/config/skills/optiram/SKILL.md" ] && \
   [ -f "$TMP_HOME/.gemini/config/skills/optiram/scripts/optiram.py" ] && \
   [ -x "$TMP_HOME/.local/bin/optiram" ]; then
  echo "  ✔ [PASS] Instalación aislada verificada con éxito."
else
  echo "  ❌ [FAIL] Error en la instalación aislada."
  rm -rf "$TMP_HOME"
  exit 1
fi
rm -rf "$TMP_HOME"

echo "🧪 [3/4] Ejecutando diagnóstico de telemetría de memoria (optiram status)..."
python3 "$REPO_DIR/scripts/optiram.py" status >/dev/null
echo "  ✔ [PASS] Motor de diagnóstico de memoria ejecutado correctamente."

echo "🧪 [4/4] Verificando ausencia total de rutas privadas absolutas..."
if git -C "$REPO_DIR" grep -I -i "/home/darwinsin" ":(exclude).git" 2>/dev/null; then
  echo "  ❌ [FAIL] Se detectaron rutas privadas absolutas."
  exit 1
else
  echo "  ✔ [PASS] 0 rutas privadas absolutas detectadas."
fi

echo ""
echo "✅ Todas las pruebas de CI de OptiRAM pasaron al 100% (Código de salida 0)."
