using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

namespace Alpaca4d.Gh
{
    public class Concrete01 : GH_Component
    {
        public Concrete01()
          : base("Concrete01 (Alpaca4d)", "Concrete01",
            "Construct an Concrete01",
            "Alpaca4d", "00_Material")
        {
            this.Message = $"{this.Name}";
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Material Name", "MatName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fco", "fco", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("fcu", "fcu", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("EpsilonCo", "EpsilonCo", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddNumberParameter("EpsilonCu", "EpsilonCu", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;

            pManager.AddBooleanParameter("MinMax", "MinMax", "", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;


        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Material", "Material", "Material");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            string matName = null;
            double fpco = 28;
            double fpcu = 35;
            double epsilonc0 = 0.002;
            double epsilonCu = 0.0035;
            bool minMax = false;


            DA.GetData(0, ref matName);
            DA.GetData(1, ref fpco);
            DA.GetData(2, ref fpcu);
            DA.GetData(3, ref epsilonc0);
            DA.GetData(4, ref epsilonCu);
            DA.GetData(5, ref minMax);


            var material = new Alpaca4d.Material.Concrete01(matName, fpco, fpcu, epsilonc0, epsilonCu, minMax);


            DA.SetData(0, material);

        }

        public override GH_Exposure Exposure => GH_Exposure.tertiary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.concreate01;

        public override Guid ComponentGuid => new Guid("{57BF0FDB-B333-491C-B9EB-50783029B8C2}");
    }
}