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
    public partial class ASDShellQ4 : EntityBase, ISerialize, IShell, IElement, IStructure
    {
        public int? Id { get; set; }
        public Mesh Mesh { get; set; }
        public IMultiDimensionSection Section { get; set; }
        public ElementType Type => ElementType.Shell;
        public List<int?> IndexNodes { get; set; }
        public int Ndf => 6;
        public Color Color { get; set; }
        public ElementClass ElementClass => ElementClass.ASDShellQ4;

        public ASDShellQ4(Mesh mesh, IMultiDimensionSection section)
        {
            this.Mesh = mesh;
            this.Section = section;
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
                model.RTreeCloudPointSixNDF.Search(new Rhino.Geometry.Sphere(pt, tol), SearchCallback);
            }

            this.IndexNodes = closestIndexes.Select(x => x + model.UniquePointsThreeNDF.Count).ToList();
        }
        public override string WriteTcl()
        {
            string tcl = $"element ASDShellQ4 {this.Id} {this.IndexNodes[0]} {this.IndexNodes[1]} {this.IndexNodes[2]} {this.IndexNodes[3]} {this.Section.Id}\n";

            return tcl;
        }
    }
}
