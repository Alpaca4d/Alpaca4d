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
    public class AnalysisSettings : GH_Component
    {
        public AnalysisSettings()
          : base("Analysis Settings (Alpaca4d)", "AnalysisSettings",
            "",
            "Alpaca4d", "07_Analysis")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.NickName} \n{this.Category}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("Damping", "Damping", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Constraint", "Constraint", "Connect a 'ValueList'\nPlain, Transformation", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Numberer", "Numberer", "Connect a 'ValueList'\nRCM, AMD, Plain", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("System", "System", "Connect a 'ValueList'\nBandGen, BandSPD, ProfileSPD, SuperLU, UmfPack, FullGeneral, SparseSYM", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Test", "Test", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Algorithm", "Algorithm", "Connect a 'ValueList'\nLinear, Newton, NewtonLineSearch, ModifiedNewton, KrylovNewton, SecantNewton, BFGS, Broyden", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("Integrator", "Integrator", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("AnalysisType", "AnalysisType", "Connect a 'ValueList'\nStatic, Transient", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddGenericParameter("AnalysisSteps", "AnalysisSteps", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Settings", "Settings", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            Alpaca4d.Damping damping = null;
            DA.GetData(0, ref damping);

            ///
            var constraint = "Transformation";
            DA.GetData(1, ref constraint);
            var constraintObj = new Constraint(constraint);

            
            ///
            var numberer = "RCM";
            DA.GetData(2, ref numberer);
            var numbererObj = new Numberer(numberer);

            ///
            var system = "BandGen";
            DA.GetData(3, ref system);
            var systemObj = new Alpaca4d.SystemEquation(system);

            ///
            var test = Alpaca4d.Test.EnergyIncr();
            DA.GetData(4, ref test);

            ///
            var algorithm = "ModifiedNewton";
            DA.GetData(5, ref algorithm);
            var algorithmObj = new Algorithm(algorithm);

            ///
            var integrator = Alpaca4d.Integrator.LoadControl(1);
            DA.GetData(6, ref integrator);

            ///
            var analysisType = "Static";
            DA.GetData(7, ref analysisType);
            var analysisObj = new Analysis(analysisType);


            var analysisStep = new Alpaca4d.AnalysisStep(1) as dynamic;
            DA.GetData(8, ref analysisStep);

            try
            {
                if(analysisStep.Value != null)
                {
                    if (analysisStep.Value.GetType() == typeof(string))
                    {
                        var step = (string)analysisStep.Value;
                        analysisStep = new Alpaca4d.AnalysisStep(step);
                    }
                    else if (analysisStep.Value.GetType() == typeof(int) || analysisStep.Value.GetType() == typeof(double))
                    {
                        var step = (int)analysisStep.Value;
                        analysisStep = new Alpaca4d.AnalysisStep(step);
                    }
                    else
                    {
                        analysisStep = analysisStep.Value;
                    }
                }
            }
            catch
            {
                // it is using the default value
            }

            if(analysisObj.Type == Analysis.AnalysisType.Transient)
            {
                if(((Alpaca4d.AnalysisStep)analysisStep).Dt  == null)
                {
                    AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Transient analysis requires an analysis step with Dt specified");
                    return;
                }
            }
            
            var settings = new Settings(constraintObj, numbererObj, systemObj, test, algorithmObj, integrator, analysisObj, analysisStep, damping);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, settings);
        }


        protected override void BeforeSolveInstance()
        {
            List<string> resultTypes;
            
            resultTypes = Enum.GetNames(typeof(Constraint.ConstraintType)).ToList();
            ValueListUtils.UpdateValueLists(this, 1, resultTypes, null);

            resultTypes = Enum.GetNames(typeof(Alpaca4d.Numberer.NumbererType)).ToList();
            ValueListUtils.UpdateValueLists(this, 2, resultTypes, null);

            resultTypes = Enum.GetNames(typeof(Alpaca4d.SystemEquation.SystemType)).ToList();
            ValueListUtils.UpdateValueLists(this, 3, resultTypes, null);

            resultTypes = Enum.GetNames(typeof(Alpaca4d.Algorithm.AlgorithmType)).ToList();
            ValueListUtils.UpdateValueLists(this, 5, resultTypes, null);

            resultTypes = Enum.GetNames(typeof(Alpaca4d.Analysis.AnalysisType)).ToList();
            ValueListUtils.UpdateValueLists(this, 7, resultTypes, null);

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
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Analysis_settings__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("9AE62757-69CC-4023-92EB-E8E1AA164AD0");
    }
}