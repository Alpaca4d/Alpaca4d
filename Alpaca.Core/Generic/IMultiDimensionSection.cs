using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alpaca4d.Generic
{
    public interface IMultiDimensionSection : ISection
    {
        public IMultiDimensionMaterial Material { get; set; }
        public double Thickness { get; set; }
    }
}
