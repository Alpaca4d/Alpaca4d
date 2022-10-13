using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Loads;
using Alpaca4d.TimeSeries;

namespace Alpaca4d.Generic
{
    public interface ILoad : ISerialize
    {
        public LoadType Type { get; set; }
        public ITimeSeries TimeSeries { get; set; }
        public void SetTag(Alpaca4d.Model model);
    }
}
