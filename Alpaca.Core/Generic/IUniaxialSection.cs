using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Rhino.Geometry;

namespace Alpaca4d.Generic
{
    public interface IUniaxialSection : ISerialize, ISection
    {
        public int? Id { get; set; }
        public double Area { get; }
        public double Izz { get; }
        public double Iyy { get; }
        public double J { get; }
        public double AlphaY { get; }
        public double AlphaZ { get; }
        public IUniaxialMaterial Material { get; set; }
        public Brep Brep { get; }
        public List<Curve> Curves { get; }
    }
}
