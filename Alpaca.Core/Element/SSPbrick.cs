using System;
using System.Drawing;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Generic;
using Rhino.Geometry;

namespace Alpaca4d.Element
{
    public partial class SSPbrick : EntityBase, ISerialize, IBrick, IStructure
    {
        public int? Id { get; set; }
        public Mesh Mesh { get; set; }
        public IMultiDimensionMaterial Material { get; set; }
        public ElementType Type => ElementType.Brick;
        public ElementClass ElementClass => ElementClass.SSPBrick;
        public List<int?> IndexNodes { get; set; }
        public double? BodyForce { get; set; }
        public int Ndf => 3;
        public Color Color { get; set; }

        public SSPbrick(Mesh mesh, IMultiDimensionMaterial material)
        {
            this.Mesh = mesh;
            this.Material = material;
        }

        public void SetTags()
        {

        }

        public void SetTopologyRTree(Alpaca4d.Model model)
        {
            var tol = model.Tollerance;
            var meshPoints = this.Mesh.Vertices.ToList();

            var closestIndexes = new List<int?>();

            void SearchCallback(object sender, RTreeEventArgs e)
            {
                closestIndexes.Add(e.Id + 1);
            }

            foreach (var pt in meshPoints)
            {
                model.RTreeCloudPointThreeNDF.Search(new Rhino.Geometry.Sphere(pt, tol), SearchCallback);
            }

            this.IndexNodes = closestIndexes;
        }

        public override string WriteTcl()
        {
            string tcl = $"element SSPbrick {this.Id} {this.IndexNodes[0]} {this.IndexNodes[1]} {this.IndexNodes[2]} {this.IndexNodes[3]} {this.IndexNodes[4]} {this.IndexNodes[5]} {this.IndexNodes[6]} {this.IndexNodes[7]} {this.Material.Id} {this.BodyForce} {this.BodyForce} {this.BodyForce}\n";
            return tcl;
        }

    }
}
