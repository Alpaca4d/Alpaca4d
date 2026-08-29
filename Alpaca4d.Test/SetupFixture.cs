using System;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using NUnit.Framework;
using Rhino.PlugIns;

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

            // Read on this thread while it still means something - see HeadlessDoc.
            HeadlessDoc = Rhino.RhinoDoc.ActiveDoc;

            LoadGrasshopperHeadless();

            // Only if starting Grasshopper did not already bring it in. On a machine
            // that has built this repo it will have: the plug-in build deploys a copy
            // into the Grasshopper libraries folder every time (CopyToGrasshopperLibraries),
            // and Grasshopper loads it during startup like any other plug-in. Loading
            // the copy next to the test assembly on top of that registers every
            // component a second time, and Grasshopper answers with its "Component ID
            // conflict" dialog - a modal dialog, in a process with nobody to click it.
            if (!PluginIsLoaded)
                LoadGHA(new[] { PluginPath });
        }

        /// <summary>
        /// Whether the Alpaca4d plug-in assembly is in the AppDomain, wherever it came
        /// from. Exactly one copy may ever be loaded - see LoadedPlugins.
        /// </summary>
        public static bool PluginIsLoaded
        {
            get { return LoadedPlugins.Length > 0; }
        }

        /// <summary>
        /// Every copy of the plug-in assembly currently loaded, by location.
        ///
        /// There must only ever be one. Two copies - typically the deployed one in the
        /// Grasshopper libraries folder and the one the project reference puts next to
        /// the test assembly - claim the same component GUIDs, which is what Grasshopper
        /// calls a Component ID conflict. `The_plugin_is_loaded_exactly_once` guards it.
        /// </summary>
        public static string[] LoadedPlugins
        {
            get
            {
                var loaded = new List<string>();

                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    if (!string.Equals(assembly.GetName().Name, "Alpaca4d.Gh", StringComparison.OrdinalIgnoreCase))
                        continue;

                    loaded.Add(assembly.IsDynamic ? "<dynamic>" : assembly.Location);
                }

                return loaded.ToArray();
            }
        }

        /// <summary>
        /// The document Rhino.Testing created, kept because there is no other way to
        /// reach it from a test.
        ///
        /// A head-less Rhino has no active document in the usual sense:
        /// <c>RhinoDoc.ActiveDoc</c> is per-thread, and set only on the thread that
        /// started Rhino. NUnit runs tests on its own threads, where it reads back null.
        /// </summary>
        public static Rhino.RhinoDoc HeadlessDoc { get; private set; }

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
        /// Loads Grasshopper into the head-less Rhino, which is Rhino.Testing's job but
        /// not something it can finish on Rhino 8.35.
        ///
        /// Its own loader asks Rhino for the plug-in object and then looks for
        /// <c>RunHeadless</c> on it with <c>GetMethod</c>. What comes back is an
        /// IDispatch wrapper - a plain <c>System.__ComObject</c>, not
        /// <c>GH_RhinoScriptInterface</c> - so the lookup finds nothing and it throws
        /// "Failed loading grasshopper (Headless)" with nothing else to go on. Late
        /// binding goes through IDispatch and starts Grasshopper exactly as intended.
        ///
        /// Hence LoadGrasshopper=false in Rhino.Testing.Configs.xml, with Eto and the
        /// RDK - which that setting would otherwise have pulled in - asked for by name.
        /// </summary>
        private void LoadGrasshopperHeadless()
        {
            var plugin = Path.GetFullPath(Path.Combine(
                Configs.RhinoSystemDir, @"..\Plug-ins\Grasshopper\GrasshopperPlugin.rhp"));

            if (!File.Exists(plugin))
                throw new FileNotFoundException("No Grasshopper next to the Rhino in Rhino.Testing.Configs.xml.", plugin);

            Guid id;
            var result = PlugIn.LoadPlugIn(plugin, out id);

            if (result != LoadPlugInResult.Success)
                throw new InvalidOperationException("Rhino would not load " + plugin + ": " + result + ".");

            var grasshopper = Rhino.RhinoApp.GetPlugInObject(id);

            if (grasshopper == null)
                throw new InvalidOperationException("Grasshopper loaded but handed back no plug-in object.");

            grasshopper.GetType().InvokeMember(
                "RunHeadless", BindingFlags.InvokeMethod, null, grasshopper, null);
        }

        /// <summary>
        /// The plug-in is built with TargetExt=.gha, and the CLR only ever probes for
        /// .dll and .exe - so a plain reference to a type in it never resolves on its own.
        /// A module initializer gets this in place before NUnit reflects over anything.
        ///
        /// Whatever Grasshopper has already loaded wins, so that a reference to a
        /// component type resolves to the plug-in on the canvas rather than quietly
        /// loading a second copy of it - which would take every component GUID twice
        /// over, and stop Grasshopper with a Component ID conflict.
        ///
        /// The Rhino SDK assemblies are a separate problem, and cannot be solved here:
        /// NUnit walks this assembly's types before any code in it runs. They are bound
        /// by codeBase instead - see BindRhinoSdkToInstalledRhino in the .csproj.
        /// </summary>
        [System.Runtime.CompilerServices.ModuleInitializer]
        public static void ResolvePluginAssembly()
        {
            AppDomain.CurrentDomain.AssemblyResolve += (sender, args) =>
            {
                var name = new AssemblyName(args.Name).Name;

                if (!string.Equals(name, "Alpaca4d.Gh", StringComparison.OrdinalIgnoreCase))
                    return null;

                foreach (var assembly in AppDomain.CurrentDomain.GetAssemblies())
                {
                    if (string.Equals(assembly.GetName().Name, name, StringComparison.OrdinalIgnoreCase))
                        return assembly;
                }

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
