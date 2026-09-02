# Solver choice

Picks the two defaults on **Analysis Settings** that decide how long a run takes: `System`,
the storage and factorisation scheme, and `Algorithm`, the iteration scheme. Both used to be
chosen without measurement, and both were wrong.

| Setting | Was | Is | Why |
| --- | --- | --- | --- |
| `System` | `SparseSPD` | `BandSPD` | fastest of the nine on every model measured, and `SparseSPD` returns wrong answers |
| `Algorithm` | `ModifiedNewton` | `Newton` | `ModifiedNewton` fails outright once anything yields |

## Correctness comes first

`correctness.py` sweeps a chain of trusses whose tip displacement is `P n L / EA` exactly,
across small degree-of-freedom counts:

```
  BandGen          ..........
  BandSPD          ..........
  ProfileSPD       ..........
  SuperLU          ..........
  UmfPack          ..........
  SparseSYM        X.X.X.....
  SparseSPD        X.X.X.....
  SparseGeneral    ..........
  FullGeneral      ..........
  free DOF:        1 2 3 4 5 6 8 10 20 40
```

`SparseSPD` — the shipped default — diverges to `inf`/`nan` at 1, 3 and 5 free DOF on a
problem with a closed-form answer. It also **fails on a framed building with a rigid
diaphragm at each floor**, which is not an edge case at all: `analyze` returns −3 while
`BandSPD`, `UmfPack`, `BandGen`, `SuperLU`, `SparseGeneral`, `ProfileSPD` and `FullGeneral`
all return the same displacement to 13 significant figures.

That is an OpenSees defect rather than an Alpaca4d one, but it landed on exactly the small
models a new user builds first.

## Then speed

`bench.py`, on a 5×5×5-bay frame, a 30×30 shell slab and a 12³ brick block, timing the whole
`analyze` including assembly, averaged over ten solves:

| system | frame | shell | brick |
| --- | --- | --- | --- |
| **BandSPD** | **5.4 ms** | **309 ms** | **210 ms** |
| UmfPack | 21.0 | 400 | 525 |
| SparseSPD *(old default)* | 21.2 | 420 | 1500 |
| BandGen | 9.0 | 515 | 1011 |
| FullGeneral | 14.0 | 1004 | 1333 |
| ProfileSPD | 28.9 | 745 | 5906 |
| SuperLU | 28.8 | 1054 | 3662 |
| SparseGeneral | 28.7 | 1056 | 3664 |

End to end, old defaults against new, same answers to 12 significant figures:

| model | `SparseSPD` + `ModifiedNewton` | `BandSPD` + `Newton` |
| --- | --- | --- |
| frame | 22.6 ms | **6.4 ms** |
| shell | 428 ms | **318 ms** |
| brick | 1499 ms | **230 ms** |

`BandSPD` needs a symmetric positive-definite matrix, which is what a supported linear or
mildly nonlinear structural model gives. It was checked against `UmfPack` under both
constraint handlers Alpaca4d offers, with rigid diaphragms, and on corotational shells at
large displacement, and agreed every time. On a genuinely unstable model every solver,
`BandSPD` included, returns −3 and says so — nothing fails silently. `UmfPack` is the
fallback worth reaching for if a model ever refuses to solve, being a general sparse solver
that assumes nothing about the matrix.

## Why `Newton` and not the faster `Linear`

On elastic models every algorithm agrees, and `Linear` is about 20 % quicker (258 ms against
310 ms on the shell) because it does one solve and never checks a residual. On a fibre-section
cantilever pushed past yield:

| algorithm | result | tip displacement |
| --- | --- | --- |
| `Newton` | converged | 24.7958 |
| `NewtonLineSearch`, `SecantNewton`, `BFGS`, `Broyden` | converged | 24.7958 |
| `Linear` | **reports success** | **24.7944** — the unconverged first guess |
| `ModifiedNewton` *(old default)* | **failed** | 0.0616 |
| `KrylovNewton` | failed | 0.0616 |

`ModifiedNewton` holds the initial tangent, so once a section yields it cannot recover inside
the iteration limit. `Linear` is the more dangerous of the two: it returns a wrong answer and
reports success. `Newton` re-forms the tangent every iteration and is correct in both regimes,
which is worth 20 % on the models where the other two happen to agree with it.

Pick `Linear` deliberately when the model is elastic throughout and the run is long enough for
20 % to matter.

## Running it

    OPENSEES=../../Alpaca4d.Gh/OpenSees-Solvers/mac/bin/OpenSees ./run.sh

Not wired into `Alpaca4d.sln` — it drives an external OpenSees, so it is a benchmark you run,
not part of the build. Timings are from the bundled macOS x86_64 binary; the ranking is worth
re-checking against the Windows build before it is treated as settled there.
