using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using Alpaca4d.Section;

namespace Alpaca4d.Template
{
    public partial class MomentCurvature
    {
        public static string OutputFolder = "FiberResults";
        public static string ForceFilePath = "FiberResults/MKsectionForce.out";
        public static string DeformationFilePath = "FiberResults/MKsectionDef.out";
        /// <summary>
        /// Where every fibre's stress and strain history goes - one file for the whole
        /// section, five columns per fibre per step. See <see cref="Alpaca4d.Recorder.FiberData"/>
        /// for why it is not a file per fibre.
        /// </summary>
        public static string FiberDataFilePath = "FiberResults/MKfiberData.out";

        /// <summary>
        /// Printed by the deck when the axial step does not converge. Nothing is recorded
        /// in that case: the recorders are only opened once the axial load is held.
        /// </summary>
        public const string AxialFailedMarker = "ALPACA_MK_AXIAL_FAILED";

        /// <summary>
        /// Printed by the deck when the curvature ramp stops early. What was reached is
        /// still recorded and still worth reading - a section that fails halfway is a
        /// result, not an error - so this is a marker and not a non-zero exit.
        /// </summary>
        public const string CurvatureIncompleteMarker = "ALPACA_MK_CURVATURE_INCOMPLETE";

        /// <summary>
        /// The section tag the deck uses. Hard-coded because the deck holds one section.
        /// </summary>
        private const int SectionTag = 1;

        /// <summary>
        /// Creates the folder the recorders write into, and clears what a previous run
        /// left there so a shorter curve cannot be read as a longer one.
        ///
        /// Separate from <see cref="Define"/>, and called after the caller has settled on
        /// a working directory: both this and the recorder paths in the deck are relative
        /// to the current directory, so they have to be resolved against the same one.
        /// </summary>
        public static void PrepareOutputFolder()
        {
            Directory.CreateDirectory(OutputFolder);

            foreach (var file in Directory.GetFiles(OutputFolder))
                File.Delete(file);
        }

