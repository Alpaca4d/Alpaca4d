using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using System.Linq;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{

    public class FiberSection : GH_Component
    {

        private List<Alpaca4d.Section.PointFiber> _pointFiber = new List<Section.PointFiber>();
        private List<Alpaca4d.Section.Layer> _layer = new List<Section.Layer>();
        private List<Alpaca4d.Section.Patch> _patch = new List<Section.Patch>();

        private Alpaca4d.Section.FiberSection _fiberSection;

        public FiberSection()
          : base("Fiber Section (Alpaca4d)", "FiberSection",
            "Construct a FiberSection",
            "Alpaca4d", "MomentCurvature_βeta")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("PointFiber", "PointFiber", "", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Layer", "Layer", "", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Patch", "Patch", "", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("GJ", "GJ", "", GH_ParamAccess.item, 1e8);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("FiberSection", "FiberSection", "");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            DA.GetDataList(0, _pointFiber);
            DA.GetDataList(1, _layer);
            DA.GetDataList(2, _patch);

            if (_pointFiber.Count == 0 && _layer.Count == 0 && _patch.Count == 0)
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "At least one fiber should be provided");
                return;
            }

            double GJ = 1000;
            DA.GetData(3, ref GJ);

            _fiberSection = new Alpaca4d.Section.FiberSection(_pointFiber, _layer, _patch, GJ);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, _fiberSection);
        }


        protected override void BeforeSolveInstance()
        {
            _pointFiber.Clear();
            _layer.Clear();
            _patch.Clear();
        }


        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            base.DrawViewportWires(args);
            if (this.Hidden || this.Locked) return;

            // Draw Point Fibers
            if (_pointFiber != null)
            {
                var points = _pointFiber.Select(x => x.Pos);
                foreach (var point in points)
                {
                    args.Display.DrawPoint(point, Rhino.Display.PointStyle.Pin, 2, System.Drawing.Color.Blue);
                }
            }

            // Draw Layers
            if (_layer != null)
            {
                var points = _layer.SelectMany(x => x.Fibers).Select(x => x.Pos);
                foreach (var point in points)
                {
                    args.Display.DrawPoint(point, Rhino.Display.PointStyle.Pin, 3, System.Drawing.Color.Red);
                }

                args.Display.DrawDottedPolyline(points, System.Drawing.Color.Black, false);
            }

            // Draw Patch
            if (_patch != null)
            {
                foreach (var patch in _patch)
                {
                    var mesh = patch.PatchGeometry;
                    args.Display.DrawMeshWires(mesh, System.Drawing.Color.Gray);

                }

                var points = _patch.SelectMany(x => x.Fibers).Select(x => x.Pos);
                foreach (var point in points)
                {
                    args.Display.DrawPoint(point, Rhino.Display.PointStyle.RoundSimple, 1, System.Drawing.Color.Black);
                }
            }


            // Draw Local Axis
            var boundingBox = new Rhino.Geometry.BoundingBox(_fiberSection.Fibers.Select(x => x.Pos));
            var center = boundingBox.Center;
            var length = boundingBox.Diagonal.Length/2;
            var yLine = new Rhino.Geometry.Line(center, new Vector3d(0,length,0));
            var zLine = new Rhino.Geometry.Line(center, new Vector3d(-length,0,0));

            args.Display.DrawLineArrow(yLine, System.Drawing.Color.Green, 3, 0.5);
            args.Display.DrawLineArrow(zLine, System.Drawing.Color.Blue, 3, 0.5);

            var yPos = (yLine.ToNurbsCurve().PointAtEnd - center)*1.1;
            var zPos = (zLine.ToNurbsCurve().PointAtEnd - center)*1.1;

            args.Display.Draw2dText("Y", System.Drawing.Color.Black, center + yPos, true, 36);
            args.Display.Draw2dText("Z", System.Drawing.Color.Black, center + zPos, true, 36);
        }


        public override GH_Exposure Exposure => GH_Exposure.secondary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Fiber_Aggregated_Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{18cd5969-e0e4-4acf-9790-0af2c22cfeb9}");
    }
}
