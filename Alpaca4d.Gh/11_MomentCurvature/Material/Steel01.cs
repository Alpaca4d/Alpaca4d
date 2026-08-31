using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

namespace Alpaca4d.Gh
{
    public class Steel01 : GH_Component
    {
        public Steel01()
          : base("Steel01 (Alpaca4d)", "Steel01",
            "Construct a bilinear steel material with kinematic hardening (OpenSees Steel01).\nStresses in kN/m2, strains dimensionless.",
            "Alpaca4d", "MomentCurvature_βeta")
        {
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            var preset = Alpaca4d.Material.Steel01.S355;

            pManager.AddTextParameter("Material Name", "MatName", "Material name.", GH_ParamAccess.item, preset.MatName);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fy", "fy", "Yield strength, in kN/m2.", GH_ParamAccess.item, preset.Fy);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("E0", "E0", "Initial elastic modulus, in kN/m2.", GH_ParamAccess.item, preset.E0);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("b", "b",
                "Strain-hardening ratio, dimensionless: the post-yield tangent over E0.",
                GH_ParamAccess.item, preset.b);
            pManager[pManager.ParamCount - 1].Optional = true;

            // The four isotropic hardening parameters are one optional group, and OpenSees
            // takes them together or not at all - so they are left empty rather than
            // defaulted, and Steel01 rejects a half-filled set.
            pManager.AddNumberParameter("a1", "a1", "Isotropic hardening in compression, dimensionless. Give a1-a4 together or leave all four empty.", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("a2", "a2", "Compression hardening limit, dimensionless. Give a1-a4 together or leave all four empty.", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("a3", "a3", "Isotropic hardening in tension, dimensionless. Give a1-a4 together or leave all four empty.", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("a4", "a4", "Tension hardening limit, dimensionless. Give a1-a4 together or leave all four empty.", GH_ParamAccess.item);
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
            var preset = Alpaca4d.Material.Steel01.S355;

            string matName = preset.MatName;
            double fy = preset.Fy;
            double e0 = preset.E0;
            double b = preset.b;
            double? a1 = null;
            double? a2 = null;
            double? a3 = null;
            double? a4 = null;


            DA.GetData(0, ref matName);
            DA.GetData(1, ref fy);
            DA.GetData(2, ref e0);
            DA.GetData(3, ref b);
            DA.GetData(4, ref a1);
            DA.GetData(5, ref a2);
            DA.GetData(6, ref a3);
            DA.GetData(7, ref a4);


            var material = new Alpaca4d.Material.Steel01(matName, fy, e0, b, a1, a2, a3, a4);


            DA.SetData(0, material);
        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Uniaxial_Material_steal01;

        public override Guid ComponentGuid => new Guid("{DEB86811-4429-426F-8A7B-02DF89C5A074}");
    }
}