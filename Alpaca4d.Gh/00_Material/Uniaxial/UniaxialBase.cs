using Alpaca4d.UIWidgets;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Special;
using Grasshopper.Kernel.Types;
using Rhino.Geometry;
using Alpaca4d.UIWidgets;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Alpaca4d.Gh;

namespace Alpaca4d.Gh
{
    public class Uniaxial : GH_SwitcherComponent
    {
        private List<SubComponent> _subcomponents = new List<SubComponent>();
        public override string UnitMenuName => "Uniaxial";
        protected override string DefaultEvaluationUnit => _subcomponents[0].name();
        public override Guid ComponentGuid => new Guid("{4F1E13F9-0B35-4F8F-A324-883CEA2F8777}");
        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override Bitmap Icon => null;

        public Uniaxial()
            : base(" Uniaxial", " Uniaxial",
              "",
              "Alpaca4d", "00_Material")
        {
            ((GH_Component)this).Hidden = true;
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        protected override void RegisterInputParams(GH_InputParamManager pManager)
        {
        }

        protected override void RegisterOutputParams(GH_OutputParamManager pManager)
        {
            pManager.RegisterParam(new Param_GenericObject(), "Material", "Material", "Material");
        }

        protected override void RegisterEvaluationUnits(EvaluationUnitManager mngr)
        {
            _subcomponents.Add(new UniaxialElastic());
            _subcomponents.Add(new UniaxialElasticPerfectlyPlastic());

            foreach (SubComponent item in _subcomponents)
            {
                item.registerEvaluationUnits(mngr);
            }
        }

        protected override void OnComponentLoaded()
        {
            base.OnComponentLoaded();
            foreach (SubComponent item in _subcomponents)
            {
                item.OnComponentLoaded();
            }
        }

        protected override void SolveInstance(IGH_DataAccess DA, EvaluationUnit unit)
        {
            if (unit == null)
            {
                return;
            }
            foreach (SubComponent item in _subcomponents)
            {
                if (unit.Name.Equals(item.name()))
                {
                    item.SolveInstance(DA, out var msg, out var level);
                    if (msg != "")
                    {
                        ((GH_ActiveObject)this).AddRuntimeMessage(level, msg);
                    }
                    return;
                }
            }
            throw new Exception("Invalid sub-component");
        }
        // Part of the code that allows to extend the menu with additional items
        // Right click on the component to see the options
        public override void AppendAdditionalMenuItems(ToolStripDropDown menu)
        {
            base.AppendAdditionalMenuItems(menu);
        }
        private void Menu_ActivateUnit(object sender, EventArgs e)
        {
            try
            {
                EvaluationUnit evaluationUnit = (EvaluationUnit)((ToolStripMenuItem)sender).Tag;
                if (evaluationUnit != null)
                {
                    SwitchUnit(evaluationUnit);
                }
            }
            catch (Exception ex)
            {
                throw;
            }
        }
    }
}