using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Grasshopper;
using Grasshopper.Kernel;
using System.Diagnostics;

namespace Alpaca4d.Gh
{
    [Obsolete]
    public class Patreon : GH_Component
    {
        public Patreon()
          : base("Sponsor (Alpaca4d)", "Sponsor",
            "Sponsor",
            "Alpaca4d", " Info")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.NickName}\n{"Alpaca4d"}";
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddBooleanParameter("Sponsor?", "Sponsor?", "", GH_ParamAccess.item);
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_StringParam("Message", "Message", "");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            bool sponsor = false;
            DA.GetData(0, ref sponsor);

            string url = "https://www.patreon.com/Alpaca4d";

            if (sponsor)
            {
                {
                    try
                    {
                        Process.Start(url);
                        DA.SetData(0, "Thanks for considering becoming a sponsor!");
                    }
                    catch (Exception ex)
                    {
                        DA.SetData(0, "An error occur!");
                        throw new Exception("Error: " + ex.Message);
                    }
                }
            }
        }

        public override GH_Exposure Exposure => GH_Exposure.hidden;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Patreon_Supporter__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{4B01AE72-F80C-4451-9747-EAE1C338B453}");
    }
}
