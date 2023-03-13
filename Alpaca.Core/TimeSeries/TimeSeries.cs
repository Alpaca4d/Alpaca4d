using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.TimeSeries
{
    public partial class Constant : EntityBase, ITimeSeries, ISerialize
    {
        public static Dictionary<double, Constant> _timeSeriesCache = new Dictionary<double, Constant>();
        public TimeSeriesType Type => TimeSeriesType.Constant;
        public double CFactor { get; set; }
        public int Id { get; set; }

        public Constant (double cFactor = 1.0)
        {
            this.CFactor = cFactor;
        }

        public static Constant Default(double cFactor = 1.0)
        {
            if (!_timeSeriesCache.ContainsKey(cFactor))
            {
                _timeSeriesCache[cFactor] = new Constant(cFactor);
            }
            return _timeSeriesCache[cFactor];
        }

        public List<double> DrawSeries()
        {
            var graph = Enumerable.Range(0, 10).Select(x => CFactor).ToList();
            return graph;
        }

        public override string WriteTcl()
        {
            var tclText = $"timeSeries Constant {Id} -factor {CFactor}\n";
            return tclText;
        }
    }

    public partial class Linear : EntityBase, ITimeSeries, ISerialize
    {
        public TimeSeriesType Type => TimeSeriesType.Linear;
        public double CFactor { get; set; }
        public int Id { get; set; }

        //Constructor
        public Linear()
        {

        }
        public Linear(double linearFactor = 1.0)
        {
            this.CFactor = linearFactor;
        }

        public List<double> DrawSeries()
        {
            var graph = Enumerable.Range(0, 10).Select(x => x * CFactor).ToList();
            return graph;
        }

        public override string WriteTcl()
        {
            var tclText = $"timeSeries Linear {Id} -factor {CFactor}\n";
            return tclText;
        }
    }

    public partial class Trigonometric : EntityBase, ITimeSeries, ISerialize
    {
        public int Id { get; set; }
        public TimeSeriesType Type => TimeSeriesType.Trigonometric;
        public double TStart { get; set; }
        public double TEnd { get; set; }
        public double Period { get; set; }
        public double Shift { get; set; }
        public double CFactor { get; set; }

        //Constructor
        public Trigonometric()
        {

        }
        public Trigonometric(double tStart, double tEnd, double period, double shift = 0.0, double cFactor = 1.0)
        {
            this.TStart = tStart;
            this.TEnd = tEnd;
            this.Period = period;
            this.Shift = shift;
            this.CFactor = cFactor;
        }

        public List<double> DrawSeries()
        {
            double value;
            double t = 0.0;
            var graph = new List<double>();

            var phi = this.Shift - this.Period / Math.PI * 2.0;
            while(t < TEnd * 1.5)
            {
                if(t < TEnd && t > TStart)
                {
                    value = this.CFactor * Math.Sin(2.0 * Math.PI * (t - this.TStart) / this.Period) + phi;
                }
                else
                {
                    value = 0.0;
                }
                graph.Add(value);
                t += 0.1;
            }
            return graph;
        }

        public override string WriteTcl()
        {
            var tclText = $"timeSeries Trig {Id} {TStart} {TEnd} {Period} -shift {Shift} -factor {CFactor}\n";
            return tclText;
        }
    }

    public partial class Triangle : EntityBase, ITimeSeries, ISerialize
    {
        public int Id { get; set; }
        public TimeSeriesType Type => TimeSeriesType.Triangle;
        public double TStart { get; set; }
        public double TEnd { get; set; }
        public double Period { get; set; }
        public double Shift { get; set; }
        public double CFactor { get; set; }

        //Constructor
        public Triangle()
        {

        }
        public Triangle(double tStart, double tEnd, double period, double shift = 0.0, double cFactor = 1.0)
        {
            this.TStart = tStart;
            this.TEnd = tEnd;
            this.Period = period;
            this.Shift = shift;
            this.CFactor = cFactor;
        }

        public void DrawSeries()
        {
            // pass
        }

        public override string WriteTcl()
        {
            var tclText = $"timeSeries Triangle {Id} {TStart} {TEnd} {Period} -shift {Shift} -factor {CFactor}\n";
            return tclText;
        }
    }

    public partial class PathTimeSeries : EntityBase, ITimeSeries, ISerialize
    {
        public int Id { get; set; }
        public TimeSeriesType Type => TimeSeriesType.Path;
        public double CFactor { get; set; }
        public List<double> Times { get; set; }
        public List<double> Values { get; set; }
        public PathTimeSeries()
        {
        }

        public PathTimeSeries(List<double> times, List<double> values, double cFactor = 1.00)
        {
            this.Times = times;
            this.Values = values;
            this.CFactor = cFactor;
        }

        public List<double> DrawSeries()
        {
            return this.Values;
        }

        public override string WriteTcl()
        {
            var times = String.Join(" ", this.Times);
            var values = String.Join(" ", this.Values);
            return $"timeSeries Path {Id} -time {{{times}}} -values {{{values}}} -factor {CFactor} -useLast\n";
        }

        public static PathTimeSeries ReadFile(string FilePath, char Sep = ',')
        {
            string[] text = System.IO.File.ReadAllLines(FilePath);

            var times = new List<double>();
            var values = new List<double>();

            foreach(string line in text)
            {
                var splittedLine = line.Split(Sep);
                if (splittedLine.Length <= 1)
                {
                    throw new Exception($"String '{line}' can not be split with the separator '{Sep}'");
                }
                times.Add(double.Parse(splittedLine[0]));
                values.Add(double.Parse(splittedLine[1]));
            }

            return new PathTimeSeries(times, values);
        }
    }


}