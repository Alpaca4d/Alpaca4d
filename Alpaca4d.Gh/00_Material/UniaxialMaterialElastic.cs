using Alpaca4d;
using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

namespace Alpaca4d.Gh
{
    public class UniaxialMaterialElastic : GH_Component
    {
        public UniaxialMaterialElastic()
          : base("Uniaxial Material Elastic (Alpaca4d)", "Uniaxial Material Elastic",
            "Construct an UniaxialMaterialElastic",
            "Alpaca4d", "00_Material")
        {
            this.Message = $"{this.NickName} \n{this.Category}";
        }

        public override IEnumerable<string> Keywords => new string[] { "ume" };


        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Material Name", "MatName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("E", "E", $"Young Modulus {Units.Force}/{Units.Length}²", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("Eneg", "Eneg", $"{Units.Force}/{Units.Length}²", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("Eta", "Eta", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("G", "G", $"{Units.Force}/{Units.Length}²", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("v", "v", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("Rho", "Rho", "Unit Mass - Density [MASS/VOLUME]", GH_ParamAccess.item);
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
            double e = 2.1e11;
            double eNeg = 2.1e11;
            double eta = 0.00;
            double g = 8.076e10;
            double v = 0.3;
            double rho = 78500;


            DA.GetData(0, ref matName);
            DA.GetData(1, ref e);
            DA.GetData(2, ref eNeg);
            DA.GetData(3, ref eta);
            DA.GetData(4, ref g);
            DA.GetData(5, ref v);
            DA.GetData(6, ref rho);


            var material = new Alpaca4d.Material.UniaxialMaterialElastic(matName, e, eNeg, eta, g, v, rho);


            DA.SetData(0, material);

        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.primary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.uniaxial_Elastic_Material__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("ED47A274-2253-4F3F-9C1C-C0DAF377E093");
    }
}