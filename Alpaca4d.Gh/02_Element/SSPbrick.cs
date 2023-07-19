using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Drawing;
using System.Collections.Generic;
using Alpaca4d.Generic;
using Alpaca4d;

namespace Alpaca4d.Gh
{
    public class SSPbrick : GH_Component
    {
        public SSPbrick()
          : base("SSP Brick (Alpaca4d)", "SSP",
            "Construct a SSP Brick element",
            "Alpaca4d", "02_Element")
        {
            // Draw a Description Underneath the component
            this.Message = $"SSP Brick (Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddMeshParameter("Mesh", "Mesh", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
            pManager.AddColourParameter("Colour", "Colour", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Element", "Element", "Element");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Mesh mesh = null;
            DA.GetData(0, ref mesh);

            IMultiDimensionMaterial material = null;
            DA.GetData(1, ref material);


            Color color = Color.Aquamarine;
            if (!DA.GetData(2, ref color))
            {
                color = Color.PaleVioletRed;
            }


            var _mesh = Utils.CleanHexahedron(mesh);

            var element = new Alpaca4d.Element.SSPbrick(_mesh, material);
            element.Color = color;

            DA.SetData(0, element);
        }


        public override GH_Exposure Exposure => GH_Exposure.tertiary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.SSP_brick__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{FDFC5598-7AA8-45CF-AE80-2C9996564EB2}");
    }
}