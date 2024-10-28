using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;
using Alpaca4d.Core.Utils;
using System.Runtime.CompilerServices;

namespace Alpaca4d.Loads
{
    /// <summary>
    /// pattern Plain $patternTag $tsTag <-fact $cFactor> {
    /// load...
    /// eleLoad...
    /// sp...
    /// }
    ///...
    /// </summary>
    public partial class LoadPattern
    {
        public int? Id { get; set; } = IdGenerator.GenerateId();
        public List<ILoad> Load;
        public ITimeSeries TimeSeries;
        public PatternType PatternType;
        public double Factor;

        public LoadPattern()
        {
        }

        public LoadPattern(PatternType patternType, ITimeSeries timeSeries, List<ILoad> load, double factor = 1)
        {
            this.PatternType = patternType;
            this.TimeSeries = timeSeries;
            this.Load = load;
            this.Factor = factor;
        }

        public string WriteTcl()
        {
            string tcl = "";
            tcl += this.TimeSeries.WriteTcl();
            if (PatternType == PatternType.Plain)
            {
                tcl += $"pattern {PatternType} {Id} {TimeSeries.Id} {{\n";
                foreach (var load in Load)
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
