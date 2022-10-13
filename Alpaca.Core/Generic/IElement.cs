using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Element;

namespace Alpaca4d.Generic
{
    public interface IElement : ISerialize
    {
        public ElementType Type { get; }
        public int? Id { get; set;  }
        public void SetTags();
        public void SetTopologyRTree(Alpaca4d.Model model);

    }
}