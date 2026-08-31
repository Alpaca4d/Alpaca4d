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

        /// <summary>
        /// Where the section results sit along the element, as normalised abscissae in [0, 1]
        /// measured from the I end, in the order OpenSees writes them. One entry per section,
        /// so the count is also the number of section force rows to expect in the recorder file.
        /// </summary>
        IReadOnlyList<double> SectionLocations(double length);
    }
}
