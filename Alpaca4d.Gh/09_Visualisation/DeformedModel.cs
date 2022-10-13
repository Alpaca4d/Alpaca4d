using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class DeformedModel : GH_Component
    {
        public DeformedModel()
          : base("Deformed Model View (Alpaca4d)", "Deformed Model View",
            "Deformed Model View",
            "Alpaca4d", "09_Visualisation")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "", GH_ParamAccess.item);
            pManager.AddIntegerParameter("Step", "Step", "", GH_ParamAccess.item, 0);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Scale", "Scale", "", GH_ParamAccess.item, 1.0);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddColourParameter("Colors", "Colors", "", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Line", "Line", "");
            pManager.Register_GenericParam("Mesh", "Mesh", "");
            pManager.Register_GenericParam("Brick", "Brick", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Model model = new Model();
            DA.GetData(0, ref model);

            int step = 0;
            DA.GetData(1, ref step);

            double scale = 1.0;
            DA.GetData(2, ref scale);

            List<System.Drawing.Color> colors = new List<System.Drawing.Color>();
            List<Mesh> mesh = null;
            List<Mesh> bricks = null;
            List<Curve> lines = null;

            if (DA.GetDataList(3, colors))
			{
                mesh = model.DeformedShell(step, scale, colors);
                lines = model.DeformedBeam(step, scale);
                bricks = model.DeformedBrick(step, scale, colors);
            }
			else
			{
                colors = Alpaca4d.Colors.Gradient(11);
                mesh = model.DeformedShell(step, scale, colors);
                lines = model.DeformedBeam(step, scale);
                bricks = model.DeformedBrick(step, scale, colors);
            }

            // Finally assign the spiral to the output parameter.
            DA.SetDataList(0, lines);
            DA.SetDataList(1, mesh);
            DA.SetDataList(2, bricks);
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
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Deformed_Model__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{C03F4DEC-0B0E-4403-A031-EA1A51923252}");
    }
}