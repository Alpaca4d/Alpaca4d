using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class ReadTimeSeries : GH_Component
    {
        public ReadTimeSeries()
          : base("Read Time Series (Alpaca4d)", "RTS",
            "Read a Path Time Series",
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
            pManager.AddTextParameter("FilePath", "FilePath", "The file should contains lines representing the times-values of a time series separated by a specific 'separator'", GH_ParamAccess.item);
            pManager.AddTextParameter("Separator", "Separator", "", GH_ParamAccess.item, ",");
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
            string filePath = "";
            DA.GetData(0, ref filePath);

            string separator = ",";
            DA.GetData(1, ref separator);

            char sep = char.Parse(separator);

            var timeSeries = Alpaca4d.TimeSeries.PathTimeSeries.ReadFile(filePath, sep);
            var graph = timeSeries.DrawSeries();

            // Assign the output parameter.
            DA.SetData(0, timeSeries);
            DA.SetDataList(1, graph);
        }


        public override GH_Exposure Exposure => GH_Exposure.secondary;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Read_Time_History__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{13327A78-0C79-4C18-B1D1-9C2056231D58}");
    }
}