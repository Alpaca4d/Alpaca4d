using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    public class CentralDifference : GH_Component
    {
        public CentralDifference()
          : base("Integrator Central Difference (Alpaca4d)", "CD",
            "",
            "Alpaca4d", "07_Analysis")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Integrator", "Integrator", "");
        }

      
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var integrator = Alpaca4d.Integrator.CentralDifference();

            DA.SetData(0, integrator);
        }



        public override GH_Exposure Exposure => GH_Exposure.tertiary;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Central_Difference__Alpaca4d_;


        public override Guid ComponentGuid => new Guid("{1CFAE408-E6B2-4013-A053-064547785CFB}");
    }
}