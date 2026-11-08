#!/bin/sh
# Use project runtimes without changing the user's global shell configuration.
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
export PATH="$project_root/.tools/node/bin:$project_root/.tools/bin:$PATH"
if [ "$#" -eq 0 ]; then
  echo "Usage: ./scripts/with-tools.sh COMMAND [ARG ...]" >&2
  exit 2
fi
exec "$@"
