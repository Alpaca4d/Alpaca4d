using System;
using Rhino.Geometry;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Generic;

namespace Alpaca4d.Element
{
    public partial class Node : IStructure
    {
        public Point3d Pos { get; set; }
        public int? Id { get; set; }
        public int Ndf { get; set; }
        public double Mass { get; set; }

        public Node()
        {

        }

        public Node(Point3d pos)
        {
            this.Pos = pos;
        }

        public Node(int id, double x, double y, double z)
        {
            this.Id = id;
            this.Pos = new Rhino.Geometry.Point3d(x, y, z);
        }

        public void SetNodeTag(Model model)
        {
            if (this.Ndf == 3)
            {
                this.Id = Alpaca4d.Utils.RTreeSearch(model.RTreeCloudPointThreeNDF, new List<Point3d>() { this.Pos }, model.Tollerance)[0] + 1;
                //this.Id = model.CloudPointThreeNDF.ClosestPoint(this.Pos) + 1;
            }
            else // ndf == 6
            {
                this.Id = Alpaca4d.Utils.RTreeSearch(model.RTreeCloudPointSixNDF, new List<Point3d>() { this.Pos }, model.Tollerance)[0] + 1 + model.UniquePointsThreeNDF.Count();
                //this.Id = model.CloudPointSixNDF.ClosestPoint(this.Pos) + 1 + model.UniquePointsThreeNDF.Count();
            }
        }

        public string WriteTcl()
        {
            string tclText;

            if (this.Ndf == 6)
            {
                tclText = $"node {this.Id} {this.Pos.X} {this.Pos.Y} {this.Pos.Z} -mass {this.Mass} {this.Mass} {this.Mass} {this.Mass} {this.Mass} {this.Mass}\n";
            }
            else if (this.Ndf == 3)
            {
                tclText = $"node {this.Id} {this.Pos.X} {this.Pos.Y} {this.Pos.Z} -mass {this.Mass} {this.Mass} {this.Mass}\n";
            }
            else
            {
                throw new Exception($"No ndf has been assigned");
            }
            return tclText;
        }
    }
}