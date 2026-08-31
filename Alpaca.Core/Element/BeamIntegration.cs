using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


using Alpaca4d.Generic;

namespace Alpaca4d.BeamIntegration
{
    public partial class NewtonContes : EntityBase, IIntegration
    {
        //only for python
        public int? Id { get; set; } 
        public int IntegrationPoint { get; set; }
        public IUniaxialSection Section { get; set; }
        public IntegrationType Type => IntegrationType.NewtonCotes;

        public NewtonContes()
        {
        }

        public NewtonContes(IUniaxialSection section, int integrationPoint)
        {
            this.Section = section;
            this.IntegrationPoint = integrationPoint;
        }

        public override string WriteTcl()
        {
            return $"{Type} {Section.Id} {IntegrationPoint}";
        }

        /// <summary>
        /// Newton-Cotes samples at equally spaced abscissae, ends included
        /// (NewtonCotesBeamIntegration::getSectionLocations: xi[i] = i/(N-1)).
        /// </summary>
        public IReadOnlyList<double> SectionLocations(double length)
        {
            int count = this.IntegrationPoint;
            if (count < 1) return new double[0];
            if (count == 1) return new[] { 0.5 };

            var xi = new double[count];
            for (int i = 0; i < count; i++)
                xi[i] = (double)i / (count - 1);

            return xi;
        }
    }
}