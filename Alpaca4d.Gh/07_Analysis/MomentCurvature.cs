using Grasshopper.Kernel;
using System;
using System.Collections.Generic;

namespace Alpaca4d.Gh
{
    public class MomentCurvature : GH_Component
    {
        public MomentCurvature()
          : base("MomentCurvature (Alpaca4d)", "MC",
            "",
            "Alpaca4d", "07_Analysis")
        {
            // Draw a Description Underneath the component
            this.Message = $"MomentCurvature\n(Alpaca4d)";
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("FiberSection", "FiberSection", "", GH_ParamAccess.item);
            pManager.AddNumberParameter("Axial", "Axial", "positive value - tension\nnegative value - compression", GH_ParamAccess.item);
            pManager.AddTextParameter("Direction", "Direction", "Rotate the structure along the y or z", GH_ParamAccess.item);
            pManager.AddIntegerParameter("NumIncr", "NumIncr", "", GH_ParamAccess.item);
            pManager.AddNumberParameter("MaxPhi", "MaxPhi", "", GH_ParamAccess.item);
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("log", "log", "");
            pManager.Register_DoubleParam("N", "N", "");
            pManager.Register_DoubleParam("My", "My", "");
            pManager.Register_DoubleParam("Mz", "Mz", "");
            pManager.Register_DoubleParam("ε", "ε", "");
            pManager.Register_DoubleParam("κy", "κy", "");
            pManager.Register_DoubleParam("κz", "κz", "");
            pManager.Register_GenericParam("fiberStressStrain", "fiberStressStrain", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Alpaca4d.Section.FiberSection fiberSection = new Alpaca4d.Section.FiberSection();
            DA.GetData(0, ref fiberSection);

            // hard code tag equal 1  because there will be only one section
            fiberSection.Id = 1;

            double axial = 0.0;
            DA.GetData(1, ref axial);

            string dir = "y";
            DA.GetData(2, ref dir);

            int numIncr = 1000;
            DA.GetData(3, ref numIncr);

            double maxPhi = 0.02;
            DA.GetData(4, ref maxPhi);

            string text = Alpaca4d.Template.MomentCurvature.Define(
                fiber: fiberSection,
                axialForce: axial,
                dof: dir,
                numIncr: numIncr,
                maxPhi: maxPhi);


            var model = new Model();
            model.Tcl.Add(text);

            bool fileExist = OnPingDocument().IsFilePathDefined;
            if (!fileExist)
            {
                throw new Exception("Have you saved the Grasshopper script?");
            }
            var filePath = OnPingDocument().FilePath;
            var currentDir = System.IO.Path.GetDirectoryName(filePath);
            System.IO.Directory.SetCurrentDirectory(currentDir);


            model.FileName = System.IO.Path.GetFullPath("MomentCurvature.tcl");
            model.Serialise();
            (string output, string error) = model.RunOpenSees();

            var forceFilePath = System.IO.Path.GetFullPath(Alpaca4d.Template.MomentCurvature.ForceFilePath);
            var forceData = System.IO.File.ReadAllLines(forceFilePath);

            var N = new List<double>();
            var My = new List<double>();
            var Mz = new List<double>();
            var T = new List<double>();

            foreach (string line in forceData)
            {
                var values = line.Split(new char[] { ' ' });
                N.Add(double.Parse(values[0]));
                My.Add(double.Parse(values[1]));
                Mz.Add(double.Parse(values[2]));
                T.Add(double.Parse(values[3]));
            }


            var deformationFilePath = System.IO.Path.GetFullPath(Alpaca4d.Template.MomentCurvature.DeformationFilePath);
            var deformationData = System.IO.File.ReadAllLines(deformationFilePath);

            var e = new List<double>();
            var ky = new List<double>();
            var kz = new List<double>();
            var g = new List<double>();

            foreach (string line in deformationData)
            {
                var values = line.Split(new char[] { ' ' });
                e.Add(double.Parse(values[0]));
                ky.Add(double.Parse(values[1]));
                kz.Add(double.Parse(values[2]));
                g.Add(double.Parse(values[3]));
            }

            
            var fiberResult = new Alpaca4d.Result.PointFiberResult();
            int i = 0;
            foreach(var fiber in fiberSection.Fibers)
            {
                (var stress, var strain) = Alpaca4d.Result.Read.FiberStress($"{Alpaca4d.Template.MomentCurvature.FiberStressFilePath}_{i}.out");
                fiberResult.Stress.AddRange(stress, new Grasshopper.Kernel.Data.GH_Path(i));
                fiberResult.Strain.AddRange(strain, new Grasshopper.Kernel.Data.GH_Path(i));
                fiberResult.Fibers.Add(fiber, new Grasshopper.Kernel.Data.GH_Path(i));
                i++;
            }


            DA.SetData(0, text);
            DA.SetDataList(1, N);
            DA.SetDataList(2, My);
            DA.SetDataList(3, Mz);
            DA.SetDataList(4, e);
            DA.SetDataList(5, ky);
            DA.SetDataList(6, kz);
            DA.SetData(7, fiberResult);
        }


        protected override void BeforeSolveInstance()
        {
            List<string> directions = new List<string> { "y", "z" };
            ValueListUtils.updateValueLists(this, 2, directions, null);
        }

        public override GH_Exposure Exposure => GH_Exposure.quinary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Moment_Curvature_Model__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{EA3284A5-4E95-4836-8663-60D8B2F5D6FE}");
    }
}