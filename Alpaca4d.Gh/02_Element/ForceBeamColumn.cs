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
    public class ForceBeamColumn : GH_Component
    {
        /// <summary>
        /// Each implementation of GH_Component must provide a public 
        /// constructor without any arguments.
        /// Category represents the Tab in which the component will appear, 
        /// Subcategory the panel. If you use non-existing tab or panel names, 
        /// new tabs/panels will automatically be created.
        /// </summary>
        public ForceBeamColumn()
          : base("Force Beam Column (Alpaca4d)", "Force Beam Column",
            "Construct a ForceBeamColumn",
            "Alpaca4d", "02_Element")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.NickName} \n{this.Category}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddCurveParameter("Line", "Line", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Section", "Section", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("GeometricTransformation", "GeomTransf", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddVectorParameter("ZAxis", "ZAxis", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
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
            Curve line = null;
            DA.GetData(0, ref line);

            IUniaxialSection section = null;
            DA.GetData(1, ref section);

            Vector3d zAxis = Vector3d.Zero;
            if(DA.GetData(3, ref zAxis))
            {
                Plane perpFrame = Alpaca4d.Utils.PerpendicularFrame(line);
                zAxis = Alpaca4d.Utils.AlignPlane(perpFrame, zAxis).XAxis;

            }
            else
            {
                Plane perpFrame = Alpaca4d.Utils.PerpendicularFrame(line);
                zAxis = perpFrame.XAxis;
            }

            

            Alpaca4d.Element.GeomTransf geomTransf = null;
            if (!DA.GetData(2, ref geomTransf))
            {
                geomTransf = new Element.GeomTransf(Alpaca4d.Element.GeomTransfType.Linear, line, zAxis);
            }

            Color color = Color.LightBlue;
            DA.GetData(4, ref color);


            var element = new Alpaca4d.Element.ForceBeamColumn(line, section, geomTransf);
            element.Color = color;

            DA.SetData(0, element);
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.primary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Force_Beam_Column__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("BA137E72-9B35-44FD-9601-5859C0E97AD4");
    }
    
}