using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alpaca4d.Loads
{
    public enum LoadType
    {
        PointLoad,
        DistributedLoad,
        MeshLoad,
        UniformExcitation,
        Mass,
        Gravity
    }
}
