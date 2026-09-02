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
            "One fibre of a fibre section - a point with an area and a material.\nCoordinates in m, area in m2. The point's X is the section's local y and its Y the local z.",
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
            pManager.AddPointParameter("Point", "Point", "Where the fibre sits, in m. X is the section's local y, Y its local z.", GH_ParamAccess.item);

            pManager.AddNumberParameter("AreaFiber", "AreaFiber",
                "Area of the fibre, in m2. Defaults to one 16 mm bar.",
                GH_ParamAccess.item, 2.011e-4);

            pManager.AddGenericParameter("Material", "Material",
                "Material of the fibre. Defaults to B450C reinforcement.",
                GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("PointFiber", "PointFiber", "The single fibre. Collect it into the PointFiber input of a Fiber Section.");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var pos = Point3d.Origin;
            double area = 2.011e-4;

            // A fibre point is nearly always a bar, so that is what it falls back to.
            Alpaca4d.Generic.IMaterial material = Alpaca4d.Material.ReinforcingSteel.B450C;

            if (!DA.GetData(0, ref pos))
                return;

            DA.GetData(1, ref area);
            DA.GetData(2, ref material);

            var fiber = new Alpaca4d.Section.PointFiber(pos, area, material);
            _pointFiber.Add(fiber);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, fiber);
        }

        private List<Alpaca4d.Section.PointFiber> _pointFiber = new List<Section.PointFiber>();
        private readonly FiberPreview _preview = new FiberPreview();

        protected override void BeforeSolveInstance()
        {
            _pointFiber.Clear();
            _preview.Clear();
        }

        protected override void AfterSolveInstance()
        {
            _preview.AddPointFibers(_pointFiber);
        }

        /// <summary>
        /// Without this the box comes from the output parameter, which holds a fibre and
        /// not geometry - so it is empty, Zoom Extents ignores the preview, and Rhino is
        /// free to cull the drawing.
        /// </summary>
        public override BoundingBox ClippingBox
        {
            get { return _preview.Box; }
        }

        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            base.DrawViewportWires(args);

            if (this.Hidden || this.Locked || _preview.IsEmpty)
                return;

            _preview.Draw(args);
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