        /// <summary>
        /// A moment-curvature deck: one zero-length fibre section, a held axial force, and
        /// a curvature ramp about the section's local y or z axis.
        /// </summary>
        /// <param name="fiber">The section. Its own Id is not used - the deck holds one section.</param>
        /// <param name="axialForce">Positive is tension.</param>
        /// <param name="dof">"y" or "z"; the local axis to bend about.</param>
        /// <param name="maxPhi">The curvature to ramp to.</param>
        /// <param name="numIncr">Increments to reach <paramref name="maxPhi"/> in.</param>
        public static string Define(FiberSection fiber, double axialForce, string dof, double maxPhi, int numIncr = 1000)
        {
            if (fiber == null)
                throw new ArgumentNullException("fiber");

            var bendAboutY = IsBendingAboutY(dof);

            if (numIncr < 1)
                throw new ArgumentOutOfRangeException("numIncr", "A moment-curvature analysis needs at least one increment.");

            var clean = "wipe\n";
            var builder = "model BasicBuilder -ndm 3 -ndf 6\n";

            // needs to be move to the center of the section
            var node1 = "node 1 0 0 0 \n";
            var node2 = "node 2 0 0 0\n";

            var fix1 = "fix 1 1 1 1 1 1 1\n";
            var fix2 = "fix 2 0 1 1 1 0 0\n";

            var materialList = new List<Generic.IMaterial>();
            materialList.AddRange(fiber.PointFibers.Select(x => x.Material));
            materialList.AddRange(fiber.Layers.Select(x => x.Material));
            materialList.AddRange(fiber.Patches.Select(x => x.Material));
            var uniqueMaterial = materialList.Where(x => x != null).Distinct();

            var material = String.Join("", uniqueMaterial.Select(x => x.WriteTcl()));

            var fiberSection = fiber.WriteTcl(SectionTag);

            var element = $"element zeroLengthSection 1 1 2 {SectionTag}\n";

            var timeSeriesAxial = "timeSeries Constant 1\n";
            var patternAxial = "pattern Plain 1 1 {\n\t"
                        + $"load 2 {TclNumber.Write(axialForce)} 0 0 0 0 0}}\n";

            var integrator = "integrator LoadControl 0\n";
            var system = "system BandGeneral\n";

            // NormDispIncr, not NormUnbalance: an unbalance tolerance is an absolute force
            // and so means something different in every unit system. 1e-10 N.mm is not
            // reachable at all - a clean eight-fibre section stalls at a norm around 1e-9 -
            // and the deck used to abandon the curve there.
            var test = "test NormDispIncr 1.0e-8 1000\n";
            var number = "numberer RCM\n";
            var constraints = "constraints Plain\n";
            var algorithm = "algorithm Newton\n";
            var analysis = "analysis Static\n";

            // analyze returns 0 or an error flag, and OpenSees exits 0 either way, so the
            // deck has to say so itself. Nothing is recorded yet, hence the bare exit.
            var analyze = "if {[analyze 1] != 0} {\n"
                        + $"\tputs \"{AxialFailedMarker}\"\n"
                        + "\twipe\n"
                        + "\texit 1\n"
                        + "}\n";
            var lc = "loadConst -time 0.0\n";

            var recorder1 = $"recorder Element -file {ForceFilePath} -ele 1 section force\n";
            var recorder2 = $"recorder Element -file {DeformationFilePath} -ele 1 section deformation\n";
            var recorder3 = Alpaca4d.Recorder.FiberData();

            var dir = bendAboutY ? "1 0" : "0 1";

            var timeSeriesMoment = "timeSeries Linear 2\n";
            var patternMoment = "pattern Plain 2 2 {\n\t"
            + $"load 2 0 0 0 0 {dir}}}\n";

            var dofInt = bendAboutY ? 5 : 6;

            var integratorDisp = $"integrator DisplacementControl 2 {dofInt} {TclNumber.Write(maxPhi / numIncr)}\n";

            // A ramp that stops early still leaves a usable curve behind, so this reports
            // and carries on to the wipe that flushes the recorders.
            var analyzeIncrement = $"if {{[analyze {numIncr}] != 0}} {{\n"
                                 + $"\tputs \"{CurvatureIncompleteMarker}\"\n"
                                 + "}\n";

            return Deck(
                clean, builder, node1, node2, fix1, fix2,
                material, fiberSection, element,
                timeSeriesAxial, patternAxial,
                integrator, system, test, number, constraints, algorithm, analysis,
                analyze, lc,
                recorder1, recorder2, recorder3,
                timeSeriesMoment, patternMoment,
                integratorDisp, analyzeIncrement,
                clean);
        }

        /// <summary>
        /// Joins the pieces of a deck, ending each one on its own line.
        ///
        /// Not plain concatenation. A piece that came without a trailing newline - the
        /// fibre recorders, joined line by line - swallowed the first line of whatever
        /// followed it, and what followed was "timeSeries Linear 2". The pattern that
        /// referred to it then failed with "none found with tag: 2" and no curvature was
        /// ever applied, whatever else the deck said. Terminating here rather than in
        /// twenty-odd string literals is the difference between one place to get it right
        /// and twenty.
        /// </summary>
        private static string Deck(params string[] chunks)
        {
            var sb = new System.Text.StringBuilder();

            foreach (var chunk in chunks)
            {
                if (string.IsNullOrWhiteSpace(chunk))
                    continue;

                sb.Append(chunk.TrimEnd('\r', '\n'));
                sb.Append('\n');
            }

            return sb.ToString();
        }

        /// <summary>
        /// Which local axis a direction names. Case-insensitive, because a value list is
        /// not the only thing that can reach this input, and anything else is rejected
        /// rather than quietly taken to mean z.
        /// </summary>
        public static bool IsBendingAboutY(string dof)
        {
            if (string.Equals(dof, "y", StringComparison.OrdinalIgnoreCase))
                return true;

            if (string.Equals(dof, "z", StringComparison.OrdinalIgnoreCase))
                return false;

            throw new ArgumentException(
                "Direction has to be \"y\" or \"z\", not \"" + dof + "\".", "dof");
        }
    }
}
