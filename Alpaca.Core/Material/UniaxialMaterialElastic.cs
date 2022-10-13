﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Material
{
    public partial class UniaxialMaterialElastic : EntityBase, IUniaxialMaterial
    {
        public int? Id { get; set; }
        public string MatName { get; set; }
        public double E { get; set; }

        public double? Eneg { get; set; }
        public double Eta { get; set; }
        public double G { get; set; }
        public double Nu { get; set; }
        public double? Rho { get; set; }

        public static UniaxialMaterialElastic Steel
        {
            get
            {
                double e = 2.1e11;
                double eNeg = 2.1e11;
                double eta = 0.00;
                double g = 8.076e10;
                double v = 0.3;
                double rho = 78500;
                return new UniaxialMaterialElastic(null, e, eNeg, eta, g, v, rho);
            }
        }

        public string MaterialDimension => "UniaxialMaterial";
        public string MaterialType => "Elastic";

        public UniaxialMaterialElastic(string matName, double e, double eNeg, double eta, double g, double v, double? rho = null)
        {
            this.MatName = matName;
            this.E = e;
            this.Eneg = eNeg;
            this.Eta = eta;
            this.G = g;
            this.Nu = v;
            this.Rho = rho;
        }

        public override string WriteTcl()
        {
            string tclText = $"uniaxialMaterial Elastic {this.Id} {this.E} {this.Eta} {this.Eneg}\n";
            return tclText;
        }
		public override string ToString()
		{
            return this.WriteTcl();
        }
	}
}
