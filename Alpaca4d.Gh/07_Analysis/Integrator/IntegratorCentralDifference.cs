using Alpaca4d.UIWidgets;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Types;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alpaca4d.Gh
{
    internal class IntegratorCentralDifference : SubComponent
    {
        public override string name() => "CentralDifference";
        public override string display_name() => "CentralDiff";

        public override void registerEvaluationUnits(EvaluationUnitManager mngr)
        {
            EvaluationUnit evaluationUnit = new EvaluationUnit(name(), display_name(), "Central Difference Integration Method");
            evaluationUnit.Icon = Alpaca4d.Gh.Properties.Resources.Central_Difference__Alpaca4d_;
            mngr.RegisterUnit(evaluationUnit);

            // Central Difference has no parameters, so no input parameters to register
        }

        public override void SolveInstance(IGH_DataAccess DA, out string msg, out GH_RuntimeMessageLevel level)
        {
            msg = "";
            level = GH_RuntimeMessageLevel.Warning;

            var integrator = Alpaca4d.Integrator.CentralDifference();

            DA.SetData(0, integrator);
        }
    }
}
