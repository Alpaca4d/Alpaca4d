using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Linq;
using System.Collections.Generic;


using Alpaca4d.Generic;
using Alpaca4d.Result;

namespace Alpaca4d.Gh
{
    public class BeamForce : GH_Component
    {
        public BeamForce()
          : base("Beam Forces (Alpaca4d)", "Beam Forces",
            "Read the Beam Forces",
            "Alpaca4d", "08_NumericalOutput")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "", GH_ParamAccess.item);
            pManager.AddBooleanParameter("History", "History", "not implemented", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Step", "Step", "", GH_ParamAccess.item, 0);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("N", "N", $"[{Units.Force}]");
            pManager.Register_GenericParam("Vy", "Vy", $"[{Units.Force}]");
            pManager.Register_GenericParam("Vz", "Vz", $"[{Units.Force}]");
            pManager.Register_GenericParam("Mx", "Mx", $"[{Units.Force}{Units.Length}]");
            pManager.Register_GenericParam("My", "My", $"[{Units.Force}{Units.Length}]");
            pManager.Register_GenericParam("Mz", "Mz", $"[{Units.Force}{Units.Length}]");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var alpacaModel = new Alpaca4d.Model();
            bool history = false;
            int step = 0;

            if (!DA.GetData(0, ref alpacaModel)) return;
            DA.GetData(1, ref history);
            DA.GetData(2, ref step);


            (var n, var mz, var vy,var my,var vz,var t) = Alpaca4d.Result.Read.ForceBeamColumn(alpacaModel, step);


            // Convert Nested List to DataTree
            var nTree = Utils.DataTreeFromNestedList(n);
            var mzTree = Utils.DataTreeFromNestedList(mz);
            var vyTree = Utils.DataTreeFromNestedList(vy);
            var myTree = Utils.DataTreeFromNestedList(my);
            var vzTree = Utils.DataTreeFromNestedList(vz);
            var tTree = Utils.DataTreeFromNestedList(t);


            // Finally assign the spiral to the output parameter.
            DA.SetDataTree(0, nTree);
            DA.SetDataTree(1, vyTree);
            DA.SetDataTree(2, vzTree);
            DA.SetDataTree(3, tTree);
            DA.SetDataTree(4, myTree);
            DA.SetDataTree(5, mzTree);
        }

        
        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.secondary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Beam_Forces__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{F25101E7-06B9-41C0-8BF1-F55ED08A4630}");
    }
}