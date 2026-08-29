using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Grasshopper.Kernel;
using NUnit.Framework;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// Whole-plug-in checks: every component has to be constructible, uniquely
    /// identified and shaped the way the approved snapshot says it is.
    /// </summary>
    [TestFixture]
    public class ComponentApiTests
    {
        private const string ApprovedFile = "ComponentApi.approved.txt";

        [Test]
        public void Every_component_can_be_constructed()
        {
            var failures = new List<string>();

            foreach (var type in ComponentApi.ComponentTypes())
            {
                try
                {
                    Activator.CreateInstance(type);
                }
                catch (Exception ex)
                {
                    var cause = ex.InnerException ?? ex;
                    failures.Add(type.FullName + " -> " + cause.GetType().Name + ": " + cause.Message);
                }
            }

            Assert.That(failures, Is.Empty, "Components that threw from their constructor:\n" + string.Join("\n", failures));
        }

        [Test]
        public void Component_guids_are_unique()
        {
            var duplicates = ComponentApi.ComponentTypes()
                .Select(t => new { Type = t, Guid = ((GH_Component)Activator.CreateInstance(t)).ComponentGuid })
                .GroupBy(x => x.Guid)
                .Where(g => g.Count() > 1)
                .Select(g => g.Key + " is used by " + string.Join(", ", g.Select(x => x.Type.FullName)))
                .ToList();

            Assert.That(duplicates, Is.Empty,
                "Two components sharing a GUID makes Grasshopper load the wrong one:\n" + string.Join("\n", duplicates));
        }

        [Test]
        public void Every_component_has_an_icon()
        {
            var missing = ComponentApi.ComponentTypes()
                .Select(t => (GH_Component)Activator.CreateInstance(t))
                .Where(c => !c.Obsolete && c.Icon_24x24 == null)
                .Select(c => c.Name)
                .ToList();

            Assert.That(missing, Is.Empty, "Non-obsolete components without an icon:\n" + string.Join("\n", missing));
        }

        [Test]
        public void Every_component_lives_in_the_Alpaca4d_tab()
        {
            var strays = ComponentApi.ComponentTypes()
                .Select(t => (GH_Component)Activator.CreateInstance(t))
                .Where(c => c.Category != "Alpaca4d")
                .Select(c => c.Name + " -> '" + c.Category + "'")
                .ToList();

            Assert.That(strays, Is.Empty, "Components outside the Alpaca4d tab:\n" + string.Join("\n", strays));
        }

        /// <summary>
        /// Compares the whole component surface against the approved snapshot.
        /// When this fails, read the diff: if the change is intended, copy the
        /// .received.txt over the approved file and commit it with the change.
        /// </summary>
        [Test]
        public void Component_api_matches_the_approved_snapshot()
        {
            var actual = Normalise(ComponentApi.Snapshot());
            var approvedPath = Path.Combine(ApprovedDirectory, ApprovedFile);
            var receivedPath = Path.Combine(ApprovedDirectory, "ComponentApi.received.txt");

            if (!File.Exists(approvedPath))
            {
                Directory.CreateDirectory(ApprovedDirectory);
                File.WriteAllText(approvedPath, actual);
                Assert.Inconclusive(
                    "No approved snapshot existed; wrote one to " + approvedPath + ". Review it and commit it.");
            }

            var approved = Normalise(File.ReadAllText(approvedPath));
            if (approved == actual)
            {
                if (File.Exists(receivedPath))
                    File.Delete(receivedPath);
                return;
            }

            File.WriteAllText(receivedPath, actual);
            Assert.Fail(
                "The component API changed." + Environment.NewLine +
                FirstDifference(approved, actual) + Environment.NewLine +
                "Full text written to " + receivedPath + Environment.NewLine +
                "If the change is intended:  cp \"" + receivedPath + "\" \"" + approvedPath + "\"");
        }

        /// <summary>
        /// The snapshot lives with the sources, not in bin/, so approving a change is a
        /// normal edit to a tracked file.
        /// </summary>
        private static string ApprovedDirectory
        {
            get
            {
                var fromSource = Path.GetFullPath(Path.Combine(
                    TestContext.CurrentContext.TestDirectory, "..", "..", "..", "Approved"));
                return Directory.Exists(fromSource)
                    ? fromSource
                    : Path.Combine(TestContext.CurrentContext.TestDirectory, "Approved");
            }
        }

        private static string Normalise(string text)
        {
            return text.Replace("\r\n", "\n").TrimEnd() + "\n";
        }

        private static string FirstDifference(string approved, string actual)
        {
            var expectedLines = approved.Split('\n');
            var actualLines = actual.Split('\n');

            for (var i = 0; i < Math.Max(expectedLines.Length, actualLines.Length); i++)
            {
                var e = i < expectedLines.Length ? expectedLines[i] : "<end of file>";
                var a = i < actualLines.Length ? actualLines[i] : "<end of file>";
                if (e != a)
                    return "First difference at line " + (i + 1) + ":" + Environment.NewLine +
                           "  approved: " + e + Environment.NewLine +
                           "  actual:   " + a;
            }

            return "Files differ only in trailing whitespace.";
        }
    }
}
