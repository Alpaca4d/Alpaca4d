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
            "Construct a reinforcing bar material (OpenSees ReinforcingSteel).\nStresses in kN/m2, strains dimensionless.",
            "Alpaca4d", "MomentCurvature_βeta")
        {
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            var preset = Alpaca4d.Material.ReinforcingSteel.B450C;

            pManager.AddTextParameter("Material Name", "MatName", "Material name.", GH_ParamAccess.item, preset.MatName);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fy", "fy", "Yield strength, in kN/m2.", GH_ParamAccess.item, preset.Fy);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fu", "fu", "Ultimate strength, in kN/m2.", GH_ParamAccess.item, preset.Fu);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("Es", "Es", "Initial elastic modulus, in kN/m2.", GH_ParamAccess.item, preset.Es);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("Esh", "Esh",
                "Tangent modulus at the onset of strain hardening, in kN/m2. Greater than zero.",
                GH_ParamAccess.item, preset.Esh);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("esh", "esh",
                "Strain at the onset of strain hardening, dimensionless. Past the yield strain fy/Es.",
                GH_ParamAccess.item, preset.EpsilonSh);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("eult", "eult", "Strain at fu, dimensionless.", GH_ParamAccess.item, preset.EpsilonUlt);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddBooleanParameter("MinMax", "MinMax",
                "Wrap the material so a bar fails once its strain passes eult in either direction.",
                GH_ParamAccess.item, false);
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
            // The registered defaults above are what these are; the fallbacks here only
            // matter if a wire is connected and carries nothing.
            var preset = Alpaca4d.Material.ReinforcingSteel.B450C;

            string matName = preset.MatName;
            double fy = preset.Fy;
            double fu = preset.Fu;
            double es = preset.Es;
            double esh = preset.Esh;
            double epsilonSh = preset.EpsilonSh;
            double epsilonUlt = preset.EpsilonUlt;
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