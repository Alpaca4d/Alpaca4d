using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;


namespace Alpaca4d.Gh
{
    public class Support : GH_Component
    {
        public Support()
          : base("Support (Alpaca4d)", "Support",
            "Construct a Support",
            "Alpaca4d", "02_Element")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddPlaneParameter("Position", "Position",
                $"Point or Plane to restrain [{Units.Length}]. A Point restrains the global axes. " +
                "A Plane restrains its own axes instead, so the support can be skewed - " +
                "an inclined roller, a support on a sloping face.", GH_ParamAccess.item);
            pManager.AddBooleanParameter("Tx", "Tx", "Translation along the support plane's X axis", GH_ParamAccess.item, true);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddBooleanParameter("Ty", "Ty", "Translation along the support plane's Y axis", GH_ParamAccess.item, true);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddBooleanParameter("Tz", "Tz", "Translation along the support plane's Z axis", GH_ParamAccess.item, true);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddBooleanParameter("Rx", "Rx", "Rotation about the support plane's X axis", GH_ParamAccess.item, true);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddBooleanParameter("Ry", "Ry", "Rotation about the support plane's Y axis", GH_ParamAccess.item, true);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddBooleanParameter("Rz", "Rz", "Rotation about the support plane's Z axis", GH_ParamAccess.item, true);
            pManager[pManager.ParamCount - 1].Optional = true;

            // Appended last on purpose: inserting a parameter renumbers the ones after it
            // and every file already holding this component loses those wires.
            pManager.AddIntegerParameter("Type", "Type",
                "One of the predefined supports, which sets all six restraints at once and " +
                "overrides Tx..Rz. Right-click the input to pick one by name. Leave it alone " +
                "to set the six restraints yourself.", GH_ParamAccess.item, UseTheBooleans);
            pManager[pManager.ParamCount - 1].Optional = true;

            var type = pManager[pManager.ParamCount - 1] as Grasshopper.Kernel.Parameters.Param_Integer;
            if (type != null)
            {
                type.AddNamedValue("Custom (use Tx..Rz)", UseTheBooleans);

                for (var index = 0; index < Alpaca4d.Element.SupportPreset.All.Count; index++)
                    type.AddNamedValue(Alpaca4d.Element.SupportPreset.All[index].Label, index);
            }
        }

        /// <summary>Type value meaning "no preset - read the six booleans instead".</summary>
        private const int UseTheBooleans = -1;

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Support", "Support", "Support");
        }

        /// <summary>
        /// This is the method that actually does the work.
        /// </summary>
        /// <param name="DA">The DA object can be used to retrieve data from input parameters and 
        /// to store data in output parameters.</param>
        [STAThread]
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            // A Point arriving on this input is cast to a world-aligned Plane at that
            // point, which is the support every model had before planes were an option.
            Plane position = Plane.WorldXY;
            bool tx = true;
            bool ty = true;
            bool tz = true;
            bool rx = true;
            bool ry = true;
            bool rz = true;

            int type = UseTheBooleans;

            if (!DA.GetData(0, ref position)) return;
            if (!DA.GetData(1, ref tx)) return;
            if (!DA.GetData(2, ref ty)) return;
            if (!DA.GetData(3, ref tz)) return;
            if (!DA.GetData(4, ref rx)) return;
            if (!DA.GetData(5, ref ry)) return;
            if (!DA.GetData(6, ref rz)) return;
            DA.GetData(7, ref type);

            Alpaca4d.Element.Support support;

            if (type == UseTheBooleans)
            {
                support = new Alpaca4d.Element.Support(position, tx, ty, tz, rx, ry, rz);
            }
            else if (type >= 0 && type < Alpaca4d.Element.SupportPreset.All.Count)
            {
                var preset = Alpaca4d.Element.SupportPreset.All[type];
                support = preset.On(position);

                AddRuntimeMessage(GH_RuntimeMessageLevel.Remark,
                    preset.Describe() + Environment.NewLine + "Tx..Rz are ignored while a Type is set.");
            }
            else
            {
                AddRuntimeMessage(GH_RuntimeMessageLevel.Error,
                    $"There is no support type {type}. Valid types are 0 to " +
                    $"{Alpaca4d.Element.SupportPreset.All.Count - 1}, or {UseTheBooleans} to use Tx..Rz.");
                return;
            }

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, support);


        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.quarternary;

        /// <summary>
        /// Provides an Icon for every component that will be visible in the User Interface.
        /// Icons need to be 24x24 pixels.
        /// You can add image files to your project resources and access them like this:
        /// return Resources.IconForThisComponent;
        /// </summary>
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Support__Alpaca4d_;

        /// <summary>
        /// Each component must have a unique Guid to identify it. 
        /// It is vital this Guid doesn't change otherwise old ghx files 
        /// that use the old ID will partially fail during loading.
        /// </summary>
        public override Guid ComponentGuid => new Guid("08A676AD-7332-4D86-8206-DABD66A17357");
    }
}