// Linear Buckling Analysis: Alpaca4d.Buckling rewrites an assembled deck for a buckling run, has
// OpenSees print K_mat and K_mat - K_geo, and solves K_mat phi = lambda K_geo phi with
// BucklingSolver. Every case here is a deck laid out the way Assemble writes one, run through
// Buckling.Analyse as the component runs it, against a closed-form answer. See README.md.
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Linq;
using Alpaca4d;

class BucklingCheck
{
    static int fails = 0;

    static void Check(string what, bool ok, string detail = "")
    {
        Console.WriteLine($"  [{(ok ? "PASS" : "FAIL")}] {what}{(detail == "" ? "" : "  " + detail)}");
        if (!ok) fails++;
    }

    static string N(double v) => v.ToString("R", CultureInfo.InvariantCulture);
    static string F(double v) => v.ToString("0.0000", CultureInfo.InvariantCulture);
    static string Pct(double got, double want) => (100 * (got / want - 1)).ToString("+0.00;-0.00", CultureInfo.InvariantCulture) + "%";

    // kN and m, as Alpaca4d writes them.
    const double E = 210e6, G = 81e6, Nu = 0.3, P = 1000.0;
    // HEB 200: Iy strong, Iz weak. IPE 300 for a beam.
    const double A = 78.1e-4, Iy = 5696e-8, Iz = 2003e-8, J = 59.3e-8;
    const double Ab = 53.8e-4, Iyb = 8356e-8, Izb = 604e-8, Jb = 20.1e-8;

    /// <summary>
    /// A deck the way Assemble lays one out - nodes, supports, sections, elements, ties, masses,
    /// then the load patterns - one Tcl entry per object, with where the patterns begin.
    /// </summary>
    sealed class Deck
    {
        readonly Dictionary<(long, long, long), int> at = new Dictionary<(long, long, long), int>();
        readonly List<string> nodes = new List<string>(), fixes = new List<string>(), sections = new List<string>(),
                              elements = new List<string>(), ties = new List<string>(), patterns = new List<string>();
        public readonly Dictionary<int, double[]> Coordinates = new Dictionary<int, double[]>();
        int element = 0, section = 100, pattern = 0;

        public int Node(double x, double y, double z)
        {
            var key = ((long)Math.Round(x * 1e6), (long)Math.Round(y * 1e6), (long)Math.Round(z * 1e6));
            if (!at.TryGetValue(key, out int tag))
            {
                at[key] = tag = at.Count + 1;
                nodes.Add($"node {tag} {N(x)} {N(y)} {N(z)}\n");
                Coordinates[tag] = new[] { x, y, z };
            }
            return tag;
        }

        public void Fix(int node, string flags) => fixes.Add($"fix {node} {flags}\n");

        public int Section(double a, double iz, double iy, double j)
        {
            sections.Add($"section Elastic {++section} {N(E)} {N(a)} {N(iz)} {N(iy)} {N(G)} {N(j)}\n");
            return section;
        }

        public int ShellSection(double t)
        {
            sections.Add($"section ElasticMembranePlateSection {++section} {N(E)} {N(Nu)} {N(t)} 0.0\n");
            return section;
        }

        /// <summary>As ForceBeamColumn.WriteTcl: a Linear transformation tagged like the element.</summary>
        public int Beam(int i, int j, int sec, double vx, double vy, double vz, double mass = 0.0)
        {
            int tag = ++element;
            elements.Add($"geomTransf Linear {tag} {N(vx)} {N(vy)} {N(vz)}\n" +
                         $"element forceBeamColumn {tag} {i} {j} {tag} NewtonCotes {sec} 5 -mass {N(mass)}\n");
            return tag;
        }

        /// <summary>As ASDShellQ4.WriteTcl with -corotational.</summary>
        public int Quad(int a, int b, int c, int d, int sec)
        {
            int tag = ++element;
            elements.Add($"element ASDShellQ4 {tag} {a} {b} {c} {d} {sec} -corotational \n");
            return tag;
        }

        public void Tie(string tcl) => ties.Add(tcl + "\n");

