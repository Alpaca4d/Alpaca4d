using Grasshopper;
using Grasshopper.Kernel;
using System.Collections.Generic;
using System.Linq;

namespace Alpaca4d.Gh
{
    /// <summary>
    /// The shared half of the History toggle on the result components: which steps a
    /// component should read, and where each step's data lands once it has read them.
    ///
    /// History off is the single step the user asked for and the output shape the
    /// component has always had. History on is every step the recorder wrote, with the
    /// step number pushed in front of whatever path the single-step result uses - so a
    /// beam force that reads {element} for one step reads {step; element} for a history.
    /// </summary>
    internal static class HistorySteps
    {
        /// <summary>
        /// The steps to read, or null when the component should give up - in which case a
        /// runtime message has already been put on it saying why.
        /// </summary>
        public static IEnumerable<int> Of(Alpaca4d.Model model, bool history, int step, GH_Component component)
        {
            if (!history)
                return new[] { step };

            // A modal run writes one step holding every mode, so walking steps would read
            // the same mode over and over. Modes are stepped through with Step instead.
            if (model.IsModal)
            {
                component.AddRuntimeMessage(GH_RuntimeMessageLevel.Warning,
                    "History does not apply to a modal analysis - its results are modes, not steps. " +
                    "Reading the single Step instead.");
                return new[] { step };
            }

            int count = Alpaca4d.Result.Read.StepCount(model);
            if (count <= 0)
            {
                component.AddRuntimeMessage(GH_RuntimeMessageLevel.Error,
                    "No recorded steps were found. Run the analysis before reading a history.");
                return null;
            }

            return Enumerable.Range(0, count);
        }

        /// <summary>
        /// Adds one step's tree to the tree being handed to the output, prefixing the path
        /// with the step number only when a history is being built.
        /// </summary>
        public static void Collect(DataTree<object> destination, DataTree<object> stepTree, int step, bool history)
        {
            if (history)
                Utils.AddStepToHistory(destination, stepTree, step);
            else
                destination.MergeTree(stepTree);
        }
    }
}
