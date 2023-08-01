using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using Rhino;
using System;
using System.Linq;
using System.Collections.Generic;

using Microsoft.CSharp.RuntimeBinder;
using Alpaca4d;
using Alpaca4d.Generic;

using Eto.Forms;

namespace Alpaca4d.Gh
{
    public class RunAnalysis : GH_Component
    {
        public RunAnalysis()
          : base(" Run Analysis (Alpaca4d)", "RA",
            "",
            "Alpaca4d", "07_Analysis")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Settings", "Settings", "", GH_ParamAccess.item);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("log", "log", "");
            pManager.Register_GenericParam("AlpacaModel", "AlpacaModel", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {

            var model = new Model();
            var settings = new Settings();


            if (!DA.GetData(0, ref model)) return;
            if (!DA.GetData(1, ref settings)) return;


            if(DateTime.Now > Alpaca4d.License.License.FreeVersionDate)
            {
                if (model.Elements.Count > Alpaca4d.Gh.Forms.Advertise.NumberOfElements)
                {
                    Alpaca4d.Gh.Forms.Advertise.Default();
                }
            }

            // create a shallow copy
            var analysisModel = model.ShallowCopy();
            analysisModel.Tcl = new List<string>(analysisModel.Tcl);


            bool fileExist = OnPingDocument().IsFilePathDefined;
            if (!fileExist)
            {
                // hops issue
                var folderPath = System.IO.Directory.GetCurrentDirectory();
                System.IO.Directory.SetCurrentDirectory(folderPath);
            }
            else
            {
                var filePath = OnPingDocument().FilePath;
                var currentDir = System.IO.Path.GetDirectoryName(filePath);
                System.IO.Directory.SetCurrentDirectory(currentDir);
            }

            string recorderName = "recorder.mpco";

            analysisModel.FileName = System.IO.Path.GetFullPath("AlpacaModel");


            analysisModel.Recorders = new List<IRecorder>();

            analysisModel.Settings = settings;
            // Recorder
            var recorder = new Alpaca4d.Recorder();
            if (settings.Analysis.Type == Analysis.AnalysisType.Static)
            {
                recorder = Alpaca4d.Recorder.MpcoStatic(recorderName);
                analysisModel.IsStatic = true;
            }

            if (settings.Analysis.Type == Analysis.AnalysisType.Transient)
            {
                recorder = Alpaca4d.Recorder.MpcoTransient(recorderName);
                analysisModel.IsTransient = true;
            }
            analysisModel.Recorders.Add(recorder);
            analysisModel.Tcl.Add(recorder.WriteTcl());

            // Settings
            analysisModel.Tcl.Add(settings.WriteTcl());
            analysisModel.Tcl.Add("wipe");

            analysisModel.Serialise();
            (var output, var error) = ((string, string))analysisModel.RunOpenSees();

            String[] separator = { "Italy."};
            var log = error.Split(separator, StringSplitOptions.RemoveEmptyEntries);
            if(log.Count() != 1)
            {
                if (error.Contains("WARNING") && error.Contains("failed"))
                {
                    AddRuntimeMessage(GH_RuntimeMessageLevel.Error, "Analysis Failed");
                    analysisModel = null;
                }
                else if (error.Contains("WARNING"))
                {
                    AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Warning! Double check the log!");
                    analysisModel = null;
                }
                DA.SetData(0, log[1]);
                DA.SetData(1, analysisModel);
            }
            else
            {
                DA.SetData(0, error);
                DA.SetData(1, analysisModel);
            }

        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Run_Analysis__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("46711AB3-D3BC-437B-A2DD-91BED579346D");
    }
}