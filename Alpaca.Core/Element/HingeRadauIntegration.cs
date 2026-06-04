using System;
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
    }
}
