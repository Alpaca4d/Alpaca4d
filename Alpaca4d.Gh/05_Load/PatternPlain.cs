using Alpaca4d.UIWidgets;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Types;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.TimeSeries;
using Alpaca4d.Loads;
using Alpaca4d.Generic;

namespace Alpaca4d.Gh
{
    internal class PatternPlain : SubComponent
    {
        public override string name() => "PlainPattern";
        public override string display_name() => "PlainPattern";

        public override void registerEvaluationUnits(EvaluationUnitManager mngr)
        {
            EvaluationUnit evaluationUnit = new EvaluationUnit(name(), display_name(), "Plain Load Pattern");
            evaluationUnit.Icon = Alpaca4d.Gh.Properties.Resources.Load_pattern__Alpaca4d_;
            mngr.RegisterUnit(evaluationUnit);

            evaluationUnit.RegisterInputParam(new Param_GenericObject(), "TimeSeries", "TimeSeries", "Time series for the load pattern", GH_ParamAccess.item, new GH_ObjectWrapper(TimeSeries.Constant.Default()));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_GenericObject(), "Loads", "Loads", "List of loads to apply", GH_ParamAccess.list, new GH_ObjectWrapper(null));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = false;

            evaluationUnit.RegisterInputParam(new Param_Number(), "Factor", "Factor", "Constant factor", GH_ParamAccess.item, new GH_Number(1));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;
        }

        public override void SolveInstance(IGH_DataAccess DA, out string msg, out GH_RuntimeMessageLevel level)
        {
            msg = "";
            level = GH_RuntimeMessageLevel.Warning;

            Alpaca4d.Generic.ITimeSeries timeSeries = TimeSeries.Constant.Default();
            DA.GetData(0, ref timeSeries);

            List<ILoad> loads = new List<ILoad>();
            DA.GetDataList(1, loads);

            double factor = 1;
            DA.GetData(2, ref factor);

            var load = new Alpaca4d.Loads.LoadPattern(PatternType.Plain, timeSeries, loads, factor);

            DA.SetData(0, load);
        }
    }
}
