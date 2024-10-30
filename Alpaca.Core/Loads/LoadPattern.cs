using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;
using Alpaca4d.Core.Utils;
using System.Runtime.CompilerServices;
using Grasshopper.Kernel.Geometry.Delaunay;

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
                    if(load.GetType() == typeof(UniformExcitation))
                        throw new Exception("UniformExcitation is not allowed in Plain Pattern");
                    tcl += load.WriteTcl();
                }
                tcl += "}\n";
            }

            // pattern UniformExcitation $patternTag $dir -accel $tsTag <-vel0 $vel0> <-fact $cFactor>
            if (PatternType == PatternType.UniformExcitation)
            {
                var loads = this.Load.OfType<UniformExcitation>().ToList();
                if (loads.Count > 1)
                {
                    throw new Exception("Only one UniformExcitation is allowed!");
                }
                else if (loads.Count == 1)
                {
                    var load = loads[0];
                    tcl += $"pattern {PatternType} {Id} {(int)load.Dof} -accel {TimeSeries.Id} -vel0 {load.Velocity} -fact {load.Factor}";
                }
            }


            return tcl;
        }
    }

    public enum PatternType
    {
        Plain,
        UniformExcitation,
        //MultipleSupport
    }
}
