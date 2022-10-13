using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    public class DisassembleSection : GH_Component
    {
        public DisassembleSection()
          : base("Disassemble Section (Alpaca4d)", "DS",
            "Disassemble a Section",
            "Alpaca4d", "01_Section")
        {
            this.Message = "Disassemble Section\n(Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("CrossSection", "CrossSection", "", GH_ParamAccess.item);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_StringParam("Name", "Name", "");
            pManager.Register_GenericParam("Material", "Material", "");
            pManager.Register_CurveParam("Geometry", "Geometry", "");
            pManager.Register_CurveParam("--------", "--------", "");
            pManager.Register_DoubleParam("Area", "Area", "");
            pManager.Register_DoubleParam("AreaY", "Areay", "");
            pManager.Register_DoubleParam("AreaZ", "AreaZ", "");
            pManager.Register_DoubleParam("AlphaY", "AlphaY", "");
            pManager.Register_DoubleParam("AlphaZ", "AlphaZ", "");
            pManager.Register_DoubleParam("Iyy", "Iyy", "");
            pManager.Register_DoubleParam("Izz", "Izz", "");
            pManager.Register_DoubleParam("J", "J", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            dynamic section = null;
            DA.GetData(0, ref section);

            var name = section.Value.SectionName;
            var material = section.Value.Material;
            var curve = section.Value.Curve;

            var area = section.Value.Area;
            var areaY = section.Value.AreaY();
            var areaZ = section.Value.AreaZ();
            var alphaY = section.Value.AlphaY;
            var alphaZ = section.Value.AlphaZ;
            var iYY = section.Value.Iyy;
            var iZZ = section.Value.Izz;
            var j = section.Value.J;


            DA.SetData(0, name);
            DA.SetData(1, material);
            DA.SetData(2, curve);
            DA.SetData(4, area);
            DA.SetData(5, areaY);
            DA.SetData(6, areaZ);
            DA.SetData(7, alphaY);
            DA.SetData(8, alphaZ);
            DA.SetData(9, iYY);
            DA.SetData(10, iZZ);
            DA.SetData(11, j);
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.quarternary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Disassemble_CrossSection__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{16E764EF-54B3-43BC-B393-FE56DA06A520}");
    }
}