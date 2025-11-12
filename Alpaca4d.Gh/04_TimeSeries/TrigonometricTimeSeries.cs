using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class TrigonometricTimeSeries : GH_Component
    {
        public TrigonometricTimeSeries()
          : base("Trigonometric Time Series (Alpaca4d)", "TTS",
            "Construct a Trigonometric Time Series",
            "Alpaca4d", "04_Time Series")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        /// double tStart, double tEnd, double period, double shift = 0.0, double cFactor = 1.0
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddNumberParameter("TStart", "TStart", "[s]", GH_ParamAccess.item, 0.0);
            pManager.AddNumberParameter("TEnd", "TEnd", "[s]", GH_ParamAccess.item);
            pManager.AddNumberParameter("Period", "Period", "[s]", GH_ParamAccess.item);
            pManager.AddNumberParameter("Shift", "Shift", "[s]", GH_ParamAccess.item, 0.0);
            pManager[pManager.ParamCount - 1].Optional = true;
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
            double tStart = 0.0;
            if (!DA.GetData(0, ref tStart)) return;

            double tEnd = 0.0;
            if (!DA.GetData(1, ref tEnd)) return;

            double period = 0.0;
            if (!DA.GetData(2, ref period)) return;

            double shift = 0.0;
            DA.GetData(3, ref shift);

            double loadFactor = 1.0;
            DA.GetData(4, ref loadFactor);


            var timeSeries = new Alpaca4d.TimeSeries.Trigonometric(tStart, tEnd, period, shift, loadFactor);
            var graph = timeSeries.DrawSeries();

            // Assign the output parameter.
            DA.SetData(0, timeSeries);
            DA.SetDataList(1, graph);
        }


        public override GH_Exposure Exposure => GH_Exposure.primary;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Periodic_Time_Series__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{5543342A-F723-421C-931A-FAD5EB4B01BE}");
    }
}