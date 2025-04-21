using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using Rhino;
using System;
using System.Linq;
using System.Text.RegularExpressions;
using System.Collections.Generic;

using Microsoft.CSharp.RuntimeBinder;
using Alpaca4d;
using Alpaca4d.Generic;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.TaskbarClock;
using System.Reflection;

namespace Alpaca4d.Gh
{
    public class NaturalVibrationAnalysis : GH_Component
    {
        private int counter = 0;
        private DateTime? firstTimeRun = DateTime.Now;
        private DateTime? lastTimeRun = null;
        public NaturalVibrationAnalysis()
          : base("Natural Vibration Analysis (Alpaca4d)", "NV",
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
            pManager.AddIntegerParameter("Vibration Modes", "Vibration Modes", "", GH_ParamAccess.item, 1);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddTextParameter("Solver", "Solver", "Connect a 'ValueList'\n-genBandArpack \n-symmBandLapack \n-fullGenLapack", GH_ParamAccess.item, "-fullGenLapack");
            pManager[pManager.ParamCount-1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("log", "log", "");
            pManager.Register_GenericParam("AlpacaModel", "AlpacaModel", "");
            pManager.Register_DoubleParam("Eigenvalues", "Eigenvalues", "");
            pManager.Register_DoubleParam("Period", "Period", "");
            pManager.Register_DoubleParam("Frequencies", "Frequencies", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var model = new Model();
            if (!DA.GetData(0, ref model)) return;

            var vibrationNumber = 1;
            DA.GetData(1, ref vibrationNumber);

            string solver = "";
            DA.GetData(2, ref solver);


            // Update last run time to the current DateTime
            lastTimeRun = DateTime.Now;

            if (counter == 0 || lastTimeRun - firstTimeRun > TimeSpan.FromMinutes(5))
            {
                // license routine
                if (!Alpaca4d.License.License.IsValid)
                {
                    if (model.Elements.Count > Alpaca4d.Gh.Forms.Advertise.NumberOfElements)
                    {
                        Alpaca4d.Gh.Forms.Advertise.Default();
                    }
                }
                firstTimeRun = DateTime.Now;
                counter++;
            }


            // create a shallow copy
            var analysisModel = model.ShallowCopy();
            analysisModel.Tcl = new List<string>(analysisModel.Tcl);

            bool fileExist = OnPingDocument().IsFilePathDefined;
            if (!fileExist)
            {
                throw new Exception("Have you saved the Grasshopper script?");
            }
            var filePath = OnPingDocument().FilePath;
            var currentDir = System.IO.Path.GetDirectoryName(filePath);
            System.IO.Directory.SetCurrentDirectory(currentDir);

            string recorderName = "recorder_eigen.mpco";
            analysisModel.ModalAnalysisReportFile = "ModalReport.txt";

            analysisModel.FileName = System.IO.Path.GetFullPath("AlpacaModel");


            // Recorder
            analysisModel.Recorders = new List<IRecorder>();
            var recorder = new Alpaca4d.Recorder();
            recorder = Alpaca4d.Recorder.MpcoEigen(recorderName);
            analysisModel.IsModal = true;
            analysisModel.NumberOfModes = vibrationNumber;

            analysisModel.Recorders.Add(recorder);
            analysisModel.Tcl.Add(recorder.WriteTcl());

            // Settings
            string eigenTcl = $"set lambdaN [eigen {solver} {vibrationNumber}]\n";
            analysisModel.Tcl.Add(eigenTcl);
            analysisModel.Tcl.Add("puts \"$lambdaN\"\n");
            analysisModel.Tcl.Add($"modalProperties -file \"{analysisModel.ModalAnalysisReportFile}\" -unorm\n");
            analysisModel.Tcl.Add("record\nwipe");

            analysisModel.Serialise();
            (var stdout, var stderr) = ((string, string))analysisModel.RunOpenSees();

            // clean string

            String[] separator = { "Italy.", "Using DomainModalProperties" };
            String[] lineSeparator = { "\r\n", " " };

            var eigenValue = stderr.Split(separator,
                   StringSplitOptions.RemoveEmptyEntries)[1].Trim().Split(lineSeparator, StringSplitOptions.RemoveEmptyEntries).Select(x => double.Parse(x.Trim())).ToList();


            var frequencies = eigenValue.Select(eigen => Math.Sqrt(eigen)/(2 * Math.PI)).ToList();
            var period = frequencies.Select(x => 1/x).ToList();

            // add error handling
            var log = new List<string>() {stderr};

            // Finally assign the spiral to the output parameter.
            DA.SetDataList(0, log);
            DA.SetData(1, analysisModel);
            DA.SetDataList(2, eigenValue);
            DA.SetDataList(3, period);
            DA.SetDataList(4, frequencies);
        }

        protected override void BeforeSolveInstance()
        {
            var resultTypes = new List<string>();

            var _resultTypes = new List<Analysis.Solver> { Analysis.Solver.genBandArpack, Analysis.Solver.symmBandLapack, Analysis.Solver.fullGenLapack };

            foreach(Analysis.Solver solver in _resultTypes)
			{
                var result = Alpaca4d.Helper.EnumHelper.SolverTypeConvert(solver);
                resultTypes.Add(result);
            }

            ValueListUtils.updateValueLists(this, 2, resultTypes, null);

        }


        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Run_Natural_Vibration_Analysis__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{F16B4D71-DBE1-4CDA-BAEE-A8CB82EE23C2}");
    }
}