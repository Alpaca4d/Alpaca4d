using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Types;

namespace Alpaca4d.Testing
{
    /// <summary>
    /// Drives a single Grasshopper component through one solution, without a canvas and
    /// without a document solution - see <see cref="Document"/> for the one document all
    /// harnesses share as context.
    ///
    /// <code>
    /// var result = ComponentHarness.For&lt;RectangleCS&gt;()
    ///                              .Set("Width", 0.4)
    ///                              .Set("Height", 0.8)
    ///                              .Solve();
    /// var section = result.Get&lt;Alpaca4d.Section.RectangleCS&gt;(0);
    /// </code>
    ///
    /// Inputs that are not set keep the default the component registered, which is
    /// exactly what a freshly placed component on the canvas would compute.
    /// </summary>
    public sealed class ComponentHarness
    {
        private static GH_Document _document;

        private readonly GH_Component _component;

        private ComponentHarness(GH_Component component)
        {
            _component = component;

            // Components are entitled to call OnPingDocument(); RunAnalysis, for one,
            // dereferences it to work out where to write the OpenSees input deck.
            // The document is only context - the harness still drives the solve itself.
            Document.AddObject(component, false);
        }

        public static ComponentHarness For<TComponent>() where TComponent : GH_Component, new()
        {
            return new ComponentHarness(new TComponent());
        }

        public static ComponentHarness For(Type componentType)
        {
            if (!typeof(GH_Component).IsAssignableFrom(componentType))
                throw new ArgumentException(componentType.FullName + " is not a GH_Component.", "componentType");

            return new ComponentHarness((GH_Component)Activator.CreateInstance(componentType));
        }

        public GH_Component Component
        {
            get { return _component; }
        }

        /// <summary>
        /// The one document every harness in the run shares, and the reason it is shared:
        /// a GH_Document subscribes four <see cref="Rhino.Display.DisplayPipeline"/>
        /// events in its constructor, and Grasshopper's own documentation says only
        /// Dispose disconnects them again. Those events are static, so an undisposed
        /// document is rooted for the life of the process - along with its scheduling
        /// timer, its components, and everything their outputs hold. A document per
        /// harness meant a hundred-odd of them per run, all still hooked into the native
        /// display pipeline when RhinoCore is torn down at the end.
        ///
        /// One document costs one handler set and is disposed deterministically, by
        /// <see cref="DisposeDocument"/>, before Rhino goes down. Components accumulate
        /// in it for the length of the run, which is the trade: cheap, and bounded by the
        /// number of components a run solves.
        /// </summary>
        public static GH_Document Document
        {
            get { return _document ?? (_document = new GH_Document()); }
        }

        /// <summary>
        /// Disposes the shared document. Called from SetupFixture's teardown, before
        /// Rhino itself is disposed - the display pipeline the document unhooks from
        /// belongs to Rhino, so the order matters.
        /// </summary>
        public static void DisposeDocument()
        {
            var document = _document;
            _document = null;

            if (document != null)
                document.Dispose();
        }

        /// <summary>
        /// Selects the evaluation unit of a switcher component (the drop-down Alpaca4d
        /// uses to fold several materials or sections into one component).
        /// </summary>
        public ComponentHarness SwitchTo(string unitName)
        {
            var switcher = _component as Alpaca4d.UIWidgets.GH_SwitcherComponent;
            if (switcher == null)
                throw new InvalidOperationException(_component.Name + " is not a switcher component.");

            switcher.SwitchUnit(unitName, recompute: false, recordEvent: false);

            if (switcher.ActiveUnit == null || switcher.ActiveUnit.Name != unitName)
                throw new ArgumentException(
                    "'" + unitName + "' is not one of the evaluation units of " + _component.Name + ": " +
                    string.Join(", ", switcher.EvalUnits.Select(u => "'" + u.Name + "'")), "unitName");

            return this;
        }

        public ComponentHarness Set(int index, params object[] values)
        {
            if (index < 0 || index >= _component.Params.Input.Count)
                throw new ArgumentOutOfRangeException("index",
                    _component.Name + " has " + _component.Params.Input.Count + " inputs, index " + index + " requested.");

            SetPersistentData(_component.Params.Input[index], values);
            return this;
        }

        /// <summary>Sets an input by parameter name or nickname (case-insensitive).</summary>
        public ComponentHarness Set(string nameOrNickname, params object[] values)
        {
            var index = IndexOfInput(nameOrNickname);
            if (index < 0)
                throw new ArgumentException(
                    _component.Name + " has no input '" + nameOrNickname + "'. Inputs: " +
                    string.Join(", ", _component.Params.Input.Select(p => "'" + p.Name + "' (" + p.NickName + ")")),
                    "nameOrNickname");

            return Set(index, values);
        }

        public SolveResult Solve()
        {
            _component.ClearData();
            _component.CollectData();
            _component.ComputeData();
            return new SolveResult(_component);
        }

        private int IndexOfInput(string nameOrNickname)
        {
            for (var i = 0; i < _component.Params.Input.Count; i++)
            {
                var param = _component.Params.Input[i];
                if (string.Equals(param.Name, nameOrNickname, StringComparison.OrdinalIgnoreCase) ||
                    string.Equals(param.NickName, nameOrNickname, StringComparison.OrdinalIgnoreCase))
                    return i;
            }

            return -1;
        }