        /// <summary>As LoadPattern.WriteTcl: its time series, then the pattern.</summary>
        public void Pattern(IEnumerable<string> loads)
        {
            int tag = ++pattern;
            patterns.Add($"timeSeries Linear {tag} -factor 1.0\n" +
                         $"pattern Plain {tag} {tag} -fact 1 {{\n" + string.Concat(loads.Select(l => "\t" + l + "\n")) + "}\n");
        }

        public (List<string> tcl, int patternStart, int nodes) Build()
        {
            var tcl = new List<string> { "model BasicBuilder -ndm 3 -ndf 6\n" };
            tcl.AddRange(nodes); tcl.AddRange(fixes); tcl.AddRange(sections);
            tcl.AddRange(elements); tcl.AddRange(ties);
            int start = tcl.Count;
            tcl.AddRange(patterns);
            return (tcl, start, at.Count);
        }
    }

    static string Folder;

    static Buckling.OpenSeesRunner Runner(string openSees) => deckPath =>
    {
        var start = new ProcessStartInfo(openSees, "\"" + deckPath + "\"")
        {
            UseShellExecute = false, RedirectStandardOutput = true, RedirectStandardError = true,
            WorkingDirectory = Path.GetDirectoryName(deckPath),
        };
        using (var p = Process.Start(start))
        {
            var stdout = p.StandardOutput.ReadToEndAsync();
            string stderr = p.StandardError.ReadToEnd();
            p.WaitForExit();
            return (stdout.Result, stderr, p.ExitCode);
        }
    };

    static Buckling.Outcome Run(string openSees, bool sparse, Deck deck, int divisions, int modes = 3,
                                string constraints = null, string recorder = null)
    {
        var (tcl, start, nodes) = deck.Build();
        var outcome = Buckling.Analyse(tcl, start, divisions, modes, nodes, Folder, "buckling", recorder, sparse,
                                       Runner(openSees), constraints);
        if (outcome.Failure != null)
            Console.WriteLine("        (" + outcome.Failure + ")");
        return outcome;
    }

    // ------------------------------------------------------------------ cases

    /// <summary>A 5 m HEB 200 column along Z, P on top; Iz bends it along Y.</summary>
    static Deck Column(string bottom, string top)
    {
        var d = new Deck();
        int a = d.Node(0, 0, 0), b = d.Node(0, 0, 5);
        d.Fix(a, bottom);
        if (top != null) d.Fix(b, top);
        int sec = d.Section(A, Iz, Iy, J);
        d.Beam(a, b, sec, 1, 0, 0);
        d.Pattern(new[] { $"load {b} 0 0 {N(-P)} 0 0 0" });
        return d;
    }

    /// <summary>x with P_cr = x² EI / L², per support, for the first modes about one axis.</summary>
    static readonly Dictionary<string, double[]> ColumnX = new Dictionary<string, double[]>
    {
        ["pinned-pinned"] = new[] { Math.PI, 2 * Math.PI },
        ["fixed-free"] = new[] { Math.PI / 2, 3 * Math.PI / 2 },
        ["fixed-pinned"] = new[] { 4.493409457909064, 7.725251836937707 },
        ["fixed-fixed"] = new[] { 2 * Math.PI, 8.986818915818128 },
    };

    static readonly Dictionary<string, (string bottom, string top)> ColumnSupports = new Dictionary<string, (string, string)>
    {
        ["pinned-pinned"] = ("1 1 1 0 0 1", "1 1 0 0 0 0"),
        ["fixed-free"] = ("1 1 1 1 1 1", null),
        ["fixed-pinned"] = ("1 1 1 1 1 1", "1 1 0 0 0 0"),
        ["fixed-fixed"] = ("1 1 1 1 1 1", "1 1 0 1 1 1"),
    };

    static double[] ColumnExact(string bc) =>
        ColumnX[bc].SelectMany(x => new[] { x * x * E * Iz / 25 / P, x * x * E * Iy / 25 / P }).OrderBy(v => v).Take(2).ToArray();

