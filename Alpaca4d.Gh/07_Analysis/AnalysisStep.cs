﻿using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    public class AnalysisStep : GH_Component
    {
        public AnalysisStep()
          : base("Analysis Step (Alpaca4d)", "AnalysisStep",
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
            pManager.AddIntegerParameter("NumIncr", "NumIncr", "", GH_ParamAccess.item, 1);
            pManager.AddNumberParameter("Dt", "Dt", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("DtMin", "DtMin", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("DtMax", "DtMax", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Jd", "Jd", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("AnalysisStep", "AnalysisStep", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            int cNumIncr = 1;
            double? dt = null;
            double? dtMin = null;
            double? dtMax = null;
            double? jD = null;


            if (!DA.GetData(0, ref cNumIncr)) return;
            DA.GetData(1, ref dt);
            DA.GetData(2, ref dtMin);
            DA.GetData(3, ref dtMax);
            DA.GetData(4, ref jD);


            var steps = new Alpaca4d.AnalysisStep(cNumIncr, dt, dtMin, dtMax, jD);

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, steps);
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
        public override Guid ComponentGuid => new Guid("{825E700F-52D7-433D-92F6-8B6730F0A217}");
    }
}