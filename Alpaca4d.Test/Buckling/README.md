# Linear buckling

    ./run.sh
    OPENSEES="/Applications/OpenSees3.8.0/bin/OpenSees /path/to/newer/OpenSees" ./run.sh

Checks `Alpaca4d.Buckling` and `Alpaca4d.BucklingSolver`, which Linear Buckling Analysis runs.
OpenSees has no buckling analysis, but it prints its stiffness matrix: with no load that is K_mat,
under the reference load K_mat − K_geo, and the load factors that buckle the model solve
K_mat φ = λ K_geo φ (Luigi Caglio's trick, as Michael Scott shows it on OpenSees Digital,
"Right under your nose", 2021).

Every case is a deck laid out the way Assemble writes one - Linear transformations,
`forceBeamColumn` with `NewtonCotes`, `ASDShellQ4 -corotational`, element loads, ties - and goes
through `Buckling.Analyse` as the component sends it: rewritten, both OpenSees runs, solved in C#,
shapes rebuilt and recorded.

| case | against |
| --- | --- |
| HEB 200 column, pinned-pinned, fixed-free, fixed-pinned, fixed-fixed, drawn as one element | Euler, both axes, two modes. PDelta converges as 1/n² from above, so n = 16 is checked to be close and above, and n = 8 and 16 extrapolated to within 0.1 % |
| the same column not split | no mode: a pinned-pinned element has no node to buckle at |
| portal frames, pinned and fixed base | the sway alignment chart, exact for an inextensible frame, so the members are made axially rigid: with their real areas the frame converges 0.12 % lower, the stretch of the beam |
| cantilever under its own weight, as an axial line load | Greenhill, (qL)_cr = 7.837 EI / L² |
| simply supported square plate, ASDShellQ4 | k = 4, after the rewrite to ShellNLDKGQ |
| two cantilevers tied by an equalDOF | the load of one, and the slave head moving and turning as the master |
| four cantilevers under a rigid diaphragm | weak sway, twist, strong sway |
| the same with one head offset by a rigid link | the same factors: a chain of ties, so on penalty |
| a column with no support, a hanging column, a plate of 6371 equations printed dense | a mechanism, nothing to buckle, refused |
| the shapes on file | an MPCO step per mode, the split nodes numbered after the model's |

What it caught on the way:

- The corotational ASDShellQ4 and ASDShellT3 of OpenSees 3.8.0 leave the stress stiffness of
  membrane forces out of their tangent, though their resisting forces have it, so a plate of them
  never buckles. Shells are rewritten as ShellNLDKGQ / ShellNLDKGT.
- After an `algorithm Linear` step ShellNLDKGQ commits the stresses of before the step and has no
  K_geo: Linear never asks for the resisting forces at the new state, which is where it updates
  them. The deck takes one Newton iteration (`test FixedNumIter 1`) instead - still a single solve,
  so the state stays first order.
- PDelta takes an element's axial force from one end, so an axial load spread along the element
  left every piece short of its mean: Greenhill was 23 % high with 16 pieces and converged as 1/n.
  The axial part of `-beamUniform` is moved onto the element's nodes, half each, and it converges as
  1/n² again.
- The Transformation handler gets a chain of ties wrong without a word - here the slave of a
  diaphragm that is also the retained node of a rigid link. A deck with one runs on penalty.

Printed dense, as OpenSees 3.8.0 can only print them, the matrices have 11 significant digits. That
is plenty for real members, but members a thousand times too stiff along their axis leave the sway
of a frame little of them: the axially rigid portal is checked to 0.4 % dense, to 0.1 % sparse. On
penalty the penalty number is measured from the stiffness of the model for the same reason.

A build newer than 3.8.0 prints them sparse, to 16 digits, and lifts the 4000-equation limit of the
dense print; with one the ties are also cross-checked against a Penalty run, which keeps every dof
an equation of its own. For scale, a plate of 39 000 equations took 28 s in OpenSees and 21 s in the
solver.
