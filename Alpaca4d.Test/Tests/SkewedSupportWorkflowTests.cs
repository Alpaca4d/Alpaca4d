using System;
using System.Linq;
using NUnit.Framework;
using Rhino.Geometry;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// A support placed on a Plane restrains that plane's axes instead of the global
    /// ones. OpenSees has no nodal coordinate system to express that with, so Alpaca4d
    /// writes a zeroLength element between the support node and a coincident node that is
    /// fixed outright, handing it the plane through <c>-orient</c>.
    ///
    /// This fixture turns the base of the cantilever without changing anything else. A
    /// support that is fully restrained is fully restrained whatever it is turned to, so
    /// the whole model has to come out exactly as it does on a world-aligned base - which
    /// is the strongest statement available that the machinery has not changed the
    /// answer, only the frame the restraints are read in.
    /// </summary>
    [TestFixture]
    [NonParallelizable]
    public class InclinedFixedSupportTests
    {
        private const double Length = 10.0;         // m
        private const double Side = 0.4;            // m
        private const double YoungsModulus = 2.1e8; // kN/m2
        private const double TipLoad = 10.0;        // kN, downwards
        private const double Incline = 30.0;        // degrees, about the global Y axis

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
                .Set("Position", SkewedSupport.Inclined(Root, Incline)));

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

        /// <summary>
        /// The deck should carry the spring rather than a plain fix, and the auxiliary
        /// node has to be numbered above every node the user drew: node results are read
        /// out of the recorder by row, rows are ordered by node tag, and an auxiliary node
        /// slipped in among the real ones would shift every row after it.
        /// </summary>
        [Test]
        public void The_deck_carries_a_zero_length_spring_on_a_node_of_its_own()
        {
            var model = _run.ResultOf("Assemble").Get<Alpaca4d.Model>(0);
            var deck = string.Join("", model.Tcl);
            var support = model.Supports.Single();

            TestContext.WriteLine(deck);

            Assert.Multiple(() =>
            {
                Assert.That(support.IsAxisAligned, Is.False, "the support was given a rotated plane");
                Assert.That(support.AuxiliaryNodeId, Is.Not.Null, "a skewed support needs a node to fix");
                Assert.That(support.AuxiliaryNodeId.Value, Is.GreaterThan(model.Nodes.Max(node => node.Id.Value)),
                    "auxiliary nodes must sort after every real node");
                Assert.That(deck, Does.Contain("element zeroLength"));
                Assert.That(deck, Does.Contain("-orient"));
                Assert.That(deck, Does.Contain("-dir 1 2 3 4 5 6"), "everything is restrained");
                Assert.That(deck, Does.Contain("fix " + support.AuxiliaryNodeId + " 1 1 1 1 1 1"));
            });
        }

        /// <summary>
        /// The penalty stiffness is not a hard-coded number - it is a multiple of the
        /// stiffest thing in the model, which is what keeps it independent of the units
        /// the model is built in. For this beam the largest diagonal term is the axial
        /// EA/L.
        /// </summary>
        [Test]
        public void The_spring_is_scaled_to_the_model_it_restrains()
        {
            var model = _run.ResultOf("Assemble").Get<Alpaca4d.Model>(0);
            var support = model.Supports.Single();

            var axial = YoungsModulus * Side * Side / Length;
            TestContext.WriteLine("EA/L = " + axial + ", spring = " + support.TranslationSpring.E);

            Assert.That(support.TranslationSpring.E, Is.EqualTo(1.0e6 * axial).Within(0.1).Percent);
        }

        [Test]
        public void OpenSees_runs_and_reports_no_failure()
        {
            Assert.That(_run.AnalysedModel, Is.Not.Null,
                "RunAnalysis returned no model, which means the solver failed:\n" + _run.Log);
            Assert.That(_run.AnalysedModel.IsAnalysed, Is.True);
        }

        /// <summary>
        /// Turning a fully fixed support cannot change the structure, so the closed form
        /// still has to hold to the same tolerance the world-aligned fixture uses.
        /// </summary>
        [Test]
        public void The_tip_deflection_still_matches_the_closed_form_cantilever()
        {
            var inertia = Math.Pow(Side, 4) / 12.0;
            var expected = TipLoad * Math.Pow(Length, 3) / (3.0 * YoungsModulus * inertia);

            var tip = _run.DisplacementAt(Tip);
            TestContext.WriteLine("tip displacement    = " + tip);
            TestContext.WriteLine("expected deflection = " + expected.ToString("F6") + " m");

            Assert.That(-tip.Z, Is.EqualTo(expected).Within(1.0).Percent,
                "an inclined fixed base is still a fixed base");
        }

        /// <summary>
        /// The spring is a penalty, so the base gives way a little rather than not at all.
        /// A millionth of the tip deflection is the size of that give, and it is the whole
        /// reason the factor is chosen the way it is.
        /// </summary>
        [Test]
        public void The_supported_end_barely_moves()
        {
            var tip = _run.DisplacementAt(Tip).Length;
            var root = _run.DisplacementAt(Root).Length;
            TestContext.WriteLine("root movement = " + root + " m, against a tip of " + tip + " m");

            Assert.That(root, Is.LessThan(1e-5 * tip),
                "a penalty support should give way by about one part in a million");
        }

        /// <summary>
        /// The reaction lives on the auxiliary node now, and the reader has to find it
        /// there. Statics fixes the answer whatever frame it is reported in, so assert on
        /// the magnitudes.
        /// </summary>
        [Test]
        public void The_reaction_reader_still_returns_the_applied_load()
        {
            var reactions = ComponentHarness.For<Alpaca4d.Gh.ReactionForce>()
                                            .Set("AlpacaModel", _run.AnalysedModel)
                                            .Solve();

            Assert.That(reactions.Errors, Is.Empty, reactions.Describe());

            // One output carries both halves: where the support is, and the axes its
            // reaction is given in.
            var support = reactions.GetList<Plane>(0).Single();
            var force = reactions.GetList<Vector3d>(1).Single();
            var moment = reactions.GetList<Vector3d>(2).Single();
            TestContext.WriteLine("reaction at " + support.Origin + ": F=" + force + " M=" + moment);

            Assert.Multiple(() =>
            {
                Assert.That(support.Origin.DistanceTo(Root), Is.LessThan(1e-9),
                    "reported against the support, not the auxiliary node");
                Assert.That(force.Length, Is.EqualTo(TipLoad).Within(0.1).Percent, "sum of vertical forces");
                Assert.That(moment.Length, Is.EqualTo(TipLoad * Length).Within(0.1).Percent, "moment about the base");
                Assert.That(support.XAxis.IsParallelTo(SkewedSupport.Inclined(Root, Incline).XAxis), Is.EqualTo(1),
                    "the plane the components are given in");
            });
        }

        /// <summary>
        /// The point of resolving onto the support's own axes: the load is vertical and
        /// the support is turned 30 degrees, so the reaction has a component on every
        /// global axis but lands where statics puts it in the local frame.
        /// </summary>
        [Test]
        public void The_reaction_is_reported_in_the_supports_own_axes()
        {
            var reactions = ComponentHarness.For<Alpaca4d.Gh.ReactionForce>()
                                            .Set("AlpacaModel", _run.AnalysedModel)
                                            .Solve();

            var local = reactions.GetList<Vector3d>(1).Single();
            var frame = SkewedSupport.Inclined(Root, Incline);
            var global = new Vector3d(0, 0, TipLoad);

            TestContext.WriteLine("local reaction = " + local);

            Assert.Multiple(() =>
            {
                Assert.That(local.X, Is.EqualTo(global * frame.XAxis).Within(0.01), "along the plane's X");
                Assert.That(local.Y, Is.EqualTo(global * frame.YAxis).Within(0.01), "along the plane's Y");
                Assert.That(local.Z, Is.EqualTo(global * frame.ZAxis).Within(0.01), "along the plane's Z");
                Assert.That(Math.Abs(local.X), Is.GreaterThan(1.0),
                    "a turned support really does carry load along its own X");
            });
        }
    }

    /// <summary>
    /// The case the feature exists for: a roller on a slope. The tip of a cantilever is
    /// held against a plane turned 30 degrees but left free to slide along it, which no
    /// combination of global <c>fix</c> flags can express.
    /// </summary>
    [TestFixture]
    [NonParallelizable]
    public class InclinedRollerTests
    {
        private const double Length = 10.0;
        private const double Side = 0.4;
        private const double YoungsModulus = 2.1e8;
        private const double TipLoad = 10.0;
        private const double Incline = 30.0;

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

            // Built in at the root, the ordinary way.
            var fixedEnd = _run.Solve("FixedEnd", ComponentHarness.For<Alpaca4d.Gh.Support>()
                .Set("Position", Root));

            // Held against the inclined plane but free to slide along its X axis, and
            // free to rotate.
            var roller = _run.Solve("Roller", ComponentHarness.For<Alpaca4d.Gh.Support>()
                .Set("Position", SkewedSupport.Inclined(Tip, Incline))
                .Set("Tx", false)
                .Set("Rx", false)
                .Set("Ry", false)
                .Set("Rz", false));

            var load = _run.Solve("Load", ComponentHarness.For<Alpaca4d.Gh.PointLoad>()
                .Set("Point", Tip)
                .Set("Force", new Vector3d(0, 0, -TipLoad)));

            var pattern = _run.Solve("Pattern", ComponentHarness.For<Alpaca4d.Gh.PatternBase>()
                .SwitchTo("PlainPattern (Alpaca4d)")
                .Set("Loads", load));

            var model = _run.Solve("Assemble", ComponentHarness.For<Alpaca4d.Gh.AssembleModel>()
                .Set("Elements", beam)
                .Set("Supports", fixedEnd, roller)
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

        /// <summary>
        /// Only the two restrained directions reach the element. A direction left out of
        /// <c>-dir</c> carries no stiffness at all, which is what makes the release exact
        /// rather than approximate.
        /// </summary>
        [Test]
        public void Only_the_restrained_directions_are_written()
        {
            var model = _run.ResultOf("Assemble").Get<Alpaca4d.Model>(0);
            var deck = string.Join("", model.Tcl);
            var roller = model.Supports.Single(support => support.NeedsSpring);

            TestContext.WriteLine(deck);

            Assert.Multiple(() =>
            {
                Assert.That(roller.RestrainedDirections, Is.EqualTo(new[] { 2, 3 }),
                    "the plane's Y and Z translations, nothing else");
                Assert.That(deck, Does.Contain("-dir 2 3"));
                Assert.That(deck, Does.Not.Contain("-dir 1 2 3"));

                // The built-in end is axis aligned, so it stays a plain fix - no spring,
                // no penalty, no extra node.
                var builtIn = model.Supports.Single(support => !support.NeedsSpring);
                Assert.That(builtIn.AuxiliaryNodeId, Is.Null);
                Assert.That(deck, Does.Contain("fix " + builtIn.Id + " 1 1 1 1 1 1"));
            });
        }

        [Test]
        public void OpenSees_runs_and_reports_no_failure()
        {
            Assert.That(_run.AnalysedModel, Is.Not.Null,
                "RunAnalysis returned no model, which means the solver failed:\n" + _run.Log);
        }

        /// <summary>
        /// The assertion the whole feature comes down to: a roller carries nothing along
        /// the direction it is free to slide in. In global components the reaction is
        /// spread across all three axes and says nothing; resolved onto the support's own
        /// axes the released one reads zero.
        /// </summary>
        [Test]
        public void The_released_direction_carries_no_reaction()
        {
            var reactions = ComponentHarness.For<Alpaca4d.Gh.ReactionForce>()
                                            .Set("AlpacaModel", _run.AnalysedModel)
                                            .Solve();

            Assert.That(reactions.Errors, Is.Empty, reactions.Describe());

            var supports = reactions.GetList<Plane>(0);
            var forces = reactions.GetList<Vector3d>(1);
            var moments = reactions.GetList<Vector3d>(2);

            var atTip = Enumerable.Range(0, supports.Count)
                                  .Single(i => supports[i].Origin.DistanceTo(Tip) < 1e-9);

            var force = forces[atTip];
            var moment = moments[atTip];
            TestContext.WriteLine("roller reaction (local) = " + force + "  moment = " + moment);

            Assert.Multiple(() =>
            {
                Assert.That(force.Length, Is.GreaterThan(1.0), "the roller does carry load");
                Assert.That(Math.Abs(force.X), Is.LessThan(1e-6 * force.Length),
                    "nothing along the direction the roller is free to slide in");
                Assert.That(moment.Length, Is.LessThan(1e-6 * TipLoad * Length),
                    "every rotation was released");
            });
        }

        /// <summary>
        /// Said again in global components, so the claim does not rest on the same
        /// rotation the reader applies: the reaction vector is perpendicular to the axis
        /// the support slides along.
        /// </summary>
        [Test]
        public void The_reaction_is_perpendicular_to_the_sliding_axis()
        {
            var model = _run.AnalysedModel;
            var roller = model.Supports.Single(support => support.NeedsSpring);

            var global = Alpaca4d.Result.Read.NodalOutput(
                model, 0, Alpaca4d.Result.ResultType.REACTION_FORCE,
                new System.Collections.Generic.List<int?> { roller.AuxiliaryNodeId }).Single();

            TestContext.WriteLine("roller reaction (global) = " + global);

            Assert.That(global * roller.Plane.XAxis, Is.EqualTo(0).Within(1e-6 * global.Length),
                "the sliding axis takes no load");
        }
    }

    internal static class SkewedSupport
    {
        /// <summary>A world-aligned frame at <paramref name="origin"/>, tipped about the global Y axis.</summary>
        public static Plane Inclined(Point3d origin, double degrees)
        {
            var frame = new Plane(origin, Vector3d.XAxis, Vector3d.YAxis);
            frame.Rotate(Rhino.RhinoMath.ToRadians(degrees), Vector3d.YAxis, origin);
            return frame;
        }
    }
}
