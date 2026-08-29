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
    public class ReactionForce : GH_Component
    {
        public ReactionForce()
          : base("Reaction Forces (Alpaca4d)", "Reaction Forces",
            "Read Reaction Forces",
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
            pManager.Register_VectorParam("ReactionForce", "ReactionForce",
                $"[{Units.Force}] in the support's own axes. For a support placed on a Point " +
                "those are the global axes; for one placed on a Plane they are the plane's.");
            pManager.Register_VectorParam("ReactionMoment", "ReactionMoment",
                $"[{Units.Force}{Units.Length}] in the support's own axes.");
            pManager.Register_PlaneParam("SupportPlane", "SupportPlane",
                "The axes the reactions above are given in, one per support.");
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

            // A skewed support carries its fix on a coincident auxiliary node, so that is
            // where OpenSees puts the reaction; the support node itself reads zero. An
            // axis-aligned support has no auxiliary node and is read where it always was.
            var nodes = alpacaModel.Supports.Select(x => x.AuxiliaryNodeId ?? x.Id).ToList();

            var globalForce = Result.Read.NodalOutput(alpacaModel, step, ResultType.REACTION_FORCE, nodes).ToList();
            var globalMoment = Result.Read.NodalOutput(alpacaModel, step, ResultType.REACTION_MOMENT, nodes).ToList();

            // Reactions come out of the recorder in global components whatever the
            // support is turned to, which for a skewed one spreads a reaction that runs
            // along a single local axis across all three global ones. Resolving them onto
            // the support's own axes is what makes a released direction read as the zero
            // it is.
            var planes = alpacaModel.Supports.Select(x => x.Plane).ToList();
            var localForce = globalForce.Select((vector, i) => InAxesOf(vector, planes[i])).ToList();
            var localMoment = globalMoment.Select((vector, i) => InAxesOf(vector, planes[i])).ToList();

            // Finally assign the spiral to the output parameter.
            DA.SetDataList(0, alpacaModel.Supports.Select(x => x.Pos).ToList());
            DA.SetDataList(1, localForce);
            DA.SetDataList(2, localMoment);
            DA.SetDataList(3, planes);
        }

        private static Vector3d InAxesOf(Vector3d vector, Plane frame)
        {
            return new Vector3d(vector * frame.XAxis, vector * frame.YAxis, vector * frame.ZAxis);
        }


        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Reaction_Forces__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{C86DB16F-84D1-4EF6-80CD-860B0F0B5A7D}");
    }
}