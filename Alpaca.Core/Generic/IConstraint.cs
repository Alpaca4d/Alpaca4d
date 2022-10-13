using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Rhino.Geometry;

using Alpaca4d.Constraints;

namespace Alpaca4d.Generic
{
    public interface IConstraint : ISerialize
    {
        public ConstraintType ConstraintType { get; }
        public void SetTopologyRTree(Model model);
    }
}
