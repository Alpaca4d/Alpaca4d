using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using NUnit.Framework;
using Rhino.Geometry;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// The moment-curvature chain, end to end through the solver.
    ///
    /// kN and m, which is what Alpaca4d works in - see Units, and the kN/m2 the material
    /// library computes in. The section is deliberately elastic and symmetric, which
    /// makes the answer arithmetic rather than a stored curve: a curvature the analysis
    /// is told to reach has to come back on the output for the axis it was applied about,
    /// times EI.
    ///
    /// [NonParallelizable] because the components write beside the current directory and
    /// <see cref="WorkflowRun"/> moves it - and because a fresh directory per run is also
    /// what covers the first-run case, where the recorder folder does not exist yet.
    /// </summary>
    [TestFixture]
    [NonParallelizable]
    public class MomentCurvatureTests
    {
        // S355, in kN/m2.
        private const double Fy = 355000.0;
        private const double E = 210000000.0;

        /// <summary>2500 mm2, in m2.</summary>
        private const double FiberArea = 2.5e-3;

        // Two rows of four fibres: y = -0.15..0.15 m, z = -0.25 and +0.25 m. Symmetric
        // about both axes, so the axial step bends the section not at all, and stiff about
        // y and soft about z by a factor of five - a result on the wrong output is wrong
        // twice over.
        private const double HalfWidth = 0.15;
        private const double HalfDepth = 0.25;
        private const int FibersPerRow = 4;

        /// <summary>kN, compression.</summary>
        private const double Axial = -100.0;

        /// <summary>rad/m. Keeps the extreme fibre at 1e-3 strain, well inside yield.</summary>
        private const double MaxPhi = 0.004;

        private const int NumIncr = 4;

        /// <summary>Sum(A z^2) over the eight fibres, m4 - bending about the local y axis.</summary>
        private static double Iy
        {
            get { return 2 * FibersPerRow * FiberArea * HalfDepth * HalfDepth; }
        }

        /// <summary>Sum(A y^2) over the eight fibres, m4 - bending about the local z axis.</summary>
        private static double Iz
        {
            get
            {
                return 2 * FiberArea * Enumerable.Range(0, FibersPerRow)
                                                 .Select(FiberY)
                                                 .Sum(y => y * y);
            }
        }

        private static double FiberY(int index)
        {
            return -HalfWidth + index * (2 * HalfWidth / (FibersPerRow - 1));
        }

        [Test]
        public void Bending_about_y_reports_the_moment_and_the_curvature_on_the_y_outputs()
        {
            using (WorkflowRun.Begin())
            {
                var result = Analyse("y");

                Assert.That(result.Errors, Is.Empty, result.Describe());

                var ky = result.GetList<double>("κy");
                var kz = result.GetList<double>("κz");
                var My = result.GetList<double>("My");
                var Mz = result.GetList<double>("Mz");

                Assert.That(ky, Has.Count.EqualTo(NumIncr), "one row per increment");

                Assert.Multiple(() =>
                {
                    Assert.That(ky.Last(), Is.EqualTo(MaxPhi).Within(0.1).Percent,
                        "the curvature the analysis was told to reach, about y");
                    Assert.That(My.Last(), Is.EqualTo(E * Iy * MaxPhi).Within(1.0).Percent,
                        "E Iy phi, the section being elastic at this curvature");

                    Assert.That(kz.Last(), Is.EqualTo(0.0).Within(MaxPhi * 1e-3),
                        "nothing was applied about z");
                    Assert.That(Mz.Last(), Is.EqualTo(0.0).Within(E * Iy * MaxPhi * 1e-3),
                        "nothing was applied about z");
                });
            }
        }

        [Test]
        public void Bending_about_z_reports_the_moment_and_the_curvature_on_the_z_outputs()
        {
            using (WorkflowRun.Begin())
            {
                var result = Analyse("z");

                Assert.That(result.Errors, Is.Empty, result.Describe());

                var ky = result.GetList<double>("κy");
                var kz = result.GetList<double>("κz");
                var My = result.GetList<double>("My");
                var Mz = result.GetList<double>("Mz");

                Assert.Multiple(() =>
                {
                    Assert.That(kz.Last(), Is.EqualTo(MaxPhi).Within(0.1).Percent,
                        "the curvature the analysis was told to reach, about z");
                    Assert.That(Mz.Last(), Is.EqualTo(E * Iz * MaxPhi).Within(1.0).Percent,
                        "E Iz phi, five times softer than about y");

                    Assert.That(ky.Last(), Is.EqualTo(0.0).Within(MaxPhi * 1e-3),
                        "nothing was applied about y");
                    Assert.That(My.Last(), Is.EqualTo(0.0).Within(E * Iz * MaxPhi * 1e-3),
                        "nothing was applied about y");
                });
            }
        }

        [Test]
        public void The_axial_force_is_held_for_the_whole_ramp()
        {
            using (WorkflowRun.Begin())
            {
                var result = Analyse("y");

                Assert.That(result.Errors, Is.Empty, result.Describe());
                Assert.That(result.GetList<double>("N"), Is.All.EqualTo(Axial).Within(0.1).Percent);
            }
        }

        /// <summary>
        /// Every fibre gets a recorder, and the reader has to pair each file back up with
        /// the fibre it belongs to - which is what the branch paths carry.
        /// </summary>
        [Test]
        public void Every_fiber_comes_back_with_its_own_stress_and_strain_history()
        {
            using (WorkflowRun.Begin())
            {
                var result = Analyse("y");

                Assert.That(result.Errors, Is.Empty, result.Describe());

                var fiberResult = result.Get<Alpaca4d.Result.PointFiberResult>("fiberStressStrain");

                Assert.That(fiberResult.Stress.BranchCount, Is.EqualTo(2 * FibersPerRow),
                    "one branch per fibre");
                Assert.That(fiberResult.Stress.Branches.Select(b => b.Count),
                    Is.All.EqualTo(NumIncr), "one reading per increment");

                // The section is elastic, so a fibre's stress is E times its own strain -
                // which also says the two are not each other's.
                foreach (var path in fiberResult.Stress.Paths)
                {
                    var stress = fiberResult.Stress.Branch(path);
                    var strain = fiberResult.Strain.Branch(path);

                    for (var i = 0; i < stress.Count; i++)
                        Assert.That(stress[i], Is.EqualTo(E * strain[i]).Within(0.1).Percent,
                            "fibre " + path + ", increment " + i);
                }
            }
        }

        /// <summary>
        /// The reader component used to hand each of the two trees to the other's output.
        /// </summary>
        [Test]
        public void FiberStressStrain_keeps_stress_and_strain_on_their_own_outputs()
        {
            using (WorkflowRun.Begin())
            {
                var analysed = Analyse("y").Get<Alpaca4d.Result.PointFiberResult>("fiberStressStrain");

                var result = ComponentHarness.For<Alpaca4d.Gh.FiberStressStrain>()
                                             .Set("FiberStressStrain", analysed)
                                             .Solve();

                Assert.That(result.Errors, Is.Empty, result.Describe());

                var stress = result.GetList<double>("Stress");
                var strain = result.GetList<double>("Strain");

                Assert.That(stress, Is.EqualTo(Flatten(analysed.Stress)).AsCollection);
                Assert.That(strain, Is.EqualTo(Flatten(analysed.Strain)).AsCollection);

                // Belt and braces: at these strains the two differ by orders of magnitude,
                // so a swap could not pass even without the comparison above.
                Assert.That(stress.Max(a => Math.Abs(a)), Is.GreaterThan(strain.Max(a => Math.Abs(a))));
            }
        }

        /// <summary>
        /// The defaults a freshly placed component carries have to describe a model the
        /// solver accepts - in Alpaca4d's units, and including the MinMax wrappers, which
        /// used to be written with their own tag as the material they wrap.
        /// </summary>
        [Test]
        public void The_default_concrete_and_reinforcement_produce_a_deck_the_solver_runs()
        {
            using (WorkflowRun.Begin())
            {
                var result = Analyse(ConcreteSection(), "y", axial: -400.0, maxPhi: 0.002, numIncr: 4);

                Assert.That(result.Errors, Is.Empty, result.Describe());
                Assert.That(result.GetList<double>("My"), Is.Not.Empty);

                var log = result.Get<string>("log");
                Assert.That(log, Does.Contain("uniaxialMaterial MinMax"));
                Assert.That(log, Does.Not.Contain("invalid otherTag"),
                    "a MinMax wrapper has to name the material it wraps");
                Assert.That(log, Does.Not.Contain("Large trial compressive strain"),
                    "the concrete defaults have to be the sign Concrete01 expects");
            }
        }

        /// <summary>
        /// A section pushed past what it can carry stops converging part way. What it
        /// reached is a result, so it comes back - with a warning saying it is short.
        /// The solver exits 0 either way, which is why this needs saying at all.
        /// </summary>
        [Test]
        public void A_ramp_that_stops_converging_warns_and_returns_what_it_reached()
        {
            using (WorkflowRun.Begin())
            {
                // Concrete, and wrapped in MinMax: past its crushing strain the fibres
                // fail and the section stops converging. Steel01 hardens for ever and
                // would happily follow any curvature it was given.
                var result = Analyse(ConcreteSection(), "y", axial: Axial, maxPhi: 1.0, numIncr: 5);

                Assert.That(result.Errors, Is.Empty, result.Describe());
                Assert.That(result.Warnings.Any(w => w.Contains("MaxPhi")), Is.True,
                    "a curve that stops short has to say so:" + result.Describe());
            }
        }

        [Test]
        public void Direction_has_to_name_an_axis()
        {
            using (WorkflowRun.Begin())
            {
                var result = Analyse(Section(), "x", axial: Axial, maxPhi: MaxPhi, numIncr: NumIncr);

                Assert.That(result.Errors, Is.Not.Empty, "\"x\" is not an axis to bend about");
                Assert.That(result.Errors.Single(), Does.Contain("\"y\" or \"z\""));
            }
        }

        /// <summary>
        /// "Y" is the same axis as "y" - a value list is not the only thing that can reach
        /// this input, and the comparison used to take anything that was not exactly "y"
        /// to mean z.
        /// </summary>
        [Test]
        public void Direction_is_read_case_insensitively()
        {
            using (WorkflowRun.Begin())
            {
                var result = Analyse(Section(), "Y", axial: Axial, maxPhi: MaxPhi, numIncr: NumIncr);

                Assert.That(result.Errors, Is.Empty, result.Describe());
                Assert.That(result.GetList<double>("κy").Last(), Is.EqualTo(MaxPhi).Within(0.1).Percent);
            }
        }

        /// <summary>
        /// The deck is Tcl, and Tcl has one number format. On a machine set to a
        /// comma-decimal locale plain interpolation writes "0,5", which Tcl reads as two
        /// arguments - so the whole deck has to go through TclNumber.
        /// </summary>
        [Test]
        public void The_deck_is_written_with_dots_whatever_the_locale()
        {
            var culture = CultureInfo.CurrentCulture;
            try
            {
                System.Threading.Thread.CurrentThread.CurrentCulture = new CultureInfo("it-IT");

                var deck = Alpaca4d.Template.MomentCurvature.Define(
                    fiber: BuildSection(),
                    axialForce: -123.45,
                    dof: "y",
                    numIncr: 8,
                    maxPhi: 0.0125);

                Assert.That(deck, Does.Not.Contain(","),
                    "a comma in the deck is a decimal separator Tcl reads as an argument break");
                Assert.That(deck, Does.Contain("-123.45"));
                Assert.That(deck, Does.Contain("fiber -0.15 -0.25 0.0025"));
            }
            finally
            {
                System.Threading.Thread.CurrentThread.CurrentCulture = culture;
            }
        }

        /// <summary>
        /// The recorder folder and the deck are both relative to the current directory, so
        /// they have to be resolved against the same one. Preparing the folder before the
        /// component had settled on a directory put it somewhere the solver never looked,
        /// and the first run of a session read files that were never written - which a
        /// fresh working directory per test is exactly the shape of.
        /// </summary>
        [Test]
        public void The_first_run_in_a_fresh_directory_writes_beside_the_deck()
        {
            using (WorkflowRun.Begin())
            {
                var here = Directory.GetCurrentDirectory();

                Assert.That(Directory.Exists(Path.Combine(here, "FiberResults")), Is.False,
                    "a run that has not happened yet");

                var result = Analyse("y");

                Assert.That(result.Errors, Is.Empty, result.Describe());
                Assert.That(File.Exists(Path.Combine(here, "MomentCurvature.tcl")), Is.True);
                Assert.That(File.Exists(Path.Combine(here, "FiberResults", "MKsectionForce.out")), Is.True);
            }
        }

        /// <summary>
        /// A section with more fibres than the solver can hold files open for.
        ///
        /// Every fibre used to get a recorder of its own, and every recorder holds its
        /// file open; the C runtime OpenSees is built against stops at 512. A real section
        /// of 2052 fibres came back with 507 fibre histories and 1545 empty ones, and the
        /// solver said nothing about it - it exits 0 either way. 700 fibres is past the
        /// limit and small enough to stay quick.
        /// </summary>
        [Test]
        public void Every_fiber_of_a_large_section_comes_back_populated()
        {
            using (WorkflowRun.Begin())
            {
                const int Rows = 175;

                var steel = Steel();
                var rows = Enumerable.Range(0, Rows)
                                     .Select(r => Row(-HalfDepth + r * (2 * HalfDepth / (Rows - 1)), steel))
                                     .ToList();

                var fiberCount = Rows * FibersPerRow;
                Assert.That(fiberCount, Is.GreaterThan(512), "the point of this test");

                var result = Analyse(Section(rows), "y", axial: Axial, maxPhi: MaxPhi, numIncr: 2);

                Assert.That(result.Errors, Is.Empty, result.Describe());
                Assert.That(result.Warnings, Is.Empty, result.Describe());

                var fiberResult = result.Get<Alpaca4d.Result.PointFiberResult>("fiberStressStrain");

                Assert.That(fiberResult.Stress.BranchCount, Is.EqualTo(fiberCount));
                Assert.That(fiberResult.Stress.Branches.Count(b => b.Count == 0), Is.Zero,
                    "no fibre may come back with an empty history");
                Assert.That(fiberResult.Strain.Branches.Count(b => b.Count == 0), Is.Zero,
                    "no fibre may come back with an empty history");
            }
        }

        /// <summary>
        /// The fibres come back paired with their own history, and not with a neighbour's.
        ///
        /// A section of layers and patches together is what shows this: OpenSees holds the
        /// fibres in the order the section declared them, and FiberSection.Fibers used to
        /// list layers and patches the other way round from WriteTcl.
        /// </summary>
        [Test]
        public void A_fiber_is_paired_with_its_own_history()
        {
            using (WorkflowRun.Begin())
            {
                var steel = Steel();

                // A patch across the section, plus a layer of bars top and bottom - so the
                // two collections are both present and cannot be interchanged.
                var patch = ComponentHarness.For<Alpaca4d.Gh.Patch>()
                                            .Set("Mesh", Mesh.CreateFromPlane(
                                                Plane.WorldXY,
                                                new Interval(-HalfWidth, HalfWidth),
                                                new Interval(-HalfDepth / 2, HalfDepth / 2), 3, 3))
                                            .Set("Material", steel)
                                            .Solve()
                                            .All(0)
                                            .Single();

                var section = ComponentHarness.For<Alpaca4d.Gh.FiberSection>()
                                              .Set("PointFiber", Row(-HalfDepth, steel).Concat(Row(HalfDepth, steel)).ToArray())
                                              .Set("Patch", patch)
                                              .Solve()
                                              .All(0)
                                              .Single();

                var result = Analyse(section, "y", axial: Axial, maxPhi: MaxPhi, numIncr: NumIncr);

                Assert.That(result.Errors, Is.Empty, result.Describe());

                var fiberResult = result.Get<Alpaca4d.Result.PointFiberResult>("fiberStressStrain");

                // Bending about y, so a fibre's strain is set by its own z: same sign as z,
                // and the two extreme rows have to come out on opposite sides. Reading a
                // history against the wrong fibre breaks that.
                foreach (var path in fiberResult.Fibers.Paths)
                {
                    var fiber = fiberResult.Fibers.Branch(path).Single();
                    var strain = fiberResult.Strain.Branch(path).Last();
                    var bending = strain - fiberResult.Strain.Branch(path).First();

                    if (Math.Abs(fiber.Pos.Y) < HalfDepth * 0.5)
                        continue;

                    Assert.That(Math.Sign(bending), Is.EqualTo(Math.Sign(fiber.Pos.Y)),
                        "fibre at z=" + fiber.Pos.Y + " strained the wrong way (" + path + ")");
                }
            }
        }

        /// <summary>
        /// A freshly placed fibre component computes, without a material wired to it.
        /// </summary>
        [Test]
        public void The_fiber_components_fall_back_to_a_material()
        {
            var fiber = ComponentHarness.For<Alpaca4d.Gh.PointFiber>()
                                        .Set("Point", new Point3d(0, HalfDepth, 0))
                                        .Solve();

            Assert.That(fiber.Errors, Is.Empty, fiber.Describe());
            Assert.That(fiber.Get<Alpaca4d.Section.PointFiber>(0).Material,
                        Is.InstanceOf<Alpaca4d.Material.ReinforcingSteel>());

            var patch = ComponentHarness.For<Alpaca4d.Gh.Patch>()
                                        .Set("Mesh", Rhino.Geometry.Mesh.CreateFromPlane(
                                            Plane.WorldXY, new Interval(-0.15, 0.15), new Interval(-0.25, 0.25), 2, 4))
                                        .Solve();

            Assert.That(patch.Errors, Is.Empty, patch.Describe());
            Assert.That(patch.Get<Alpaca4d.Section.Patch>(0).Material,
                        Is.InstanceOf<Alpaca4d.Material.Concrete01>());
        }

        // ---------------------------------------------------------------- helpers

        private static SolveResult Analyse(string direction)
        {
            return Analyse(Section(), direction, Axial, MaxPhi, NumIncr);
        }

        private static SolveResult Analyse(object section, string direction, double axial, double maxPhi, int numIncr)
        {
            return ComponentHarness.For<Alpaca4d.Gh.MomentCurvature>()
                                   .Set("FiberSection", section)
                                   .Set("Axial", axial)
                                   .Set("Direction", direction)
                                   .Set("NumIncr", numIncr)
                                   .Set("MaxPhi", maxPhi)
                                   .Solve();
        }

        /// <summary>
        /// Concrete over the depth with reinforcement in the two outer rows, both
        /// materials exactly as a freshly placed component makes them and both wrapped in
        /// MinMax so the fibres can fail.
        /// </summary>
        private static object ConcreteSection()
        {
            var concrete = Material<Alpaca4d.Gh.Concrete01>();
            var reinforcement = Material<Alpaca4d.Gh.ReinforcingSteel>();

            return Section(new[]
            {
                Row(-HalfDepth, reinforcement),
                Row(-HalfDepth / 2, concrete),
                Row(HalfDepth / 2, concrete),
                Row(HalfDepth, reinforcement),
            });
        }

        private static object Material<TComponent>() where TComponent : Grasshopper.Kernel.GH_Component, new()
        {
            return ComponentHarness.For<TComponent>()
                                   .Set("MinMax", true)
                                   .Solve()
                                   .All(0)
                                   .Single();
        }

        /// <summary>The two-row steel section, assembled through the components.</summary>
        private static object Section()
        {
            var steel = Steel();
            return Section(new[] { Row(-HalfDepth, steel), Row(HalfDepth, steel) });
        }

        private static object Steel()
        {
            return ComponentHarness.For<Alpaca4d.Gh.Steel01>()
                                   .Set("fy", Fy)
                                   .Set("E0", E)
                                   .Set("b", 0.01)
                                   .Solve()
                                   .All(0)
                                   .Single();
        }

        /// <summary>One row of fibres at a given local z, as Fiber Point components.</summary>
        private static List<object> Row(double z, object material)
        {
            return Enumerable.Range(0, FibersPerRow)
                             .Select(i => ComponentHarness.For<Alpaca4d.Gh.PointFiber>()
                                                          .Set("Point", new Point3d(FiberY(i), z, 0))
                                                          .Set("AreaFiber", FiberArea)
                                                          .Set("Material", material)
                                                          .Solve()
                                                          .All(0)
                                                          .Single())
                             .ToList();
        }

        private static object Section(IEnumerable<List<object>> rows)
        {
            return ComponentHarness.For<Alpaca4d.Gh.FiberSection>()
                                   .Set("PointFiber", rows.SelectMany(r => r).ToArray())
                                   .Solve()
                                   .All(0)
                                   .Single();
        }

        /// <summary>The same section as <see cref="Section()"/>, without the components.</summary>
        private static Alpaca4d.Section.FiberSection BuildSection()
        {
            var steel = Alpaca4d.Material.Steel01.S355;

            var fibers = new[] { -HalfDepth, HalfDepth }
                .SelectMany(z => Enumerable.Range(0, FibersPerRow)
                                           .Select(i => new Alpaca4d.Section.PointFiber(
                                               new Point3d(FiberY(i), z, 0), FiberArea, steel)))
                .ToList();

            return new Alpaca4d.Section.FiberSection(
                fibers,
                new List<Alpaca4d.Section.Layer>(),
                new List<Alpaca4d.Section.Patch>(),
                1e8);
        }

        private static List<double> Flatten(Grasshopper.DataTree<double> tree)
        {
            return tree.Paths.SelectMany(path => tree.Branch(path)).ToList();
        }
    }
}
