using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d;
using Alpaca4d.Generic;
using Rhino.Geometry;

namespace Alpaca4d.Loads
{
    public partial class LineLoad : ILoad
    {
        public int? Id { get; set; }
        public List<int> Range { get; set; }
        public List<IBeam> AllElements { get; set; }
        public IBeam Element { get; set; }
        public Vector3d GlobalForce { get; set; }
        public Vector3d LocalForce { get; set; }
        private double? Wx => LocalForce.X;
        private double Wy => LocalForce.Y;
        private double Wz => LocalForce.Z;
        public int Ndf { get; set; }
        public LoadType Type { get; set; } = LoadType.DistributedLoad;
        public int PatternTag { get; set; }
        public ITimeSeries TimeSeries { get; set; }
        public bool IsLocal { get; set; }

        public LineLoad()
        {

        }
        public LineLoad(Alpaca4d.Generic.IBeam element, Vector3d force, ITimeSeries timeSeries, bool local = false)
        {
            this.Element = element;
            this.TimeSeries = timeSeries;
            this.IsLocal = local;

            if (local)
                this.LocalForce = force;
            else
                this.GlobalForce = force;

            if (element != null)
            {
                this.LocalForce = this.GlobalToLocal(force);
            }
        }

        public Vector3d GlobalToLocal(Vector3d force)
        {
            var localX = this.Element.GeomTransf.LocalZ; // Rhino Place LocalX
            var localY = this.Element.GeomTransf.LocalY; // Rhino Place LocalX
            var plane = new Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, localX, localY);
            return Utils.PlaceCoordinates(new Rhino.Geometry.Point3d(force), plane);
        }

        public void SetTag(Model model)
        {

        }

        /// <summary>
        /// eleLoad -ele $eleTag1 <$eleTag2 ....> -type -beamUniform $Wy $Wz <$Wx>
        /// </summary>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>
        public string WriteTcl()
        {
            string tcl;
            tcl = $"\teleLoad -ele {this.Element.Id} -type -beamUniform {this.Wy} {this.Wz} {this.Wx}\n";
            return tcl;
        }
    }
}