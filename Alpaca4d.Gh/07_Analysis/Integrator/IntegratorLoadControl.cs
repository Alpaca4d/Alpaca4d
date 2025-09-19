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
    internal class IntegratorLoadControl : SubComponent
    {
        public override string name() => "LoadControl";
        public override string display_name() => "LoadControl";

        public override void registerEvaluationUnits(EvaluationUnitManager mngr)
        {
            EvaluationUnit evaluationUnit = new EvaluationUnit(name(), display_name(), "Load Control Integrator");
            evaluationUnit.Icon = Alpaca4d.Gh.Properties.Resources.Load_Control_Integrator__Alpaca4d_;
            mngr.RegisterUnit(evaluationUnit);

            evaluationUnit.RegisterInputParam(new Param_Number(), "Lambda", "Lambda", "Load factor increment", GH_ParamAccess.item, new GH_Number(1));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Integer(), "NumIter", "NumIter", "Number of iterations", GH_ParamAccess.item, new GH_Integer(10));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "MinLambda", "MinLambda", "Minimum lambda value", GH_ParamAccess.item, new GH_Number(0.01));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "MaxLambda", "MaxLambda", "Maximum lambda value", GH_ParamAccess.item, new GH_Number(10));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;
        }

        public override void SolveInstance(IGH_DataAccess DA, out string msg, out GH_RuntimeMessageLevel level)
        {
            msg = "";
            level = GH_RuntimeMessageLevel.Warning;

            double lambda = 1;
            int? numIter = null;
            double? minLambda = null;
            double? maxLambda = null;

            DA.GetData(0, ref lambda);
            DA.GetData(1, ref numIter);
            DA.GetData(2, ref minLambda);
            DA.GetData(3, ref maxLambda);

            var integrator = Alpaca4d.Integrator.LoadControl(lambda, numIter, minLambda, maxLambda);

            DA.SetData(0, integrator);
        }
    }
}
