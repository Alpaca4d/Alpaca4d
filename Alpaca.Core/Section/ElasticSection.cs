using System;
using Rhino.Geometry;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Generic;

namespace Alpaca4d.Section
{
    public partial class ElasticSection : ISerialize, IUniaxialSection
    {
        public string SectionName { get; set; }
        public double Area { get; set; }
        public double Izz { get; set; }
        public double Iyy { get; set; }
        public double J { get; set; }
        public double AlphaY { get; set; }
        public double AlphaZ { get; set; }
        public int? Id { get; set; }
        public IUniaxialMaterial Material { get; set; }
        public List<Curve> Curves { get; set; }
        public Brep Brep { get; }

        public ElasticSection()
        {

        }

        public ElasticSection(string secName, double area, double iZZ, double iYY, double j, double alphaY, double alphaZ, IUniaxialMaterial material)
        {
            this.SectionName = secName;
            this.Area = area;
            this.Izz = iZZ;
            this.Iyy = iYY;
            this.J = j;
            this.AlphaY = alphaY;
            this.AlphaZ = alphaZ;
            this.Material = material;
        }

        public string WriteTcl()
        {
            string tclText = $"section Elastic {Id} {Material.E} {Area} {Izz} {Iyy} {Material.G} {J} {AlphaY} {AlphaZ}\n";
            return tclText;
        }
    }

    
}