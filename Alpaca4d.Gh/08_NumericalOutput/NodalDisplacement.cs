using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Linq;
using System.Collections.Generic;


using Alpaca4d.Generic;
using Alpaca4d.Result;

namespace Alpaca4d.Gh
{
    public class NodalDisplacement : GH_Component
    {
        public NodalDisplacement()
          : base("Nodal Displacements (Alpaca4d)", "ND",
            "Read Nodal Displacements",
            "Alpaca4d", "08_NumericalOutput")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        public override IEnumerable<string> Keywords => new string[] { "nd" };

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "", GH_ParamAccess.item);
            pManager.AddBooleanParameter("History", "History", "not implemented", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Step", "Step", "", GH_ParamAccess.item, 0);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_VectorParam("Displacement", "Displacement", $"[{Units.Length}]");
            pManager.Register_VectorParam("Rotation", "Rotation", $"[{Units.Angle}]");
            pManager.Register_GenericParam("--------", "--------", "");
            pManager.Register_VectorParam("Velocity", "Velocity", $"[{Units.Length}/{Units.Time}]");
            pManager.Register_VectorParam("Acceleration", "Acceleration", $"[{Units.Length}/{Units.Time}²]");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var alpacaModel = new Alpaca4d.Model();
            bool history = false;
            int step = 0;

            if (!DA.GetData(0, ref alpacaModel)) return;
            DA.GetData(1, ref history);
            DA.GetData(2, ref step);


			if (alpacaModel.IsModal == false)
			{
                if(history == false)
                {
                    var disp = Enumerable.Empty<Rhino.Geometry.Vector3d>();
                    var rot = Enumerable.Empty<Rhino.Geometry.Vector3d>();
                    var vel = Enumerable.Empty<Rhino.Geometry.Vector3d>();
                    var acc = Enumerable.Empty<Rhino.Geometry.Vector3d>();

                    disp = Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.DISPLACEMENT);
                    rot = Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.ROTATION);
                    if (alpacaModel.IsTransient)
                    {
                        vel = Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.VELOCITY);
                        acc = Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.ACCELERATION);
                    }

                    // Finally assign the spiral to the output parameter.
                    DA.SetDataList(0, disp);
                    DA.SetDataList(1, rot);
                    DA.SetDataList(3, vel);
                    DA.SetDataList(4, acc);
                }
                else if(history == true)
                {
                    var disp = new DataTree<Vector3d>();
                    var rot = new DataTree<Vector3d>();
                    var vel = new DataTree<Vector3d>();
                    var acc = new DataTree<Vector3d>();

                    for(step = 0; step < alpacaModel.Settings.AnalysisStep.NumIncr; step++)
                    {
                        disp.AddRange(Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.DISPLACEMENT), new Grasshopper.Kernel.Data.GH_Path(step));
                        rot.AddRange(Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.ROTATION), new Grasshopper.Kernel.Data.GH_Path(step));
                        if (alpacaModel.IsTransient)
                        {
                            vel.AddRange(Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.VELOCITY), new Grasshopper.Kernel.Data.GH_Path(step));
                            acc.AddRange(Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.ACCELERATION), new Grasshopper.Kernel.Data.GH_Path(step));
                        }
                    }

                    DA.SetDataTree(0, disp);
                    DA.SetDataTree(1, rot);
                    DA.SetDataTree(2, vel);
                    DA.SetDataTree(3, acc);
                }
			}
			else
			{
                var disp = Enumerable.Empty<Rhino.Geometry.Vector3d>();
                var rot = Enumerable.Empty<Rhino.Geometry.Vector3d>();

                disp = Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.MODES_OF_VIBRATION_U);
                rot = Alpaca4d.Result.Read.NodalOutput(alpacaModel, step, Alpaca4d.Result.ResultType.MODES_OF_VIBRATION_R);

                // Finally assign the spiral to the output parameter.
                DA.SetDataList(0, disp);
                DA.SetDataList(1, rot);
            }
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.primary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Nodal_Displacements__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("{25085EAB-6C66-487E-B83B-BAB5AB02B1BB}");
    }
}