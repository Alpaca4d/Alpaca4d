using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class MassPointLoad : GH_Component
    {
        public MassPointLoad()
          : base("Mass Point (Alpaca4d)", "Mass Point",
            "Construct a PointLoad",
            "Alpaca4d", "05_Load")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddPointParameter("Point", "Point", "", GH_ParamAccess.item);
            pManager.AddVectorParameter("TransMass", "TransMass", $"[{Units.Mass}]", GH_ParamAccess.item); ;
            pManager.AddVectorParameter("RotationalMass", "RotationalMass", "", GH_ParamAccess.item, Vector3d.Zero);
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
            var transMass = Vector3d.Zero;
            var rotationMass = Vector3d.Zero;

            if (!DA.GetData(0, ref pos)) return;
            if (!DA.GetData(1, ref transMass)) return;
            DA.GetData(2, ref rotationMass);

            transMass = transMass * 9.81/1000;
            var load = new Alpaca4d.Loads.MassLoad(pos, transMass, rotationMass);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, load);
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.tertiary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Mass_Point__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{5C7056ED-01D4-4DDE-AD9E-46A5266ECEE6}");
    }
}