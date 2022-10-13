using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Generic;
using Alpaca4d.TimeSeries;

namespace Alpaca4d.Generic
{
    public interface ITimeSeries : ISerialize
    {
        public int Id { get; set; }
        public TimeSeriesType Type { get; }
        public double CFactor { get; set; }
    }
}
