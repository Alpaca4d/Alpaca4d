using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using Alpaca4d;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class CustomCode : GH_Component
    {
        public CustomCode()
          : base("Custom code (Alpaca4d)", "CC",
            "Add a custom OpenSees code",
            "Alpaca4d", "10_Utility")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "Model to be serialized.", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddTextParameter("CustomCode", "CustomCode", "", GH_ParamAccess.list);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("AlpacaModel", "AlpacaModel", "");
            pManager.Register_StringParam("Tcl", "Tcl", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Model _model = null;
            if(!DA.GetData(0, ref _model))
            {
                _model = new Model();
                _model.Tcl = new List<string>();
            }

            List<string> customCode = new List<string>();
            DA.GetDataList(1, customCode);


            var analysisModel = _model.ShallowCopy();
            analysisModel.Tcl = new List<string>(analysisModel.Tcl);

            analysisModel.Tcl.AddRange(customCode);

            var tcl = analysisModel.Tcl;
            // Finally assign the spiral to the output parameter.
            DA.SetData(0, analysisModel);
            DA.SetDataList(1, tcl);
        }

        public override GH_Exposure Exposure => GH_Exposure.tertiary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Custom_code__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{4D46782D-0ABE-4097-8040-D9607C645165}");
    }
}