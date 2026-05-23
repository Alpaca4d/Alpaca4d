# Alpaca4d.Utils

Utility to generate `data.bin` from `data.json`.

## Prerequisites

- [Mono](https://www.mono-project.com/) (includes `msbuild` and `mono`)

Install on macOS:

```bash
brew install mono
```

## Build & Run

1. Restore NuGet packages:

```bash
nuget restore /Users/mp/Documents/GitHub/Alpaca4d/Alpaca4d.sln
```

2. Build the project:

```bash
msbuild /Users/mp/Documents/GitHub/Alpaca4d/Alpaca4d.Utils/Alpaca4d.Utils.csproj /p:Configuration=Debug
```

3. Run from `bin/Debug/` (required for relative paths to resolve correctly):

```bash
cd Alpaca4d.Utils/bin/Debug && mono CreateLicense.exe
```

## Output

`data.bin` is created in the `Alpaca4d.Utils/` directory.

> **Note:** The executable must be run from `bin/Debug/` because it reads `data.json` from the working directory and writes `data.bin` two directories up.
