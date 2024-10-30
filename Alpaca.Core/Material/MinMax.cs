using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Generic;
using Alpaca4d.Core.Utils;

namespace Alpaca4d.Material
{
    // uniaxialMaterial MinMax $matTag $otherTag <-min $minStrain> <-max $maxStrain>
    public partial class MinMax : EntityBase
    {
        public string MatName { get; set; }
        public int? Id { get; set; } = IdGenerator.GenerateId();
        public double MinStrain { get; set; }
        public double MaxStrain { get; set; }

        public MinMax(string matName, double minStrain, double maxStrain)
        {
            this.MatName = matName;
            this.MinStrain = minStrain;
            this.MaxStrain = maxStrain;
        }

        public override string WriteTcl()
        {
            string tcl = $"uniaxialMaterial MinMax {this.Id} {this.Id} -min {this.MinStrain} -max {this.MaxStrain}\n";
            return tcl;
        }
    }
}
