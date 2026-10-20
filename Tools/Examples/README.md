# Examples

    ./make.sh                                   # FootbridgeStudy.gh, next to its script
    ./make.sh path/to/Script.py [out.gh]         # any script with a build(doc), next to it
    ./make.sh SteelCantilever.py                # the Utilisation example
    ./make.sh ColumnDomain.py                   # the Interaction Domain example

Each example is a Python script that builds a Grasshopper definition from the real Grasshopper
and Alpaca4d components: it places them, wires them, names and groups them. `make.sh` writes it
straight to a `.gh` file, without Rhino. The same script also runs inside Rhino, where it opens
the definition on the canvas instead: in Rhino 8 open it in the ScriptEditor and press Run, in
Rhino 7 use `_RunPythonScript`.

| Example | Builds |
| --- | --- |
| `FootbridgeStudy.py` | The Explorer example: a steel truss footbridge analysed with Alpaca4d, and a design study of 108 designs over its span, depth, panels and chord section. |
| `SteelCantilever.py` | The Utilisation example: a 4 m steel cantilever checked to EN 1993-1-1, with the buckling lengths a cantilever needs and the Design menu open on the report. |
| `ColumnDomain.py` | The Interaction Domain example: a 400 x 600 reinforced concrete column's N-My-Mz domain, three combinations checked against it, and the domain drawn with Domain 3D, N-M Diagram and My-Mz Diagram beside the section. |
| `MixedModelSpeed.py` | A speed test of Assemble Model: a shell slab on steel beams and columns, cut at the slab's nodes, on a brick raft, with point, line, mesh and gravity loads in one pattern. One slider takes it from a hundred elements to forty thousand. |
| `../../Alpaca4d.Test/Optimisation/NonLinearOptimisationCases.py` | The eight test cases of Non-Linear Optimisation, each with a known answer. |

A script works with make.sh when it makes its objects through `emit()`, which uses `make_object`
when it is set, and has a `build(doc)` that adds them to `doc` and runs nothing at import.

## What it needs

* A Release build of `Alpaca4d.Gh`.
* mono with libgdiplus (`brew install mono`).
* Rhino 7 for Mac, for the IronPython it ships, the Visual Basic runtime Grasshopper needs and
  Grasshopper's component libraries - curve, maths, vector, transform, surface and mesh, and
  Galapagos. Point `R7` elsewhere if it is not in `/Applications`.
* Grasshopper and RhinoCommon 7.18 from the NuGet cache, which the build has already restored.

## How it works

Grasshopper's own document cannot be made outside Rhino: it needs Rhino's native core. Its
components can, and they can save themselves.

1. **GhHost.cs** runs IronPython in mono with Grasshopper, GH_IO and RhinoCommon loaded. Grasshopper
   refers to two Windows-only assemblies, its script editor and Eto's Windows platform; IronPython
   reads every type of an assembly it loads, so the host answers for those two with empty ones.
2. **WriteGh.py** makes every object the component libraries hold, to know each one's GUID, and
   hands the example script those objects and a document to collect them in.
3. The example's `build(doc)` makes, wires and lays out the definition as it does on the canvas.
   Its grid layout measures each object once Grasshopper has laid it out, so the sizes are the
   components' own.
4. **WriteGh.py** then saves the objects as Grasshopper saves a document: a header, the plug-ins
   used, and each object's own serialisation, framed so the file opens on the whole definition. It
   names any two objects that cover one another, as a check on the layout. Components with menus
   are left out of that check: mono measures their menus' text too wide, and Rhino lays them out
   again when it opens the file.

Alpaca4d's switcher components (ForceBeamColumn, Load Pattern) write a diagnostic to Rhino's
command line when they save, which is not there outside Rhino; WriteGh.py clears the parent the
diagnostic checks for, and the component sets it back as it saves.

The three examples are in the docs, under Examples, as `doc/examples/steel-cantilever`,
`footbridge-study` and `non-linear-optimisation` of the website repository: after writing a
`.gh` again, copy it there under that name.
