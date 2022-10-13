using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Element;
using Rhino.Geometry;

namespace Alpaca4d.Generic
{
    public interface IShell : IElement
    {
        public Mesh Mesh { get; set; }
        public List<int?> IndexNodes { get; set; }
        public IMultiDimensionSection Section { get; set; }
        public System.Drawing.Color Color { get; set; }
        public ElementClass ElementClass { get; }
    }
}
