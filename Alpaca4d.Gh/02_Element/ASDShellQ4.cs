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
    public class ASDShellQ4 : GH_Component
    {
        /// <summary>
        /// Each implementation of GH_Component must provide a public 
        /// constructor without any arguments.
        /// Category represents the Tab in which the component will appear, 
        /// Subcategory the panel. If you use non-existing tab or panel names, 
        /// new tabs/panels will automatically be created.
        /// </summary>
        public ASDShellQ4()
          : base("ASD ShellQ4 (Alpaca4d)", "ASDQ4/DKGT",
            "Construct a ASDShellQ4 element or DKGT Shell",
            "Alpaca4d", "02_Element")
        {
            // Draw a Description Underneath the component
            this.Message = $"ASDShellQ4(Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddMeshParameter("Mesh", "Mesh", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Section", "Section", "", GH_ParamAccess.item);
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
            Mesh _mesh = null;
            DA.GetData(0, ref _mesh);

            IMultiDimensionSection section = null;
            DA.GetData(1, ref section);

            Color color = Color.AliceBlue;
            if (!DA.GetData(2, ref color))
            {
                color = Color.IndianRed;
            }


            var meshes = new List<Mesh>();

            if (_mesh.Faces.Count > 0)
            {
                meshes = Utils.ExplodeMesh(_mesh);
            }
            else
            {
                meshes.Add(_mesh);
            }

            foreach(var mesh in meshes)
            {
                var elements = new List<Alpaca4d.Generic.IShell>();

                if(mesh.Vertices.Count == 4)
                {
                    var element = new Alpaca4d.Element.ASDShellQ4(mesh, section);
                    element.Color = color;

                    elements.Add(element);
                    DA.SetDataList(0, elements);
                }
                else if (mesh.Vertices.Count == 3)
                {
                    var element = new Alpaca4d.Element.ShellDKGT(mesh, section);
                    element.Color = color;

                    elements.Add(element);
                    DA.SetDataList(0, elements);
                }
            }
        }


        public override GH_Exposure Exposure => GH_Exposure.secondary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.ASD_ShellQ4__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{81cd5969-e0e4-4acf-9790-0af2c22cfeb9}");
    }

}