using Grasshopper;
using Grasshopper.Kernel;
using System;
using System.Drawing;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

namespace Alpaca4d.Gh
{
    public class Info : GH_AssemblyInfo
    {
        public override string Name => "Alpaca4d";
        public override Bitmap Icon => null;
        public override string Description => "Alpaca4d is a Grasshopper plugin which has been developed on top of OpenSees. It lets you analyse beam, shell and brick elements through Static, Dynamic, Linear and Not Linear Analysis.";
        public override Guid Id => new Guid("52A09029-AC68-4356-803D-724D05588549");
        public override string AuthorName => "Marco Pellegrino";
        public override string AuthorContact => "pellegrino.marco@icloud.com";

        public override string AssemblyVersion
        {
            get
            {
                IEnumerable<AssemblyName> assembly = Assembly.GetExecutingAssembly().GetReferencedAssemblies().Where(x => x.Name.Contains("Alpaca4d.Core"));
                string assemblyVersion = assembly.First().Version?.ToString();
                return assemblyVersion;
            }
        }
    }

    public class Alpaca4dCategoryIcon : Grasshopper.Kernel.GH_AssemblyPriority
    {
        public override Grasshopper.Kernel.GH_LoadingInstruction PriorityLoad()
        {
            Grasshopper.Instances.ComponentServer.AddCategoryIcon("Alpaca4d", Alpaca4d.Gh.Properties.Resources.Logo);
            Grasshopper.Instances.ComponentServer.AddCategorySymbolName("Alpaca4d", 'A');
            return Grasshopper.Kernel.GH_LoadingInstruction.Proceed;
        }
    }

    public class License : GH_Component
    {
        public License()
          : base(" License (Alpaca4d)", "License",
            "License",
            "Alpaca4d", " Info")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.NickName}\n{"Alpaca4d"}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("License", "License", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var license = new List<string>();
            license.Add("Alpaca4d has been developed on top of OpenSees.");
            license.Add("You are free to use this program, but everything is subject to the OpenSees license terms.");
            license.Add("");
            license.Add("LICENSE TERMS");
            license.Add(Alpaca4d.Gh.Properties.Resources.License);

            // Finally assign the spiral to the output parameter.
            DA.SetDataList(0, license);
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
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Logo;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{AE522510-4F2D-4E11-BDF4-FB0B135EDBEB}");
    }

}