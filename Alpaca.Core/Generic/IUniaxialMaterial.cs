using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Generic
{
    public interface IUniaxialMaterial : IMaterial, ISerialize
    {
        public double E { get; set; }
        public double G { get; set; }
        public int? Id { get; set; }
        public double? Rho { get; set; }
    }
}
