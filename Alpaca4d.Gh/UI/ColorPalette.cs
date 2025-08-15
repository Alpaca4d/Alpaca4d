using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Drawing;

namespace Alpaca4d.UI
{
    internal static class Palette
    {
        public static Color DarkTech => Color.FromArgb(42, 45, 49);
        public static Color LightGrey => Color.FromArgb(244, 244, 244);

        // Alpaca4d Brand Colors (from logo)
        public static Color AlpacaRed => Color.FromArgb(254, 0, 0);        // Red from head/torso
        public static Color AlpacaOrange => Color.FromArgb(235, 108, 63);     // Orange from head/neck
        public static Color AlpacaPurple => Color.FromArgb(158, 53, 218);    // Purple from mid-body
        public static Color AlpacaLightGreen => Color.FromArgb(175, 201, 48); // Light green from hindquarters
        public static Color AlpacaLightBlue => Color.FromArgb(66, 136, 247);  // Light blue from hindquarters
        public static Color AlpacaDarkBlue => Color.FromArgb(1, 30, 254);     // Dark blue from tail
    }
}
