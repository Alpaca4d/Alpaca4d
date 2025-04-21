using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    [Obsolete]
    public class LinearLoad_obsolete : GH_Component
    {
        public LinearLoad_obsolete()
          : base("Linear Load (Alpaca4d)", "LinearLoad",
            "Construct a LinearLoad",
            "Alpaca4d", "05_Load")
        {
            // Draw a Description Underneath the component
            this.Message = $"Linear Load (Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("BeamElement", "BeamElement", "By Default, the load will be applied to all the beam elements.", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddVectorParameter("Force", "Force", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("TimeSeries", "TimeSeries", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
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
            Generic.IBeam element = null;
            DA.GetData(0, ref element);
            
            var force = Vector3d.Zero;
            DA.GetData(1, ref force);

            Alpaca4d.Generic.ITimeSeries timeSeries = Alpaca4d.TimeSeries.Constant.Default();
            DA.GetData(2, ref timeSeries);

            bool local = false;
            var linearLoad = new Alpaca4d.Loads.LineLoad(element, force, timeSeries, local);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, linearLoad);
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
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Line_load;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{C575E59A-2A81-4DDE-8DDA-5FC8BD7FBE36}");
    }
}