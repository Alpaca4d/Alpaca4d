using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Rhino.Geometry;
using Alpaca4d.Generic;

namespace Alpaca4d.Section
{
    public partial class Layer : ISerialize
    {
        public Curve Curve { get; set; }
        public int NumberOfFibers { get; set; }
        public double AreaFiber { get; set; }
        public IMaterial Material { get; set; }
        public List<PointFiber> Fibers
        {
            get
            {
                var fibers = new List<PointFiber>();

                int numberOfFiber = this.Curve.IsClosed == true ? this.NumberOfFibers : this.NumberOfFibers - 1;
                var parameters = this.Curve.DivideByCount(numberOfFiber, true);
                foreach (var parameter in parameters)
                {
                    var point = this.Curve.PointAt(parameter);
                    var fiber = new PointFiber(point, this.AreaFiber, this.Material);
                    fibers.Add(fiber);

                }

                return fibers;
            }
        }
        public Layer(Curve curve, int numberFibers, double areaFiber, IMaterial material)
        {
            this.Curve = curve;
            this.NumberOfFibers = numberFibers;
            this.AreaFiber = areaFiber;
            this.Material = material;
        }
        public string WriteTcl()
        {
            string tcl = "";
            foreach(var fiber in this.Fibers)
                tcl += fiber.WriteTcl();
            return tcl;
        }
    }
}