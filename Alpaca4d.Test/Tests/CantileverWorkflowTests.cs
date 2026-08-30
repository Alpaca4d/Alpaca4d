using System;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using Rhino.Geometry;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// The beam pipeline, component by component, exactly as it would run on a canvas:
    /// material -> section -> beam -> support + load -> pattern -> assemble -> settings ->
    /// run analysis (a real OpenSees process) -> read displacements back out of the
    /// recorder file.
    ///
    /// The model is a square-section cantilever with a tip load, so the answer is known
    /// in closed form and the assertion is on structural engineering rather than on a
    /// stored blob: delta = P L^3 / (3 E I).
    /// </summary>
    [TestFixture]
    [NonParallelizable]
    public class CantileverWorkflowTests
    {
        private const double Length = 10.0;         // m
        private const double Side = 0.4;            // m, square so section orientation cannot matter
        private const double YoungsModulus = 2.1e8; // kN/m2
        private const double TipLoad = 10.0;        // kN, downwards

        private static readonly Point3d Root = new Point3d(0, 0, 0);
        private static readonly Point3d Tip = new Point3d(Length, 0, 0);

        private WorkflowRun _run;

        [OneTimeSetUp]
        public void RunTheAnalysisOnce()
        {
            _run = WorkflowRun.Begin();

            var material = _run.Solve("Material", ComponentHarness.For<Alpaca4d.Gh.Uniaxial>()
                .SwitchTo("UniaxialElastic (Alpaca4d)")
                .Set("MatName", "S355")
                .Set("E", YoungsModulus));

            var section = _run.Solve("Section", ComponentHarness.For<Alpaca4d.Gh.RectangleCS>()
                .Set("SectionName", "SQ400")
                .Set("Width", Side)
                .Set("Height", Side)
                .Set("Material", material));

            var beam = _run.Solve("Beam", ComponentHarness.For<Alpaca4d.Gh.BeamBase>()
                .SwitchTo("ForceBeamColumn (Alpaca4d)")
                .Set("Line", new LineCurve(Root, Tip))
                .Set("Section", section));

            var support = _run.Solve("Support", ComponentHarness.For<Alpaca4d.Gh.Support>()
                .Set("Position", Root));

            var load = _run.Solve("Load", ComponentHarness.For<Alpaca4d.Gh.PointLoad>()
                .Set("Point", Tip)
                .Set("Force", new Vector3d(0, 0, -TipLoad)));

            var pattern = _run.Solve("Pattern", ComponentHarness.For<Alpaca4d.Gh.PatternBase>()
                .SwitchTo("PlainPattern (Alpaca4d)")
                .Set("Loads", load));

            var model = _run.Solve("Assemble", ComponentHarness.For<Alpaca4d.Gh.AssembleModel>()
                .Set("Elements", beam)
                .Set("Supports", support)
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

        [Test]
        public void Every_component_in_the_chain_solves_without_errors()
        {
            Assert.That(_run.Complaints(), Is.Empty,
                "Components that reported an error:\n" + string.Join("\n", _run.Complaints()) +
                "\n\nOpenSees log:\n" + _run.Log);
        }

        [Test]
        public void The_assembled_model_has_the_expected_topology()
        {
            var model = _run.ResultOf("Assemble").Get<Alpaca4d.Model>(0);

            Assert.That(model.Elements, Has.Count.EqualTo(1));
            Assert.That(model.Nodes, Has.Count.EqualTo(2));
            Assert.That(model.Supports, Has.Count.EqualTo(1));
        }

        [Test]
        public void The_model_reports_its_own_mass()
        {
            var mass = _run.ResultOf("Assemble").Get<double>(1);
            var expected = Side * Side * Length * 7850.0; // the default steel density

            Assert.That(mass, Is.EqualTo(expected).Within(0.1).Percent);
        }

        [Test]
        public void OpenSees_runs_and_reports_no_failure()
        {
            Assert.That(_run.Log, Is.Not.Null.And.Not.Empty);
            Assert.That(_run.AnalysedModel, Is.Not.Null,
                "RunAnalysis returned no model, which means the solver failed:\n" + _run.Log);
            Assert.That(_run.AnalysedModel.IsAnalysed, Is.True);
        }

        [Test]
        public void The_tip_deflection_matches_the_closed_form_cantilever()
        {
            var inertia = Math.Pow(Side, 4) / 12.0;
            var expected = TipLoad * Math.Pow(Length, 3) / (3.0 * YoungsModulus * inertia);

            var tip = _run.DisplacementAt(Tip);
            TestContext.WriteLine("tip displacement    = " + tip);
            TestContext.WriteLine("expected deflection = " + expected.ToString("F6") + " m");

            Assert.Multiple(() =>
            {
                Assert.That(-tip.Z, Is.EqualTo(expected).Within(1.0).Percent,
                    "P L^3 / (3 E I) for a slender cantilever; shear adds ~0.2%.");
                Assert.That(tip.X, Is.EqualTo(0).Within(1e-9), "no axial load was applied");
                Assert.That(tip.Y, Is.EqualTo(0).Within(1e-9), "the load is in the X-Z plane");
            });
        }

        /// <summary>
        /// The reaction reader pulls REACTION_FORCE / REACTION_MOMENT back out of the
        /// recorder file. Statics fixes both: the base carries the whole tip load, and
        /// P L of moment with it.
        /// </summary>
        [Test]
        public void The_reaction_reader_returns_the_applied_load()
        {
            var reactions = ComponentHarness.For<Alpaca4d.Gh.ReactionForce>()
                                            .Set("AlpacaModel", _run.AnalysedModel)
                                            .Solve();

            Assert.That(reactions.Errors, Is.Empty, reactions.Describe());

            var support = reactions.GetList<Plane>(0).Single();
            var force = reactions.GetList<Vector3d>(1).Single();
            var moment = reactions.GetList<Vector3d>(2).Single();
            TestContext.WriteLine("reaction at " + support.Origin + ": F=" + force + " M=" + moment);

            Assert.Multiple(() =>
            {
                Assert.That(support.Origin.DistanceTo(Root), Is.LessThan(1e-9));
                Assert.That(force.Length, Is.EqualTo(TipLoad).Within(0.1).Percent, "sum of vertical forces");
                Assert.That(moment.Length, Is.EqualTo(TipLoad * Length).Within(0.1).Percent, "moment about the base");
            });
        }

        /// <summary>
        /// The beam force reader returns one branch of section forces per element. Which
        /// of Vy/Vz and My/Mz carries the load depends on the element's local axes, so
        /// the assertions are on the resultants - those are fixed by statics whatever the
        /// orientation.
        /// </summary>
        [Test]
        public void The_beam_force_reader_matches_statics()
        {
            var forces = ComponentHarness.For<Alpaca4d.Gh.BeamForce>()
                                         .Set("AlpacaModel", _run.AnalysedModel)
                                         .Solve();

            Assert.That(forces.Errors, Is.Empty, forces.Describe());
            Assert.That(forces.Branches("N"), Has.Count.EqualTo(1), "one branch per beam element");

            var axial = forces.GetList<double>("N");
            var shear = Resultant(forces.GetList<double>("Vy"), forces.GetList<double>("Vz"));
            var bending = Resultant(forces.GetList<double>("My"), forces.GetList<double>("Mz"));
            TestContext.WriteLine("sections=" + axial.Count + " max shear=" + shear.Max() + " max moment=" + bending.Max());

            Assert.Multiple(() =>
            {
                Assert.That(axial.Max(Math.Abs), Is.LessThan(1e-6), "nothing was applied along the beam");
                Assert.That(shear.Max(), Is.EqualTo(TipLoad).Within(0.1).Percent, "shear is constant at P");
                Assert.That(bending.Max(), Is.EqualTo(TipLoad * Length).Within(0.1).Percent, "peak moment is P L at the base");
                Assert.That(bending.Min(), Is.LessThan(0.01 * TipLoad * Length), "and zero at the free end");
            });
        }

        private static IReadOnlyList<double> Resultant(IReadOnlyList<double> first, IReadOnlyList<double> second)
        {
            return first.Zip(second, (a, b) => Math.Sqrt(a * a + b * b)).ToList();
        }

        [Test]
        public void The_supported_end_does_not_move()
        {
            Assert.That(_run.DisplacementAt(Root).Length, Is.EqualTo(0).Within(1e-12));
        }
    }
}
