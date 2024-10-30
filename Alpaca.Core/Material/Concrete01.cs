using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Core.Utils;
using Alpaca4d.Generic;

namespace Alpaca4d.Material
{
    public partial class Concrete01 : EntityBase, IMaterial
    {
        /// <summary>
        /// Integer tag identifying material 
        /// </summary>
        public int? Id { get; set; } = IdGenerator.GenerateId();
        /// <summary>
        /// Concrete compressive strength at 28 days 
        /// </summary>
        public double FpCo { get; set; }
        /// <summary>
        /// Concrete crushing strength
        /// </summary>
        public double FpCu { get; set; }
        /// <summary>
        /// Concrete strain at maximum strength
        /// </summary>
        public double EpsilonCo { get; set; }
        /// <summary>
        /// Concrete strain at crushing strength
        /// </summary>
        public double EpsilonCu { get; set; }
        public MinMax MinMax { get; set; }
        public string MatName { get; set; }
        public string MaterialDimension => "UniaxialMaterial";
        public double? Rho { get; set; }


        public Concrete01(string matName, double fpco, double fpcu, double epsilonCo, double epsilonCu, bool isMinMax)
        {
            this.MatName = matName;
            this.FpCo = fpco;
            this.FpCu = fpcu;
            this.EpsilonCo = epsilonCo;
            this.EpsilonCu = epsilonCu;
            if (isMinMax == true)
                this.MinMax = new Alpaca4d.Material.MinMax(matName, this.EpsilonCu, 0.0);
        }

        public override string WriteTcl()
        {
            string tcl = $"uniaxialMaterial Concrete01 {this.Id} {this.FpCo} {this.EpsilonCo} {this.FpCu} {this.EpsilonCu}\n";
            if (this.MinMax != null)
                tcl += this.MinMax.WriteTcl();
            return tcl;
        }
    }
}
