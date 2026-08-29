using System;
using System.IO;
using NUnit.Framework;

namespace Alpaca4d.Testing
{
    /// <summary>
    /// Points Alpaca4d at the OpenSees binary that ships with the plug-in.
    ///
    /// In Grasshopper the path comes from settings.json, written by
    /// Alpaca4d -> Settings -> Set OpenSees Executable. A test process has no such
    /// setting, so it selects the copy that the build already placed next to the test
    /// assembly - the exact binary an installed Alpaca4d would use.
    /// </summary>
    public static class OpenSees
    {
        public static void UseBundledSolver()
        {
            var executable = BundledExecutable();

            if (!File.Exists(executable))
                Assert.Ignore(
                    "No bundled OpenSees solver at " + executable + "; the analysis tests need one.");

            Alpaca4d.AlpacaSettings.OpenSeesPath = executable;
        }

        public static string BundledExecutable()
        {
            var root = Path.Combine(TestContext.CurrentContext.TestDirectory, "OpenSees-Solvers");

            return Path.Combine(root, "win", "bin", "OpenSees.exe");
        }
    }
}
