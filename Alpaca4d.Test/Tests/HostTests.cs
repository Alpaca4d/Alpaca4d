using NUnit.Framework;
using Rhino.Geometry;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// Fails first and loudest when the head-less Rhino is not up, so the rest of the
    /// suite does not drown in resolution errors.
    /// </summary>
    [TestFixture]
    public class HostTests
    {
        [Test]
        public void Rhino_is_running_head_less()
        {
            TestContext.WriteLine("Rhino " + Rhino.RhinoApp.Version);
            Assert.That(Rhino.RhinoDoc.ActiveDoc, Is.Not.Null, "Rhino.Testing should have created a document.");
        }

        [Test]
        public void Grasshopper_is_loaded()
        {
            var assembly = typeof(Grasshopper.Kernel.GH_Component).Assembly;
            TestContext.WriteLine("Grasshopper " + assembly.GetName().Version + " from " + assembly.Location);
            Assert.That(assembly.GetName().Name, Is.EqualTo("Grasshopper"));
        }

        [Test]
        public void The_Alpaca4d_plugin_is_loaded()
        {
            TestContext.WriteLine("Plug-in: " + ComponentApi.PluginAssembly.Location);
            Assert.That(ComponentApi.ComponentTypes(), Is.Not.Empty);
        }

        /// <summary>
        /// The whole Rhino geometry kernel is available, not just openNURBS - Alpaca4d
        /// uses arc length, mesh mass properties and mesh/line intersection.
        /// </summary>
        [Test]
        public void The_full_geometry_kernel_is_available()
        {
            var mesh = Mesh.CreateFromPlane(Plane.WorldXY, new Interval(0, 2), new Interval(0, 3), 2, 3);

            Assert.Multiple(() =>
            {
                Assert.That(new LineCurve(Point3d.Origin, new Point3d(3, 4, 0)).GetLength(),
                    Is.EqualTo(5.0).Within(1e-9), "Curve.GetLength");
                Assert.That(AreaMassProperties.Compute(mesh).Area,
                    Is.EqualTo(6.0).Within(1e-9), "AreaMassProperties.Compute");
            });
        }
    }
}
