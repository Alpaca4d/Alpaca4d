using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Core.Utils;
using Alpaca4d.Generic;

namespace Alpaca4d.Material
{
    public partial class ReinforcingSteel : EntityBase, IMaterial
    {
        public string MatName { get; set; }
        public int? Id { get; set; } = IdGenerator.GenerateId();
        public double Fy { get; set; }
        public double Fu { get; set; }
        public double Es { get; set; }
        public double Esh { get; set; }
        public double EpsilonSh { get; set; }
        public double EpsilonUlt { get; set; }
        public MinMax MinMax { get; set; }
        public string MaterialDimension => "UniaxialMaterial";
        public double? Rho { get; set; }


        public ReinforcingSteel(string matName, double fy, double fu, double es, double esh, double epislonSh, double epsilponUlt, bool isMinMax)
        {
            this.MatName = matName;
            this.Fy = fy;
            this.Fu = fu;
            this.Es = es;
            this.Esh = esh;
            this.EpsilonSh = epislonSh;
            this.EpsilonUlt = epsilponUlt;
            if (isMinMax == true)
                this.MinMax = new Alpaca4d.Material.MinMax(matName, - this.EpsilonUlt, this.EpsilonUlt);
        }

        public override string WriteTcl()
        {
            string tcl = $"uniaxialMaterial ReinforcingSteel {this.Id} {this.Fy} {this.Fu} {this.Es} {this.Esh} {this.EpsilonSh} {this.EpsilonUlt}\n";
            if (this.MinMax != null)
                tcl += this.MinMax.WriteTcl();
            return tcl;
        }
    }
}
