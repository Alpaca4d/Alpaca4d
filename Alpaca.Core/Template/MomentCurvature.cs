using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Alpaca4d.Section;

namespace Alpaca4d.Template
{
    public partial class MomentCurvature
    {
        public static string ForceFilePath = "FiberResults/MKsectionForce.out";
        public static string DeformationFilePath = "FiberResults/MKsectionDef.out";
        public static string FiberStressFilePath = "FiberResults/MKsectionStressFiber";
        public static string Define(FiberSection fiber, double axialForce, string dof, double maxPhi, int numIncr = 1000)
        {
            var clean = "wipe\n";
            var builder = "model BasicBuilder -ndm 3 -ndf 6\n";

            // needs to be move to the center of the section
            var node1 = "node 1 0 0 0 \n";
            var node2 = "node 2 0 0 0\n";

            var fix1 = "fix 1 1 1 1 1 1 1\n";
            var fix2 = "fix 2 0 1 1 1 0 0\n";

            var materialList = new List<Generic.IMaterial>();
            materialList.AddRange(fiber.PointFibers.Select(x => x.Material).Distinct());
            materialList.AddRange(fiber.Layers.Select(x => x.Material).Distinct());
            materialList.AddRange(fiber.Patches.Select(x => x.Material).Distinct());
            var uniqueMaterial = materialList.Distinct().Select(x => x.WriteTcl());
            var material = String.Join("", uniqueMaterial);

            var fiberSection = fiber.WriteTcl();


            var element = $"element zeroLengthSection 1 1 2 {fiber.Id}\n";


            var patternAxial = "pattern Plain 1 \"Constant\" {\n\t"
                        + $"load 2 {axialForce} 0 0 0 0 0}}\n";

            var integrator = "integrator LoadControl 0\n";
            var system = "system BandGeneral\n";
            var test = "test NormUnbalance 1e-10 1000\n";
            var number = "numberer RCM\n";
            var constraints = "constraints Plain\n";
            var algorithm = "algorithm Newton\n";
            var analysis = "analysis Static\n";
            var analyze = "analyze 1\n";
            var lc = "loadConst -time 0.0\n";


            //Create Folder and delete previously calculated file
            System.IO.Directory.CreateDirectory(MomentCurvature.ForceFilePath.Split('/').First());

            var files = System.IO.Directory.GetFiles(MomentCurvature.ForceFilePath.Split('/').First());
            foreach (var file in files)
            {
                File.Delete(file);
            }


            var recorder1 = $"recorder Element -file {MomentCurvature.ForceFilePath} -ele 1 section force\n";
            var recorder2 = $"recorder Element -file {MomentCurvature.DeformationFilePath} -ele 1 section deformation\n";
            var fiberRecorder = Alpaca4d.Recorder.Fiber(fiber);
            var recorder3 = String.Join("\n", fiberRecorder);

            var dir = (dof == "y") ? "1 0" : "0 1";

            var patternMoment = "\npattern Plain 2 \"Linear\" {\n\t"
            + $"load 2 0 0 0 0 {dir}}}\n";

            var dofInt = dof == "y" ? 5 : 6;

            var integratorDisp = $"integrator DisplacementControl 2 {dofInt} {maxPhi / numIncr}\n";
            var analyzeIncrement = $"analyze {numIncr}\n";

            return clean + builder + node1 + node2 + fix1 + fix2 + material + fiberSection + element + patternAxial + integrator + system + test + number + constraints + algorithm + analysis + analyze + lc + recorder1 + recorder2 + recorder3 + patternMoment + integratorDisp + analyzeIncrement + clean;
        }

        public static string Define(FiberSection fiber, double axialForce, double maxPhi, double alpha = 0.00, int numIncr = 1000)
        {
            var clean = "wipe\n";
            var builder = "model BasicBuilder -ndm 3 -ndf 6\n";

            // needs to be move to the center of the section
            var node1 = "node 1 0 0 0 \n";
            var node2 = "node 2 0 0 0\n";

            var fix1 = "fix 1 1 1 1 1 1 1\n";
            var fix2 = "fix 2 0 1 1 1 0 0\n";

            var materialList = new List<Generic.IMaterial>();
            materialList.AddRange(fiber.PointFibers.Select(x => x.Material).Distinct());
            materialList.AddRange(fiber.Layers.Select(x => x.Material).Distinct());
            materialList.AddRange(fiber.Patches.Select(x => x.Material).Distinct());
            var uniqueMaterial = materialList.Distinct().Select(x => x.WriteTcl());
            var material = String.Join("", uniqueMaterial);

            var fiberSection = fiber.WriteTcl();


            // to add orientation
            var element = $"element zeroLengthSection 1 1 2 {fiber.Id} -orient 1 0 0 0 {Math.Cos(alpha)} {Math.Sin(alpha)}\n";



            var patternAxial = "pattern Plain 1 \"Constant\" {\n\t"
                        + $"load 2 {axialForce} 0 0 0 0 0}}\n";

            var integrator = "integrator LoadControl 0\n";
            var system = "system BandGeneral\n";
            var test = "test NormUnbalance 1e-10 1000\n";
            var number = "numberer RCM\n";
            var constraints = "constraints Plain\n";
            var algorithm = "algorithm Newton\n";
            var analysis = "analysis Static\n";
            var analyze = "analyze 1\n";
            var lc = "loadConst -time 0.0\n";


            //Define reference moment 
            var recorder1 = $"recorder Element -file {MomentCurvature.ForceFilePath} -ele 1 section force\n";
            var recorder2 = $"recorder Element -file {MomentCurvature.DeformationFilePath} -ele 1 section deformation\n";
            var recorder3 = $"recorder Element -file {MomentCurvature.FiberStressFilePath} -ele 1 section fiber 0 stressStrain\n";


            var patternMoment = "pattern Plain 2 \"Linear\" {\n\t"
            + $"load 2 0 0 0 0 {Math.Cos(alpha)} {Math.Sin(alpha)}}}\n";


            var integratorDisp = $"integrator DisplacementControl 2 5 {maxPhi / numIncr}\n";
            var analyzeIncrement = $"analyze {numIncr}\n";

            return clean + builder + node1 + node2 + fix1 + fix2 + material + fiberSection + element + patternAxial + integrator + system + test + number + constraints + algorithm + analysis + analyze + lc + recorder1 + recorder2 + recorder3 + patternMoment + integratorDisp + analyzeIncrement + clean;
        }
    }
}
