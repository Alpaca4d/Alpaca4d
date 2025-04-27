using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Loads
{
    public partial class Gravity : ILoad
    {
        public LoadType Type { get; set; } = LoadType.Gravity;
        public ITimeSeries TimeSeries { get; set; }
        public double Factor { get; set; }

        public Gravity()
        {
        }

        public Gravity(double factor, ITimeSeries timeSeries)
        {
            this.Factor = factor;
            this.TimeSeries = timeSeries;
        }

        public Gravity(ITimeSeries timeSeries)
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