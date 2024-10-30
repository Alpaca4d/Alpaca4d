using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    public class AssembleModel : GH_Component
    {
        public AssembleModel()
          : base("AssembleModel (Alpaca4d)", "Assemble Model",
            "Assemble a Model",
            "Alpaca4d", "06_Assemble")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.NickName} \n{this.Category}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("Elements", "Elements", "", GH_ParamAccess.list);
            pManager.AddGenericParameter("Supports", "Supports", "", GH_ParamAccess.list);
            pManager.AddGenericParameter("LoadPatterns", "LoadPatterns", "", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Constraints", "Constraints", "", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Recorders", "Recorders", "", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Tolerance", "Tolerance", "", GH_ParamAccess.item, 0.01);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("AlpacaModel", "AlpacaModel", "");
            pManager.Register_DoubleParam("Mass", "Mass", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var element = new List<Alpaca4d.Generic.IElement>();
            var support = new List<Alpaca4d.Element.Support>();
            var loadPattern = new List<Alpaca4d.Loads.LoadPattern>();
            var constraint = new List<Alpaca4d.Generic.IConstraint>();
            var recorder = new List<Alpaca4d.Generic.IRecorder>();
            double tolerance = 0.01;


            if (!DA.GetDataList(0, element)) return;
            if (!DA.GetDataList(1, support)) return;
            DA.GetDataList(2, loadPattern);
            DA.GetDataList(3, constraint);
            DA.GetDataList(4, recorder);
            DA.GetData(5, ref tolerance);

            var model = new Model(element, support, loadPattern, constraint, recorder);
            model.Tollerance = tolerance;
            model.Assemble();
            
            // Finally assign the spiral to the output parameter.
            DA.SetData(0, model);
            DA.SetData(1, model.TotalMass);
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
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Assemble_Model__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("B6978C42-7B88-4F1A-A5DF-85EF89F154F9");
    }
}