        /// <summary>
        /// Pushes values into a parameter's persistent data - the same slot the canvas
        /// fills when you type a value straight into an input.
        /// GH_PersistentParam&lt;T&gt;.SetPersistentData(params object[]) does the goo
        /// conversion for us, but it is only reachable through the closed generic type.
        /// </summary>
        private static void SetPersistentData(IGH_Param param, object[] values)
        {
            var setter = param.GetType()
                .GetMethods(BindingFlags.Public | BindingFlags.Instance)
                .FirstOrDefault(m => m.Name == "SetPersistentData"
                                     && m.GetParameters().Length == 1
                                     && m.GetParameters()[0].ParameterType == typeof(object[]));

            if (setter == null)
                throw new NotSupportedException(
                    "Cannot pre-set input '" + param.Name + "' of type " + param.GetType().Name +
                    ": it is not a persistent parameter.");

            // SetPersistentData appends, and RegisterInputParams may already have stored a
            // default. Leaving both in place would make the component iterate twice.
            var persistent = param.GetType().GetProperty("PersistentData", BindingFlags.Public | BindingFlags.Instance);
            if (persistent != null)
            {
                var structure = persistent.GetValue(param, null);
                structure.GetType().GetMethod("Clear", Type.EmptyTypes).Invoke(structure, null);
            }

            setter.Invoke(param, new object[] { values });
        }
    }

    /// <summary>Outputs and runtime messages of a single component solution.</summary>
    public sealed class SolveResult
    {
        private readonly GH_Component _component;

        internal SolveResult(GH_Component component)
        {
            _component = component;
            Errors = component.RuntimeMessages(GH_RuntimeMessageLevel.Error).ToList();
            Warnings = component.RuntimeMessages(GH_RuntimeMessageLevel.Warning).ToList();
            Remarks = component.RuntimeMessages(GH_RuntimeMessageLevel.Remark).ToList();
        }

        public IReadOnlyList<string> Errors { get; private set; }
        public IReadOnlyList<string> Warnings { get; private set; }
        public IReadOnlyList<string> Remarks { get; private set; }

        /// <summary>All values on an output, unwrapped from their goo.</summary>
        public IReadOnlyList<object> All(int outputIndex)
        {
            var data = _component.Params.Output[outputIndex].VolatileData;
            return data.AllData(true).Select(Unwrap).ToList();
        }

        public IReadOnlyList<object> All(string nameOrNickname)
        {
            return All(IndexOfOutput(nameOrNickname));
        }

        /// <summary>The single value on an output; fails when the output is empty or a list.</summary>
        public T Get<T>(int outputIndex)
        {
            var values = All(outputIndex);
            if (values.Count != 1)
                throw new InvalidOperationException(
                    "Output " + outputIndex + " of " + _component.Name + " holds " + values.Count +
                    " items, expected exactly 1." + Describe());

            return Cast<T>(values[0], outputIndex);
        }

        public T Get<T>(string nameOrNickname)
        {
            return Get<T>(IndexOfOutput(nameOrNickname));
        }

        public IReadOnlyList<T> GetList<T>(int outputIndex)
        {
            return All(outputIndex).Select(v => Cast<T>(v, outputIndex)).ToList();
        }

        public IReadOnlyList<T> GetList<T>(string nameOrNickname)
        {
            return GetList<T>(IndexOfOutput(nameOrNickname));
        }

        /// <summary>
        /// An output's data tree, branch by branch. The result readers publish one branch
        /// per element, so this is how to tell elements apart.
        /// </summary>
        public IReadOnlyList<IReadOnlyList<object>> Branches(int outputIndex)
        {
            var data = _component.Params.Output[outputIndex].VolatileData;

            return data.Paths
                       .Select(path => (IReadOnlyList<object>)data.get_Branch(path)
                                                                  .Cast<IGH_Goo>()
                                                                  .Select(Unwrap)
                                                                  .ToList())
                       .ToList();
        }

        public IReadOnlyList<IReadOnlyList<object>> Branches(string nameOrNickname)
        {
            return Branches(IndexOfOutput(nameOrNickname));
        }

        public int Count(int outputIndex)
        {
            return _component.Params.Output[outputIndex].VolatileData.DataCount;
        }

        /// <summary>Multi-line dump of every message the component raised; handy in assertion text.</summary>
        public string Describe()
        {
            var lines = new List<string>();
            foreach (var e in Errors) lines.Add("  error:   " + e);
            foreach (var w in Warnings) lines.Add("  warning: " + w);
            foreach (var r in Remarks) lines.Add("  remark:  " + r);
            return lines.Count == 0
                ? Environment.NewLine + "  (no runtime messages)"
                : Environment.NewLine + string.Join(Environment.NewLine, lines);
        }

        private int IndexOfOutput(string nameOrNickname)
        {
            for (var i = 0; i < _component.Params.Output.Count; i++)
            {
                var param = _component.Params.Output[i];
                if (string.Equals(param.Name, nameOrNickname, StringComparison.OrdinalIgnoreCase) ||
                    string.Equals(param.NickName, nameOrNickname, StringComparison.OrdinalIgnoreCase))
                    return i;
            }

            throw new ArgumentException(
                _component.Name + " has no output '" + nameOrNickname + "'. Outputs: " +
                string.Join(", ", _component.Params.Output.Select(p => "'" + p.Name + "'")), "nameOrNickname");
        }

        private T Cast<T>(object value, int outputIndex)
        {
            if (value is T)
                return (T)value;

            if (value == null)
                throw new InvalidOperationException(
                    "Output " + outputIndex + " of " + _component.Name + " is null, expected " + typeof(T).Name + "." + Describe());

            throw new InvalidOperationException(
                "Output " + outputIndex + " of " + _component.Name + " is a " + value.GetType().FullName +
                ", expected " + typeof(T).FullName + "." + Describe());
        }

        private static object Unwrap(IGH_Goo goo)
        {
            if (goo == null)
                return null;

            var wrapper = goo as GH_ObjectWrapper;
            if (wrapper != null)
                return wrapper.Value;

            // ScriptVariable() is what a GhPython/C# component would receive.
            return goo.ScriptVariable();
        }
    }
}
