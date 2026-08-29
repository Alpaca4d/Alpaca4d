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

            // Not RhinoDoc.ActiveDoc: it is per-thread in a head-less Rhino and set
            // only on the thread that started it, so it reads back null here.
            Assert.That(SetupFixture.HeadlessDoc, Is.Not.Null, "Rhino.Testing should have created a document.");
            Assert.That(SetupFixture.HeadlessDoc.IsHeadless, Is.True, "The document should be head-less.");
        }

        [Test]
        public void Grasshopper_is_loaded()
        {
            var assembly = typeof(Grasshopper.Kernel.GH_Component).Assembly;
            TestContext.WriteLine("Grasshopper " + assembly.GetName().Version + " from " + assembly.Location);
            Assert.That(assembly.GetName().Name, Is.EqualTo("Grasshopper"));
        }

        /// <summary>
        /// Twice is not the same as once. Grasshopper loads the deployed plug-in out of
        /// its libraries folder during startup, and the test bench has a second copy of
        /// the same file next to the test assembly; load both and every component GUID
        /// is claimed twice, which Grasshopper reports as a Component ID conflict - a
        /// modal dialog, in a process with nobody to click it.
        /// </summary>
        [Test]
        public void The_plugin_is_loaded_exactly_once()
        {
            var loaded = SetupFixture.LoadedPlugins;

            foreach (var location in loaded)
                TestContext.WriteLine(location);

            Assert.That(loaded, Has.Length.EqualTo(1),
                        "Alpaca4d.Gh is loaded " + loaded.Length + " times: " + string.Join(" / ", loaded));
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
