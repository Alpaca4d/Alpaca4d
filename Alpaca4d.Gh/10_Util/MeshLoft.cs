using System;
using System.Collections.Generic;
using Rhino.Geometry;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Types;


namespace Alpaca4d.Gh
{
    public class MeshLoft : GH_Component
    {
        public MeshLoft()
          : base("MeshLoft (Alpaca4d)", "ML",
            "Mesh Loft",
            "Alpaca4d", "10_Utility")
        {
            // Draw a Description Underneath the component
            this.Message = "Mesh Loft (Alpaca4d)";
        }


        /// <inheritdoc />
        protected override void RegisterInputParams(GH_InputParamManager pManager)
        {
            pManager.AddCurveParameter("Polylines", "Polylines", "", GH_ParamAccess.list);
        }


        /// <inheritdoc />
        protected override void RegisterOutputParams(GH_OutputParamManager pManager)
        {
            pManager.AddMeshParameter("Mesh", "Mesh", "Lofted mesh", GH_ParamAccess.item);
        }


        /// <inheritdoc />
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            List<Curve> curves = new List<Curve>();

            if (!DA.GetDataList(0, curves)) return;

            var polys = curves.ConvertAll(crv =>
            {
                if (!crv.TryGetPolyline(out Polyline poly))
                    throw new ArgumentException();

                return poly;
            });

            var mesh = Alpaca4d.Utils.CreateLoft(polys);

            DA.SetData(0, mesh);
        }


        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// </summary>
        protected override System.Drawing.Bitmap Icon
        {
            get { return Properties.Resources.Mesh_Loft__Alpaca4d_; }
        }


        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid
        {
            get { return new Guid("{7646895B-AF39-4BA3-91C2-3E5C00B21DCD}"); }
        }
    }
}