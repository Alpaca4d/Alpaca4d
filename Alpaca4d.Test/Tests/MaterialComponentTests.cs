using System.Linq;
using NUnit.Framework;

namespace Alpaca4d.Testing.Tests
{
    [TestFixture]
    public class MaterialComponentTests
    {
        [Test]
        public void ElasticIsotropic_uses_the_registered_defaults_when_nothing_is_wired()
        {
            var result = ComponentHarness.For<SimplexGh.nD>()
                                         .SwitchTo("ElasticIsotropic (Alpaca4d)")
                                         .Solve();

            Assert.That(result.Errors, Is.Empty, result.Describe());

            var material = result.Get<Alpaca4d.Material.ElasticIsotropicMaterial>(0);
            Assert.Multiple(() =>
            {
                Assert.That(material.E, Is.EqualTo(210000000).Within(1e-9));
                Assert.That(material.G, Is.EqualTo(80760000).Within(1e-9));
                Assert.That(material.Nu, Is.EqualTo(0.3).Within(1e-12));
                Assert.That(material.Rho, Is.EqualTo(7850).Within(1e-9));
            });
        }

        [Test]
        public void ElasticIsotropic_passes_its_inputs_through_to_the_core_material()
        {
            var result = ComponentHarness.For<SimplexGh.nD>()
                                         .SwitchTo("ElasticIsotropic (Alpaca4d)")
                                         .Set("MatName", "S355")
                                         .Set("E", 2.1e8)
                                         .Set("G", 8.0e7)
                                         .Set(3, 0.25)      // the Poisson input is named with a Greek nu
                                         .Set("Rho", 7800.0)
                                         .Solve();

            Assert.That(result.Errors, Is.Empty, result.Describe());

            var material = result.Get<Alpaca4d.Material.ElasticIsotropicMaterial>(0);
            Assert.Multiple(() =>
            {
                Assert.That(material.MatName, Is.EqualTo("S355"));
                Assert.That(material.E, Is.EqualTo(2.1e8).Within(1e-6));
                Assert.That(material.G, Is.EqualTo(8.0e7).Within(1e-6));
                Assert.That(material.Nu, Is.EqualTo(0.25).Within(1e-12));
                Assert.That(material.Rho, Is.EqualTo(7800).Within(1e-9));
            });
        }

        /// <summary>
        /// The OpenSees input deck is what Alpaca4d actually ships to the solver, so it
        /// is worth asserting on the text and not only on the C# object.
        /// </summary>
        [Test]
        public void ElasticIsotropic_writes_the_expected_OpenSees_command()
        {
            var result = ComponentHarness.For<SimplexGh.nD>()
                                         .SwitchTo("ElasticIsotropic (Alpaca4d)")
                                         .Set("E", 2.1e8)
                                         .Set(3, 0.3)
                                         .Set("Rho", 7850.0)
                                         .Solve();

            var material = result.Get<Alpaca4d.Material.ElasticIsotropicMaterial>(0);

            Assert.That(material.WriteTcl().Trim(),
                Is.EqualTo("nDMaterial ElasticIsotropic " + material.Id + " 210000000 0.3 7850"));
        }

        [Test]
        public void A_component_solved_twice_does_not_accumulate_output()
        {
            var harness = ComponentHarness.For<SimplexGh.nD>().SwitchTo("ElasticIsotropic (Alpaca4d)");

            Assert.That(harness.Solve().Count(0), Is.EqualTo(1));
            Assert.That(harness.Solve().Count(0), Is.EqualTo(1));
        }
    }
}
