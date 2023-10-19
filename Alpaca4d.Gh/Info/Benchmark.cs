using System;
using System.Collections.Generic;
using System.Diagnostics;
using Grasshopper.Kernel;
using Rhino.Geometry;

namespace Alpaca4d
{
    public class Benchmark : GH_Component
    {
        /// <summary>
        /// Initializes a new instance of the MyComponent1 class.
        /// </summary>
        public Benchmark()
          : base("Benchmark", "Alpaca4d Benchmark",
              "Get website with Alpaca4d/OpenSees Benchmark",
              "Alpaca4d", " Info")
        {
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddBooleanParameter("Benchmark", "Go to Benchmarks", "See the benchmark process and performace", GH_ParamAccess.item);
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            //pManager.Register_StringParam("Message", "Message", "");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            bool benchmark = false;
            DA.GetData(0, ref benchmark);

            string url = "https://alpaca4d.gitbook.io/docs/benchmark/intro";

            if (benchmark)
            {
                Process.Start(url);
            }
        }

        public override GH_Exposure Exposure => GH_Exposure.primary;
        protected override System.Drawing.Bitmap Icon => null;
        public override Guid ComponentGuid => new Guid("{ea517ec2-0ee8-401b-aba6-e1c0ef34adcc}");
    }
}