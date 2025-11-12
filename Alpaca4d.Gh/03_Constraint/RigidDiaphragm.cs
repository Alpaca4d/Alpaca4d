using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;


namespace Alpaca4d.Gh
{
    public class RigidDiaphragm : GH_Component
    {
        public RigidDiaphragm()
          : base("Rigid Diaphragm (Alpaca4d)", "Rigid Diaphragm",
            "Construct a Rigid Diaphgram",
            "Alpaca4d", "03_Constraint")
        {
            // Draw a Description Underneath the component
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddPointParameter("SlavePoints", "SlavePoints", "Points which define a rigid diaphgram", GH_ParamAccess.list);
            pManager.AddPointParameter("MasterPoint", "MasterPoint", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Direction", "Direction", "Direction perpendicular to the rigid plane.\n1 - yz plane\n2 - xz plane\n3 - xy plane) ", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Constraint", "Constraint", "");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            var slaveNodes = new List<Point3d>();
            DA.GetDataList(0, slaveNodes);
            
            var result = Rhino.Geometry.Plane.FitPlaneToPoints(slaveNodes, out Plane myPlane, out double deviation);
            if (deviation > Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance)
                throw new Exception("Points are not in a plane!");

            Point3d? masterNode = null;
            DA.GetData(1, ref masterNode);

            int dir = 3;
            DA.GetData(2, ref dir);
            if(dir > 3 || dir < 0)
            {
                throw new Exception("Value must be 1, 2 or 3");
            }
            var diaphgram = new Alpaca4d.Constraints.RigidDiaphragm(slaveNodes, masterNode, dir);

            DA.SetData(0, diaphgram);
        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Rigid_Diaphgram__Alpaca4d_;

        public override Guid ComponentGuid => new Guid("{BDA8CE51-1B34-48C7-B0B1-80A25E7E5754}");
    }
}