using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    public class DisassembleMaterial : GH_Component
    {
        public DisassembleMaterial()
          : base("Disassemble Material (Alpaca4d)", "DM",
            "Disassemble a Material",
            "Alpaca4d", "00_Material")
        {
            this.Message = "Disassemble Material\n(Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_StringParam("Name", "Name", "");
            pManager.Register_DoubleParam("E", "E", "");
            pManager.Register_DoubleParam("G", "G", "");
            pManager.Register_DoubleParam("v", "v", "");
            pManager.Register_DoubleParam("Rho", "Rho", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            dynamic material = null;
            DA.GetData(0, ref material);


            var name = material.Value.MatName;
            var E = material.Value.E;
            var G = material.Value.G;
            var v = material.Value.Nu;
            var rho = material.Value.Rho;


            DA.SetData(0, name);
            DA.SetData(1, E);
            DA.SetData(2, G);
            DA.SetData(3, v);
            DA.SetData(4, rho);
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
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.disassemble_material;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{DC7692D4-1B63-4800-8AE4-FF88BA2C0715}");
    }
}