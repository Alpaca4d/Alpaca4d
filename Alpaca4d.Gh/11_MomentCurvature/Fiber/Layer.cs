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
            "A row of equally spaced fibres along a curve - a layer of reinforcement.\nCurve in m, area in m2.",
            "Alpaca4d", "MomentCurvature_βeta")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddCurveParameter("Curve", "Curve",
                "The line the fibres are spread along, in m, in the section's local yz plane.",
                GH_ParamAccess.item);

            pManager.AddIntegerParameter("NumberOfFibers", "NumberOfFibers",
                "How many fibres to space along the curve, ends included.",
                GH_ParamAccess.item, 3);

            pManager.AddNumberParameter("AreaFiber", "AreaFiber",
                "Area of each fibre, in m2. Defaults to one 16 mm bar.",
                GH_ParamAccess.item, 2.011e-4);

            pManager.AddGenericParameter("Material", "Material",
                "Material of the fibres. Defaults to B450C reinforcement.",
                GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Layer", "Layer", "");
        }
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Rhino.Geometry.Curve curve = null;
            int numberFiber = 3;
            double area = 2.011e-4;

            // A layer is a row of bars, so that is what it falls back to.
            Alpaca4d.Generic.IMaterial material = Alpaca4d.Material.ReinforcingSteel.B450C;

            if (!DA.GetData(0, ref curve) || curve == null)
                return;

            DA.GetData(1, ref numberFiber);
            DA.GetData(2, ref area);
            DA.GetData(3, ref material);

            if (numberFiber < 2)
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Error,
                    "A layer needs at least two fibres, not " + numberFiber + ".");
                return;
            }

            var fiber = new Alpaca4d.Section.Layer(curve, numberFiber, area, material);
            _fibers.Add(fiber);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, fiber);
        }


        private List<Alpaca4d.Section.Layer> _fibers = new List<Section.Layer>();
        private readonly FiberPreview _preview = new FiberPreview();

        protected override void BeforeSolveInstance()
        {
            _fibers.Clear();
            _preview.Clear();
        }

        protected override void AfterSolveInstance()
        {
            _preview.AddLayers(_fibers);
        }

        /// <summary>
        /// Without this the box comes from the output parameter, which holds a layer and
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
        public override GH_Exposure Exposure => GH_Exposure.secondary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Layer__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{4ED2C47B-F1DF-4A8A-AD93-CB0F3CCB375B}");
    }
}





    //            args.Display.DrawPoint(((Rhino.Geometry.Point)obj).Location, Rhino.Display.PointStyle.Circle, 2, solidClr);
    //break;

    //        case Rhino.DocObjects.ObjectType.Curve:
    //            args.Display.DrawCurve((Curve)obj, solidClr);
    //break;