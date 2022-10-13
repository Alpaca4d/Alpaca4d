﻿using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using Alpaca4d;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
    public class Serialize : GH_Component
    {
        public Serialize()
          : base("Serialize (Alpaca4d)", "SLRZ",
            "Serialize a model and write the content to a file",
            "Alpaca4d", "10_Utility")
        {
            // Draw a Description Underneath the component
            this.Message = "Serialize (Alpaca4d)";
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
            pManager.Register_StringParam("Tcl", "Tcl", "");
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

            bool save = false;
            DA.GetData(2, ref save);


            string filePath = null;
            DA.GetData(1, ref filePath);

            var tclText = model.Tcl;

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
			else if(filePath != null && save == true)
			{
                System.IO.File.WriteAllLines(filePath, tclText);
			}
            

            // Finally assign the spiral to the output parameter.
            DA.SetDataList(0, tclText);
        }

        public override GH_Exposure Exposure => GH_Exposure.secondary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Serialize;
        public override Guid ComponentGuid => new Guid("{5C46782D-0ABE-4097-8040-D9607C645165}");
    }
}