    static void Columns(string os, bool sparse)
    {
        Console.WriteLine("Columns, HEB 200, L = 5 m, P = 1000 kN, drawn as one element");
        foreach (var bc in ColumnX.Keys)
        {
            var exact = ColumnExact(bc);
            var (bottom, top) = ColumnSupports[bc];
            var l8 = Run(os, sparse, Column(bottom, top), 8, 2).Factors;
            var l16 = Run(os, sparse, Column(bottom, top), 16, 2).Factors;
            if (l8.Length < 2 || l16.Length < 2) { Check($"{bc}: two modes", false); continue; }
            for (int m = 0; m < 2; m++)
            {
                // PDelta converges as 1/n², from above, about 85 % / m² off with m elements to a
                // half wave: n = 16 is close, and the two together extrapolate to the exact value.
                // A second mode has shorter half waves, so it is further off at the same n.
                double richardson = (4 * l16[m] - l8[m]) / 3;
                Check($"{bc,-14} mode {m + 1}: n = 16 {F(l16[m])} ({Pct(l16[m], exact[m])}), from above",
                      l16[m] >= exact[m] * 0.9999 && l16[m] <= exact[m] * (m == 0 ? 1.015 : 1.03));
                Check($"{bc,-14} mode {m + 1}: extrapolated {F(richardson)} = {F(exact[m])}",
                      Math.Abs(richardson / exact[m] - 1) < 1e-3, Pct(richardson, exact[m]));
            }
        }

        // Not split, a pinned-pinned column has no node to buckle at.
        var whole = Run(os, sparse, Column(ColumnSupports["pinned-pinned"].bottom, ColumnSupports["pinned-pinned"].top), 1, 1);
        Check("pinned-pinned, not split: no buckling mode", whole.Failure == null && whole.Factors.Length == 0,
              whole.Factors.Length > 0 ? F(whole.Factors[0]) : "");
    }

    /// <summary>A portal frame in the XZ plane, HEB 200 columns, IPE 300 beam, out of plane held.</summary>
    static Deck Portal(bool fixedBase, double areaFactor = 1, double h = 4, double l = 6)
    {
        var d = new Deck();
        int a = d.Node(0, 0, 0), b = d.Node(0, 0, h), c = d.Node(l, 0, h), e = d.Node(l, 0, 0);
        d.Fix(a, fixedBase ? "1 1 1 1 1 1" : "1 1 1 1 0 1");
        d.Fix(e, fixedBase ? "1 1 1 1 1 1" : "1 1 1 1 0 1");
        d.Fix(b, "0 1 0 1 0 1");
        d.Fix(c, "0 1 0 1 0 1");
        int col = d.Section(A * areaFactor, Iz, Iy, J), beam = d.Section(Ab * areaFactor, Izb, Iyb, Jb);
        d.Beam(a, b, col, 1, 0, 0);
        d.Beam(e, c, col, 1, 0, 0);
        d.Beam(b, c, beam, 0, 0, 1);
        d.Pattern(new[] { $"load {b} 0 0 {N(-P)} 0 0 0", $"load {c} 0 0 {N(-P)} 0 0 0" });
        return d;
    }

    static double Bisect(Func<double, double> f, double lo, double hi)
    {
        for (int k = 0; k < 200; k++)
        {
            double mid = 0.5 * (lo + hi);
            if (Math.Sign(f(mid)) == Math.Sign(f(lo))) lo = mid; else hi = mid;
        }
        return 0.5 * (lo + hi);
    }

