using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class PointLoad : GH_Component
    {
        // Point load comment
        public PointLoad()
          : base("Point Load (Alpaca4d)", "Point Load",
            "Construct a PointLoad",
            "Alpaca4d", "05_Load")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.NickName} \n{this.Category}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddPointParameter("Point", "Point", "Point to Restraint", GH_ParamAccess.item);
            pManager.AddVectorParameter("Force", "Force", $"[{Units.Force}]", GH_ParamAccess.item);
            pManager.AddVectorParameter("Moment", "Moment", $"[{Units.Force}{Units.Length}]", GH_ParamAccess.item, Vector3d.Zero);
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
            var pos = Point3d.Origin;
            var force = Vector3d.Zero;
            var moment = Vector3d.Zero;

            if (!DA.GetData(0, ref pos)) return;
            if (!DA.GetData(1, ref force)) return;

            DA.GetData(2, ref moment);

            var load = new Alpaca4d.Loads.PointLoad(pos, force, moment, null);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, load);
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.primary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Point_Load__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{069017B3-4A2F-40FE-87BA-126100908BC8}");
    }
}