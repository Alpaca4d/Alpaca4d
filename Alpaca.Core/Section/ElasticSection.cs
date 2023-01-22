﻿using System;
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
        public List<Curve> Curves
        {
            get
            {
                var plane = Rhino.Geometry.Plane.WorldXY;

                var p1 = plane.PointAt(0.701254, -0.065731);
                var p2 = plane.PointAt(0.543647, 0.311231);
                var p3 = plane.PointAt(0.421856, 0.69971);
                var p4 = plane.PointAt(0.066123, 0.86248);
                var p5 = plane.PointAt(-0.274192, 0.64723);
                var p6 = plane.PointAt(-0.562272, 0.35572);
                var p7 = plane.PointAt(-0.720374, -0.012156);
                var p8 = plane.PointAt(-0.647997, -0.408899);
                var p9 = plane.PointAt(-0.331969, -0.665398);
                var p10 = plane.PointAt(0.037216, -0.840361);
                var p11 = plane.PointAt(0.430678, -0.799355);
                var p12 = plane.PointAt(0.65998, -0.46282);

                var wireframe = new List<Point3d>() { p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p1 };
                var boundaryCurves = new List<Curve>() { new Rhino.Geometry.Polyline(wireframe).ToNurbsCurve() };

                return boundaryCurves;
            }
            set { }
        }
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