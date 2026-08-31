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

        // Transparency factor for colors
        public static double TransparencyFactor = 0.5;

        // Tech Colors
        public static Color DarkTech => Fade(Alpaca4d.Colors.DarkTech);
        public static Color LightGrey => Fade(Alpaca4d.Colors.LightGrey);

        // Alpaca4d Brand Colors (from logo). The values live in Alpaca4d.Colors, in the
        // core, because the elements carry a colour of their own and are built there; these
        // are the same six with this palette's transparency applied.
        public static Color AlpacaRed => Fade(Alpaca4d.Colors.AlpacaRed);              // Red from head/torso
        public static Color AlpacaOrange => Fade(Alpaca4d.Colors.AlpacaOrange);        // Orange from head/neck
        public static Color AlpacaPurple => Fade(Alpaca4d.Colors.AlpacaPurple);        // Purple from mid-body
        public static Color AlpacaLightGreen => Fade(Alpaca4d.Colors.AlpacaLightGreen);// Light green from hindquarters
        public static Color AlpacaLightBlue => Fade(Alpaca4d.Colors.AlpacaLightBlue);  // Light blue from hindquarters
        public static Color AlpacaDarkBlue => Fade(Alpaca4d.Colors.AlpacaDarkBlue);    // Dark blue from tail

        /// <summary>The same colour at this palette's transparency.</summary>
        private static Color Fade(Color colour)
        {
            return Color.FromArgb((int)(255 * TransparencyFactor), colour.R, colour.G, colour.B);
        }

        // Force Diagrams Colors
        public static Color N_Positive => System.Drawing.Color.FromArgb((int)(255 * TransparencyFactor), 254, 0, 0);
        public static Color N_Negative => Color.FromArgb((int)(255 * TransparencyFactor), 1, 30, 254);
        public static Color Vy_Positive => System.Drawing.Color.FromArgb((int)(255 * TransparencyFactor), 235, 108, 63);
        public static Color Vy_Negative => System.Drawing.Color.FromArgb((int)(255 * TransparencyFactor), 66, 136, 247);
        public static Color Vz_Positive => Color.FromArgb((int)(255 * TransparencyFactor), 158, 53, 218);
        public static Color Vz_Negative => System.Drawing.Color.FromArgb((int)(255 * TransparencyFactor), 175, 201, 48);
        public static Color Torsion_Positive => System.Drawing.Color.FromArgb((int)(255 * TransparencyFactor), 254, 0, 0);
        public static Color Torsion_Negative => System.Drawing.Color.FromArgb((int)(255 * TransparencyFactor), 1, 30, 254);
        public static Color My_Positive => Color.FromArgb((int)(255 * TransparencyFactor), 235, 108, 63);
        public static Color My_Negative => Color.FromArgb((int)(255 * TransparencyFactor), 66, 136, 247);
        public static Color Mz_Positive => Color.FromArgb((int)(255 * TransparencyFactor), 158, 53, 218);
        public static Color Mz_Negative => Color.FromArgb((int)(255 * TransparencyFactor), 175, 201, 48);
    }
}
