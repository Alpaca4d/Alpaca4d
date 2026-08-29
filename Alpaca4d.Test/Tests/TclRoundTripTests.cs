using System;
using System.IO;
using System.Linq;
using NUnit.Framework;
using Rhino.Geometry;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// Serialize -> Deserialise, and then the solver on what came back.
    ///
    /// The cantilever is the same one <see cref="CantileverWorkflowTests"/> builds, so the answer is
    /// still the closed form delta = P L^3 / (3 E I). Here it is asked of a model that was written out
    /// as an OpenSees deck and read back in, which only holds if the sections, the material stiffness,
    /// the density (which the deck carries only as the element's -mass), the geometric transformation,
    /// the support and the load pattern all survived the trip.
    /// </summary>
    [TestFixture]
    [NonParallelizable]
    public class TclRoundTripTests
    {
        private const double Length = 10.0;         // m
        private const double Side = 0.4;            // m
        private const double YoungsModulus = 2.1e8; // kN/m2
        private const double Density = 7850.0;      // kg/m3, the default steel
        private const double TipLoad = 10.0;        // kN, downwards

        private static readonly Point3d Root = new Point3d(0, 0, 0);
        private static readonly Point3d Tip = new Point3d(Length, 0, 0);

        private WorkflowRun _run;
        private string[] _tcl;

        [OneTimeSetUp]
        public void RunTheRoundTripOnce()
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
                .Set("Point", Root));

            var load = _run.Solve("Load", ComponentHarness.For<Alpaca4d.Gh.PointLoad>()
                .Set("Point", Tip)
                .Set("Force", new Vector3d(0, 0, -TipLoad)));

            var pattern = _run.Solve("Pattern", ComponentHarness.For<Alpaca4d.Gh.PatternBase>()
                .SwitchTo("PlainPattern (Alpaca4d)")
                .Set("Loads", load));

            var original = _run.Solve("Assemble", ComponentHarness.For<Alpaca4d.Gh.AssembleModel>()
                .Set("Elements", beam)
                .Set("Supports", support)
                .Set("LoadPatterns", pattern));

            _tcl = _run.SolveMany("Serialize", ComponentHarness.For<Alpaca4d.Gh.Serialize>()
                .Set("AlpacaModel", original))
                .Cast<string>()
                .ToArray();

            _run.Solve("Deserialise", ComponentHarness.For<Alpaca4d.Gh.Deserialize>()
                .Set("Text", _tcl.Cast<object>().ToArray()));

            var settings = _run.Solve("Settings", ComponentHarness.For<Alpaca4d.Gh.AnalysisSettings>());

            _run.Analyse(Reread, settings);
        }

        [OneTimeTearDown]
        public void CleanUp()
        {
            if (_run != null)
                _run.Dispose();
        }

        private Alpaca4d.Model Original
        {
            get { return _run.ResultOf("Assemble").Get<Alpaca4d.Model>(0); }
        }

        private Alpaca4d.Model Reread
        {
            get { return _run.ResultOf("Deserialise").Get<Alpaca4d.Model>(0); }
        }

        private static Alpaca4d.Generic.IBeam BeamOf(Alpaca4d.Model model)
        {
            return (Alpaca4d.Generic.IBeam)model.Elements.Single();
        }

        [Test]
        public void Every_component_in_the_chain_solves_without_errors()
        {
            Assert.That(_run.Complaints(), Is.Empty,
                "Components that reported an error:\n" + string.Join("\n", _run.Complaints()) +
                "\n\nOpenSees log:\n" + _run.Log);
        }

        /// <summary>
        /// Serialize hands out one item per WriteTcl() call, and several of those hold more than one
        /// command - a beam emits its geomTransf on a line of its own. A reader that treats "\n" as
        /// plain whitespace silently loses every command after the first of each item, so the shape of
        /// this output is what the reader has to cope with.
        /// </summary>
        [Test]
        public void The_serialized_text_packs_several_commands_into_single_items()
        {
            Assert.That(_tcl.Any(item => item.TrimEnd('\n', '\r').Contains("\n")),
                "Serialize no longer emits multi-command items; the reader's line splitting is untested.");
        }

        [Test]
        public void Deserialise_reports_nothing_it_could_not_read()
        {
            var result = _run.ResultOf("Deserialise");

            Assert.That(result.Errors, Is.Empty, result.Describe());
            Assert.That(result.Warnings, Is.Empty, result.Describe());
        }

        [Test]
        public void The_reread_model_has_the_same_topology()
        {
            Assert.Multiple(() =>
            {
                Assert.That(Reread.Elements, Has.Count.EqualTo(Original.Elements.Count));
                Assert.That(Reread.Nodes, Has.Count.EqualTo(Original.Nodes.Count));
                Assert.That(Reread.Supports, Has.Count.EqualTo(Original.Supports.Count));
                Assert.That(Reread.LoadPatterns, Has.Count.EqualTo(Original.LoadPatterns.Count));
                Assert.That(Reread.Nodes.Select(n => n.Pos),
                    Is.EquivalentTo(Original.Nodes.Select(n => n.Pos)));
            });
        }

        [Test]
        public void The_section_and_its_material_survive_the_round_trip()
        {
            var before = BeamOf(Original).Section;
            var after = BeamOf(Reread).Section;

            Assert.Multiple(() =>
            {
                Assert.That(after.Area, Is.EqualTo(before.Area).Within(1e-9).Percent);
                Assert.That(after.Izz, Is.EqualTo(before.Izz).Within(1e-9).Percent);
                Assert.That(after.Iyy, Is.EqualTo(before.Iyy).Within(1e-9).Percent);
                Assert.That(after.J, Is.EqualTo(before.J).Within(1e-9).Percent);
                Assert.That(after.AlphaY, Is.EqualTo(before.AlphaY).Within(1e-9).Percent);
                Assert.That(after.AlphaZ, Is.EqualTo(before.AlphaZ).Within(1e-9).Percent);
                Assert.That(after.Material.E, Is.EqualTo(YoungsModulus).Within(1e-9).Percent);
                Assert.That(after.Material.G, Is.EqualTo(before.Material.G).Within(1e-9).Percent);
            });
        }

        /// <summary>
        /// Density is the one property an OpenSees deck never states outright: it reaches the file only
        /// as the element's -mass, which is the section's mass per unit length in tonnes.
        /// </summary>
        [Test]
        public void The_density_is_recovered_from_the_element_mass()
        {
            Assert.That(BeamOf(Reread).Section.Material.Rho, Is.EqualTo(Density).Within(0.01).Percent);
            Assert.That(Reread.TotalMass, Is.EqualTo(Side * Side * Length * Density).Within(0.1).Percent);
        }

        [Test]
        public void The_local_axes_of_the_beam_survive_the_round_trip()
        {
            Assert.That(BeamOf(Reread).GeomTransf.LocalZ, Is.EqualTo(BeamOf(Original).GeomTransf.LocalZ));
            Assert.That(BeamOf(Reread).GeomTransf.Type, Is.EqualTo(BeamOf(Original).GeomTransf.Type));
        }

        [Test]
        public void The_support_and_the_load_survive_the_round_trip()
        {
            var support = Reread.Supports.Single();
            var load = Reread.LoadPatterns.Single().Load.OfType<Alpaca4d.Loads.PointLoad>().Single();

            Assert.Multiple(() =>
            {
                Assert.That(support.Pos.DistanceTo(Root), Is.LessThan(1e-9));
                Assert.That(new[] { support.Tx, support.Ty, support.Tz, support.Rx, support.Ry, support.Rz },
                    Is.All.True, "a fully fixed support");
                Assert.That(load.Pos.DistanceTo(Tip), Is.LessThan(1e-9));
                Assert.That(load.Force.Z, Is.EqualTo(-TipLoad).Within(1e-9));
            });
        }

        [Test]
        public void Reading_from_a_file_gives_the_same_model_as_reading_from_text()
        {
            var path = Path.Combine(Path.GetTempPath(), "alpaca4d-roundtrip-" + Guid.NewGuid().ToString("N") + ".tcl");
            File.WriteAllLines(path, _tcl);

            try
            {
                var result = ComponentHarness.For<Alpaca4d.Gh.Deserialize>().Set("FilePath", path).Solve();

                Assert.That(result.Errors, Is.Empty, result.Describe());
                Assert.That(result.Warnings, Is.Empty, result.Describe());

                // Material, section and pattern tags come from a global counter, so two reads of the
                // same deck are numbered differently. What has to match is the model, not the tags.
                var fromFile = result.Get<Alpaca4d.Model>(0);
                Assert.That(fromFile.Elements, Has.Count.EqualTo(Reread.Elements.Count));
                Assert.That(fromFile.Nodes.Select(n => n.Pos), Is.EquivalentTo(Reread.Nodes.Select(n => n.Pos)));
                Assert.That(fromFile.TotalMass, Is.EqualTo(Reread.TotalMass).Within(1e-9).Percent);
            }
            finally
            {
                File.Delete(path);
            }
        }

        [Test]
        public void A_missing_file_is_an_error_on_the_component_rather_than_a_crash()
        {
            var result = ComponentHarness.For<Alpaca4d.Gh.Deserialize>()
                .Set("FilePath", Path.Combine(Path.GetTempPath(), "no-such-alpaca-file.tcl"))
                .Solve();

            Assert.That(result.Errors, Is.Not.Empty);
        }

        /// <summary>
        /// Section, material, time series and pattern tags are re-issued by the read and need not match
        /// the file. Node and element tags are a different matter: Assemble derives them from the
        /// element order, and the element order is the file order, so they do come back unchanged.
        /// </summary>
        [Test]
        public void The_node_and_element_tags_are_the_ones_the_file_used()
        {
            Assert.Multiple(() =>
            {
                Assert.That(Reread.Elements.Select(e => e.Id), Is.EqualTo(Original.Elements.Select(e => e.Id)));
                Assert.That(Reread.Nodes.Select(n => n.Id), Is.EqualTo(Original.Nodes.Select(n => n.Id)));
                Assert.That(Reread.Nodes.Select(n => n.Pos), Is.EqualTo(Original.Nodes.Select(n => n.Pos)));
                Assert.That(BeamOf(Reread).INode, Is.EqualTo(BeamOf(Original).INode));
                Assert.That(BeamOf(Reread).JNode, Is.EqualTo(BeamOf(Original).JNode));
            });
        }

        [Test]
        public void The_reread_model_solves_to_the_closed_form_cantilever()
        {
            var inertia = Math.Pow(Side, 4) / 12.0;
            var expected = TipLoad * Math.Pow(Length, 3) / (3.0 * YoungsModulus * inertia);

            Assert.That(_run.AnalysedModel, Is.Not.Null,
                "RunAnalysis returned no model for the re-read deck:\n" + _run.Log);

            var tip = _run.DisplacementAt(Tip);
            TestContext.WriteLine("tip displacement    = " + tip);
            TestContext.WriteLine("expected deflection = " + expected.ToString("F6") + " m");

            Assert.Multiple(() =>
            {
                Assert.That(-tip.Z, Is.EqualTo(expected).Within(1.0).Percent,
                    "P L^3 / (3 E I) for a slender cantilever; shear adds ~0.2%.");
                Assert.That(_run.DisplacementAt(Root).Length, Is.EqualTo(0).Within(1e-12));
            });
        }
    }

    /// <summary>
    /// The same trip for a shell, which travels through a different set of commands: nDMaterial,
    /// section PlateFiber and element ASDShellQ4. Density is written on the material here, so unlike
    /// the beam it does not have to be inferred.
    /// </summary>
    [TestFixture]
    [NonParallelizable]
    public class ShellTclRoundTripTests
    {
        private const double Length = 10.0;
        private const double Width = 1.0;
        private const double Thickness = 0.3;
        private const double YoungsModulus = 2.1e8;
        private const double Density = 7850.0;
        private const int Divisions = 10;

        private WorkflowRun _run;

        [OneTimeSetUp]
        public void RunTheRoundTripOnce()
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
                ComponentHarness.For<Alpaca4d.Gh.Support>().Set("Point", p))).ToArray();

            var original = _run.Solve("Assemble", ComponentHarness.For<Alpaca4d.Gh.AssembleModel>()
                .Set("Elements", elements.ToArray())
                .Set("Supports", supports));

            var tcl = _run.SolveMany("Serialize", ComponentHarness.For<Alpaca4d.Gh.Serialize>()
                .Set("AlpacaModel", original))
                .ToArray();

            _run.Solve("Deserialise", ComponentHarness.For<Alpaca4d.Gh.Deserialize>()
                .Set("Text", tcl));
        }

        [OneTimeTearDown]
        public void CleanUp()
        {
            if (_run != null)
                _run.Dispose();
        }

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

        private Alpaca4d.Model Reread
        {
            get { return _run.ResultOf("Deserialise").Get<Alpaca4d.Model>(0); }
        }

        [Test]
        public void Every_component_in_the_chain_solves_without_errors()
        {
            Assert.That(_run.Complaints(), Is.Empty,
                "Components that reported an error:\n" + string.Join("\n", _run.Complaints()));
        }

        [Test]
        public void Deserialise_reports_nothing_it_could_not_read()
        {
            var result = _run.ResultOf("Deserialise");
            Assert.That(result.Warnings, Is.Empty, result.Describe());
        }

        [Test]
        public void Every_shell_comes_back_with_its_section_and_material()
        {
            var shells = Reread.Elements.OfType<Alpaca4d.Generic.IShell>().ToList();

            Assert.That(shells, Has.Count.EqualTo(Divisions));
            Assert.That(Reread.Nodes, Has.Count.EqualTo(2 * (Divisions + 1)));

            Assert.Multiple(() =>
            {
                foreach (var shell in shells)
                {
                    Assert.That(shell.Mesh.Vertices.Count, Is.EqualTo(4));
                    Assert.That(shell.Section.Thickness, Is.EqualTo(Thickness).Within(1e-9).Percent);
                    Assert.That(shell.Section.Material.Rho, Is.EqualTo(Density).Within(1e-9).Percent);
                }
            });

            // One section object for the whole set, or Assemble would write it once per element.
            Assert.That(shells.Select(s => s.Section).Distinct().Count(), Is.EqualTo(1));
        }

        [Test]
        public void The_reread_model_reports_the_same_mass()
        {
            Assert.That(Reread.TotalMass, Is.EqualTo(Length * Width * Thickness * Density).Within(0.1).Percent);
        }

    }
}
