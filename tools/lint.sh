#!/usr/bin/env bash
# The ONLY sanctioned invocation of the vault linter (CHARLIE.md section 10).
# The parser-sensitive command is encoded exactly once, here, and never retyped.
# Usage: tools/lint.sh [optional-vault-path]   (defaults to ../KB)
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$DIR/lint_vault.py" "$@"
