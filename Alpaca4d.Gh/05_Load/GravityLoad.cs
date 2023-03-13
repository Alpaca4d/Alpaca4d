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
            pManager.AddTextParameter("TimeSeriesType", "TimeSeriesType", "Connect a 'ValueList'\nConstant, Linear", GH_ParamAccess.item, "Constant");
            pManager.AddNumberParameter("GFactor", "GFactor", "", GH_ParamAccess.item, 9.81);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        protected override void BeforeSolveInstance()
        {
            List<string> resultTypes = new List<string> { "Constant", "Linear" };
            ValueListUtils.updateValueLists(this, 0, resultTypes, null);
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
            var timeSeriesType = "Constant";
            DA.GetData(0, ref timeSeriesType);

            var gFactor = 9.81;
            DA.GetData(1, ref gFactor);

            Alpaca4d.Generic.ITimeSeries timeSeries = null;
            if (timeSeriesType == TimeSeriesType.Constant.ToString())
                timeSeries = new Alpaca4d.TimeSeries.Constant(1);
            else if (timeSeriesType == TimeSeriesType.Linear.ToString())
                timeSeries = new Alpaca4d.TimeSeries.Linear(1);
            else
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Error, $"{timeSeriesType} does not exist!");
                return;
            }

            var load = new Alpaca4d.Loads.Gravity(gFactor ,timeSeries);
            // Finally assign the spiral to the output parameter.
            DA.SetData(0, load);
        }


        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Gravity_Load__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{CA7FAEE8-AA4B-4183-A77D-0FFF58686465}");
    }
}