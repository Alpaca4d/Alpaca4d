using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.BeamIntegration;

namespace Alpaca4d.Generic
{
    public interface IIntegration
    {
        public int? Id { get; set; }
        public IntegrationType Type { get; }
        public IUniaxialSection Section { get; set; }
        public int IntegrationPoint { get; set; }
        public string WriteTcl();
    }
}
