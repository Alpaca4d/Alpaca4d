# Section properties

## Torsion constant of a solid rectangle

`RectangleCS.J` uses the closed form

    J = k a b^3        a = long side, b = short side
    k = 1 / (3 + 4.1 (b/a)^1.5)

which tracks the standard series

    J = a b^3 [ 1/3 - 0.21 (b/a) (1 - (b/a)^4 / 12) ]

to within about 2 % over the whole aspect-ratio range.

It only does so with the exponent **1.5**. It was written as `Math.Pow(..., 3 / 2)`, and
`3 / 2` in C# is integer division — so the exponent was **1**, and `J` came out low:

| b/a | error with the integer exponent |
| --- | --- |
| 0.05 | −3.4 % |
| 0.10 | −6.1 % |
| 0.25 | −11.5 % |
| 0.40 | −13.6 % |
| 0.50 | −13.5 % |
| 0.80 | −6.9 % |
| 1.00 | 0 % |

A **square is exactly right either way** — the ratio is one, so the exponent drops out. That
is why the check below tests a spread of aspect ratios and not just a square, and why the
bug survived: the obvious test case cannot see it.

`J` feeds the `section Elastic` line, so the effect is torsional stiffness only: members
carrying torsion were about 12 % too flexible about their own axis.

## Running it

    ./run.sh
