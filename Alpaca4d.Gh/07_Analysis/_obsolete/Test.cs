using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Grasshopper.Kernel.Special;
using System.Linq;
using Alpaca4d;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    [Obsolete]
    public class Test : GH_Component
    {
        public Test()
          : base("Test (Alpaca4d)", "Test",
            "",
            "Alpaca4d", "07_Analysis")
        {
            // Draw a Description Underneath the component
            this.Message = $"Test (Alpaca4d)";
        }


        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("TestType", "TestType", "Connect a 'ValueList'\nNormUnbalance, NormDispIncr, EnergyIncr, RelativeNormUnbalance, RelativeNormDispIncr, RelativeTotalNormDispIncr, RelativeEnergyIncr, FixedNumIter", GH_ParamAccess.item, "EnergyIncr");
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Tollerance", "Tollerance", "", GH_ParamAccess.item, 1e-8);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Iteration", "Iteration", "", GH_ParamAccess.item, 10);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Flag", "Flag", "0 - Nothing\n1 - EachTime\n2 - Successful\n4 - EachStep\n5 - ErrorMessage", GH_ParamAccess.item, 0);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Norm", "Norm", "0 - MaxNorm, 1 - OneNorm, 2 - TwoNorm", GH_ParamAccess.item, 2);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("MaxIncr", "MaxIncr", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Test", "Test", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            ///
            var type = "EnergyIncr";
            DA.GetData(0, ref type);

            var testType = (Alpaca4d.Test.TestType) Enum.Parse(typeof(Alpaca4d.Test.TestType), type, true);

            double tol = 1e-8;
            DA.GetData(1, ref tol);

            int iter = 10;
            DA.GetData(2, ref iter);

            int flag = 0;
            DA.GetData(3, ref flag);
            var flagEnum = (Alpaca4d.Test.FlagType)flag;

            int norm = 2;
            DA.GetData(4, ref norm);
            var normEnum = (Alpaca4d.Test.NormType)norm;

            int maxIncr = 2;
            DA.GetData(5, ref maxIncr);

            var test = new Alpaca4d.Test(testType, tol, iter, flagEnum, normEnum, maxIncr);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, test);
        }

        protected override void BeforeSolveInstance()
        {
            List<string> resultTypes;

            resultTypes = Enum.GetNames(typeof(Alpaca4d.Test.TestType)).ToList();
            ValueListUtils.UpdateValueLists(this, 0, resultTypes, null);

        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.hidden;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Analysis_settings__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{4D7EAFC1-A0FF-473D-BB04-03DA99F6B41C}");
    }
}
