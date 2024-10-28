using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Core.Utils;
using Alpaca4d.Generic;

namespace Alpaca4d.Loads
{
    public partial class UniformExcitation : ILoad
    {
        public int? Id { get; set; } = IdGenerator.GenerateId();
        public Direction Dof { get; set; } = Direction.X;
        public LoadType Type { get; set; } = LoadType.UniformExcitation;
        public ITimeSeries TimeSeries { get; set; }
        public double Factor { get; set; } = 1.0;

        public double Velocity { get; set; } = 0.0;


        public UniformExcitation(Direction direction, ITimeSeries timeSeries, double velocity = 0.0, double factor = 1.0)
        {
            this.Dof = direction;
            this.Velocity = velocity;
            this.Factor = factor;
            this.TimeSeries = timeSeries;
        }

        public void SetTag(Alpaca4d.Model model)
        {
        }
        public string WriteTcl()
        {
            return $"pattern {Type} {Id} {(int)Dof} -accel {TimeSeries.Id} -vel0 {Velocity} -fact {Factor}";
        }
    }

    public enum Direction
    {
        X = 1,
        Y = 2,
        Z = 3,
        XX = 4,
        YY = 5,
        ZZ = 6,
    }
}