    static void Portals(string os, bool sparse)
    {
        // The alignment chart takes the members as inextensible, so they are made so here: with
        // their real areas the frame converges 0.12 % below it, the stretch of the beam.
        Console.WriteLine("Portal frames, h = 4 m, L = 6 m, sway, out of plane held, members axially rigid");
        double gTop = (Iy / 4) / (Iyb / 6);
        foreach (bool fixedBase in new[] { false, true })
        {
            // The sway alignment chart, which is exact for this frame:
            // pinned base x tan x = 6 / G, fixed base tan x = -x G / 6.
            double x = fixedBase
                ? Bisect(v => Math.Tan(v) + v * gTop / 6, Math.PI / 2 + 1e-9, Math.PI - 1e-9)
                : Bisect(v => v * Math.Tan(v) - 6 / gTop, 1e-9, Math.PI / 2 - 1e-9);
            double exact = x * x * E * Iy / 16 / P;
            var l8 = Run(os, sparse, Portal(fixedBase, 1000), 8, 1).Factors;
            var l16 = Run(os, sparse, Portal(fixedBase, 1000), 16, 1).Factors;
            if (l8.Length == 0 || l16.Length == 0) { Check($"{(fixedBase ? "fixed" : "pinned")} base: a mode", false); continue; }
            double richardson = (4 * l16[0] - l8[0]) / 3;
            string name = fixedBase ? "fixed base " : "pinned base";
            Check($"{name}: n = 8 {F(l8[0])} ({Pct(l8[0], exact)})", Math.Abs(l8[0] / exact - 1) < 0.01);
            // Printed dense, to 11 digits, members a thousand times too stiff along their axis
            // leave little of the sway stiffness: it is the difference of entries of 10^9 and more.
            // To 16 digits the same deck comes out exact.
            Check($"{name}: extrapolated {F(richardson)} = {F(exact)}", Math.Abs(richardson / exact - 1) < (sparse ? 1e-3 : 4e-3), Pct(richardson, exact));
        }
    }

    /// <summary>
    /// A cantilever buckling under its own weight, as an axial line load: Greenhill's
    /// (qL)_cr = 7.837 EI / L². The load is an eleLoad on the one element the column is drawn as,
    /// so it reaches the pieces only if the rewrite puts it on them.
    /// </summary>
    static void Greenhill(string os, bool sparse)
    {
        Console.WriteLine("Cantilever under its own weight (Greenhill)");
        const double q = 10.0, L = 5.0;
        double exact = 7.837347 * E * Iz / (L * L) / (q * L);
        var factors = new List<double>();
        foreach (int n in new[] { 8, 16 })
        {
            var d = new Deck();
            int a = d.Node(0, 0, 0), b = d.Node(0, 0, L);
            d.Fix(a, "1 1 1 1 1 1");
            int t = d.Beam(a, b, d.Section(A, Iz, Iy, J), 1, 0, 0);
            d.Pattern(new[] { $"eleLoad -ele {t} -type -beamUniform 0 0 {N(-q)}" });
            var l = Run(os, sparse, d, n, 1).Factors;
            factors.Add(l.Length > 0 ? l[0] : double.NaN);
            Check($"n = {n}: {F(factors.Last())} ({Pct(factors.Last(), exact)})", Math.Abs(factors.Last() / exact - 1) < (n == 8 ? 0.02 : 0.005));
        }
        double richardson = (4 * factors[1] - factors[0]) / 3;
        Check($"extrapolated {F(richardson)} = {F(exact)}", Math.Abs(richardson / exact - 1) < 2e-3, Pct(richardson, exact));
    }

    /// <summary>A square plate in the XY plane, simply supported, compressed along X, as ASDShellQ4 -corotational.</summary>
    static Deck Plate(int n, double t = 0.01)
    {
        var d = new Deck();
        var tag = new int[n + 1, n + 1];
        for (int i = 0; i <= n; i++)
            for (int j = 0; j <= n; j++)
                tag[i, j] = d.Node((double)i / n, (double)j / n, 0);
        int sec = d.ShellSection(t);
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                d.Quad(tag[i, j], tag[i + 1, j], tag[i + 1, j + 1], tag[i, j + 1], sec);
        for (int i = 0; i <= n; i++)
            for (int j = 0; j <= n; j++)
            {
                bool edge = i == 0 || i == n || j == 0 || j == n;
                if (i == 0 && j == 0) d.Fix(tag[i, j], "1 1 1 0 0 1");   // one drilling dof
                else if (i == 0) d.Fix(tag[i, j], "1 0 1 0 0 0");
                else if (edge) d.Fix(tag[i, j], "0 0 1 0 0 0");
            }
        d.Pattern(Enumerable.Range(0, n + 1).Select(j =>
            $"load {tag[n, j]} {N(-P / n * (j == 0 || j == n ? 0.5 : 1.0))} 0 0 0 0 0"));
        return d;
    }

