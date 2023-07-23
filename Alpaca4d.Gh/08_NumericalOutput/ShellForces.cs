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
    public class ShellForces : GH_Component
    {
        public ShellForces()
          : base("Shell Forces (Alpaca4d)", "SF",
            "Read the Shell Forces",
            "Alpaca4d", "08_NumericalOutput")
        {
            // Draw a Description Underneath the component
            this.Message = "Shell Forces\n(Alpaca4d)";
        }

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
            pManager.Register_GenericParam("Fx", "Fx", "");
            pManager.Register_GenericParam("Fy", "Fy", "");
            pManager.Register_GenericParam("Fxy", "Fxy", "");
            pManager.Register_GenericParam("Mx", "Mx", "");
            pManager.Register_GenericParam("My", "My", "");
            pManager.Register_GenericParam("Mxy", "Mxy", "");
            pManager.Register_GenericParam("Vxz", "Vxz", "");
            pManager.Register_GenericParam("Vyz", "Vyz", "");
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

            var fxQuad = new List<List<double>>();
            var fyQuad = new List<List<double>>();
            var fxyQuad = new List<List<double>>();
            var mxQuad = new List<List<double>>();
            var myQuad = new List<List<double>>();
            var mxyQuad = new List<List<double>>();
            var vxzQuad = new List<List<double>>();
            var vyzQuad = new List<List<double>>();

            var fxTri = new List<List<double>>();
            var fyTri = new List<List<double>>();
            var fxyTri = new List<List<double>>();
            var mxTri = new List<List<double>>();
            var myTri = new List<List<double>>();
            var mxyTri = new List<List<double>>();
            var vxzTri = new List<List<double>>();
            var vyzTri = new List<List<double>>();


            if (alpacaModel.HasQuadShell)
                (fxQuad, fyQuad, fxyQuad, mxQuad, myQuad, mxyQuad, vxzQuad, vyzQuad) = Alpaca4d.Result.Read.ASDQ4Forces(alpacaModel, step);
            if(alpacaModel.HasTriShell)
                (fxTri, fyTri, fxyTri, mxTri, myTri, mxyTri, vxzTri, vyzTri) = Alpaca4d.Result.Read.DKGTForces(alpacaModel, step);

            var ids = alpacaModel.Shells.Select(d => d.Id).ToList();

            // Convert Nested List to DataTree
            var quadShellId = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ASDShellQ4).Select(x => x.Id-1).ToList();

            var fxQuadTree = Utils.DataTreeFromNestedList(fxQuad, quadShellId);
            var fyQuadTree = Utils.DataTreeFromNestedList(fyQuad, quadShellId);
            var fxyQuadTree = Utils.DataTreeFromNestedList(fxyQuad, quadShellId);
            var mxQuadTree = Utils.DataTreeFromNestedList(mxQuad, quadShellId);
            var myQuadTree = Utils.DataTreeFromNestedList(myQuad, quadShellId);
            var mxyQuadTree = Utils.DataTreeFromNestedList(mxyQuad, quadShellId);
            var vxzQuadTree =  Utils.DataTreeFromNestedList(vxzQuad, quadShellId);
            var vyzQuadTree =  Utils.DataTreeFromNestedList(vyzQuad, quadShellId);

            // Convert Nested List to DataTree
            var triShellId = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ShellDKGT).Select(x => x.Id-1).ToList();

            var fxTriTree = Utils.DataTreeFromNestedList(fxTri, triShellId);
            var fyTriTree = Utils.DataTreeFromNestedList(fyTri, triShellId);
            var fxyTriTree = Utils.DataTreeFromNestedList(fxyTri, triShellId);
            var mxTriTree = Utils.DataTreeFromNestedList(mxTri, triShellId);
            var myTriTree = Utils.DataTreeFromNestedList(myTri, triShellId);
            var mxyTriTree = Utils.DataTreeFromNestedList(mxyTri, triShellId);
            var vxzTriTree = Utils.DataTreeFromNestedList(vxzTri, triShellId);
            var vyzTriTree = Utils.DataTreeFromNestedList(vyzTri, triShellId);
            

            fxQuadTree.MergeTree(fxTriTree);
            fyQuadTree.MergeTree(fyTriTree);
            fxyQuadTree.MergeTree(fxyTriTree);
            mxQuadTree.MergeTree(mxTriTree);
            myQuadTree.MergeTree(myTriTree);
            mxyQuadTree.MergeTree(mxyTriTree);
            vxzQuadTree.MergeTree(vxzTriTree);
            vyzQuadTree.MergeTree(vyzTriTree);

            // Finally assign the spiral to the output parameter.
            DA.SetDataTree(0, fxQuadTree);
            DA.SetDataTree(1, fyQuadTree);
            DA.SetDataTree(2, fxyQuadTree);
            DA.SetDataTree(3, mxQuadTree);
            DA.SetDataTree(4, myQuadTree);
            DA.SetDataTree(5, mxyQuadTree);
            DA.SetDataTree(6, vxzQuadTree);
            DA.SetDataTree(7, vyzQuadTree);
        }


        /// <summary>
        /// The Exposure property controls where in the panel a component icon 
        /// will appear. There are seven possible locations (primary to septenary), 
        /// each of which can be combined with the GH_Exposure.obscure flag, which 
        /// ensures the component will only be visible on panel dropdowns.
        /// </summary>
        public override GH_Exposure Exposure => GH_Exposure.tertiary;

        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.meshForces;

        public override Guid ComponentGuid => new Guid("{8A27E0D6-4D39-417E-A9E9-202AB291CE01}");
    }
}