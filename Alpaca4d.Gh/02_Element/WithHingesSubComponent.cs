using Alpaca4d.UIWidgets;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Types;
using Rhino.Geometry;
using System;
using System.Drawing;

namespace Alpaca4d.Gh
{
    internal class WithHingesSubComponent : SubComponent
    {
        public override string name() => "WithHinges (Alpaca4d)";
        public override string display_name() => "WithHinges";

        public override void registerEvaluationUnits(EvaluationUnitManager mngr)
        {
            EvaluationUnit evaluationUnit = new EvaluationUnit(name(), display_name(), "Construct a BeamWithHinges element using HingeRadau integration.");
            evaluationUnit.Icon = Alpaca4d.Gh.Properties.Resources.Force_Beam_Column__Alpaca4d_;
            mngr.RegisterUnit(evaluationUnit);

            evaluationUnit.RegisterInputParam(new Param_Curve(), "Line", "Line", $"[{Units.Length}]", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = false;

            evaluationUnit.RegisterInputParam(new Param_GenericObject(), "Section", "Section", "Interior cross-section.", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = false;

            evaluationUnit.RegisterInputParam(new Param_GenericObject(), "GeometricTransformation", "GeomTransf", "Optional geometric transformation. If omitted, Linear is used.", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Vector(), "ZAxis", "ZAxis", "Local Z-axis direction (optional).", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_GenericObject(), "ReleaseI", "ReleaseI", "Release condition at the I end.", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "LpI", "LpI", $"Plastic hinge length at I end [{Units.Length}].", GH_ParamAccess.item, new GH_Number(0.01));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_GenericObject(), "ReleaseJ", "ReleaseJ", "Release condition at the J end.", GH_ParamAccess.item);
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Number(), "LpJ", "LpJ", $"Plastic hinge length at J end [{Units.Length}].", GH_ParamAccess.item, new GH_Number(0.01));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;

            evaluationUnit.RegisterInputParam(new Param_Colour(), "Colour", "Colour", "", GH_ParamAccess.item, new GH_Colour(Color.FromArgb(255, 13, 13, 13)));
            evaluationUnit.Inputs[evaluationUnit.Inputs.Count - 1].Parameter.Optional = true;
        }

        public override void SolveInstance(IGH_DataAccess DA, out string msg, out GH_RuntimeMessageLevel level)
        {
            msg = "";
            level = GH_RuntimeMessageLevel.Warning;

            Curve line = null;
            if (!DA.GetData(0, ref line)) return;

            Alpaca4d.Generic.IUniaxialSection section = null;
            if (!DA.GetData(1, ref section)) return;

            Vector3d zAxis = Vector3d.Zero;
            if (DA.GetData(3, ref zAxis))
            {
                Plane perpFrame = Alpaca4d.Utils.PerpendicularFrame(line);
                zAxis = Alpaca4d.Utils.AlignPlane(perpFrame, zAxis).XAxis;
            }
            else
            {
                Plane perpFrame = Alpaca4d.Utils.PerpendicularFrame(line);
                zAxis = perpFrame.XAxis;
            }

            Alpaca4d.Element.GeomTransf geomTransf = null;
            if (!DA.GetData(2, ref geomTransf))
            {
                geomTransf = new Alpaca4d.Element.GeomTransf(Alpaca4d.Element.GeomTransfType.Linear, line, zAxis);
            }

            Alpaca4d.Element.Release releaseI = null;
            DA.GetData(4, ref releaseI);
            if (releaseI == null) releaseI = Alpaca4d.Element.Release.FullFixed;

            double lpI = 0.0;
            DA.GetData(5, ref lpI);

            Alpaca4d.Element.Release releaseJ = null;
            DA.GetData(6, ref releaseJ);
            if (releaseJ == null) releaseJ = Alpaca4d.Element.Release.FullFixed;

            double lpJ = 0.0;
            DA.GetData(7, ref lpJ);

            Color color = Color.FromArgb(255, 13, 13, 13);
            DA.GetData(8, ref color);

            var element = new Alpaca4d.Element.BeamWithHinges(line, section, geomTransf, releaseI, lpI, releaseJ, lpJ);
            element.Color = color;

            DA.SetData(0, element);
        }
    }
}
