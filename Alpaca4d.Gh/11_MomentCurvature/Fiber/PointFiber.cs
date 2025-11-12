using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using System.Linq;
using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class PointFiber : GH_Component
    {
        public PointFiber()
          : base("Fiber Point(Alpaca4d)", "Fiber Point",
            "Construct a FiberPoint",
            "Alpaca4d", "MomentCurvature_βeta")
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
            pManager.AddNumberParameter("AreaFiber", "AreaFiber", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("PointFiber", "PointFiber", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var pos = Point3d.Origin;
            double area = 0.0;
            Alpaca4d.Generic.IMaterial material = null; ;

            DA.GetData(0, ref pos);
            DA.GetData(1, ref area);
            DA.GetData(2, ref material);

            var fiber = new Alpaca4d.Section.PointFiber(pos, area, material);
            _pointFiber.Add(fiber);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, fiber);
        }

        private List<Alpaca4d.Section.PointFiber> _pointFiber = new List<Section.PointFiber>();
        protected override void BeforeSolveInstance()
        {
            _pointFiber.Clear();
        }

        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            if (_pointFiber.Count == 0)
                return;

            base.DrawViewportWires(args);
            if (this.Hidden || this.Locked) return;

            if (_pointFiber != null)
            {
                var points = _pointFiber.Select(x => x.Pos);
                foreach (var point in points)
                {
                    args.Display.DrawPoint(point, Rhino.Display.PointStyle.Pin, 2, System.Drawing.Color.Blue);
                }
            }
        }

        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.secondary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Fiber_Point__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{934021CE-8D12-4FCA-8CF1-9158EB08208A}");
    }
}
