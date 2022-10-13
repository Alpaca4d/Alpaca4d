using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Grasshopper.Kernel;
using Grasshopper.Kernel.Types;

using Alpaca4d.Generic;
using Rhino.Geometry;

namespace Alpaca4d.Element
{
    public partial class GeomTransf : EntityBase, ISerialize
    {
        public GeomTransfType Type { get; set; }
        public Curve Line { get; set; }
        public int? Id { get; set; }
        public Vector3d LocalZ { get; set; }
        public Vector3d LocalY
        {
            get
            {
                Vector3d lineVector = new Rhino.Geometry.Vector3d(Line.PointAtEnd - Line.PointAtStart);
                lineVector.Unitize();
                return Vector3d.CrossProduct(LocalZ, lineVector);
            }
        }

        // Constructor

        public GeomTransf()
        {
        }


        public GeomTransf(GeomTransfType type, Curve line, Vector3d refVector)
        {
            this.Type = type;
            this.Line = line;
            this.LocalZ = refVector;
        }

        public override string WriteTcl()
        {
            string tclText = $"geomTransf {Type} {Id} {LocalZ.X} {LocalZ.Y} {LocalZ.Z}\n";
            return tclText;
        }
    }

    public enum GeomTransfType
    {
        Linear,
        PDelta,
        Corotational
    }
}
