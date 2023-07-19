using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using Alpaca4d;
using System.Collections.Generic;
using FemDesign;
using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class FEM_Design : GH_Component
    {
        public FEM_Design()
          : base("Export to FEM-Design (Alpaca4d)", "Export to FEM-Design",
            "",
            "Alpaca4d", "10_Utility")
        {
            // Draw a Description Underneath the component
            this.Message = "Export to FEM-Design (Alpaca4d)";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "Model to be serialized.", GH_ParamAccess.item);
            pManager.AddTextParameter("FilePath", "FilePath", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddBooleanParameter("Save", "Save", "", GH_ParamAccess.item, true);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("FEM-Design Model", "FEM-Design Model", "");
            pManager.Register_StringParam(".struxml", ".struxml", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Model model = null;
            DA.GetData(0, ref model);

            string filePath = null;
            DA.GetData(1, ref filePath);

            bool save = false;
            DA.GetData(2, ref save);

            var struxml = new List<string>();
            FemDesign.Model fdModel = null;

            if (filePath == null && save == true)
            {
                bool fileExist = OnPingDocument().IsFilePathDefined;
                if (!fileExist)
                {
                    AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "Save your .gh script or specfy a FilePath.");
                    return;
                }
                filePath = OnPingDocument().FilePath;
                filePath = System.IO.Path.ChangeExtension(filePath, "tcl");
            }

            // Finally assign the spiral to the output parameter.
            DA.SetDataList(0, struxml);
            DA.SetData(1, fdModel);
        }

        public override GH_Exposure Exposure => GH_Exposure.secondary;
        protected override System.Drawing.Bitmap Icon => null;
        public override Guid ComponentGuid => new Guid("{29735140-F6E6-4E31-9282-87708CE6682D}");
    }
}