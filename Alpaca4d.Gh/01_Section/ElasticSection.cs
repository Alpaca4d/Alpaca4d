using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Alpaca4d.Generic;
using Alpaca4d;

namespace Alpaca4d.Gh
{
    public class ElasticSection : GH_Component
    {
        public ElasticSection()
          : base("Generic Section (Alpaca4d)", "Generic Section",
            "Construct an Generic Section",
            "Alpaca4d", "01_Section")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("SectionName", "SecName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Area", "A", "Young Modulus", GH_ParamAccess.item);
            pManager.AddNumberParameter("Izz", "Izz", "", GH_ParamAccess.item);
            pManager.AddNumberParameter("Iyy", "Iyy", "", GH_ParamAccess.item);
            pManager.AddNumberParameter("J", "J", "", GH_ParamAccess.item);
            pManager.AddNumberParameter("AlphaY", "AlphaY", "", GH_ParamAccess.item);
            pManager.AddNumberParameter("AlphaZ", "AlphaZ", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Section", "Section", "Section");

        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            // Input
            string secName = "";
            double area = 0.00;
            double iZZ = 0.00;
            double iYY = 0.00;
            double j = 0.00;
            double alphaY = 0.00;
            double alphaZ = 0.00;
            IUniaxialMaterial material = Alpaca4d.Material.UniaxialMaterialElastic.Steel;


            DA.GetData(0, ref secName);
            if (!DA.GetData(1, ref area)) return;
            if (!DA.GetData(2, ref iZZ)) return;
            if (!DA.GetData(3, ref iYY)) return;
            if (!DA.GetData(4, ref j)) return;
            if (!DA.GetData(5, ref alphaY)) return;
            if (!DA.GetData(6, ref alphaZ)) return;
            DA.GetData(7, ref material);


            var section = new Alpaca4d.Section.ElasticSection(secName, area, iZZ, iYY, j, alphaY, alphaZ, material);

            DA.SetData(0, section);
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
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Generic_Section__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("A1CB6DF1-6E45-4D64-9F17-FC1D8E4211AB");
    }
}