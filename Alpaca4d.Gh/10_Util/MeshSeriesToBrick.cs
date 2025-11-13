using System;
using System.Collections.Generic;
using Rhino.Geometry;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Types;


namespace Alpaca4d.Gh
{
    public class MeshSeriesToBrick : GH_Component
    {
        public MeshSeriesToBrick()
          : base("MeshSeriesToBrick (Alpaca4d)", "Mesh Series to Brick",
            "MeshSeriesToBrick",
            "Alpaca4d", "10_Utility")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }


        /// <inheritdoc />
        protected override void RegisterInputParams(GH_InputParamManager pManager)
        {
            pManager.AddMeshParameter("Meshes", "Meshes", "", GH_ParamAccess.list);
            pManager.AddBooleanParameter("Closed", "Closed", "", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;
        }


        /// <inheritdoc />
        protected override void RegisterOutputParams(GH_OutputParamManager pManager)
        {
            pManager.Register_MeshParam("Mesh", "Mesh", "");
        }


        /// <inheritdoc />
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var meshes = new List<Mesh>();
            DA.GetDataList(0, meshes);

            var closed = false;
            DA.GetData(1, ref closed);

            List<Mesh> mesh;
            if (closed)
            {
                meshes.Add(meshes[0]);
                mesh = Alpaca4d.Utils.MeshSeriesToBrick(meshes);
            }
            else
            {
                mesh = Alpaca4d.Utils.MeshSeriesToBrick(meshes);
            }

            DA.SetDataList(0, mesh);
        }


        protected override System.Drawing.Bitmap Icon => Properties.Resources.Mesh_Series_to_Brick__Alpaca4d_;
        

        public override GH_Exposure Exposure => GH_Exposure.secondary;

        public override Guid ComponentGuid
        {
            get { return new Guid("{95F0E8F1-33B7-4A2D-ABAE-693DAA6AA8B9}"); }
        }
    }
}