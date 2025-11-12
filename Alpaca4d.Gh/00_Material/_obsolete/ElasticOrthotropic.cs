using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections.Generic;



namespace Alpaca4d.Gh
{
    [Obsolete]
    public class ElasticOrthotropicMaterial : GH_Component
    {
        public ElasticOrthotropicMaterial()
          : base("Elastic Orthotropic Material (Alpaca4d)", "EOM",
            "Construct an ElasticOrthotropicMaterial",
            "Alpaca4d", "00_Material")
        {
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        /// <summary>
        /// Registers all the input parameters for this component.
        /// </summary>
        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Material Name", "MatName", "", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Ex", "Ex", $"Young Modulus [{Units.Force}/{Units.Length}²]", GH_ParamAccess.item, 210000000);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Ey", "Ey", $"Young Modulus [{Units.Force}/{Units.Length}²]", GH_ParamAccess.item, 210000000);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Ez", "Ez", $"Young Modulus [{Units.Force}/{Units.Length}²]", GH_ParamAccess.item, 210000000);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Gxy", "Gxy", $"[{Units.Force}/{Units.Length}²]", GH_ParamAccess.item, 90760000);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Gyz", "Gyz", $"[{Units.Force}/{Units.Length}²]", GH_ParamAccess.item, 90760000);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Gzx", "Gzx", $"[{Units.Force}/{Units.Length}²]", GH_ParamAccess.item, 90760000);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("vxy", "vxy", "", GH_ParamAccess.item, 0.3);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("vyz", "vyz", "", GH_ParamAccess.item, 0.3);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("vzx", "vzx", "", GH_ParamAccess.item, 0.3);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Rho", "Rho", $"Density [{Units.Mass}/{Units.Length}³]", GH_ParamAccess.item);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        /// <summary>
        /// Registers all the output parameters for this component.
        /// </summary>
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("Material", "Material", "Material");
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            // default values are in N - m
            string matName = null;
            double ex = 2.1e11;
            double ey = 2.1e11;
            double ez = 2.1e11;
            double gxy = 8.076e10;
            double gyz = 8.076e10;
            double gzx = 8.076e10;
            double vxy = 0.3;
            double vyz = 0.3;
            double vzx = 0.3;
            double rho = 78500;


            DA.GetData(0, ref matName);
            DA.GetData(1, ref ex);
            DA.GetData(2, ref ey);
            DA.GetData(3, ref ez);

            DA.GetData(4, ref gxy);
            DA.GetData(5, ref gyz);
            DA.GetData(6, ref gzx);

            DA.GetData(7, ref vxy);
            DA.GetData(8, ref vyz);
            DA.GetData(9, ref vzx);

            DA.GetData(10, ref rho);

            //rho = rho * 9.81 / 1000;
            var material = new Alpaca4d.Material.ElasticOrthotropicMaterial(matName, ex, ey, ez, gxy, gyz, gzx, vxy, vyz, vzx, rho);


            DA.SetData(0, material);

        }



        public override GH_Exposure Exposure => GH_Exposure.hidden;


        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Elastic_Orthotropic_Material__Alpaca4d_;


        public override Guid ComponentGuid => new Guid("{9EBA4A6E-33B5-4FA2-8B13-1546FD465745}");
    }
}