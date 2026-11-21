#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$ROOT_DIR/skills"

print_help() {
  cat <<'EOF'
Usage:
  ./skill.sh list
  ./skill.sh validate
  ./skill.sh help

Commands:
  list      Lista carpetas de skills disponibles
  validate  Valida frontmatter, referencias y evaluaciones
  help      Muestra esta ayuda
EOF
}

cmd="${1:-list}"

case "$cmd" in
  list)
    find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d ! -name "*-workspace" -exec basename {} \; | sort
    ;;
  validate)
    if command -v python3 >/dev/null 2>&1; then
      python3 "$ROOT_DIR/scripts/validate-skills.py"
    else
      exit_code=0
      while IFS= read -r skill_dir; do
        skill_name="$(basename "$skill_dir")"
        if [[ ! -f "$skill_dir/SKILL.md" ]]; then
          echo "ERROR: falta SKILL.md en $skill_name"
          exit_code=1
        fi
      done < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d ! -name "*-workspace" | sort)

      if [[ "$exit_code" -eq 0 ]]; then
        echo "OK: todos los skills tienen SKILL.md"
        echo "Nota: instala python3 para la validación completa."
      fi

      exit "$exit_code"
    fi
    ;;
  help|-h|--help)
    print_help
    ;;
  *)
    echo "Comando no reconocido: $cmd"
    print_help
    exit 1
    ;;
esac
