using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;
using Alpaca4d.Loads;
using System.Linq;
using Alpaca4d.Generic;
using Alpaca4d.Core.Utils;

namespace Alpaca4d.Gh
{
    [Obsolete]
    public class PlainPattern : GH_Component
    {
        public PlainPattern()
          : base("Load Pattern (Alpaca4d)", "Load Pattern",
            "Construct a Load Pattern",
            "Alpaca4d", "05_Load")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// pattern UniformExcitation $patternTag $dir -accel $tsTag <-vel0 $vel0> <-fact $cFactor>

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("TimeSeries", "TimeSeries", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Loads", "Loads", "", GH_ParamAccess.list);
            pManager.AddNumberParameter("Factor", "Factor", "Constant factor", GH_ParamAccess.item, 1);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("LoadPattern", "", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Alpaca4d.Generic.ITimeSeries timeSeries = TimeSeries.Constant.Default();
            DA.GetData(0, ref timeSeries);

            List<ILoad> loads = new List<ILoad>();
            DA.GetDataList(1, loads);

            double factor = 1;
            DA.GetData(2, ref factor);

            var load = new Alpaca4d.Loads.LoadPattern(PatternType.Plain, timeSeries, loads, factor);

            DA.SetData(0, load);
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.hidden;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Load_pattern__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{E0A01D43-26F4-4506-B2F5-A9A33A0DDF59}");

        protected override void BeforeSolveInstance()
        {
            List<string> patternType;

            patternType = Enum.GetNames(typeof(Alpaca4d.Loads.PatternType)).ToList();
            ValueListUtils.UpdateValueLists(this, 0, patternType, null);
        }

    }
}
