using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class PathTimeSeries : GH_Component
    {
        public PathTimeSeries()
          : base("Path Time Series (Alpaca4d)", "PTS",
            "Construct a Path Time Series",
            "Alpaca4d", "04_Time Series")
        {
            // Draw a Description Underneath the component
            this.Message = $"Path (Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        /// double tStart, double tEnd, double period, double shift = 0.0, double cFactor = 1.0
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddNumberParameter("Times", "Times", "", GH_ParamAccess.list);
            pManager.AddNumberParameter("Values", "Values", "", GH_ParamAccess.list);
            pManager.AddNumberParameter("LoadFactor", "LoadFactor", "", GH_ParamAccess.item, 1.0);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("TimeSeries", "TimeSeries", "");
            pManager.Register_DoubleParam("Graph", "Graph", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            List<double> times = new List<double>();
            if (!DA.GetDataList(0, times)) return;

            List<double> values = new List<double>();
            if (!DA.GetDataList(1, values)) return;

            double loadFactor = 1.0;
            DA.GetData(2, ref loadFactor);


            var timeSeries = new Alpaca4d.TimeSeries.PathTimeSeries(times, values, loadFactor);
            var graph = timeSeries.DrawSeries();

            // Assign the output parameter.
            DA.SetData(0, timeSeries);
            DA.SetDataList(1, graph);
        }


        public override GH_Exposure Exposure => GH_Exposure.primary;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Path_Time_Series__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{AFAF03A6-6C4E-4DAB-AA46-EB60DFB95DFB}");
    }
}