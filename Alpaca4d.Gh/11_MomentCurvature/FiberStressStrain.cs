using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;


namespace Alpaca4d.Gh
{
    public class FiberStressStrain : GH_Component
    {
        public FiberStressStrain()
          : base("Fiber Stress Strain (Alpaca4d)", "FBS",
            "Splits a MomentCurvature fibre result into its fibres, stresses and strains - one branch per fibre.",
            "Alpaca4d", "MomentCurvature_βeta")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("FiberStressStrain", "FiberStressStrain",
                "The fiberStressStrain output of a MomentCurvature component.",
                GH_ParamAccess.item);
        }


        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("FiberPoint", "FiberPoint", "The fibres of the analysed section, one branch each.");
            pManager.Register_GenericParam("Stress", "Stress", "Stress history of each fibre, in kN/m2, one branch per fibre.");
            pManager.Register_GenericParam("Strain", "Strain", "Strain history of each fibre, dimensionless, one branch per fibre.");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Alpaca4d.Result.PointFiberResult fiberPointResult = null;

            if (!DA.GetData(0, ref fiberPointResult) || fiberPointResult == null)
                return;

            // Stress on the Stress output and strain on the Strain one; these two were
            // handed to each other's parameter.
            DA.SetDataTree(0, fiberPointResult.Fibers);
            DA.SetDataTree(1, fiberPointResult.Stress);
            DA.SetDataTree(2, fiberPointResult.Strain);
        }

        public override GH_Exposure Exposure => GH_Exposure.quarternary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Fiber_Stress_Strain__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{34dc5969-e0e4-4acf-9790-0af2c22cfeb9}");
    }
}