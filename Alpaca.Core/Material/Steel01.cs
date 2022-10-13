using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Generic;

namespace Alpaca4d.Material
{
    public partial class Steel01 : EntityBase, IMaterial
    {
        public string MatName { get; set; }
        public int? Id { get; set; }
        public double Fy { get; set; }
        public double E0 { get; set; }
        public double b { get; set; }
        public double? a1 { get; set; }
        public double? a2 { get; set; }
        public double? a3 { get; set; }
        public double? a4 { get; set; }
        public MinMax MinMax { get; set; }
        public string MaterialDimension => "UniaxialMaterial";
        public double? Rho { get; set; }

        public Steel01(string matName, double fy, double e0, double b, double? a1 = null, double? a2 = null, double? a3 = null, double? a4 = null)
        {
            this.MatName = matName;
            this.Fy = fy;
            this.E0 = e0;
            this.b = b;
            this.a1 = a1;
            this.a2 = a2;
            this.a3 = a3;
            this.a4 = a4;
        }

        public override string WriteTcl()
        {
            string tcl = $"uniaxialMaterial Steel01 {this.Id} {this.Fy} {this.E0} {this.b} {this.a2} {this.a2} {this.a3} {this.a4}\n";
            return tcl;
        }
    }
}
