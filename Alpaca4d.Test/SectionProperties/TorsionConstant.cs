// RectangleCS.J against the standard series for a solid rectangle:
//     J = a b^3 [ 1/3 - 0.21 (b/a) (1 - (b/a)^4 / 12) ]      a = long side, b = short side
// The shipped closed form k = 1/(3 + 4.1 (b/a)^1.5) tracks that to within a few percent.
// It only does so with the exponent 1.5; written as the integer expression 3/2 it is 1,
// which is what this guards against.
using System;
using Alpaca4d.Material;
using Alpaca4d.Section;

class TorsionConstant
{
    static int fails = 0;

    static double Series(double w, double h)
    {
        double a = Math.Max(w, h), b = Math.Min(w, h), r = b / a;
        return a * Math.Pow(b, 3) * (1.0 / 3.0 - 0.21 * r * (1 - Math.Pow(r, 4) / 12.0));
    }

    static void Main()
    {
        var mat = new UniaxialMaterialElastic("steel", 2.1e8, 2.1e8, 0.0, 8.077e7, 0.3, 7850);
        Console.WriteLine("RectangleCS.J vs the series\n");
        Console.WriteLine($"  {"w x h",-16}{"b/a",7}{"Alpaca4d",15}{"series",15}{"err %",9}");

        foreach (var wh in new[] { (0.10,0.10), (0.20,0.10), (0.40,0.10), (0.25,0.10),
                                   (0.30,0.15), (0.60,0.30), (0.10,0.40), (1.00,0.05) })
        {
            var sec = new RectangleCS("r", wh.Item1, wh.Item2, mat);
            double got = sec.J, want = Series(wh.Item1, wh.Item2);
            double err = 100 * (got / want - 1);
            bool ok = Math.Abs(err) <= 3.0;           // the closed form is an approximation
            if (!ok) fails++;
            Console.WriteLine($"  [{(ok ? "PASS" : "FAIL")}] {wh.Item1:F2} x {wh.Item2:F2}" +
                              $"{Math.Min(wh.Item1,wh.Item2)/Math.Max(wh.Item1,wh.Item2),7:F2}" +
                              $"{got,14:E4}{want,14:E4}{err,9:+0.00;-0.00}");
        }

        // A square is the one shape the integer-division bug could not affect: the ratio is
        // one, so the exponent drops out. Keep it, so the guard cannot pass on squares alone.
        var sq = new RectangleCS("sq", 0.3, 0.3, mat);
        double k = sq.J / Math.Pow(0.3, 4);
        bool sqOk = Math.Abs(k - 0.1408) < 1e-3;
        if (!sqOk) fails++;
        Console.WriteLine($"\n  [{(sqOk ? "PASS" : "FAIL")}] square k = J/a^4 = {k:F5}  (Saint-Venant 0.1406)");

        Console.WriteLine(fails == 0 ? "\nALL PASS" : $"\n{fails} FAILED");
        Environment.Exit(fails == 0 ? 0 : 1);
    }
}
