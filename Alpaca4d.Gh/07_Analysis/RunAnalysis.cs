using Alpaca4d;
using Alpaca4d.Generic;
using Alpaca4d.License;
using Eto.Forms;
using GH_IO.Serialization;
using Grasshopper;
using Grasshopper.Kernel;
using Microsoft.CSharp.RuntimeBinder;
using Rhino;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Windows.Forms;

namespace Alpaca4d.Gh
{
    public class RunAnalysis : GH_Component
    {
        private int counter = 0;
        private DateTime? firstTimeRun = DateTime.Now;
        private DateTime? lastTimeRun = null;

        public RunAnalysis()
          : base(" Run Analysis (Alpaca4d)", "RA",
            "",
            "Alpaca4d", "07_Analysis")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
            this._settings = true;
        }

        public bool _settings { get; set; }

        public override bool Write(GH_IWriter writer)
        {
            // Save the version when this component was created
            writer.SetBoolean("settings", _settings);
            return base.Write(writer);
        }

        public override bool Read(GH_IReader reader)
        {
            // Read the version when this component was created
            try
            {
                _settings = reader.GetBoolean("settings");
            }
            catch (NullReferenceException) { } // In case the info component was created before the VersionWhenFirstCreated was implemented.
            return base.Read(reader);
        }

        protected override void AppendAdditionalComponentMenuItems(System.Windows.Forms.ToolStripDropDown menu)
        {
            // Append the item to the menu, making sure it's always enabled and checked if Absolute is True.
            ToolStripMenuItem item = Menu_AppendItem(menu, "Do not use settings", Menu_AbsoluteClicked, null, true, !_settings);
        }

        private void Menu_AbsoluteClicked(object sender, EventArgs e)
        {
            _settings = !_settings;
            ExpireSolution(true);
        }




        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "", GH_ParamAccess.item);
            pManager.AddGenericParameter("Settings", "Settings", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
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
            Settings settings = null;


            if (!DA.GetData(0, ref model)) return;
            
            DA.GetData(1, ref settings);
            if (_settings == true && settings == null)
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Input parameter Settings failed to collect data");
                return;
            }


            // Validate license
            if (!Alpaca4d.License.License.ValidateLicense(model, false, () => Alpaca4d.UI.LicenseManagementForm.ShowForm(), Alpaca4d.Gh.Forms.Advertise.NumberOfElements))
            {
                // add a warning on component saying that the message will be shown every 5 minutes
                AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "License validation failed. The license management form will be shown every 5 minutes.");
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


            analysisModel.FileName = System.IO.Path.GetFullPath("AlpacaModel");



            if(settings != null)
            {
                string recorderName = "recorder.mpco";
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
            }


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