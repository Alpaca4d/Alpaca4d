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
            // Rhino is up the moment this returns, and from here on every exit from this
            // method has to take it down again - see OneTimeTearDown for what a Rhino
            // nobody owns costs.
            base.OneTimeSetup();

            try
            {
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

                // Nothing is watching this run, so a solver that hangs must not be able to
                // hold it open; see Application.OpenSeesTimeout. Generous on purpose - the
                // workflow fixtures solve in about a second, so anything near this is a
                // solver that is never coming back.
                Alpaca4d.Application.OpenSeesTimeout = TimeSpan.FromMinutes(10);
            }
            catch
            {
                base.OneTimeTearDown();
                throw;
            }
        }

        /// <summary>
        /// Takes the head-less Rhino down again, innermost first.
        ///
        /// The order is the point. The shared GH_Document holds handlers on Rhino's
        /// static DisplayPipeline, which is backed by native callbacks; disposing
        /// RhinoCore while they are still attached tears the native side out from under
        /// them. That is how a test host ends up half-exited - every managed thread gone,
        /// one thread stuck in native shutdown, the process still holding every file it
        /// had loaded until someone terminates it by hand.
        ///
        /// Grasshopper itself is not shut down here because it cannot be: Rhino has no
        /// API to unload a plug-in, so the RunHeadless started in OneTimeSetup lives
        /// until the process does. TestSessionTimeout in .runsettings is the backstop
        /// for the case where it does not.
        /// </summary>
        public override void OneTimeTearDown()
        {
            ComponentHarness.DisposeDocument();
            base.OneTimeTearDown();
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

            // Between loading the plug-in and starting it: the assembly is in the
            // AppDomain, so GH_ComponentServer resolves, and the library scan has not run.
            RestrictPluginsToAlpaca4d();

            grasshopper.GetType().InvokeMember(
                "RunHeadless", BindingFlags.InvokeMethod, null, grasshopper, null);
        }

        /// <summary>
        /// Narrows Grasshopper's start-up scan to its own component libraries plus
        /// Alpaca4d, leaving every other installed plug-in on disk untouched and unloaded.
        ///
        /// Starting Grasshopper normally loads every .gha it can find - the user's
        /// Libraries folder and every Rhino package. That is someone else's code running
        /// in the test host, and some of it phones home: Karamba3D opens HTTPS
        /// connections for a licence check during load, and when that call does not come
        /// back neither does the test run. The host is left alive holding every assembly
        /// it had loaded, the Grasshopper libraries folder included, so the next build
        /// cannot copy over them either. None of those plug-ins have anything to do with
        /// Alpaca4d.
        ///
        /// GH_ComponentServer.SetExternalGHAs is Grasshopper's own answer to this -
        /// "specify a subset of components to load in order to reduce start time", as its
        /// summary puts it. It is internal and marked work-in-progress, hence the
        /// reflection and the soft landing: if a future Grasshopper drops it the run still
        /// works, it just loads everything again.
        ///
        /// The filter matches by path suffix and applies to the whole scan, so
        /// Grasshopper's own libraries have to be named too or the standard components
        /// disappear with the rest.
        /// </summary>
        private static void RestrictPluginsToAlpaca4d()
        {
            var setExternalGHAs = typeof(Grasshopper.Kernel.GH_ComponentServer).GetMethod(
                "SetExternalGHAs", BindingFlags.Static | BindingFlags.NonPublic);

            if (setExternalGHAs == null)
            {
                TestContext.WriteLine(
                    "GH_ComponentServer.SetExternalGHAs is gone from this Grasshopper; " +
                    "loading every installed plug-in, which is slower and can hang on a " +
                    "third-party licence check. See RestrictPluginsToAlpaca4d.");
                return;
            }

            var allowed = new List<string>();

            // Grasshopper's own component libraries, in Components next to Grasshopper.dll.
            var components = Path.Combine(
                Path.GetDirectoryName(typeof(Grasshopper.Kernel.GH_Component).Assembly.Location),
                "Components");

            if (Directory.Exists(components))
                allowed.AddRange(Directory.GetFiles(components, "*.gha"));

            // Whichever copy of the plug-in is deployed - matched as a suffix, so this is
            // the libraries folder copy without having to work out where that is. If none
            // is deployed nothing matches, PluginIsLoaded stays false, and OneTimeSetup
            // falls back to the copy next to the test assembly.
            allowed.Add(Path.DirectorySeparatorChar + "Alpaca4d.Gh.gha");

            setExternalGHAs.Invoke(null, new object[] { allowed });

            TestContext.WriteLine(
                "Grasshopper plug-in scan restricted to " + allowed.Count + " entries (Alpaca4d and Grasshopper's own).");
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
