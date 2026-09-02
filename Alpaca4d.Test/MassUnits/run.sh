#!/usr/bin/env bash
# Mass-unit regression check. Needs: a built Alpaca4d.Core, a C# compiler (mcs or csc),
# a net48 RhinoCommon, python3, and OpenSees on PATH.
set -e
cd "$(dirname "$0")"

CORE=${CORE:-../../Alpaca.Core/bin/Release/net48/Alpaca4d.Core.dll}
RHINO=${RHINO:-$(ls ~/.nuget/packages/rhinocommon/7.18.*/lib/net48/RhinoCommon.dll 2>/dev/null | head -1)}

[ -f "$CORE" ]  || { echo "build Alpaca.Core first, or set CORE=..."; exit 1; }
[ -f "$RHINO" ] || { echo "set RHINO=/path/to/net48/RhinoCommon.dll"; exit 1; }

work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
cp MassUnits.cs cross_element.py "$work/"
cp "$CORE" "$RHINO" "$work/"

( cd "$work"
  mcs -target:exe -out:MassUnits.exe -r:Alpaca4d.Core.dll -r:RhinoCommon.dll MassUnits.cs
  mono MassUnits.exe          # part 1: the Tcl Alpaca.Core writes
  echo
  python3 cross_element.py )  # part 2: does OpenSees agree, across element families
