using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using System.Linq;
using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class DeconstructFiberPoint_OBSOLETE : GH_Component
    {
        public DeconstructFiberPoint_OBSOLETE()
          : base("Deconstruct Fiber Point(Alpaca4d)", "Deconstruct Fiber Point",
            "Deconstruct a FiberPoint",
            "Alpaca4d", "MomentCurvature_βeta")
        {
            // Draw a Description Underneath the component
            this.Message = "Deconstruct Fiber Point\n(Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("FiberPoint", "FiberPoint", "", GH_ParamAccess.item);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_PointParam("Pos", "Pos", "");
            pManager.Register_DoubleParam("Area", "Area", "");
            pManager.Register_GenericParam("Material", "Material", "");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Alpaca4d.Section.PointFiber fiberPoint = null;
            DA.GetData(0, ref fiberPoint);

            var pos = fiberPoint.Pos;
            var area = fiberPoint.Area;
            var material = fiberPoint.Material;

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, pos);
            DA.SetData(1, area);
            DA.SetData(2, material);
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
        protected override System.Drawing.Bitmap Icon => null;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{92cd5969-e0e4-4acf-9790-0af2c22cfeb9}");
    }
}
