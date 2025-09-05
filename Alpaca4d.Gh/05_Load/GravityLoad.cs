using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class GravityLoad : GH_Component
    {
        public GravityLoad()
          : base("Gravity Load (Alpaca4d)", "Gravity Load",
            "Construct a Gravity Load",
            "Alpaca4d", "05_Load")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddNumberParameter("Factor", "Factor", "", GH_ParamAccess.item, 1.0);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        protected override void BeforeSolveInstance()
        {
            List<string> resultTypes = new List<string> { "Constant", "Linear" };
            ValueListUtils.UpdateValueLists(this, 0, resultTypes, null);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Load", "Load", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            double factor = 1;
            DA.GetData(0, ref factor);

            var load = new Alpaca4d.Loads.Gravity(factor ,null);
            // Finally assign the spiral to the output parameter.
            DA.SetData(0, load);
        }


        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Gravity_Load__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{4B6FA7FD-9388-4699-B374-B94F94583A53}");
    }
}