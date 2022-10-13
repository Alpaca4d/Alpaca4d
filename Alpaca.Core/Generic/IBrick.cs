using System;
using System.Drawing;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Element;
using Rhino.Geometry;

namespace Alpaca4d.Generic
{
    public interface IBrick : IElement
    {
        public int? Id { get; set; }
        public Mesh Mesh { get; set; }
        public ElementClass ElementClass { get; }
        public IMultiDimensionMaterial Material { get; set; }
        public List<int?> IndexNodes { get; set; }
        public Color Color { get; set; }

    }
}