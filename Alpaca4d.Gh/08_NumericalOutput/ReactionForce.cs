using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Linq;
using System.Collections.Generic;

using HDF5CSharp;
using HDF5CSharp.DataTypes;
using Alpaca4d.Generic;
using Alpaca4d.Result;

namespace Alpaca4d.Gh
{
    public class ReactionForce : GH_Component
    {
        public ReactionForce()
          : base("Reaction Forces (Alpaca4d)", "RF",
            "Read Reaction Forces",
            "Alpaca4d", "08_NumericalOutput")
        {
            // Draw a Description Underneath the component
            this.Message = "Reaction Force (Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "", GH_ParamAccess.item);
            pManager.AddBooleanParameter("History", "History", "not implemented", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Step", "Step", "", GH_ParamAccess.item, 0);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("SupportPosition", "SupportPosition", "");
            pManager.Register_VectorParam("ReactionForce", "ReactionForce", "");
            pManager.Register_VectorParam("ReactionMoment", "ReactionMoment", "");
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

            var reactionForce = Result.Read.NodalOutput(alpacaModel, step, ResultType.REACTION_FORCE, alpacaModel.Supports.Select(x => x.Id).ToList());
            var reactionMoment = Result.Read.NodalOutput(alpacaModel, step, ResultType.REACTION_MOMENT, alpacaModel.Supports.Select(x => x.Id).ToList());
            // Finally assign the spiral to the output parameter.
            DA.SetDataList(0, alpacaModel.Supports.Select(x => x.Pos).ToList());
            DA.SetDataList(1, reactionForce);
            DA.SetDataList(2, reactionMoment);
        }


        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Reaction_Forces__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{C86DB16F-84D1-4EF6-80CD-860B0F0B5A7D}");
    }
}