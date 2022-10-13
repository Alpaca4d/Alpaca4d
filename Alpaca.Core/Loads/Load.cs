using System;
using Alpaca4d.Generic;

namespace Alpaca4d.Loads
{
    public partial class Load
    {
        public PointLoad PointLoad { get; set; }
        public LineLoad LineLoad { get; set; }
        public MeshLoad MeshLoad { get; set; }

        public ILoad Loads { get; set; }

        public Load()
        {
        }
    }
}
