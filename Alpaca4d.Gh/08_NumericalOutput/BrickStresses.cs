using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Linq;
using System.Collections.Generic;

using Alpaca4d.Generic;
using Alpaca4d.Result;

namespace Alpaca4d.Gh
{
    public class BrickStress : GH_Component
    {
        public BrickStress()
          : base("Brick Stresses (Alpaca4d)", "Brick Stresses",
            "Read the Brick Stresses",
            "Alpaca4d", "08_NumericalOutput")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "", GH_ParamAccess.item);
            pManager.AddBooleanParameter("History", "History",
                "Read every recorded step instead of one. Each output then becomes a tree with " +
                "one branch per step, {step}, holding that step's value per element. Step is ignored.",
                GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Step", "Step", "Which recorded step to read.", GH_ParamAccess.item, 0);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Sigma11", "σ₁₁", "");
            pManager.Register_GenericParam("Sigma22", "σ₂₂", "");
            pManager.Register_GenericParam("Sigma33", "σ₃₃", "");
            pManager.Register_GenericParam("Sigma12", "σ₁₂", "");
            pManager.Register_GenericParam("Sigma23", "σ₂₃", "");
            pManager.Register_GenericParam("Sigma13", "σ₁₃", "");
            pManager.Register_DoubleParam("VonMises", "VonMises", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var alpacaModel = new Alpaca4d.Model();
            bool history = false;
            int step = 0;

            if (!DA.GetData(0, ref alpacaModel)) return;
            DA.GetData(1, ref history);
            DA.GetData(2, ref step);

            var steps = HistorySteps.Of(alpacaModel, history, step, this);
            if (steps == null) return;

            // Six components plus von Mises, in the output order.
            var outputs = Enumerable.Range(0, 7).Select(_ => new DataTree<double>()).ToArray();

            foreach (int current in steps)
            {
                var stresses = StressesAt(alpacaModel, current);
                for (int i = 0; i < outputs.Length; i++)
                    outputs[i].AddRange(stresses[i], new Grasshopper.Kernel.Data.GH_Path(current));
            }

            // Finally assign the spiral to the output parameter.
            for (int i = 0; i < outputs.Length; i++)
            {
                // A single step keeps the flat list it has always been; a history is a tree
                // with one branch per step.
                if (history)
                    DA.SetDataTree(i, outputs[i]);
                else
                    DA.SetDataList(i, outputs[i].AllData());
            }
        }

        /// <summary>
        /// The six stress components and von Mises at one step, in the order the outputs are
        /// registered, each holding one value per brick.
        /// </summary>
        private static List<double>[] StressesAt(Alpaca4d.Model alpacaModel, int step)
        {
            List<double> tetraSigma11 = new List<double>();
            List<double> tetraSigma22 = new List<double>();
            List<double> tetraSigma33 = new List<double>();
            List<double> tetraSigma12 = new List<double>();
            List<double> tetraSigma23 = new List<double>();
            List<double> tetraSigma13 = new List<double>();

            List<double> sspSigma11 = new List<double>();
            List<double> sspSigma22 = new List<double>();
            List<double> sspSigma33 = new List<double>();
            List<double> sspSigma12 = new List<double>();
            List<double> sspSigma23 = new List<double>();
            List<double> sspSigma13 = new List<double>();

            if (alpacaModel.HasTetrahedron)
            {
                (tetraSigma11, tetraSigma22, tetraSigma33, tetraSigma12, tetraSigma23, tetraSigma13) = Alpaca4d.Result.Read.TetrahedronStress(alpacaModel, step);
            }
            if (alpacaModel.HasSSpBrick)
            {
                (sspSigma11, sspSigma22, sspSigma33, sspSigma12, sspSigma23, sspSigma13) = Alpaca4d.Result.Read.SSPBrickStress(alpacaModel, step);
            }


            var ids = alpacaModel.Bricks.Select(d => d.Id).ToList();

            var sigma11 = tetraSigma11.Concat(sspSigma11).OrderBy(i => ids).ToList();
            var sigma22 = tetraSigma22.Concat(sspSigma22).OrderBy(i => ids).ToList();
            var sigma33 = tetraSigma33.Concat(sspSigma33).OrderBy(i => ids).ToList();
            var sigma12 = tetraSigma12.Concat(sspSigma12).OrderBy(i => ids).ToList();
            var sigma23 = tetraSigma23.Concat(sspSigma23).OrderBy(i => ids).ToList();
            var sigma13 = tetraSigma13.Concat(sspSigma13).OrderBy(i => ids).ToList();

            // Calculate Con Mises stress

            List<double> vonMises = new List<double>();
            
            for (int i = 0; i < sigma11.Count(); i++) 
            {
                double _vonMises = Math.Sqrt(
                0.5 * ((sigma11[i] - sigma22[i]) * (sigma11[i] - sigma22[i]) +
                       (sigma22[i] - sigma33[i]) * (sigma22[i] - sigma33[i]) +
                       (sigma33[i] - sigma11[i]) * (sigma33[i] - sigma11[i]) +
                       6.0 * (sigma12[i] * sigma12[i] + sigma23[i] * sigma23[i] + sigma13[i] * sigma13[i]))
                );

                vonMises.Add(_vonMises);
            }

            return new[] { sigma11, sigma22, sigma33, sigma12, sigma23, sigma13, vonMises };
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.quarternary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Brick_Stresses__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{DF03EC57-E1FA-4A3D-82BB-7F65526CF0B6}");
    }
}