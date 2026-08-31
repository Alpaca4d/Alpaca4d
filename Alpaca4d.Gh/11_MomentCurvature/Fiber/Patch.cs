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
            "An area of the section filled with fibres - one fibre per mesh face, at its centroid.\nMesh in m, so fibre areas come out in m2.",
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
            pManager.AddMeshParameter("Mesh", "Mesh",
                "The area to fill, in m, in the section's local yz plane. Each face becomes one fibre, so the mesh density is the fibre density.",
                GH_ParamAccess.item);

            pManager.AddGenericParameter("Material", "Material",
                "Material of the fibres. Defaults to C25/30 concrete.",
                GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
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

            // A patch is the filled area of a section, which for a fibre model is
            // normally the concrete.
            Alpaca4d.Generic.IMaterial material = Alpaca4d.Material.Concrete01.C2530;

            if (!DA.GetData(0, ref geometry) || geometry == null)
                return;

            DA.GetData(1, ref material);
            
            var patch = new Alpaca4d.Section.Patch(geometry, material);
            _patch.Add(patch);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, patch);
        }


        private List<Alpaca4d.Section.Patch> _patch = new List<Section.Patch>();
        private readonly FiberPreview _preview = new FiberPreview();

        protected override void BeforeSolveInstance()
        {
            _patch.Clear();
            _preview.Clear();
        }

        protected override void AfterSolveInstance()
        {
            _preview.AddPatches(_patch);
        }

        /// <summary>
        /// Without this the box comes from the output parameter, which holds a patch and
        /// not geometry - so it is empty, Zoom Extents ignores the preview, and Rhino is
        /// free to cull the drawing.
        /// </summary>
        public override BoundingBox ClippingBox
        {
            get { return _preview.Box; }
        }

        /// <summary>
        /// Wires, not meshes: a patch is only ever drawn as its mesh edges and the
        /// centroids of its faces, so it belongs in the wire pass - which is also the pass
        /// Fiber Section draws it in.
        /// </summary>
        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            base.DrawViewportWires(args);

            if (this.Hidden || this.Locked || _preview.IsEmpty)
                return;

            _preview.Draw(args);
        }

        public override GH_Exposure Exposure => GH_Exposure.secondary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Patch__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{49DDD2E0-99B5-4D14-976E-531481B07909}");
    }
}