﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Material
{
    public partial class ElasticOrthotropicMaterial : EntityBase, IMultiDimensionMaterial
    {
        public int? Id { get; set; }
        public string MatName { get; set; }
        public double E { get; set; } // it will be null
        public double Ex { get; set; }
        public double Ey { get; set; }
        public double Ez { get; set; }
        public double Gxy { get; set; }
        public double Gyz { get; set; }
        public double Gzx { get; set; }
        public double NuXy { get; set; }
        public double NuYz { get; set; }
        public double NuZx { get; set; }
        public double? Rho { get; set; }

        public string MaterialDimension => "nDMaterial";
        public string MaterialType => "Elastic";

        public ElasticOrthotropicMaterial(string matName, double ex, double ey, double ez, double gxy, double gyz, double gzx, double vxy, double vyz, double vzx, double? rho = null)
        {
            this.MatName = matName;
            this.Ex = ex;
            this.Ey = ey;
            this.Ez = ez;
            this.Gxy = gxy;
            this.Gyz = gyz;
            this.Gzx = gzx;
            this.NuXy = vxy;
            this.NuYz = vyz;
            this.NuZx = vzx;
            this.Rho = rho;
        }

        public override string WriteTcl()
        {
            string tclText = $"nDMaterial ElasticOrthotropic {this.Id} {this.Ex} {this.Ey} {this.Ez} {this.NuXy} {this.NuYz} {this.NuZx} {this.Gxy} {this.Gyz} {this.Gzx} {this.Rho}\n";
            return tclText;
        }
    }
}
