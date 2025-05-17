using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using System.Linq;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class Patch : GH_Component
    {
        public Patch()
          : base("Patch (Alpaca4d)", "Patch",
            "Construct a Patch",
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
            pManager.AddMeshParameter("Mesh", "Mesh", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Patch", "Patch", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Rhino.Geometry.Mesh geometry = null;
            Alpaca4d.Generic.IMaterial material = null;

            DA.GetData(0, ref geometry);
            DA.GetData(1, ref material);
            
            var patch = new Alpaca4d.Section.Patch(geometry, material);
            _patch.Add(patch);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, patch);
        }


        private List<Alpaca4d.Section.Patch> _patch = new List<Section.Patch>();

        protected override void BeforeSolveInstance()
        {
            _patch.Clear();
        }
        public override void DrawViewportMeshes(IGH_PreviewArgs args)
        {
            base.DrawViewportMeshes(args);
        
            if (_patch.Count == 0)
                return;

            if (this.Hidden || this.Locked) return;

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
        }

        public override GH_Exposure Exposure => GH_Exposure.secondary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Patch__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{49DDD2E0-99B5-4D14-976E-531481B07909}");
    }
}