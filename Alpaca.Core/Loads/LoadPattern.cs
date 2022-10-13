using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Loads
{
    public partial class LoadPattern
    {
        public int? Id;
        public List<ILoad> Load;
        public ITimeSeries TimeSeries;
        public PatternType PatternType;

        public LoadPattern()
        {
        }

        public LoadPattern(int id, List<ILoad> load, PatternType patternType, ITimeSeries timeSeries)
        {
            this.Id = id;
            this.Load = load;
            this.PatternType = patternType;
            this.TimeSeries = timeSeries;
        }

        public string WriteTcl()
        {
            string tcl = "";
            tcl += this.TimeSeries.WriteTcl();
            if(PatternType == PatternType.Plain)
            {
                tcl += $"pattern {PatternType} {Id} {TimeSeries.Id} {{\n";
                foreach(var load in Load)
                {
                    tcl += load.WriteTcl();
                }
            }
            tcl += "}\n";

            return tcl;
        }
    }

    public enum PatternType
    {
        Plain,
        UniformExcitation,
        MultipleSupport
    }
}
