using System;
using System.Collections.Generic;

using Rhino.Geometry;
using Alpaca4d.Generic;
using Alpaca4d.BeamIntegration;
using Alpaca4d.Section;
using Alpaca4d.Core.Utils;

namespace Alpaca4d.Element
{
    public partial class BeamWithHinges : EntityBase, IStructure, IBeam, ISerialize
    {
        public Curve Curve { get; set; }
        public IUniaxialSection Section { get; set; }
        public GeomTransf GeomTransf { get; set; } = new GeomTransf();
        public IIntegration BeamIntegration { get; set; }
        public Vector3d LocalZAxis
        {
            get { return this.GeomTransf.LocalZ; }
        }
        public ElementType Type => ElementType.Beam;
        public int? Id { get; set; }
        public int? INode { get; set; }
        public int? JNode { get; set; }
        public int Ndf => 6;
        public double? MassDens => this.Section.Area * this.Section.Material.Rho;
        public System.Drawing.Color Color { get; set; }

        private HingeRadauIntegration HingeIntegration => (HingeRadauIntegration)this.BeamIntegration;

        public BeamWithHinges(
            Curve curve,
            IUniaxialSection section,
            GeomTransf geomTransf,
            Release releaseI, double lpI,
            Release releaseJ, double lpJ)
        {
            this.Curve = curve;
            this.Section = section;
            this.GeomTransf = geomTransf;

            var sectionI = CreateHingeSection(section, releaseI);
            var sectionJ = CreateHingeSection(section, releaseJ);

            this.BeamIntegration = new HingeRadauIntegration(sectionI, lpI, sectionJ, lpJ, section);
        }

        private static ElasticSection CreateHingeSection(IUniaxialSection baseSection, Release release)
        {
            const double factor = 1e-6;

            double area   = release.Tx ? baseSection.Area   : baseSection.Area   * factor;
            double izz    = release.Mz ? baseSection.Izz    : baseSection.Izz    * factor;
            double iyy    = release.My ? baseSection.Iyy    : baseSection.Iyy    * factor;
            double j      = release.Rx ? baseSection.J      : baseSection.J      * factor;
            double alphaY = release.Ty ? baseSection.AlphaY : baseSection.AlphaY * factor;
            double alphaZ = release.Tz ? baseSection.AlphaZ : baseSection.AlphaZ * factor;

            return new ElasticSection(
                baseSection.GetType().Name + "_hinge",
                area, izz, iyy, j, alphaY, alphaZ,
                baseSection.Material);
        }

        public void SetTags()
        {
            this.GeomTransf.Id = this.Id;
            this.BeamIntegration.Id = this.Id;
        }

        public void SetTopologyRTree(Model model)
        {
            var tol = model.Tollerance;
            var pointAtStart = this.Curve.PointAtStart;
            var pointAtEnd = this.Curve.PointAtEnd;
            var curvePoints = new List<Point3d> { pointAtStart, pointAtEnd };

            var closestIndexes = new List<int>();

            void SearchCallback(object sender, RTreeEventArgs e)
            {
                closestIndexes.Add(e.Id + 1);
            }

            foreach (var pt in curvePoints)
            {
                model.RTreeCloudPointSixNDF.Search(new Sphere(pt, tol), SearchCallback);
            }

            this.INode = closestIndexes[0] + model.UniquePointsThreeNDF.Count;
            this.JNode = closestIndexes[1] + model.UniquePointsThreeNDF.Count;
        }

        public override string WriteTcl()
        {
            string geomTransf  = this.GeomTransf.WriteTcl();
            string sectionI    = this.HingeIntegration.SectionI.WriteTcl();
            string sectionJ    = this.HingeIntegration.SectionJ.WriteTcl();
            string integration = this.HingeIntegration.WriteTcl();
            // HingeRadau is a compound integration spec and must be a single TCL token → wrap in { }
            string beam = $"element forceBeamColumn {Id} {INode} {JNode} {GeomTransf.Id} {integration} -mass {MassDens / 1000}\n";
            return geomTransf + sectionI + sectionJ + beam;
        }
    }
}
