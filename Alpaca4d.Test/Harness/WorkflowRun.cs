using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using NUnit.Framework;
using Rhino.Geometry;

namespace Alpaca4d.Testing
{
    /// <summary>
    /// Runs a whole Alpaca4d chain the way a canvas would: each component is solved, its
    /// single output handed to the next, and every step recorded so a failure can name
    /// the component that caused it and print the solver log beside it.
    ///
    /// The run owns a temporary working directory, because RunAnalysis writes the
    /// OpenSees input deck and recorder file relative to the current directory - which is
    /// also why fixtures using this must be [NonParallelizable].
    /// </summary>
    public sealed class WorkflowRun : IDisposable
    {
        private readonly List<Step> _steps = new List<Step>();
        private readonly string _workingDirectory;
        private readonly string _previousDirectory;
        private bool _disposed;

        private WorkflowRun()
        {
            _previousDirectory = Directory.GetCurrentDirectory();
            _workingDirectory = Path.Combine(Path.GetTempPath(), "alpaca4d-test-" + Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(_workingDirectory);
            Directory.SetCurrentDirectory(_workingDirectory);
        }

        public static WorkflowRun Begin()
        {
            // Before the constructor, not after. Without a bundled solver this calls
            // Assert.Ignore, which throws: anything the constructor had already done
            // would belong to a run the caller never receives and so can never dispose -
            // and the working directory it changes is the whole process's.
            OpenSees.UseBundledSolver();

            return new WorkflowRun();
        }

        public void Dispose()
        {
            if (_disposed)
                return;

            _disposed = true;

            Directory.SetCurrentDirectory(_previousDirectory);

            // Best-effort: a solver that is still writing, or a virus scanner holding a
            // recorder file open, must not fail the test that just passed.
            try { Directory.Delete(_workingDirectory, true); }
            catch (IOException) { }
            catch (UnauthorizedAccessException) { }
        }

        /// <summary>The OpenSees console output of the last <see cref="Analyse"/>.</summary>
        public string Log { get; private set; }

        /// <summary>The model RunAnalysis returned, or null if the solver failed.</summary>
        public Alpaca4d.Model AnalysedModel { get; private set; }

        public IReadOnlyList<Vector3d> Displacements { get; private set; }

        public IReadOnlyList<Step> Steps { get { return _steps; } }

        /// <summary>Solves a component and returns its single output, ready to wire onwards.</summary>
        public object Solve(string name, ComponentHarness harness)
        {
            var outputs = SolveMany(name, harness);

            Assert.That(outputs, Has.Count.EqualTo(1),
                name + " produced " + outputs.Count + " outputs instead of 1." + ResultOf(name).Describe());

            return outputs[0];
        }

        /// <summary>Solves a component whose output is a list, such as a meshed shell.</summary>
        public IReadOnlyList<object> SolveMany(string name, ComponentHarness harness)
        {
            var result = harness.Solve();
            _steps.Add(new Step { Name = name, Result = result });
            return result.All(0);
        }

        public SolveResult ResultOf(string name)
        {
            var step = _steps.LastOrDefault(s => s.Name == name);

            if (step == null)
                throw new InvalidOperationException(
                    "The chain stopped before '" + name + "'. Steps so far: " +
                    string.Join(", ", _steps.Select(s => s.Name)) + Environment.NewLine + Log);

            return step.Result;
        }

        /// <summary>Every component that reported an error, formatted for an assertion message.</summary>
        public IReadOnlyList<string> Complaints()
        {
            return _steps
                .Where(s => s.Result.Errors.Count > 0)
                .Select(s => s.Name + ":" + s.Result.Describe())
                .ToList();
        }

        /// <summary>Runs the solver on an assembled model and reads the nodal displacements back.</summary>
        public void Analyse(object model, object settings)
        {
            var analysis = ComponentHarness.For<Alpaca4d.Gh.RunAnalysis>()
                                           .Set("AlpacaModel", model)
                                           .Set("Settings", settings)
                                           .Solve();

            _steps.Add(new Step { Name = "RunAnalysis", Result = analysis });
            Log = analysis.All(0).FirstOrDefault() as string;
            AnalysedModel = analysis.All(1).FirstOrDefault() as Alpaca4d.Model;

            if (AnalysedModel == null)
                return;

            var displacements = ComponentHarness.For<Alpaca4d.Gh.NodalDisplacement>()
                                                .Set("AlpacaModel", AnalysedModel)
                                                .Solve();

            _steps.Add(new Step { Name = "NodalDisplacement", Result = displacements });
            Displacements = displacements.GetList<Vector3d>(0);
        }

        /// <summary>Nodal results come back in model node order, so match on position.</summary>
        public Vector3d DisplacementAt(Point3d position)
        {
            Assert.That(Displacements, Is.Not.Null, "The analysis produced no displacements." + Environment.NewLine + Log);

            for (var i = 0; i < AnalysedModel.Nodes.Count; i++)
            {
                if (AnalysedModel.Nodes[i].Pos.DistanceTo(position) < 1e-9)
                    return Displacements[i];
            }

            throw new AssertionException("The model has no node at " + position);
        }

        public sealed class Step
        {
            public string Name { get; set; }
            public SolveResult Result { get; set; }
        }
    }
}
