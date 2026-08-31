using System;
using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using Rhino.Geometry;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// Reading section forces back out of a model that mixes plain beams with BeamWithHinges.
    ///
    /// MPCORecorder does not group element results by integration type. It groups them by the
    /// normalised Gauss point locations it finds, handing out
    /// <c>74-ForceBeamColumn3d[1000:&lt;n&gt;:0]</c> in order of discovery
    /// (MPCORecorder.cpp, ElementCollection::mapElements). HingeRadau locations follow lpI/L and
    /// lpJ/L, so this cantilever - one NewtonCotes beam plus two hinged beams with different
    /// hinge lengths - lands in three separate groups, one more than a reader that knows only
    /// two hard-coded keys can see.
    ///
    /// The cantilever is straight and its three elements share one section, so statics gives the
    /// bending moment at every station: M(x) = P * (L - x). Because the stations of a hinged beam
    /// are NOT evenly spread, that also pins down where each recorded value belongs.
    /// </summary>
    [TestFixture]
    [NonParallelizable]
    public class HingedBeamForceTests
    {
        private const double Span = 10.0;           // m per element
        private const double Total = 3 * Span;      // m of cantilever
        private const double Side = 0.4;            // m, square section
        private const double YoungsModulus = 2.1e8; // kN/m2
        private const double TipLoad = 10.0;        // kN, downwards

        /// <summary>lp/L = 0.08, so it cannot share a Gauss rule with the 0.05 default.</summary>
        private const double LongHingeRatio = 0.08;

        private static readonly Point3d Root = new Point3d(0, 0, 0);
        private static readonly Point3d Tip = new Point3d(Total, 0, 0);

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

            // NewtonCotes, five evenly spaced sections.
            var plainBeam = _run.Solve("PlainBeam", ComponentHarness.For<Alpaca4d.Gh.BeamBase>()
                .SwitchTo("ForceBeamColumn (Alpaca4d)")
                .Set("Line", new LineCurve(new Point3d(0, 0, 0), new Point3d(Span, 0, 0)))
                .Set("Section", section));

            // HingeRadau with the default lp/L = 0.05, six sections. LpI and LpJ are left empty,
            // which is what asks for that default.
            var defaultHinges = _run.Solve("DefaultHinges", ComponentHarness.For<Alpaca4d.Gh.BeamBase>()
                .SwitchTo("WithHinges (Alpaca4d)")
                .Set("Line", new LineCurve(new Point3d(Span, 0, 0), new Point3d(2 * Span, 0, 0)))
                .Set("Section", section));

            // HingeRadau with lp/L = 0.08: same element class, same section count, different
            // Gauss locations, so MPCORecorder gives it a group of its own.
            var longHinges = _run.Solve("LongHinges", ComponentHarness.For<Alpaca4d.Gh.BeamBase>()
                .SwitchTo("WithHinges (Alpaca4d)")
                .Set("Line", new LineCurve(new Point3d(2 * Span, 0, 0), new Point3d(Total, 0, 0)))
                .Set("Section", section)
                .Set("LpI", LongHingeRatio)
                .Set("LpJ", LongHingeRatio));

            var support = _run.Solve("Support", ComponentHarness.For<Alpaca4d.Gh.Support>()
                .Set("Position", Root));

            var load = _run.Solve("Load", ComponentHarness.For<Alpaca4d.Gh.PointLoad>()
                .Set("Point", Tip)
                .Set("Force", new Vector3d(0, 0, -TipLoad)));

            var pattern = _run.Solve("Pattern", ComponentHarness.For<Alpaca4d.Gh.PatternBase>()
                .SwitchTo("PlainPattern (Alpaca4d)")
                .Set("Loads", load));

            var model = _run.Solve("Assemble", ComponentHarness.For<Alpaca4d.Gh.AssembleModel>()
                .Set("Elements", plainBeam, defaultHinges, longHinges)
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
        public void The_hinged_beams_use_HingeRadau_with_the_hinge_ratios_that_were_asked_for()
        {
            var beams = AnalysedBeams();

            Assert.That(beams[0].BeamIntegration.Type,
                Is.EqualTo(Alpaca4d.BeamIntegration.IntegrationType.NewtonCotes));

            var defaultHinges = (Alpaca4d.BeamIntegration.HingeRadauIntegration)beams[1].BeamIntegration;
            var longHinges = (Alpaca4d.BeamIntegration.HingeRadauIntegration)beams[2].BeamIntegration;

            Assert.Multiple(() =>
            {
                // The integration still carries lp as the length HingeRadau needs; the ratio is
                // what the component was given.
                Assert.That(defaultHinges.LpI, Is.EqualTo(0.05 * Span).Within(1e-9), "an empty LpI means lp/L = 0.05");
                Assert.That(defaultHinges.LpJ, Is.EqualTo(0.05 * Span).Within(1e-9));
                Assert.That(longHinges.LpI, Is.EqualTo(LongHingeRatio * Span).Within(1e-9), "0.08 is inside the clamp");
                Assert.That(longHinges.LpJ, Is.EqualTo(LongHingeRatio * Span).Within(1e-9));

                Assert.That(((Alpaca4d.Element.BeamWithHinges)beams[1]).LpRatioI,
                    Is.EqualTo(Alpaca4d.Element.BeamWithHinges.DefaultLpRatio).Within(1e-12));
                Assert.That(((Alpaca4d.Element.BeamWithHinges)beams[2]).LpRatioI,
                    Is.EqualTo(LongHingeRatio).Within(1e-12));
            });
        }

        /// <summary>
        /// The abscissae of <see cref="Alpaca4d.BeamIntegration.HingeRadauIntegration"/>, checked
        /// against HingeRadauBeamIntegration::getSectionLocations. OpenSees prints exactly these
        /// for `recorder Element -ele n integrationPoints`.
        /// </summary>
        [Test]
        public void HingeRadau_reports_the_section_locations_OpenSees_integrates_over()
        {
            var beams = AnalysedBeams();

            var defaultHinges = beams[1].BeamIntegration.SectionLocations(Span);
            var longHinges = beams[2].BeamIntegration.SectionLocations(Span);

            Assert.Multiple(() =>
            {
                AssertStations(defaultHinges,
                    new[] { 0.0, 0.133333, 0.326795, 0.673205, 0.866667, 1.0 }, "lp/L = 0.05");
                AssertStations(longHinges,
                    new[] { 0.0, 0.213333, 0.396077, 0.603923, 0.786667, 1.0 }, "lp/L = 0.08");
                AssertStations(beams[0].BeamIntegration.SectionLocations(Span),
                    new[] { 0.0, 0.25, 0.5, 0.75, 1.0 }, "NewtonCotes with 5 points");
            });
        }

        /// <summary>
        /// The reader has to find all three groups. A reader that knows only two keys loses a
        /// whole beam and hands back an empty branch for it without complaining.
        /// </summary>
        [Test]
        public void Every_beam_gets_its_section_forces_back()
        {
            var forces = Alpaca4d.Result.Read.ForceBeamColumn(_run.AnalysedModel, 0);

            Assert.Multiple(() =>
            {
                Assert.That(forces.n, Has.Count.EqualTo(3), "one entry per beam");
                Assert.That(forces.n[0], Has.Count.EqualTo(5), "NewtonCotes 5");
                Assert.That(forces.n[1], Has.Count.EqualTo(6), "HingeRadau, lp/L = 0.05");
                Assert.That(forces.n[2], Has.Count.EqualTo(6), "HingeRadau, lp/L = 0.08");
            });
        }

        /// <summary>
        /// Statics on a straight cantilever: the bending moment at a section is the tip load
        /// times the distance left to the tip. Reading a value at the wrong station shows up
        /// here, because the hinged beams do not sample at even steps.
        /// </summary>
        [Test]
        public void The_recorded_moments_match_statics_at_the_station_each_one_belongs_to()
        {
            var forces = Alpaca4d.Result.Read.ForceBeamColumn(_run.AnalysedModel, 0);
            var beams = AnalysedBeams();

            Assert.Multiple(() =>
            {
                for (var b = 0; b < beams.Count; b++)
                {
                    var beam = beams[b];
                    var start = beam.Curve.PointAtStart.X;
                    var stations = beam.BeamIntegration.SectionLocations(Span);

                    Assert.That(stations, Has.Count.EqualTo(forces.my[b].Count),
                        "beam " + b + " reports a different number of sections than it integrates over");

                    for (var s = 0; s < stations.Count; s++)
                    {
                        var x = start + stations[s] * Span;
                        var expected = TipLoad * (Total - x);

                        // The section's local axes follow the geometric transformation, so compare
                        // the resultant of the two bending components and leave the sign alone.
                        var bending = Math.Sqrt(
                            forces.my[b][s] * forces.my[b][s] + forces.mz[b][s] * forces.mz[b][s]);

                        Assert.That(bending, Is.EqualTo(expected).Within(0.01 * TipLoad * Total),
                            "beam " + b + ", section " + s + " sits at x = " + x.ToString("F3"));
                        Assert.That(forces.n[b][s], Is.EqualTo(0.0).Within(1e-6),
                            "beam " + b + ", section " + s + ": nothing loads this cantilever axially");
                    }
                }
            });
        }

        /// <summary>The Beam Forces component publishes one branch per beam, none of them empty.</summary>
        [Test]
        public void The_Beam_Forces_component_publishes_a_branch_for_every_beam()
        {
            var result = ComponentHarness.For<Alpaca4d.Gh.BeamForce>()
                                         .Set("AlpacaModel", _run.AnalysedModel)
                                         .Solve();

            Assert.That(result.Errors, Is.Empty, result.Describe());

            var branches = result.Branches(0); // N
            Assert.That(branches, Has.Count.EqualTo(3));
            Assert.That(branches.Select(branch => branch.Count), Is.EqualTo(new[] { 5, 6, 6 }));
        }

        private IReadOnlyList<Alpaca4d.Generic.IBeam> AnalysedBeams()
        {
            Assert.That(_run.AnalysedModel, Is.Not.Null,
                "RunAnalysis returned no model, which means the solver failed:\n" + _run.Log);

            // Model.Beams follows the order the elements were assembled in.
            return _run.AnalysedModel.Beams;
        }

        private static void AssertStations(IReadOnlyList<double> actual, double[] expected, string what)
        {
            Assert.That(actual, Has.Count.EqualTo(expected.Length), what);

            for (var i = 0; i < expected.Length; i++)
                Assert.That(actual[i], Is.EqualTo(expected[i]).Within(1e-6), what + ", station " + i);
        }
    }
}
