using System;
using System.Collections.Generic;
using Alpaca4d.Generic;
using Alpaca4d.Section;

namespace Alpaca4d.BeamIntegration
{
    public class HingeRadauIntegration : IIntegration
    {
        public int? Id { get; set; }
        public IntegrationType Type => IntegrationType.HingeRadau;

        /// <summary>Interior (elastic) section.</summary>
        public IUniaxialSection Section { get; set; }

        /// <summary>Auto-generated hinge section at the I end.</summary>
        public ElasticSection SectionI { get; set; }

        /// <summary>Plastic hinge length at the I end.</summary>
        public double LpI { get; set; } = 0.01;

        /// <summary>Auto-generated hinge section at the J end.</summary>
        public ElasticSection SectionJ { get; set; }

        /// <summary>Plastic hinge length at the J end.</summary>
        public double LpJ { get; set; } = 0.01;

        // IIntegration requires IntegrationPoint; not used for HingeRadau.
        public int IntegrationPoint { get; set; } = 0;

        public HingeRadauIntegration(
            ElasticSection sectionI, double lpI,
            ElasticSection sectionJ, double lpJ,
            IUniaxialSection interiorSection)
        {
            SectionI = sectionI;
            LpI = lpI;
            SectionJ = sectionJ;
            LpJ = lpJ;
            Section = interiorSection;
        }

        /// <summary>
        /// Returns only the inline integration arguments for the element command.
        /// The section Tcl lines are written by BeamWithHinges.WriteTcl().
        /// </summary>
        public string WriteTcl()
        {
            return $"HingeRadau {SectionI.Id} {LpI} {SectionJ.Id} {LpJ} {Section.Id}";
        }

        /// <summary>Number of sections TclForceBeamColumnCommand builds for HingeRadau.</summary>
        public const int NumSections = 6;

        /// <summary>
        /// The six HingeRadau abscissae, straight from
        /// HingeRadauBeamIntegration::getSectionLocations: a section at each end, one Radau point
        /// at 8/3*lp inside each end, and two Gauss-Legendre points over the interior. They are
        /// NOT evenly spaced, so a diagram drawn at equal steps puts the values in the wrong place.
        /// </summary>
        public IReadOnlyList<double> SectionLocations(double length)
        {
            if (length <= 0.0) return new double[0];

            double oneOverL = 1.0 / length;
            var xi = new double[NumSections];

            xi[0] = 0.0;
            xi[1] = 8.0 / 3.0 * LpI * oneOverL;
            xi[4] = 1.0 - 8.0 / 3.0 * LpJ * oneOverL;
            xi[5] = 1.0;

            double oneRoot3 = 1.0 / Math.Sqrt(3.0);
            double alpha = 0.5 - 2.0 * (LpI + LpJ) * oneOverL;
            double beta  = 0.5 + 2.0 * (LpI - LpJ) * oneOverL;
            xi[2] = alpha * (-oneRoot3) + beta;
            xi[3] = alpha * (oneRoot3) + beta;

            return xi;
        }
    }
}
