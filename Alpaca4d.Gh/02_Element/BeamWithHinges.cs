using Alpaca4d.UIWidgets;
using Grasshopper.Kernel;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace Alpaca4d.Gh
{
    public class BeamWithHinges : GH_SwitcherComponent
    {
        private readonly List<SubComponent> _subcomponents = new List<SubComponent>();

        public override string UnitMenuName => "Element Type";
        protected override string DefaultEvaluationUnit => "Beam (Alpaca4d)";

        public BeamWithHinges()
          : base("Beam With Hinges (Alpaca4d)", "Beam With Hinges",
            "Construct a beam element. Switch between a standard ForceBeamColumn (Beam) " +
            "and a beam with plastic hinge zones (WithHinges).",
            "Alpaca4d", "02_Element")
        {
            ((GH_Component)this).Hidden = false;
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        protected override void RegisterInputParams(GH_InputParamManager pManager) { }

        protected override void RegisterOutputParams(GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Element", "Element", "Beam element.");
        }

        protected override void RegisterEvaluationUnits(EvaluationUnitManager mngr)
        {
            _subcomponents.Add(new BeamSubComponent());
            _subcomponents.Add(new WithHingesSubComponent());

            foreach (var sub in _subcomponents)
                sub.registerEvaluationUnits(mngr);
        }

        protected override void OnComponentLoaded()
        {
            base.OnComponentLoaded();
            foreach (var sub in _subcomponents)
                sub.OnComponentLoaded();
        }

        protected override void SolveInstance(IGH_DataAccess DA, EvaluationUnit unit)
        {
            if (unit == null) return;

            foreach (var sub in _subcomponents)
            {
                if (unit.Name.Equals(sub.name()))
                {
                    sub.SolveInstance(DA, out var msg, out var level);
                    if (!string.IsNullOrEmpty(msg))
                        ((GH_ActiveObject)this).AddRuntimeMessage(level, msg);
                    return;
                }
            }

            throw new Exception("Invalid sub-component");
        }

        public override void AppendAdditionalMenuItems(ToolStripDropDown menu)
        {
            base.AppendAdditionalMenuItems(menu);
        }

        public override GH_Exposure Exposure => GH_Exposure.secondary;

        protected override Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Force_Beam_Column__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("A1B2C3D4-E5F6-7A8B-9C0D-E1F2A3B4C5D6");
    }
}
