using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

namespace Alpaca4d.Gh
{
    public class ElasticIsotropicMaterial : GH_Component
    {
        public ElasticIsotropicMaterial()
          : base("Elastic Isotropic Material (Alpaca4d)", "EIM",
            "Construct an ElasticIsotropicMaterial",
            "Alpaca4d", "00_Material")
        {
            this.Message = "ElasticIsotropicMaterial\n(Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Material Name", "MatName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("E", "E", "Young Modulus", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("G", "G", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("v", "v", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Rho", "Rho", "", GH_ParamAccess.item);
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
            double g = 8.076e10;
            double v = 0.3;
            double rho = 78500;


            DA.GetData(0, ref matName);
            DA.GetData(1, ref e);

            DA.GetData(2, ref g);
            DA.GetData(3, ref v);

            DA.GetData(4, ref rho);


            var material = new Alpaca4d.Material.ElasticIsotropicMaterial(matName, e, g, v, rho);


            DA.SetData(0, material);

        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.secondary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Elastic_Isotropic_Material__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{7D150634-C4D9-473E-AEC2-935CF385C699}");
    }
}