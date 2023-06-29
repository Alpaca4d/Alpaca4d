using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Alpaca4d.Generic;
using Alpaca4d;

namespace Alpaca4d.Gh
{
    public class RectangleCS : GH_Component
    {
        public RectangleCS()
          : base("RectangleCS (Alpaca4d)", "RectangleCS",
            "Construct an Rectangle Cross Section",
            "Alpaca4d", "01_Section")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("SectionName", "SecName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Width", "Width", "", GH_ParamAccess.item, 0.30);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Height", "Height", "", GH_ParamAccess.item, 0.60);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Section", "Section", "Section");

        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            // Input
            string secName = "";
            double width = 0.30;
            double height = 0.60;
            IUniaxialMaterial material = Alpaca4d.Material.UniaxialMaterialElastic.Steel;


            DA.GetData(0, ref secName);
            DA.GetData(1, ref width);
            DA.GetData(2, ref height);
            DA.GetData(3, ref material);


            var section = new Alpaca4d.Section.RectangleCS(secName, width, height, material);

            DA.SetData(0, section);
        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Rectangular_Section__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{888184F3-A448-4F82-9DCA-E57EFAC8E840}");
    }
}