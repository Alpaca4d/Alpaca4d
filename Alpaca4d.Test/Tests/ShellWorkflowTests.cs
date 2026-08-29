using System;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using Rhino.Geometry;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// The shell pipeline: nD material -> plate fibre section -> a meshed ASD shell ->
    /// supports along one edge -> tip loads -> assemble -> run analysis -> displacements.
    ///
    /// The model is a narrow cantilever strip, one metre wide and ten long, so it bends
    /// like a beam and the tip deflection is again a closed form. Poisson's ratio is zero
    /// so that beam theory applies exactly; what is left is discretisation error.
    /// </summary>
    [TestFixture]
    [NonParallelizable]
    public class ShellWorkflowTests
    {
        private const double Length = 10.0;         // m
        private const double Width = 1.0;           // m
        private const double Thickness = 0.3;       // m
        private const double YoungsModulus = 2.1e8; // kN/m2
        private const double Density = 7850.0;      // kg/m3, the material default
        private const double TotalLoad = 10.0;      // kN, downwards, split over the two tip nodes
        private const int Divisions = 10;

        private WorkflowRun _run;

        [OneTimeSetUp]
        public void RunTheAnalysisOnce()
        {
            _run = WorkflowRun.Begin();

            var material = _run.Solve("Material", ComponentHarness.For<SimplexGh.nD>()
                .SwitchTo("ElasticIsotropic (Alpaca4d)")
                .Set("E", YoungsModulus)
                .Set(3, 0.0)               // Poisson's ratio, registered under a Greek nu
                .Set("Rho", Density));

            var section = _run.Solve("Section", ComponentHarness.For<Alpaca4d.Gh.PlateFiberSection>()
                .Set("Thickness", Thickness)
                .Set("Material", material));

            var elements = _run.SolveMany("Shell", ComponentHarness.For<Alpaca4d.Gh.ASDShell>()
                .Set("Mesh", Strip())
                .Set("Section", section));

            var supports = EdgeAt(0).Select(p => _run.Solve("Support",
                ComponentHarness.For<Alpaca4d.Gh.Support>().Set("Position", p))).ToArray();

            var loads = EdgeAt(Length).Select(p => _run.Solve("Load",
                ComponentHarness.For<Alpaca4d.Gh.PointLoad>()
                    .Set("Point", p)
                    .Set("Force", new Vector3d(0, 0, -TotalLoad / 2)))).ToArray();

            var pattern = _run.Solve("Pattern", ComponentHarness.For<Alpaca4d.Gh.PatternBase>()
                .SwitchTo("PlainPattern (Alpaca4d)")
                .Set("Loads", loads));

            var model = _run.Solve("Assemble", ComponentHarness.For<Alpaca4d.Gh.AssembleModel>()
                .Set("Elements", elements.ToArray())
                .Set("Supports", supports)
                .Set("LoadPatterns", pattern));

            var settings = _run.Solve("Settings", ComponentHarness.For<Alpaca4d.Gh.AnalysisSettings>());

            _run.Analyse(model, settings);
        }

        [OneTimeTearDown]
        public void CleanUp()
        {
            if (_run != null)
                _run.Dispose();
        }

        /// <summary>A quad-meshed strip in the world XY plane, one quad across its width.</summary>
        private static Mesh Strip()
        {
            var mesh = new Mesh();

            for (var i = 0; i <= Divisions; i++)
            {
                mesh.Vertices.Add(i * Length / Divisions, 0, 0);
                mesh.Vertices.Add(i * Length / Divisions, Width, 0);
            }

            for (var i = 0; i < Divisions; i++)
                mesh.Faces.AddFace(2 * i, 2 * i + 2, 2 * i + 3, 2 * i + 1);

            return mesh;
        }

        private static Point3d[] EdgeAt(double x)
        {
            return new[] { new Point3d(x, 0, 0), new Point3d(x, Width, 0) };
        }

        [Test]
        public void Every_component_in_the_chain_solves_without_errors()
        {
            Assert.That(_run.Complaints(), Is.Empty,
                "Components that reported an error:\n" + string.Join("\n", _run.Complaints()) +
                "\n\nOpenSees log:\n" + _run.Log);
        }

        [Test]
        public void The_mesh_becomes_one_shell_element_per_face()
        {
            Assert.That(_run.ResultOf("Shell").Count(0), Is.EqualTo(Divisions));
            Assert.That(_run.ResultOf("Assemble").Get<Alpaca4d.Model>(0).Nodes,
                Has.Count.EqualTo(2 * (Divisions + 1)));
        }

        [Test]
        public void The_model_reports_its_own_mass()
        {
            var mass = _run.ResultOf("Assemble").Get<double>(1);

            Assert.That(mass, Is.EqualTo(Length * Width * Thickness * Density).Within(0.1).Percent);
        }

        [Test]
        public void The_tip_deflection_matches_the_closed_form_strip()
        {
            var inertia = Width * Math.Pow(Thickness, 3) / 12.0;
            var expected = TotalLoad * Math.Pow(Length, 3) / (3.0 * YoungsModulus * inertia);

            foreach (var corner in EdgeAt(Length))
            {
                var tip = _run.DisplacementAt(corner);
                TestContext.WriteLine(corner + " -> " + tip);

                Assert.That(-tip.Z, Is.EqualTo(expected).Within(2.0).Percent,
                    "P L^3 / (3 E I) for a narrow strip; the rest is discretisation.");
            }
        }

        [Test]
        public void The_reaction_reader_balances_the_applied_load()
        {
            var reactions = ComponentHarness.For<Alpaca4d.Gh.ReactionForce>()
                                            .Set("AlpacaModel", _run.AnalysedModel)
                                            .Solve();

            Assert.That(reactions.Errors, Is.Empty, reactions.Describe());

            var forces = reactions.GetList<Vector3d>(1);
            var total = forces.Aggregate(Vector3d.Zero, (sum, f) => sum + f);
            TestContext.WriteLine("reactions: " + string.Join(" + ", forces) + " = " + total);

            Assert.That(forces, Has.Count.EqualTo(2), "one per supported corner");
            Assert.That(total.Z, Is.EqualTo(TotalLoad).Within(0.1).Percent, "the edge carries the whole load");
        }

        /// <summary>
        /// The shell force reader returns membrane forces, bending moments and shears per
        /// unit width, one branch per element, sampled at the element centre.
        ///
        /// The bending lands in myy and the shear in vyz because the elements take their
        /// local axes from OpenSees' default for the node order of each quad - Alpaca4d
        /// only writes "-local" when the component's LocalX input is wired.
        /// </summary>
        [Test]
        public void The_shell_force_reader_matches_the_cantilever_diagram()
        {
            var forces = ComponentHarness.For<Alpaca4d.Gh.ShellForces>()
                                         .Set("AlpacaModel", _run.AnalysedModel)
                                         .Solve();

            Assert.That(forces.Errors, Is.Empty, forces.Describe());

            var bending = PerElement(forces, "myy");
            var shear = PerElement(forces, "vyz");
            TestContext.WriteLine("|myy| support to tip: " + string.Join(", ", bending.Select(v => v.ToString("F1"))));

            Assert.That(bending, Has.Count.EqualTo(Divisions), "one branch per shell element");

            Assert.Multiple(() =>
            {
                var elementLength = Length / Divisions;

                for (var i = 0; i < Divisions; i++)
                {
                    // Sampled at the element centre, so the lever arm is measured from there.
                    var leverArm = Length - (i + 0.5) * elementLength;

                    Assert.That(bending[i], Is.EqualTo(TotalLoad * leverArm / Width).Within(0.1).Percent,
                        "bending per unit width at element " + i);
                    Assert.That(shear[i], Is.EqualTo(TotalLoad / Width).Within(0.1).Percent,
                        "shear per unit width at element " + i);
                }

                foreach (var membrane in new[] { "pxx", "pyy", "pxy" })
                    Assert.That(PerElement(forces, membrane).Max(), Is.LessThan(1e-6),
                        membrane + ": pure bending puts nothing in the membrane");
            });
        }

        /// <summary>The largest magnitude each element reports for one of the force outputs.</summary>
        private static IReadOnlyList<double> PerElement(SolveResult forces, string output)
        {
            return forces.Branches(output)
                         .Select(branch => branch.Cast<double>().Max(Math.Abs))
                         .ToList();
        }

        [Test]
        public void The_supported_edge_does_not_move()
        {
            foreach (var corner in EdgeAt(0))
                Assert.That(_run.DisplacementAt(corner).Length, Is.EqualTo(0).Within(1e-12));
        }
    }
}
