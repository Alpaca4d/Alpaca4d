using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using Alpaca4d;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class Gradients : GH_Component
    {
        public Gradients()
          : base("Colors (Alpaca4d)", "CLR",
            "Preset of gradient colors perfect for Data Visualisation",
            "Alpaca4d", "10_Utility")
        {
            // Draw a Description Underneath the component
            this.Message = "Colors (Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddIntegerParameter("GradientIndex", "Index", "gradIndex: An index refering to one of the following possible gradients: \n 0 - Orignal Ladybug\n1 - Nuanced Ladybug\n2 - Multi - colored Ladybug\n3 - Ecotect\n4 - Thermal Comfort Percentage\n5 - Thermal Comfort Colors\n6 - Shade Benefit / Harm\n7 - Shade Harm\n8 - Shade Benefit\n9 - CFD Colors\n10 - Radiation Benefit\n11 - Gsa10 Colour\n12 - Gsa9 Colour", GH_ParamAccess.item, 11);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_ColourParam("Colors", "Colors", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            int index = 11;

            DA.GetData(0, ref index);

            var colors = Alpaca4d.Colors.Gradient(index);

            // Finally assign the spiral to the output parameter.
            DA.SetDataList(0, colors);
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
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Colors__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{E8E95FB2-1A9E-4447-BF23-11171C02E400}");
    }
}