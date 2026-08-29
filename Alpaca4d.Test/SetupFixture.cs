using System;
using System.IO;
using System.Reflection;
using NUnit.Framework;

namespace Alpaca4d.Testing
{
    /// <summary>
    /// Starts a head-less Rhino once per test run, through McNeel's Rhino.Testing
    /// (which wraps Rhino.Inside). Everything after that - RhinoCommon, the full Rhino
    /// geometry kernel, Grasshopper - is the real thing, so component code behaves as it
    /// does on a canvas.
    ///
    /// Which Rhino, and what gets loaded with it, is configured in
    /// Rhino.Testing.Configs.xml next to the test assembly.
    /// </summary>
    [SetUpFixture]
    public sealed class SetupFixture : Rhino.Testing.Fixtures.RhinoSetupFixture
    {
        public override void OneTimeSetup()
        {
            base.OneTimeSetup();

            LoadGHA(new[] { PluginPath });
        }

        /// <summary>The Alpaca4d plug-in the tests exercise, built by the project reference.</summary>
        public static string PluginPath
        {
            get
            {
                return Path.Combine(
                    Path.GetDirectoryName(new Uri(typeof(SetupFixture).Assembly.CodeBase).LocalPath),
                    "Alpaca4d.Gh.gha");
            }
        }

        /// <summary>
        /// The plug-in is built with TargetExt=.gha, and the CLR only ever probes for
        /// .dll and .exe - so a plain reference to a type in it never resolves on its own.
        /// A module initializer gets this in place before NUnit reflects over anything.
        /// </summary>
        [System.Runtime.CompilerServices.ModuleInitializer]
        public static void ResolvePluginAssembly()
        {
            AppDomain.CurrentDomain.AssemblyResolve += (sender, args) =>
            {
                var name = new AssemblyName(args.Name).Name;

                if (!string.Equals(name, "Alpaca4d.Gh", StringComparison.OrdinalIgnoreCase))
                    return null;

                return File.Exists(PluginPath) ? Assembly.LoadFrom(PluginPath) : null;
            };
        }
    }
}

namespace System.Runtime.CompilerServices
{
    // Module initializers are a C# 9 feature; the attribute is not in the net48
    // reference assemblies, so declare it here.
    [AttributeUsage(AttributeTargets.Method, Inherited = false)]
    internal sealed class ModuleInitializerAttribute : Attribute
    {
    }
}
