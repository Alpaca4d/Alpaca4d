using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;

using Alpaca4d.TimeSeries;
using Alpaca4d.Loads;
using System.Linq;

namespace Alpaca4d.Gh
{
    [Obsolete]
    public class UniformExcitationPattern : GH_Component
    {
        public UniformExcitationPattern()
          : base("Uniform Excitation (Alpaca4d)", "Uniform Excitation",
            "Construct a Uniform Excitation Load",
            "Alpaca4d", "05_Load")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.NickName} \n{this.Category}";
        }

        /// pattern UniformExcitation $patternTag $dir -accel $tsTag <-vel0 $vel0> <-fact $cFactor>

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Dof", "Dof", "Degree of freedom direction the ground motion acts\n" + 
            "x : corresponds to translation along the global X axis\n" +
            "y : corresponds to translation along the global Y axis\n" +
            "z : corresponds to translation along the global Z axis\n" +
            "xx : corresponds to rotation about the global X axis\n" +
            "yy : corresponds to rotation about the global Y axis\n" +
            "zz : corresponds to rotation about the global Z axis\n", GH_ParamAccess.item);
            pManager.AddGenericParameter("TimeSeries", "TimeSeries", "", GH_ParamAccess.item);
            pManager.AddNumberParameter("Velocity", "Velocity", $"The initial velocity [{Units.Length}/s]", GH_ParamAccess.item, 0);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Factor", "Factor", "Constant factor", GH_ParamAccess.item, 1);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("UniformExcitation", "UniformExcitation", "");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            string _direction = "X";
            if (!DA.GetData(0, ref _direction)) return;

            Alpaca4d.Generic.ITimeSeries timeSeries = null;
            if (!DA.GetData(1, ref timeSeries)) return;

            double velocity = 0;
            DA.GetData(2, ref velocity);

            double factor = 1;
            DA.GetData(3, ref factor);

            var direction = (Alpaca4d.Loads.Direction)Enum.Parse(typeof(Alpaca4d.Loads.Direction), _direction, true);

            var load = Alpaca4d.Loads.LoadPattern.CreateUniformExcitation(direction, timeSeries, velocity, factor);

            DA.SetData(0, load);
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.hidden;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Uniform_excitation;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{2064D9F5-EFCB-4D35-8389-3BEC2F87E413}");

        protected override void BeforeSolveInstance()
        {
            List<string> directions;

            directions = Enum.GetNames(typeof(Loads.Direction)).ToList();
            ValueListUtils.UpdateValueLists(this, 0, directions, null);
        }

    }
}
