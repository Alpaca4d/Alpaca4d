using System.Globalization;

namespace Alpaca4d
{
    /// <summary>
    /// Numbers on the way to and from a .tcl file.
    ///
    /// A .tcl deck is written with a dot for the decimal separator whatever the machine's
    /// locale is - OpenSees is a Tcl interpreter, and Tcl has one number format. Plain
    /// string interpolation does not give that: on a machine set to a comma-decimal
    /// locale <c>$"{0.5}"</c> writes <c>0,5</c>, which Tcl reads as two arguments, and
    /// <c>double.Parse</c> reads the solver's <c>0.5</c> back as five.
    ///
    /// Under an English locale these produce exactly what the interpolation did, so a
    /// deck that worked keeps working byte for byte.
    /// </summary>
    public static class TclNumber
    {
        /// <summary>A number as a Tcl literal.</summary>
        public static string Write(double value)
        {
            return value.ToString(CultureInfo.InvariantCulture);
        }

        /// <summary>A number as a Tcl literal; null becomes the empty string, as interpolation did.</summary>
        public static string Write(double? value)
        {
            return value.HasValue ? Write(value.Value) : string.Empty;
        }

        /// <summary>
        /// A number out of a recorder file. Invariant first, because that is what the
        /// solver writes; the machine's own locale is only a fallback for a hand-edited file.
        /// </summary>
        public static double Read(string token)
        {
            double value;
            if (double.TryParse(token, NumberStyles.Float, CultureInfo.InvariantCulture, out value))
                return value;

            return double.Parse(token, NumberStyles.Float, CultureInfo.CurrentCulture);
        }
    }
}
