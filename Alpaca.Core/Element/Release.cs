using System;

namespace Alpaca4d.Element
{
    public class Release
    {
        /// <summary>Axial translation along X. False = released (low stiffness).</summary>
        public bool Tx { get; set; } = true;
        /// <summary>Translation along Y. False = released (low stiffness).</summary>
        public bool Ty { get; set; } = true;
        /// <summary>Translation along Z. False = released (low stiffness).</summary>
        public bool Tz { get; set; } = true;
        /// <summary>Torsional rotation about X. False = released (low stiffness).</summary>
        public bool Rx { get; set; } = true;
        /// <summary>Bending about Y. False = released (low stiffness).</summary>
        public bool My { get; set; } = true;
        /// <summary>Bending about Z. False = released (low stiffness).</summary>
        public bool Mz { get; set; } = true;

        public static readonly Release FullFixed = new Release();

        public Release() { }

        public Release(bool tx, bool ty, bool tz, bool rx, bool my, bool mz)
        {
            Tx = tx;
            Ty = ty;
            Tz = tz;
            Rx = rx;
            My = my;
            Mz = mz;
        }
    }
}