    static void Plates(string os, bool sparse)
    {
        Console.WriteLine("Square plate 1 x 1 m, t = 10 mm, simply supported, uniaxial compression, as ASDShellQ4");
        double dPlate = E * 1e-6 / (12 * (1 - Nu * Nu));
        double exact = 4 * Math.PI * Math.PI * dPlate / P;
        foreach (int n in new[] { 8, 16 })
        {
            var outcome = Run(os, sparse, Plate(n), 1, 2);
            Check($"{n} x {n}: the ASDShellQ4 became ShellNLDKGQ", outcome.Deck.QuadShellsReplaced == n * n);
            var l = outcome.Factors;
            Check($"{n} x {n}: {(l.Length > 0 ? F(l[0]) : "none")} = {F(exact)} (k = 4)",
                  l.Length > 0 && Math.Abs(l[0] / exact - 1) < (n == 8 ? 0.005 : 0.002), l.Length > 0 ? Pct(l[0], exact) : "");
        }
    }

    // ------------------------------------------------------------------ ties

    /// <summary>
    /// Two identical cantilevers 3 m apart, their heads tied in X and Y by an equalDOF. Loaded alike
    /// they sway together at the load of one, and the tie carries nothing.
    /// </summary>
    static Deck TiedPair()
    {
        var d = new Deck();
        int a = d.Node(0, 0, 0), b = d.Node(0, 0, 5), c = d.Node(3, 0, 0), e = d.Node(3, 0, 5);
        d.Fix(a, "1 1 1 1 1 1"); d.Fix(c, "1 1 1 1 1 1");
        int sec = d.Section(A, Iz, Iy, J);
        d.Beam(a, b, sec, 1, 0, 0);
        d.Beam(c, e, sec, 1, 0, 0);
        d.Tie($"equalDOF {b} {e} 1 2");
        d.Pattern(new[] { $"load {b} 0 0 {N(-P)} 0 0 0", $"load {e} 0 0 {N(-P)} 0 0 0" });
        return d;
    }

    /// <summary>
    /// Four cantilevers on a 2 x 2 m square, their heads held by a rigid diaphragm about a node in
    /// the middle; and the same with one head offset by a rigid link, the load on the offset end.
    /// </summary>
    static Deck Diaphragm(bool link)
    {
        var d = new Deck();
        int sec = d.Section(A, Iz, Iy, J);
        var heads = new List<int>();
        foreach (var corner in new[] { new[] { 0.0, 0.0 }, new[] { 2.0, 0.0 }, new[] { 2.0, 2.0 }, new[] { 0.0, 2.0 } })
        {
            int a = d.Node(corner[0], corner[1], 0), b = d.Node(corner[0], corner[1], 5);
            d.Fix(a, "1 1 1 1 1 1");
            d.Beam(a, b, sec, 1, 0, 0);
            heads.Add(b);
        }
        int centre = d.Node(1, 1, 5);
        d.Fix(centre, "0 0 1 1 1 0");
        d.Tie($"rigidDiaphragm 3 {centre} {string.Join(" ", heads)}");
        var loads = heads.Select(h => $"load {h} 0 0 {N(-P)} 0 0 0").ToList();
        if (link)
        {
            int arm = d.Node(2.5, 2.0, 5);
            d.Tie($"rigidLink beam {heads[2]} {arm}");
            loads[2] = $"load {arm} 0 0 {N(-P)} 0 0 0";
        }
        d.Pattern(loads);
        return d;
    }

