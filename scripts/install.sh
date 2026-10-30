#!/usr/bin/env bash
# ==============================================================================
# OptiRAM — Instalador Automatizado e Idempotente para Google Antigravity & Linux
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_DIR="${HOME}/.gemini/config/skills/optiram"
BIN_DIR="${HOME}/.local/bin"

echo "🧠 Instalando OptiRAM en Google Antigravity y entorno local..."

# 1. Instalar Skill en Antigravity
mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/assets"
cp -u "$REPO_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
cp -u "$REPO_DIR/scripts/optiram.py" "$SKILL_DIR/scripts/optiram.py"
chmod +x "$SKILL_DIR/scripts/optiram.py"

if [ -d "$REPO_DIR/assets" ]; then
  cp -ru "$REPO_DIR/assets/"* "$SKILL_DIR/assets/"
fi

# 2. Instalar CLI global en ~/.local/bin
mkdir -p "$BIN_DIR"
cat << 'BIN_EOF' > "$BIN_DIR/optiram"
#!/usr/bin/env bash
exec python3 "${HOME}/.gemini/config/skills/optiram/scripts/optiram.py" "$@"
BIN_EOF
chmod +x "$BIN_DIR/optiram"

echo "✔ OptiRAM instalado correctamente:"
echo "  • Skill: $SKILL_DIR"
echo "  • CLI:   $BIN_DIR/optiram"
echo "  Disponible en Antigravity mediante: 'optiram', 'optimizar ram' o 'liberar ram'."
