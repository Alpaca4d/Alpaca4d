using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Rhino.Geometry;
using Alpaca4d.Generic;

namespace Alpaca4d.Section
{
    public partial class RectangleCS : ISerialize, IUniaxialSection
    {
        public int? Id { get; set; }
        public IUniaxialMaterial Material { get; set; }
        public string SectionName { get; set; }
        public double Width { get; set; }
        public double Height { get; set; }
        public double Area
        {
            get
            {
                double area = this.Width * this.Height;
                return area;
            }
        }
        public double AlphaY => 5.0 / 6.0;
        public double AlphaZ => 5.0 / 6.0;
        public double Izz
        {
            get
            {
                double iZZ = this.Width * Math.Pow(this.Height, 3) / 12.0;
                return iZZ;
            }
        }

        public double Iyy
        {
            get
            {
                double iYY = Math.Pow(this.Width, 3) * this.Height / 12.0;
                return iYY;
            }
        }

        public double J
        {
            get
            {
                double j;
                double k;
                if(this.Height < this.Width)
                {
                    k = 1 / (3 + 4.1 * Math.Pow((this.Height / this.Width), 3 / 2));
                    j = k * this.Width * Math.Pow(this.Height, 3);
                }
                else
                {
                    k = 1 / (3 + 4.1 * Math.Pow((this.Width / this.Height), 3 / 2));
                    j = k * this.Height * Math.Pow(this.Width, 3);
                }
                return j;
            }
        }

        public List<Curve> Curves
        {
            get
            {
                var curves = new List<Curve>();
                var width = new Interval(-Width, Width);
                var heigth = new Interval(-Height, Height);
                curves.Add(new Rhino.Geometry.Rectangle3d(Rhino.Geometry.Plane.WorldXY, width, heigth).ToNurbsCurve());
                return curves;
            }
        }

        public Brep Brep
        {
            get
            {
                return Rhino.Geometry.Brep.CreatePlanarBreps(this.Curves, 0.01)[0];
            }
        }

        public RectangleCS(string secName, double width, double height, IUniaxialMaterial material)
        {
            this.SectionName = secName;
            this.Width = width;
            this.Height = height;
            this.Material = material;
        }

        public double GetAreaY()
        {
            return this.Area * this.AlphaY;
        }

        public double GetAreaZ()
        {
            return this.Area * this.AlphaZ;
        }

        public string WriteTcl()
        {
            string tclText = $"section Elastic {Id} {Material.E} {Area} {Izz} {Iyy} {Material.G} {J} {AlphaY} {AlphaZ}\n";
            return tclText;
        }
    }
}
