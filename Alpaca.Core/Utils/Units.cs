using Rhino;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alpaca4d
{
    public static class Units
    {
        public static LengthUnit Length = LengthUnit.m;
        public static ForceUnit Force = ForceUnit.kN;
        public static MassUnits Mass = MassUnits.kg;
        public static TimeUnit Time = TimeUnit.s;
        public static AngleUnit Angle = AngleUnit.rad;
    }

    public enum AngleUnit
    {
        deg,
        rad,
    }
    public enum TimeUnit
    {
        s,
        min,
        h,
    }

    public enum LengthUnit
    {
        mm,
        m,
    }

    public enum ForceUnit
    {
        N,
        kN,
    }

    public enum MassUnits
    {
        kg,
    }
}
