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
    }
}