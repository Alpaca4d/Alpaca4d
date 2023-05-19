using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Alpaca4d.Generic;
using Alpaca4d;

namespace Alpaca4d.Gh
{
    public class PlateFiberSection : GH_Component
    {
        public PlateFiberSection()
          : base("Plate Fiber Section (Alpaca4d)", "PFS",
            "Construct an Plate Fiber Section",
            "Alpaca4d", "01_Section")
        {
            // Draw a Description Underneath the component
            this.Message = $"Plate Fiber Section\n(Alpaca4d";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("SectionName", "SecName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Thickness", "Thickness", "", GH_ParamAccess.item, 0.15);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Section", "Section", "");

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
            double thickness = 0.15;

            IMultiDimensionMaterial material = new Alpaca4d.Material.ElasticIsotropicMaterial(null, 2.1e11, 8.076e10, 0.3, 78500);


            DA.GetData(0, ref secName);
            DA.GetData(1, ref thickness);
            if (!DA.GetData(2, ref material)) { return; };


            var section = new Alpaca4d.Section.PlateFiberSection(secName, thickness, material);

            DA.SetData(0, section);
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.secondary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Fiber_section__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{d54fadef-3e36-492c-9241-4e9b8f48ee26}");
    }
}