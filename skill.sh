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
  validate  Verifica que cada skill tenga SKILL.md
  help      Muestra esta ayuda
EOF
}

cmd="${1:-list}"

case "$cmd" in
  list)
    find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
    ;;
  validate)
    exit_code=0
    while IFS= read -r skill_dir; do
      skill_name="$(basename "$skill_dir")"
      if [[ ! -f "$skill_dir/SKILL.md" ]]; then
        echo "ERROR: falta SKILL.md en $skill_name"
        exit_code=1
      fi
    done < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d | sort)

    if [[ "$exit_code" -eq 0 ]]; then
      echo "OK: todos los skills tienen SKILL.md"
    fi

    exit "$exit_code"
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
