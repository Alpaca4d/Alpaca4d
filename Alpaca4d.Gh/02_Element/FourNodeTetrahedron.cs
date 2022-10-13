﻿using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Drawing;
using System.Collections.Generic;
using Alpaca4d.Generic;
using Alpaca4d;

namespace Alpaca4d.Gh
{
    public class FourNodeTetrahedron : GH_Component
    {
        /// <summary>
        /// Each implementation of GH_Component must provide a public 
        /// constructor without any arguments.
        /// Category represents the Tab in which the component will appear, 
        /// Subcategory the panel. If you use non-existing tab or panel names, 
        /// new tabs/panels will automatically be created.
        /// </summary>
        public FourNodeTetrahedron()
          : base("FourNodeTetrahedron (Alpaca4d)", "FNT",
            "Construct a FourNodeTetrahedron element",
            "Alpaca4d", "02_Element")
        {
            // Draw a Description Underneath the component
            this.Message = $"FourNodeTetrahedron (Alpaca4d)";
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


            Color color = Color.AliceBlue;
            if (!DA.GetData(2, ref color))
            {
                color = Color.IndianRed;
            }

            var element = new Alpaca4d.Element.Tetrahedron(mesh, material);
            element.Color = color;
            DA.SetData(0, element);
        }


        public override GH_Exposure Exposure => GH_Exposure.tertiary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Four_Node_Tetrahedron__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{4e0b2529-f2fb-4d7d-9be3-cdf53ff2c22f}");
    }
}