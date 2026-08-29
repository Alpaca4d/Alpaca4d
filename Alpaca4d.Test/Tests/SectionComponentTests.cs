using System.Linq;
using NUnit.Framework;

namespace Alpaca4d.Testing.Tests
{
    [TestFixture]
    public class SectionComponentTests
    {
        [Test]
        public void RectangleCS_computes_the_section_properties()
        {
            var result = ComponentHarness.For<Alpaca4d.Gh.RectangleCS>()
                                         .Set("SectionName", "R400x800")
                                         .Set("Width", 0.4)
                                         .Set("Height", 0.8)
                                         .Solve();

            Assert.That(result.Errors, Is.Empty, result.Describe());

            var section = result.Get<Alpaca4d.Section.RectangleCS>(0);
            Assert.Multiple(() =>
            {
                Assert.That(section.SectionName, Is.EqualTo("R400x800"));
                Assert.That(section.Area, Is.EqualTo(0.32).Within(1e-12));
                Assert.That(section.Izz, Is.EqualTo(0.4 * 0.8 * 0.8 * 0.8 / 12.0).Within(1e-12));
                Assert.That(section.Iyy, Is.EqualTo(0.4 * 0.4 * 0.4 * 0.8 / 12.0).Within(1e-12));
            });
        }

        [Test]
        public void RectangleCS_falls_back_to_the_default_steel_material()
        {
            var result = ComponentHarness.For<Alpaca4d.Gh.RectangleCS>().Solve();

            Assert.That(result.Errors, Is.Empty, result.Describe());
            Assert.That(result.Get<Alpaca4d.Section.RectangleCS>(0).Material, Is.Not.Null);
        }

        /// <summary>
        /// Components are chained by handing one solve's output object to the next
        /// component's input - the same objects Grasshopper moves along a wire.
        /// </summary>
        [Test]
        public void A_material_component_can_feed_a_section_component()
        {
            var material = ComponentHarness.For<Alpaca4d.Gh.Uniaxial>()
                                           .SwitchTo("UniaxialElastic (Alpaca4d)")
                                           .Solve()
                                           .All(0)
                                           .Single();

            var result = ComponentHarness.For<Alpaca4d.Gh.RectangleCS>()
                                         .Set("Material", material)
                                         .Solve();

            Assert.That(result.Errors, Is.Empty, result.Describe());
            Assert.That(result.Get<Alpaca4d.Section.RectangleCS>(0).Material, Is.SameAs(material));
        }

        /// <summary>
        /// Exercises the openNURBS layer: the section draws itself with real Rhino
        /// geometry, and that has to work with no Rhino process behind it.
        /// </summary>
        [Test]
        public void RectangleCS_produces_real_Rhino_geometry()
        {
            var section = ComponentHarness.For<Alpaca4d.Gh.RectangleCS>()
                                          .Set("Width", 0.4)
                                          .Set("Height", 0.8)
                                          .Solve()
                                          .Get<Alpaca4d.Section.RectangleCS>(0);

            var outline = section.Curves.Single();
            var box = outline.GetBoundingBox(true);

            Assert.That(outline.IsClosed, Is.True);
            Assert.That(box.Diagonal.X, Is.EqualTo(0.4).Within(1e-9));
            Assert.That(box.Diagonal.Y, Is.EqualTo(0.8).Within(1e-9));
            Assert.That(box.Center.EpsilonEquals(Rhino.Geometry.Point3d.Origin, 1e-9), Is.True);
        }
    }
}
