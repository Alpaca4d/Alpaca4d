# Alpaca4d.Test — running Grasshopper components without Grasshopper

Solves real Alpaca4d components against a head-less Rhino: no Rhino window, no
Grasshopper canvas, no `.gh` file. Fast enough to run on every change.

```
dotnet test
```

**Windows only.** It runs Rhino in-process through
[Rhino.Testing](https://github.com/mcneel/Rhino.Testing), McNeel's NUnit host for
Rhino.Inside, which needs **Rhino 8 or newer installed** on the machine. If Rhino lives
somewhere other than `C:\Program Files\Rhino 8\System`, edit
[Rhino.Testing.Configs.xml](Rhino.Testing.Configs.xml).

> Rhino.Inside is not available for macOS — McNeel's position as of June 2026 is that
> Rhino.Testing "hinges on Rhino.Inside working for macOS, which is not ready yet."
> Rhino for Mac's frameworks resolve symbols out of the `Rhinoceros` executable, so they
> cannot be loaded into a test process at all.

## What it covers

Because a real Rhino is running, component code behaves exactly as it does on a canvas:
the full geometry kernel, real Grasshopper parameters and goo, real `SolveInstance`.

* every component constructed, with its parameter surface checked against an approved snapshot;
* `SolveInstance` end to end — defaults, wired inputs, list inputs, runtime messages;
* switcher components (`nD`, `Uniaxial`, `BeamBase`, …) including unit selection;
* chaining components by handing one solve's output to the next input;
* the Alpaca4d.Core objects that come out, including their `WriteTcl()` text;
* **two whole workflows, solver included** — see below.

Still out of reach, because there is no canvas and no viewport: drawing
(`DrawViewportWires/Meshes`, the 09_Visualisation components), Eto dialogs, component
menu items, and `GH_Document.NewSolution` — the harness drives components directly
rather than running a document solution.

## Running

```
dotnet test                                     all tests
dotnet test --filter Shell                      one fixture
dotnet test --filter FullyQualifiedName~Cantilever
dotnet test --logger "trx;LogFileName=results.trx"
```

Visual Studio's Test Explorer works too. `.runsettings` forces an x64 test host, which
Rhino.Inside requires.

## The workflow tests

`CantileverWorkflowTests` and `ShellWorkflowTests` run the chains a user would build on
the canvas — material → section → element → supports + loads → load pattern → assemble →
analysis settings → **run analysis** → nodal displacements — and start a real OpenSees
process from the `OpenSees-Solvers` folder the build copies next to the test assembly.

Both models are chosen so the answer is known in closed form rather than stored as a
blob:

| Fixture | Model | Check | Measured |
| --- | --- | --- | --- |
| `CantileverWorkflowTests` | 10 m beam, square 0.4 m section, 10 kN tip load | `δ = P L³ / (3 E I)` = 7.4405 mm | 7.4487 mm (+0.11%, shear) |
| `ShellWorkflowTests` | 10 × 1 m strip, 0.3 m thick, 10 ASD shell quads, 10 kN tip load | `δ = P L³ / (3 E I)` = 7.0547 mm | 7.0408 mm (−0.2%, discretisation) |

Each assertion covers the components, the generated OpenSees input deck, the solver, the
`.mpco` recorder file and the HDF5 read-back — in about a second.

### The result readers

The 08_NumericalOutput components are read back and checked against statics, not against
stored numbers:

| Reader | Checked against |
| --- | --- |
| `NodalDisplacement` | the closed-form deflection, in both workflows |
| `ReactionForce` | equilibrium — the support returns `P` and `P L`; on the shell, the two corners sum to `P` |
| `BeamForce` | `N = 0`, shear `= P`, peak moment `= P L`, zero at the free end |
| `ShellForces` | the whole cantilever diagram: `myy` = 95 → 5 kNm/m across the ten elements, `vyz` = 10 kN/m, membrane zero |

Vy/Vz and My/Mz depend on an element's local axes, so the beam assertions use the
resultants, which statics fixes whatever the orientation. The shell values land in `myy`
and `vyz` because OpenSees derives each quad's local axes from its node order — Alpaca4d
only writes `-local` when the component's `LocalX` input is wired.

`ShellStresses` has no test because the component does not exist: every line of
`08_NumericalOutput/ShellStresses.cs` is commented out. `ModalAnalysisReport` needs a
natural-vibration workflow, which no fixture builds yet.

`WorkflowRun` is the shared scaffolding: it owns a temporary working directory (hence
`[NonParallelizable]`, since `RunAnalysis` changes the process working directory),
records every step so a failure names the component that caused it, and prints the
solver log next to it. To add a workflow, follow the shape of the two existing fixtures.

## Writing a component test

```csharp
[Test]
public void RectangleCS_computes_the_section_properties()
{
    var result = ComponentHarness.For<Alpaca4d.Gh.RectangleCS>()
                                 .Set("Width", 0.4)
                                 .Set("Height", 0.8)
                                 .Solve();

    Assert.That(result.Errors, Is.Empty, result.Describe());

    var section = result.Get<Alpaca4d.Section.RectangleCS>(0);
    Assert.That(section.Area, Is.EqualTo(0.32).Within(1e-12));
}
```

`Set` takes a parameter name, nickname or index, and any number of values (for list
inputs). Inputs left alone keep the default the component registered, so a bare
`.Solve()` computes what a freshly placed component would. `result.Errors`,
`result.Warnings` and `result.Describe()` cover the runtime messages;
`Get<T>`/`GetList<T>`/`All` read the outputs with the goo already unwrapped.

For a switcher component, pick the unit first:

```csharp
ComponentHarness.For<SimplexGh.nD>().SwitchTo("ElasticIsotropic (Alpaca4d)").Solve();
```

## The component API snapshot

`Approved/ComponentApi.approved.txt` records the GUID, name, category, exposure and full
parameter list of all ~87 components, plus each switcher's declared default and
evaluation units. (That last part earns its keep already: `BeamBase` declares a default
unit of `Beam (Alpaca4d)`, which no longer matches any registered unit — harmless, since
the base class falls back to the first one, but now visible.)

> The checked-in snapshot was generated against Grasshopper 7. If the first run on
> Rhino 8 reports a difference, read it before re-approving — it should be empty, since
> everything in the snapshot comes from Alpaca4d's own code rather than from Rhino.

A component's GUID and its parameter order, access and optionality are load-bearing:
change one and every Grasshopper file that already contains that component silently
loses wires or data, with no error anywhere.

`Component_api_matches_the_approved_snapshot` turns that into a failing test. When it
fires, read the diff it prints. If the change is deliberate, copy `.received.txt` over
the approved file and commit it *together with* the change, so the review shows exactly
which existing definitions are affected.

## Layout

```
SetupFixture.cs               starts the head-less Rhino, loads the .gha
Rhino.Testing.Configs.xml     which Rhino, and what to load with it
Harness/ComponentHarness.cs   Set(...) / Solve() / SolveResult
Harness/WorkflowRun.cs        multi-component runs: working directory, steps, results
Harness/ComponentApi.cs       the component-surface snapshot
Harness/OpenSees.cs           points Alpaca4d at the bundled solver
```
