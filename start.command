#!/bin/bash
set -euo pipefail

PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$PROJECT_DIR"

if [[ "$(uname -s)" != "Darwin" || "$(uname -m)" != "x86_64" ]]; then
  echo "Ошибка: start.command предназначен для Intel Mac (x86_64)." >&2
  exit 1
fi

if [[ ! -x "$PROJECT_DIR/.venv/bin/parser-2gis-new" ]]; then
  echo "Первый запуск: сначала будет создана локальная .venv."
  "$PROJECT_DIR/install.command"
fi

echo "Запуск Parser2GIS: http://127.0.0.1:8666/"
echo "Для завершения нажмите Ctrl+C или закройте это окно терминала."
exec "$PROJECT_DIR/.venv/bin/parser-2gis-new" --web "$@"

