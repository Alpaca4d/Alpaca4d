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
    public partial class MassLoad : ILoad
    {
        public Point3d Pos { get; set; }
        public Vector3d TransMass { get; set; }
        public Vector3d RotationMass { get; set; }
        public int? Ndf { get; set; }
        public LoadType Type { get; set; } = LoadType.Mass;
        public ITimeSeries TimeSeries { get; set; }
        public int? Id { get; set; }

        public MassLoad()
        {

        }
        public MassLoad(Point3d pos, Vector3d transMass, Vector3d rotationMass)
        {
            this.Pos = pos;
            this.TransMass = transMass;
            this.RotationMass = rotationMass;
        }

        public void SetTag(Model model)
        {
            try
            {
                if (this.Pos.DistanceTo(Rhino.Collections.Point3dList.ClosestPointInList(model.UniquePointsThreeNDF, this.Pos)) < model.Tollerance)
                {
                    this.Id = model.CloudPointThreeNDF.ClosestPoint(this.Pos) + 1;
                    this.Ndf = 3;
                }
                else if (this.Pos.DistanceTo(Rhino.Collections.Point3dList.ClosestPointInList(model.UniquePointsSixNDF, this.Pos)) < model.Tollerance)
                {
                    this.Id = model.CloudPointSixNDF.ClosestPoint(this.Pos) + 1 + model.UniquePointsThreeNDF.Count();
                    this.Ndf = 6;
                }
            }
            catch
            {
                if (this.Pos.DistanceTo(Rhino.Collections.Point3dList.ClosestPointInList(model.UniquePointsSixNDF, this.Pos)) < model.Tollerance)
                {
                    this.Id = model.CloudPointSixNDF.ClosestPoint(this.Pos) + 1 + model.UniquePointsThreeNDF.Count();
                    this.Ndf = 6;
                }
                else if (this.Pos.DistanceTo(Rhino.Collections.Point3dList.ClosestPointInList(model.UniquePointsThreeNDF, this.Pos)) < model.Tollerance)
                {
                    this.Id = model.CloudPointThreeNDF.ClosestPoint(this.Pos) + 1;
                    this.Ndf = 3;
                }
            }
        }

        public override string ToString()
        {
            return base.ToString();
        }
        public string WriteTcl()
        {
            string tclText;

            if (this.Ndf == 6)
            {
                tclText = $"mass {Id} {TransMass.X} {TransMass.Y} {TransMass.Z} {RotationMass.X} {RotationMass.Y} {RotationMass.Z}\n";
            }
            else if(this.Ndf == 3)
            {
                tclText = $"mass {Id} {TransMass.X} {TransMass.Y} {TransMass.Z}\n";
            }
            else
            {
                throw new Exception("No ndf has been assigned");
            }
            return tclText;
        }

    }
}

