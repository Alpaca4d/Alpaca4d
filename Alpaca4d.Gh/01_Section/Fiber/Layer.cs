using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using System.Linq;

using Alpaca4d;
using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class LayerFiber : GH_Component
    {
        public LayerFiber()
          : base("Layer Fiber (Alpaca4d)", "Layer Fiber",
            "Construct a LayerFiber",
            "Alpaca4d", "01_Section")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddCurveParameter("Curve", "Curve", "", GH_ParamAccess.item);
            pManager.AddIntegerParameter("NumberOfFibers", "NumberOfFibers", "", GH_ParamAccess.item);
            pManager.AddNumberParameter("AreaFiber", "AreaFiber", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
        }
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Layer", "Layer", "");
        }
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Rhino.Geometry.Curve curve = null;
            int numberFiber = 3;
            double area = 0.0;
            Alpaca4d.Generic.IMaterial material = null;

            DA.GetData(0, ref curve);
            DA.GetData(1, ref numberFiber);
            DA.GetData(2, ref area);
            DA.GetData(3, ref material);

            var fiber = new Alpaca4d.Section.Layer(curve, numberFiber, area, material);
            _fibers.Add(fiber);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, fiber);
        }


        private List<Alpaca4d.Section.Layer> _fibers = new List<Section.Layer>();

        protected override void BeforeSolveInstance()
        {
            _fibers.Clear();
        }
        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            if (_fibers.Count == 0)
                return;

            base.DrawViewportWires(args);
            if (this.Hidden || this.Locked) return;

            if(_fibers != null)
            {
                var points = _fibers.SelectMany(x => x.Fibers).Select(x => x.Pos);
                foreach (var point in points)
                {
                    args.Display.DrawPoint(point, Rhino.Display.PointStyle.Pin, 3, System.Drawing.Color.Red);
                }

                args.Display.DrawDottedPolyline(points, System.Drawing.Color.Black, false);
            }
        }
        public override GH_Exposure Exposure => GH_Exposure.tertiary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Layer__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{4ED2C47B-F1DF-4A8A-AD93-CB0F3CCB375B}");
    }
}





    //            args.Display.DrawPoint(((Rhino.Geometry.Point)obj).Location, Rhino.Display.PointStyle.Circle, 2, solidClr);
    //break;

    //        case Rhino.DocObjects.ObjectType.Curve:
    //            args.Display.DrawCurve((Curve)obj, solidClr);
    //break;