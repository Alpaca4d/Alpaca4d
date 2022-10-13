using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Generic
{
	public abstract class EntityBase : ISerialize
	{
		public abstract string WriteTcl();
		public override string ToString()
		{
			return this.WriteTcl();
		}
	}
}
