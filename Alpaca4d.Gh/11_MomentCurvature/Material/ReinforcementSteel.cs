using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

namespace Alpaca4d.Gh
{
    public class ReinforcingSteel : GH_Component
    {
        public ReinforcingSteel()
          : base("ReinforcingSteel (Alpaca4d)", "ReinforcingSteel",
            "Construct an ReinforcingSteel",
            "Alpaca4d", "MomentCurvature")
        {
            this.Message = $"{this.Name}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Material Name", "MatName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fy", "fy", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fu", "fu", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("Es", "Es", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("Esh", "Esh", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("esh", "esh", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("eult", "eult", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddBooleanParameter("MinMax", "MinMax", "", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;


        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Material", "Material", "Material");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            string matName = null;
            double fy = 319.300;
            double fu = 469.560;
            double es = 200000;
            double esh = 0.0;
            double epsilonSh = 0.001957;
            double epsilonUlt = 0.0675;
            bool minMax = false;


            DA.GetData(0, ref matName);
            DA.GetData(1, ref fy);
            DA.GetData(2, ref fu);
            DA.GetData(3, ref es);
            DA.GetData(4, ref esh);
            DA.GetData(5, ref epsilonSh);
            DA.GetData(6, ref epsilonUlt);
            DA.GetData(7, ref minMax);


            var material = new Alpaca4d.Material.ReinforcingSteel(matName, fy, fu, es, esh, epsilonSh, epsilonUlt, minMax);


            DA.SetData(0, material);

        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.reinforcing_steel_material;

        public override Guid ComponentGuid => new Guid("{47B04CA7-0F7E-4585-8F89-D31592E61394}");
    }
}