    static double ShapeDifference(Dictionary<int, double[]> a, Dictionary<int, double[]> b)
    {
        // A mode is found up to its sign, and a double one up to a rotation within its plane, so
        // compare only modes that are single, after matching the sign.
        double dot = a.Keys.Sum(k => a[k].Zip(b[k], (x, y) => x * y).Sum());
        double s = dot < 0 ? -1 : 1, worst = 0;
        foreach (var k in a.Keys)
            for (int d = 0; d < a[k].Length; d++)
                worst = Math.Max(worst, Math.Abs(a[k][d] - s * b[k][d]));
        return worst;
    }

    static void Ties(string os, bool sparse)
    {
        Console.WriteLine("Ties: equalDOF, rigidDiaphragm, rigidLink");
        double cantilever = Math.PI * Math.PI / 4 * E * Iz / 25 / P;

        var pair = Run(os, sparse, TiedPair(), 16, 1);
        var l = pair.Factors;
        Check($"equalDOF pair sways at the load of one: {(l.Length > 0 ? F(l[0]) : "none")} ~ {F(cantilever)}",
              l.Length > 0 && l[0] > cantilever && l[0] < cantilever * 1.005, l.Length > 0 ? Pct(l[0], cantilever) : "");
        if (pair.Shapes.Count > 0)
        {
            // The slave head's own dofs come from where nodeDOFs puts them, and by symmetry they
            // are the master head's: the same sway, the same rotations.
            var shape = pair.Shapes[0];
            double worst = Enumerable.Range(0, 6).Max(dof => Math.Abs(shape[2][dof] - shape[4][dof]));
            Check("equalDOF pair: slave head moves and turns as the master head", worst < 1e-6, worst.ToString("g3"));
        }

        // The columns bend about their weak axis along Y and their strong one along X, so the
        // diaphragm sways along Y at the load of one column, twists, then sways along X.
        double strong = cantilever * Iy / Iz;
        var square = Run(os, sparse, Diaphragm(false), 16, 3);
        l = square.Factors;
        Check($"diaphragm: sways along Y at the load of one column, {(l.Length > 0 ? F(l[0]) : "none")} ~ {F(cantilever)}",
              l.Length > 0 && Math.Abs(l[0] / cantilever - 1) < 0.005);
        Check($"diaphragm: twists in between, {(l.Length > 1 ? F(l[1]) : "none")}", l.Length > 2 && l[1] > l[0] * 1.01 && l[1] < l[2] / 1.01);
        Check($"diaphragm: sways along X at the strong-axis load, {(l.Length > 2 ? F(l[2]) : "none")} ~ {F(strong)}",
              l.Length > 2 && Math.Abs(l[2] / strong - 1) < 0.005);
        Check("diaphragm: Transformation, the ties not chained", square.Constraints == "Transformation" && square.Deck.ChainedNodes.Count == 0);

        // A rigid arm on one head, the load on its end: the slave of the diaphragm is the retained
        // node of the link, a chain the Transformation handler gets wrong. On penalty the column
        // still carries its load, so nothing changes.
        var chained = Run(os, sparse, Diaphragm(true), 16, 3);
        Check($"chained ties found and put on penalty ({chained.Constraints})",
              chained.Deck.ChainedNodes.SequenceEqual(new[] { 6 }) && chained.Constraints.StartsWith("Penalty"));
        for (int m = 0; m < 3 && m < l.Length; m++)
            Check($"chained mode {m + 1}: {(chained.Factors.Length > m ? F(chained.Factors[m]) : "none")} = {F(l[m])} without the arm",
                  chained.Factors.Length > m && Math.Abs(chained.Factors[m] / l[m] - 1) < 5e-4,
                  chained.Factors.Length > m ? Pct(chained.Factors[m], l[m]) : "");

        if (!sparse)
            return;

        // Under Penalty every dof is an equation of its own, so the shapes need no rebuilding:
        // what the Transformation run rebuilt for the tied nodes has to match. Only with the
        // matrices printed to 16 digits - at 11 the penalty numbers swamp K_geo of the tied dofs.
        foreach (bool link in new[] { false })
        {
            string name = "diaphragm";
            Func<Deck> deck = () => Diaphragm(link);
            var folded = Run(os, true, deck(), 16, 3, "Transformation");
            var penalty = Run(os, true, deck(), 16, 3, "Penalty 1.0e12 1.0e12");
            if (folded.Factors.Length < 3 || penalty.Factors.Length < 3) { Check($"{name}: three modes both ways", false); continue; }
            for (int m = 0; m < 3; m++)
                Check($"{name} mode {m + 1}: Transformation {F(folded.Factors[m])} = Penalty {F(penalty.Factors[m])}",
                      Math.Abs(folded.Factors[m] / penalty.Factors[m] - 1) < 1e-5);
            // The twist is single; the sway pair is not.
            double diff = ShapeDifference(folded.Shapes[2], penalty.Shapes[2]);
            Check($"{name}: the twist rebuilt on the tied nodes as Penalty has it", diff < 1e-4, diff.ToString("g3"));
        }
    }

