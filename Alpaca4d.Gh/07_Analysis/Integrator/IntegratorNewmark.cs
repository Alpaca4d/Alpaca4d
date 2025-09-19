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
    internal class IntegratorNewmark : SubComponent
    {
        public override string name() => "Newmark";
        public override string display_name() => "Newmark";

        public override void registerEvaluationUnits(EvaluationUnitManager mngr)
        {
            EvaluationUnit evaluationUnit = new EvaluationUnit(name(), display_name(), "Newmark Integration Method");
            evaluationUnit.Icon = Alpaca4d.Gh.Properties.Resources.Newmark_Integrator__Alpaca4d_;
            mngr.RegisterUnit(evaluationUnit);

            evaluationUnit.RegisterInputParam(new Param_Number(), "Gamma", "Gamma", "Gamma parameter", GH_ParamAccess.item, new GH_Number(0.5));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "Beta", "Beta", "Beta parameter", GH_ParamAccess.item, new GH_Number(0.25));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;
        }

        public override void SolveInstance(IGH_DataAccess DA, out string msg, out GH_RuntimeMessageLevel level)
        {
            msg = "";
            level = GH_RuntimeMessageLevel.Warning;

            double gamma = 0.5;
            double beta = 0.25;

            DA.GetData(0, ref gamma);
            DA.GetData(1, ref beta);

            var integrator = Alpaca4d.Integrator.Newmark(gamma, beta);

            DA.SetData(0, integrator);
        }
    }
}
