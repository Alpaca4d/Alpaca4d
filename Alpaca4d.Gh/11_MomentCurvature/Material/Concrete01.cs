using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

namespace Alpaca4d.Gh
{
    public class Concrete01 : GH_Component
    {
        public Concrete01()
          : base("Concrete01 (Alpaca4d)", "Concrete",
            "Construct a concrete material with zero tensile strength (OpenSees Concrete01).\nStresses in kN/m2, strains dimensionless, compression negative.",
            "Alpaca4d", "MomentCurvature_βeta")
        {
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            var preset = Alpaca4d.Material.Concrete01.C2530;

            pManager.AddTextParameter("Material Name", "MatName", "Material name.", GH_ParamAccess.item, preset.MatName);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fco", "fco",
                "Compressive strength, in kN/m2. Negative, as every stress and strain in Concrete01 is.",
                GH_ParamAccess.item, preset.FpCo);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fcu", "fcu",
                "Crushing strength, in kN/m2 - what is left at EpsilonCu, past the peak. Negative, and no larger in magnitude than fco.",
                GH_ParamAccess.item, preset.FpCu);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("EpsilonCo", "EpsilonCo",
                "Strain at fco. Negative, dimensionless.",
                GH_ParamAccess.item, preset.EpsilonCo);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("EpsilonCu", "EpsilonCu",
                "Strain at fcu. Negative, dimensionless.",
                GH_ParamAccess.item, preset.EpsilonCu);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddBooleanParameter("MinMax", "MinMax",
                "Wrap the material so a fibre fails once its strain leaves the range between EpsilonCu and zero.",
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
            var preset = Alpaca4d.Material.Concrete01.C2530;

            string matName = preset.MatName;
            double fpco = preset.FpCo;
            double fpcu = preset.FpCu;
            double epsilonc0 = preset.EpsilonCo;
            double epsilonCu = preset.EpsilonCu;
            bool minMax = false;


            DA.GetData(0, ref matName);
            DA.GetData(1, ref fpco);
            DA.GetData(2, ref fpcu);
            DA.GetData(3, ref epsilonc0);
            DA.GetData(4, ref epsilonCu);
            DA.GetData(5, ref minMax);


            var material = new Alpaca4d.Material.Concrete01(matName, fpco, fpcu, epsilonc0, epsilonCu, minMax);


            DA.SetData(0, material);

        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.concreate01;

        public override Guid ComponentGuid => new Guid("{57BF0FDB-B333-491C-B9EB-50783029B8C2}");
    }
}