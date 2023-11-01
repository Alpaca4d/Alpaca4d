using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    public class DisassembleMaterial_OBSOLETE : GH_Component
    {
        public DisassembleMaterial_OBSOLETE()
          : base("Disassemble Material (Alpaca4d)", "DM",
            "Disassemble a Material",
            "Alpaca4d", "00_Material")
        {
            this.Message = "Disassemble Material\n(Alpaca4d)";
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("Material", "Material", "", GH_ParamAccess.item);
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_StringParam("Name", "Name", "");
            pManager.Register_DoubleParam("E", "E", "");
            pManager.Register_DoubleParam("G", "G", "");
            pManager.Register_DoubleParam("v", "v", "");
            pManager.Register_DoubleParam("Rho", "Rho", "");
        }

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


        public override GH_Exposure Exposure => GH_Exposure.hidden;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.disassemble_material;

        public override Guid ComponentGuid => new Guid("{DC7692D4-1B63-4800-8AE4-FF88BA2C0715}");
    }
}