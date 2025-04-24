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
