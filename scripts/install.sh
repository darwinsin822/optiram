#!/usr/bin/env bash
# ==============================================================================
# OptiRAM — Instalador Automatizado e Idempotente Universal
# Compatible con: Google Antigravity, Claude Code, OpenCode CLI & Linux
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_DIR="${HOME}/.gemini/config/skills/optiram"
BIN_DIR="${HOME}/.local/bin"

echo "🧠 Instalando OptiRAM (Universal)..."

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

# 3. Claude Code (Si el directorio ~/.claude existe)
if [ -d "${HOME}/.claude" ]; then
  CLAUDE_TARGET="${HOME}/.claude/skills/optiram"
  mkdir -p "$CLAUDE_TARGET"
  cp -u "$REPO_DIR/SKILL.md" "$CLAUDE_TARGET/SKILL.md"
  echo "✔ OptiRAM vinculado a Claude Code: $CLAUDE_TARGET"
fi

# 4. OpenCode CLI (Si el directorio ~/.config/opencode existe)
if [ -d "${HOME}/.config/opencode" ]; then
  OPENCODE_TARGET="${HOME}/.config/opencode/skills/optiram"
  mkdir -p "$OPENCODE_TARGET"
  cp -u "$REPO_DIR/SKILL.md" "$OPENCODE_TARGET/SKILL.md"
  echo "✔ OptiRAM vinculado a OpenCode CLI: $OPENCODE_TARGET"
fi

echo "✔ OptiRAM instalado correctamente:"
echo "  • Skill: $SKILL_DIR"
echo "  • CLI:   $BIN_DIR/optiram"
echo "  Disponible en terminal y en Antigravity mediante: 'optiram', 'optimizar ram' o 'liberar ram'."
