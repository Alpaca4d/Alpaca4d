﻿using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;


namespace Alpaca4d.Gh
{
    public class FiberStressStrain : GH_Component
    {
        public FiberStressStrain()
          : base("Fiber Stress Strain (Alpaca4d)", "Fiber Stress Strain",
            "Read the stress strain in a fiber",
            "Alpaca4d", "08_NumericalOutput")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }


        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("FiberStressStrain", "FiberStressStrain", "", GH_ParamAccess.item);
        }


        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("FiberPoint", "FiberPoint", "");
            pManager.Register_GenericParam("Stress", "Stress", "");
            pManager.Register_GenericParam("Strain", "Strain", "");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Alpaca4d.Result.PointFiberResult fiberPointResult = null;

            DA.GetData(0, ref fiberPointResult);

            var fiberPoint = fiberPointResult.Fibers;
            var stress = fiberPointResult.Stress;
            var strain = fiberPointResult.Strain;

            // Finally assign the spiral to the output parameter.
            DA.SetDataTree(0, fiberPoint);
            DA.SetDataTree(1, strain);
            DA.SetDataTree(2, stress);
        }


        public override GH_Exposure Exposure => GH_Exposure.senary;


        protected override System.Drawing.Bitmap Icon => null;


        public override Guid ComponentGuid => new Guid("{34dc5969-e0e4-4acf-9790-0af2c22cfeb9}");
    }
}