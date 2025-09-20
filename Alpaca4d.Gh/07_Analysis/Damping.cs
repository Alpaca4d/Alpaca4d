using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    public class Damping : GH_Component
    {
        public Damping()
          : base("Damping (Alpaca4d)", "Damping",
            "This command is used to assign damping to all previously-defined elements and nodes. When using rayleigh damping in OpenSees, the damping matrix for an element or node, D is specified as a combination of stiffness and mass-proportional damping matrices:" +
                "\nD = alphaM * M + [betaKcurrent * Kcurrent] + [betaKinit * Kinit] + [betaKcomm * KlastCommit]" +
                "\nxDamp = 0.05;                        # 5% damping ratio" +
                "\nalphaM = 0.00;                       # M-prop damping;                               alphaM*M" +
                "\nbetaKcurrent = 0.00;                 # K-proportional damping;                       beatKcurr*KCurrent" +
                "\nbetaKinit = 0.00;                    # initial-stiffness proportional damping;       beatKinit*Kinit" +
                "\nbetaKcomm = 2.*xDamp/omega;          # K-prop. damping parameter;                    betaKcomm*KlastCommitt",
            "Alpaca4d", "07_Analysis")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }


        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddNumberParameter("AlphaM", "AlphaM", "factor applied to elements or nodes mass matrix", GH_ParamAccess.item, 0.0);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("BetaKCurr", "BetaKCurr", "factor applied to elements current stiffness matrix.", GH_ParamAccess.item, 0.0);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("BetaKInit", "BetaKInit", "factor applied to elements initial stiffness matrix.", GH_ParamAccess.item, 0.0);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("BetaKComm", "BetaKComm", "factor applied to elements committed stiffness matrix.", GH_ParamAccess.item);
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Damping", "Damping", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {

            double alphaM = 0.0;
            DA.GetData(0, ref alphaM);

            double betaKCurr = 0.00;
            DA.GetData(1, ref betaKCurr);

            double betaKInit = 0.00;
            DA.GetData(2, ref betaKInit);

            double betaKComm = 0.00;
            DA.GetData(3, ref betaKComm);


            var damping = new Alpaca4d.Damping(alphaM, betaKCurr, betaKInit, betaKComm);

            DA.SetData(0, damping);
        }



        public override GH_Exposure Exposure => GH_Exposure.quarternary;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Rayleigh_Damping__Alpaca4d_;


        public override Guid ComponentGuid => new Guid("{EB8C2885-7DEF-4B12-B978-FD81A1A5763E}");
    }
}