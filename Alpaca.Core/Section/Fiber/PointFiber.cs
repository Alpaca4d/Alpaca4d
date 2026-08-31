using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;
using Rhino.Geometry;

namespace Alpaca4d.Section
{
    public partial class PointFiber : ISerialize
    {
        public int Index { get; set; }
        public Point3d Pos { get; set; }
        public double Area { get; set; }
        public IMaterial Material { get; set; }
        public List<double> Stress { get; set; } = new List<double>();
        public List<double> Strain { get; set; } = new List<double>();

        public PointFiber(Point3d point, double area, IMaterial material)
        {
            this.Pos = point;
            this.Area = area;
            this.Material = material;
        }
        public string WriteTcl()
        {
            // MinMax.FiberTag, not Material.Id: a material wrapped in MinMax is declared
            // under two tags, and the fibre has to name the wrapper for the strain limits
            // to apply to it at all.
            string tcl = $"fiber {TclNumber.Write(this.Pos.X)} {TclNumber.Write(this.Pos.Y)} {TclNumber.Write(this.Area)} {Alpaca4d.Material.MinMax.FiberTag(this.Material)}\n";
            return tcl;
        }
    }
}
