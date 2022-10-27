using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel;
using System.Text.RegularExpressions;

using System.Drawing;
using Rhino.Geometry;
using Grasshopper;
using Grasshopper.Kernel.Data;

namespace Alpaca4d
{
    public partial class Colors
    {

        public static byte interpolate(byte a, byte b, double p)
        {
            return (byte)(a * (1 - p) + b * p);
        }

        public static Color GetColor(double v, SortedDictionary<double, Color> d)
        {
            KeyValuePair<double, Color> kvp_previous = new KeyValuePair<double, Color>(-1, d.Values.First());
            foreach (KeyValuePair<double, Color> kvp in d)
            {
                if (kvp.Key > v)
                {
                    double p = (v - kvp_previous.Key) / (double)(kvp.Key - kvp_previous.Key);
                    Color a = kvp_previous.Value;
                    Color b = kvp.Value;
                    Color c = Color.FromArgb(
                        interpolate(a.R, b.R, p),
                        interpolate(a.G, b.G, p),
                        interpolate(a.B, b.B, p));
                    return c;
                }
                else if (kvp.Key == v)
                {
                    return kvp.Value;
                }
                kvp_previous = kvp;
            }

            return d.Values.Last();
        }

        public static List<System.Drawing.Color> Gradient(int index)
        {
            {
                List<Color> colors;
                var keyValuePairs = new Dictionary<int, List<System.Drawing.Color>>();
                keyValuePairs.Add(0, new List<Color> { System.Drawing.Color.FromArgb(75, 107, 169), System.Drawing.Color.FromArgb(115, 147, 202), System.Drawing.Color.FromArgb(170, 200, 247), System.Drawing.Color.FromArgb(193, 213, 208), System.Drawing.Color.FromArgb(245, 239, 103), System.Drawing.Color.FromArgb(252, 230, 74), System.Drawing.Color.FromArgb(239, 156, 21), System.Drawing.Color.FromArgb(234, 123, 0), System.Drawing.Color.FromArgb(234, 74, 0), System.Drawing.Color.FromArgb(234, 38, 0) });
                keyValuePairs.Add(1, new List<Color> { System.Drawing.Color.FromArgb(49, 54, 149), System.Drawing.Color.FromArgb(69, 117, 180), System.Drawing.Color.FromArgb(116, 173, 209), System.Drawing.Color.FromArgb(171, 217, 233), System.Drawing.Color.FromArgb(224, 243, 248), System.Drawing.Color.FromArgb(255, 255, 191), System.Drawing.Color.FromArgb(254, 224, 144), System.Drawing.Color.FromArgb(253, 174, 97), System.Drawing.Color.FromArgb(244, 109, 67), System.Drawing.Color.FromArgb(215, 48, 39), System.Drawing.Color.FromArgb(165, 0, 38) });
                keyValuePairs.Add(2, new List<Color> { System.Drawing.Color.FromArgb(4, 25, 145), System.Drawing.Color.FromArgb(7, 48, 224), System.Drawing.Color.FromArgb(7, 88, 255), System.Drawing.Color.FromArgb(1, 232, 255), System.Drawing.Color.FromArgb(97, 246, 156), System.Drawing.Color.FromArgb(166, 249, 86), System.Drawing.Color.FromArgb(254, 244, 1), System.Drawing.Color.FromArgb(255, 121, 0), System.Drawing.Color.FromArgb(239, 39, 0), System.Drawing.Color.FromArgb(138, 17, 0) });
                keyValuePairs.Add(3, new List<Color> { System.Drawing.Color.FromArgb(0, 0, 255), System.Drawing.Color.FromArgb(53, 0, 202), System.Drawing.Color.FromArgb(107, 0, 148), System.Drawing.Color.FromArgb(160, 0, 95), System.Drawing.Color.FromArgb(214, 0, 41), System.Drawing.Color.FromArgb(255, 12, 0), System.Drawing.Color.FromArgb(255, 66, 0), System.Drawing.Color.FromArgb(255, 119, 0), System.Drawing.Color.FromArgb(255, 173, 0), System.Drawing.Color.FromArgb(255, 226, 0), System.Drawing.Color.FromArgb(255, 255, 0) });
                keyValuePairs.Add(4, new List<Color> { System.Drawing.Color.FromArgb(0, 0, 0), System.Drawing.Color.FromArgb(110, 0, 153), System.Drawing.Color.FromArgb(255, 0, 0), System.Drawing.Color.FromArgb(255, 255, 102), System.Drawing.Color.FromArgb(255, 255, 255) });
                keyValuePairs.Add(5, new List<Color> { System.Drawing.Color.FromArgb(0, 136, 255), System.Drawing.Color.FromArgb(200, 225, 255), System.Drawing.Color.FromArgb(255, 255, 255), System.Drawing.Color.FromArgb(255, 230, 230), System.Drawing.Color.FromArgb(255, 0, 0) });
                keyValuePairs.Add(6, new List<Color> { System.Drawing.Color.FromArgb(5, 48, 97), System.Drawing.Color.FromArgb(33, 102, 172), System.Drawing.Color.FromArgb(67, 147, 195), System.Drawing.Color.FromArgb(146, 197, 222), System.Drawing.Color.FromArgb(209, 229, 240), System.Drawing.Color.FromArgb(255, 255, 255), System.Drawing.Color.FromArgb(253, 219, 199), System.Drawing.Color.FromArgb(244, 165, 130), System.Drawing.Color.FromArgb(214, 96, 77), System.Drawing.Color.FromArgb(178, 24, 43), System.Drawing.Color.FromArgb(103, 0, 31) });
                keyValuePairs.Add(7, new List<Color> { System.Drawing.Color.FromArgb(255, 255, 255), System.Drawing.Color.FromArgb(253, 219, 199), System.Drawing.Color.FromArgb(244, 165, 130), System.Drawing.Color.FromArgb(214, 96, 77), System.Drawing.Color.FromArgb(178, 24, 43), System.Drawing.Color.FromArgb(103, 0, 31) });
                keyValuePairs.Add(8, new List<Color> { System.Drawing.Color.FromArgb(255, 255, 255), System.Drawing.Color.FromArgb(209, 229, 240), System.Drawing.Color.FromArgb(146, 197, 222), System.Drawing.Color.FromArgb(67, 147, 195), System.Drawing.Color.FromArgb(33, 102, 172), System.Drawing.Color.FromArgb(5, 48, 97) });
                keyValuePairs.Add(9, new List<Color> { System.Drawing.Color.FromArgb(0, 16, 120), System.Drawing.Color.FromArgb(38, 70, 160), System.Drawing.Color.FromArgb(5, 180, 222), System.Drawing.Color.FromArgb(16, 180, 109), System.Drawing.Color.FromArgb(59, 183, 35), System.Drawing.Color.FromArgb(143, 209, 19), System.Drawing.Color.FromArgb(228, 215, 29), System.Drawing.Color.FromArgb(246, 147, 17), System.Drawing.Color.FromArgb(243, 74, 0), System.Drawing.Color.FromArgb(255, 0, 0) });
                keyValuePairs.Add(10, new List<Color> { System.Drawing.Color.FromArgb(0, 191, 48), System.Drawing.Color.FromArgb(255, 238, 184), System.Drawing.Color.FromArgb(255, 0, 0) });
                keyValuePairs.Add(11, new List<Color> { System.Drawing.Color.FromArgb(204, 0, 71), System.Drawing.Color.FromArgb(255, 182, 71), System.Drawing.Color.FromArgb(206, 255, 115), System.Drawing.Color.FromArgb(26, 180, 214), System.Drawing.Color.FromArgb(0, 0, 207) });
                keyValuePairs.Add(12, new List<Color> { System.Drawing.Color.FromArgb(255, 51, 51), System.Drawing.Color.FromArgb(255, 170, 51), System.Drawing.Color.FromArgb(255, 255, 51), System.Drawing.Color.FromArgb(170, 255, 125), System.Drawing.Color.FromArgb(51, 255, 231), System.Drawing.Color.FromArgb(51, 170, 255), System.Drawing.Color.FromArgb(51, 51, 255) });
                bool success = keyValuePairs.TryGetValue(index, out colors);
                if (!success)
                {
                    keyValuePairs.TryGetValue(9, out colors);
                }
                return colors;
            }
        }
    }
}
