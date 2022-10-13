using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Element;

using Rhino.Geometry;

namespace Alpaca4d.Generic
{
    public interface IBeam : IElement
    {
        public Curve Curve { get; set; }
        public GeomTransf GeomTransf { get; set; }
        public IUniaxialSection Section { get; set; }
        public IIntegration BeamIntegration { get; set; }
        public int? INode { get; set; }
        public int? JNode { get; set; }
        public System.Drawing.Color Color { get; set; }

    }
}