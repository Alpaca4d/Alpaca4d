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
    internal class UniaxialElasticPerfectlyPlastic : SubComponent
    {
        public override string name() => "ElasticPerfectlyPlastic (Alpaca4d)";
        public override string display_name() => "ElasticPerfectlyPlastic";

        public override void registerEvaluationUnits(EvaluationUnitManager mngr)
        {
            EvaluationUnit evaluationUnit = new EvaluationUnit(name(), display_name(), "");
            evaluationUnit.Icon = Alpaca4d.Gh.Properties.Resources.uniaxial_Elastic_Material__Alpaca4d_;
            mngr.RegisterUnit(evaluationUnit);


            evaluationUnit.RegisterInputParam(new Param_String(), "Material Name", "MatName", "", GH_ParamAccess.item, new GH_String(""));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            // E, epsyP, epsyN=epsyP, eps0=0.0

            evaluationUnit.RegisterInputParam(new Param_Number(), "E", "E", $"Young Modulus [{Units.Force}/{Units.Length}²]", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "epsyP", "epsyP", $"", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "epsyN", "epsyN", "", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "eps0", "eps0", $"", GH_ParamAccess.item, new GH_Number(0));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "Rho", "Rho", $"Density [{Units.Mass}/{Units.Length}³]", GH_ParamAccess.item, new GH_Number(7850));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;
        }

        public override void SolveInstance(IGH_DataAccess DA, out string msg, out GH_RuntimeMessageLevel level)
        {
            msg = "UniaxialElasticPerfectlyPlastic not YET implemented";
            level = GH_RuntimeMessageLevel.Warning;

            string matName = null;
            double e = 210000000;
            double epsyP = double.NaN;
            double epsyN = double.NaN;
            double eps0 = 0.0;
            double rho = 7850.0;


            DA.GetData(0, ref matName);
            DA.GetData(1, ref e);
            DA.GetData(2, ref epsyP);
            DA.GetData(3, ref epsyN);
            DA.GetData(4, ref eps0);
            DA.GetData(5, ref rho);

            return;
        }

    }
}
