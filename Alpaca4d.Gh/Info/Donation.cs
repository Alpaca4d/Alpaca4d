using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Grasshopper;
using Grasshopper.Kernel;
using System.Diagnostics;

namespace Alpaca4d
{
    public class Paypal : GH_Component
    {
        public Paypal()
          : base("Donation (Alpaca4d)", "Donation",
            "Donation",
            "Alpaca4d", " Info")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddBooleanParameter("Donate?", "Donate?", "", GH_ParamAccess.item);
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_StringParam("Message", "Message", "");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            bool donate = false;
            DA.GetData(0, ref donate);

            string url = "https://www.paypal.com/paypalme/alpaca4d";

            if (donate)
            {
                {
                    try
                    {
                        Process.Start(url);
                        DA.SetData(0, "Thanks for considering becoming a sponsor!");
                    }
                    catch (Exception ex)
                    {
                        throw new Exception("Error: " + ex.Message);
                        DA.SetData(0, "An error occur!");
                    }
                }
            }
        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Donate_Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{B249A4F6-27F1-4DA2-B03C-E490384ED350}");
    }
}
