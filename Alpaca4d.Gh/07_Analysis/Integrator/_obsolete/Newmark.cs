using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    [Obsolete]
    public class Newmark : GH_Component
    {
        public Newmark()
          : base("Integrator Newmark (Alpaca4d)", "NM",
            "",
            "Alpaca4d", "07_Analysis")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }


        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddNumberParameter("Gamma", "Gamma", "", GH_ParamAccess.item, 0.5);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Beta", "Beta", "", GH_ParamAccess.item, 0.25);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Integrator", "Integrator", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            double gamma = 0.5;
            DA.GetData(0, ref gamma);
            double beta = 0.25;

            DA.GetData(1, ref beta);


            var integrator = Alpaca4d.Integrator.Newmark(gamma, beta);

            DA.SetData(0, integrator);
        }



        public override GH_Exposure Exposure => GH_Exposure.hidden;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Newmark_Integrator__Alpaca4d_;


        public override Guid ComponentGuid => new Guid("{68DB1D53-3344-4494-886B-6813DA404024}");
    }
}
