using System;

namespace Alpaca4d.Generic
{
    public interface IMaterial : ISerialize
    {
        public int? Id { get; set; }
        public double? Rho { get; set; }
    }
}
