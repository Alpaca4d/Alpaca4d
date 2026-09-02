using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Alpaca4d.Generic;
using Alpaca4d;

namespace Alpaca4d.Gh
{
    public class RectangleHollowCS : GH_Component
    {
        public RectangleHollowCS()
          : base("RectangleHollow (Alpaca4d)", "RectangleHollowCS",
            "Construct an Rectangle Hollow Section Cross Section",
            "Alpaca4d", "01_Section")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("SectionName", "SecName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Width", "Width", $"[{Units.Length}]", GH_ParamAccess.item, 0.30);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Height", "Height", $"[{Units.Length}]", GH_ParamAccess.item, 0.60);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Web", "Web", $"[{Units.Length}]", GH_ParamAccess.item, 0.02);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("TopFlange", "TopFlange", $"[{Units.Length}]", GH_ParamAccess.item, 0.02);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("BottomFlange", "BottomFlange", $"[{Units.Length}]", GH_ParamAccess.item, 0.02);
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
            double web = 0.02;
            double topFlange = 0.02;
            double bottomFlange = 0.02;
            IUniaxialMaterial material = Alpaca4d.Material.UniaxialMaterialElastic.Steel;

            DA.GetData(0, ref secName);
            DA.GetData(1, ref width);
            DA.GetData(2, ref height);
            DA.GetData(3, ref web);
            DA.GetData(4, ref topFlange);
            DA.GetData(5, ref bottomFlange);
            DA.GetData(6, ref material);

            var section = new Alpaca4d.Section.RectangleHollowCS(secName, width, height, web, topFlange, bottomFlange, material);

            DA.SetData(0, section);
        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Rectangular_Hollow_cross_section__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{0DA19D50-BCDF-4AFA-9777-45AE6A5392CC}");
    }
}