#!/usr/bin/env bash
# Solver and algorithm benchmark. Needs python3 and an OpenSees binary.
# Set OPENSEES to point at one, e.g. the bundled solver:
#   OPENSEES=../../Alpaca4d.Gh/OpenSees-Solvers/mac/bin/OpenSees ./run.sh
set -e
cd "$(dirname "$0")"
export OPENSEES=${OPENSEES:-OpenSees}
command -v "$OPENSEES" >/dev/null 2>&1 || [ -x "$OPENSEES" ] || {
  echo "set OPENSEES=/path/to/OpenSees"; exit 1; }

python3 correctness.py     # which solvers can be trusted at all
echo
python3 bench.py           # and of those, which is quickest