    static void Edges(string os, bool sparse)
    {
        Console.WriteLine("Edges");
        var loose = Column("0 0 0 0 0 0", null);
        var outcome = Run(os, sparse, loose, 4, 1);
        Check("a column with no support is a mechanism", outcome.Failure != null && outcome.Factors.Length == 0);

        var hanging = new Deck();
        int a = hanging.Node(0, 0, 0), b = hanging.Node(0, 0, -5);
        hanging.Fix(a, "1 1 1 1 1 1");
        hanging.Beam(a, b, hanging.Section(A, Iz, Iy, J), 1, 0, 0);
        hanging.Pattern(new[] { $"load {b} 0 0 {N(-P)} 0 0 0" });
        outcome = Run(os, sparse, hanging, 4, 1);
        Check("a hanging column buckles under nothing", outcome.Failure == null && outcome.Factors.Length == 0);

        if (!sparse)
        {
            outcome = Run(os, false, Plate(32), 1, 1);
            Check($"dense refuses {outcome.Equations} equations (over {Buckling.DenseLimit})",
                  outcome.Failure != null && outcome.Equations > Buckling.DenseLimit);
        }
    }

    /// <summary>The second run: the modes recorded as steps an MPCO reader finds, step 0 the first.</summary>
    static void Recorder(string os, bool sparse)
    {
        Console.WriteLine("The buckled shapes on file");
        string path = Path.Combine(Folder, "buckling_modes.mpco");
        var outcome = Run(os, sparse, Column("1 1 1 1 1 1", null), 4, 2, recorder: path);
        Check("the shapes were written", outcome.Failure == null && File.Exists(path) && new FileInfo(path).Length > 0);
        Check("the cantilever's split nodes follow the model's two, without a gap",
              Buckling.OutputTag(outcome.Deck, outcome.Deck.SplitNodes[0].Tag, 2) == 3 &&
              Buckling.OutputTag(outcome.Deck, outcome.Deck.SplitNodes.Last().Tag, 2) == 5);
        var tip = outcome.Shapes[0][2];
        Check("the first shape is normalised to a tip sway of 1", Math.Abs(Math.Max(Math.Abs(tip[0]), Math.Abs(tip[1])) - 1) < 1e-12);
    }

    static void Main(string[] args)
    {
        Folder = Path.Combine(Path.GetTempPath(), "alpaca4d_buckling_" + Process.GetCurrentProcess().Id);
        Directory.CreateDirectory(Folder);
        try
        {
            foreach (var os in args.Where(File.Exists))
            {
                bool sparse = Buckling.CanPrintSparse(Folder, Runner(os));
                Console.WriteLine($"\n=== {os}: matrices printed {(sparse ? "sparse" : "dense")} ===\n");
                Columns(os, sparse);
                Portals(os, sparse);
                Greenhill(os, sparse);
                Plates(os, sparse);
                Ties(os, sparse);
                Edges(os, sparse);
                Recorder(os, sparse);
            }
        }
        finally
        {
            try { Directory.Delete(Folder, true); } catch (IOException) { }
        }

        Console.WriteLine(fails == 0 ? "\nAll checks passed." : $"\n{fails} check(s) failed.");
        Environment.Exit(fails == 0 ? 0 : 1);
    }
}
