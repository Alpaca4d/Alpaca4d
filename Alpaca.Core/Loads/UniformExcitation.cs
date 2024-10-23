using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Loads
{
    public partial class UniformExcitation : ILoad
    {
        public LoadType Type { get; set; } = LoadType.UniformExcitation;
        public ITimeSeries TimeSeries { get; set; }
        public double GFactor { get; set; }

        public UniformExcitation()
        {
        }

        public UniformExcitation(double gFactor, ITimeSeries timeSeries)
        {
            this.GFactor = gFactor;
            this.TimeSeries = timeSeries;
        }

        public UniformExcitation(ITimeSeries timeSeries)
        {
            this.TimeSeries = timeSeries;
        }

        public void SetTag(Alpaca4d.Model model)
        {
        }
        public string WriteTcl()
        {
            return "";
        }
    }
}