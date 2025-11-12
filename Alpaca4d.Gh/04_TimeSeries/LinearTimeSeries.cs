using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class LinearTimeSeries : GH_Component
    {
        public LinearTimeSeries()
          : base("Linear Time Series (Alpaca4d)", "Linear Time Series",
            "Construct a Linear Time Series",
            "Alpaca4d", "04_Time Series")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddNumberParameter("LinearFactor", "LinearFactor", "Linear Factor", GH_ParamAccess.item, 1.0);
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
            var linearFactor = 1.00;

            if (!DA.GetData(0, ref linearFactor)) return;


            var timeSeries = new Alpaca4d.TimeSeries.Linear(linearFactor);
            var graph = timeSeries.DrawSeries();

            // Assign the output parameter.
            DA.SetData(0, timeSeries);
            DA.SetDataList(1, graph);
        }


        public override GH_Exposure Exposure => GH_Exposure.primary;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Linear_Time_Series__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("05134721-D2DC-483E-BAD7-1A1AF0238A3D");
    }
}