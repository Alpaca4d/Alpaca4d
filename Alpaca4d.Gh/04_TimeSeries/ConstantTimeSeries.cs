using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class ConstantTimeSeries : GH_Component
    {
        public ConstantTimeSeries()
          : base("Constant Time Series (Alpaca4d)", "Constant Time Series",
            "Construct a Constant Time Series",
            "Alpaca4d", "04_Time Series")
        {
            // Draw a Description Underneath the component
            this.Message = $"Constant (Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddNumberParameter("LoadFactor", "LoadFactor", "", GH_ParamAccess.item, 1.0);
            pManager[pManager.ParamCount-1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("TimeSeries", "TimeSeries", "");
            pManager.Register_GenericParam("Graph", "Graph", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var cFactor = 1.00;

            if (!DA.GetData(0, ref cFactor)) return;

            var timeSeries = new Alpaca4d.TimeSeries.Constant(cFactor);
            var graph = timeSeries.DrawSeries();

            // Assign the output parameter.
            DA.SetData(0, timeSeries);
            DA.SetDataList(1, graph);

        }
        public override GH_Exposure Exposure => GH_Exposure.primary;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Constant_Time_Series__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("680B7C5B-660C-46B3-8A6B-CEE7D1DC644A");
    }
}