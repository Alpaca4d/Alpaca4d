using System;
using System.Collections.Generic;
using Alpaca4d.Generic;
using Alpaca4d.Template;

namespace Alpaca4d
{
    public class Recorder : IRecorder
    {
        public string FileName { get; set; }
        public bool Displacement { get; set; }
        public bool Rotation { get; set; }
        public bool Velocity { get; set; }
        public bool Acceleration { get; set; }
        public bool ReactionForce { get; set; }
        public bool ReactionMoment { get; set; }
        public bool ModesOfVibration { get; set; }
        public bool ModesOfVibrationRotational { get; set; }
        public bool Force { get; set; }
        public bool Stress { get; set; }
        public bool SectionForce { get; set; }
        public bool SectionFiberStress { get; set; }

        public Recorder()
        {
        }

        public Recorder(string filePath, bool displacements = false, bool rotations = true, bool velocity = false, bool accelerations = false, bool reactionForces = false, bool reactionMoments = false, bool modesOfVibrations = false, bool modesOfVibrationsRotational = false, bool forces = false, bool stresses = false, bool sectionForces = false, bool sectionFiberStresses = false)
        {
            this.FileName = filePath;
            this.Displacement = displacements;
            this.Rotation = rotations;
            this.Velocity = velocity;
            this.Acceleration = accelerations;
            this.ReactionForce = reactionForces;
            this.ReactionMoment = reactionMoments;
            this.ModesOfVibration = modesOfVibrations;
            this.ModesOfVibrationRotational = modesOfVibrationsRotational;
            this.Force = forces;
            this.Stress = stresses;
            this.SectionForce = sectionForces;
            this.SectionFiberStress = SectionFiberStress;
        }

        public string WriteTcl()
        {
            string nodeRespType = "";

            if (this.Displacement)
                nodeRespType += " displacement";

            if (this.Rotation)
                nodeRespType += " rotation";

            if (this.Velocity)
                nodeRespType += " velocity";

            if (this.Acceleration)
                nodeRespType += " acceleration";

            if (this.ReactionForce)
                nodeRespType += " reactionForce";

            if (this.ReactionMoment)
                nodeRespType += " reactionMoment";

            if (this.ModesOfVibration)
                nodeRespType += " modesOfVibration";

            if (this.ModesOfVibrationRotational)
                nodeRespType += " modesOfVibrationRotational";

            string elementRespType = "";

            if (this.Force)
                elementRespType += " force";

            if (this.Stress)
                elementRespType += " stresses";

            if (this.SectionForce)
                elementRespType += " section.force";

            if (this.SectionFiberStress)
                elementRespType += " section.fiber.stress";

            return $"recorder mpco {this.FileName} -N {nodeRespType} -E {elementRespType}\n";
        }

        public static Recorder MpcoStatic(string filePath,
                                  bool displacements = true,
                                  bool rotations = true,
                                  bool velocity = false,
                                  bool accelerations = false,
                                  bool reactionForces = true,
                                  bool reactionMoments = true,
                                  bool modesOfVibrations = false,
                                  bool modesOfVibrationsRotational = false,
                                  bool forces = true,
                                  bool stresses = true,
                                  bool sectionForces = true,
                                  bool sectionFiberStresses = true)
        {
            return new Recorder(filePath, displacements, rotations, velocity, accelerations, reactionForces, reactionMoments, modesOfVibrations, modesOfVibrationsRotational, forces, stresses, sectionForces, sectionFiberStresses);
        }

        public static Recorder MpcoTransient(string filePath,
                          bool displacements = true,
                          bool rotations = true,
                          bool velocity = true,
                          bool accelerations = true,
                          bool reactionForces = true,
                          bool reactionMoments = true,
                          bool modesOfVibrations = false,
                          bool modesOfVibrationsRotational = false,
                          bool forces = true,
                          bool stresses = true,
                          bool sectionForces = true,
                          bool sectionFiberStresses = true)
        {
            return new Recorder(filePath, displacements, rotations, velocity, accelerations, reactionForces, reactionMoments, modesOfVibrations, modesOfVibrationsRotational, forces, stresses, sectionForces, sectionFiberStresses);
        }

        public static Recorder MpcoEigen(string filePath,
                  bool displacements = false,
                  bool rotations = false,
                  bool velocity = false,
                  bool accelerations = false,
                  bool reactionForces = false,
                  bool reactionMoments = false,
                  bool modesOfVibrations = true,
                  bool modesOfVibrationsRotational = true,
                  bool forces = false,
                  bool stresses = false,
                  bool sectionForces = false,
                  bool sectionFiberStresses = false)
        {
            return new Recorder(filePath, displacements, rotations, velocity, accelerations, reactionForces, reactionMoments, modesOfVibrations, modesOfVibrationsRotational, forces, stresses, sectionForces, sectionFiberStresses);
        }


        public static List<string> Fiber(Alpaca4d.Section.FiberSection FiberSection, string type = "stressStrain")
        {
            var recorders = new List<string>();

            int i = 0;
            foreach (var fiber in FiberSection.Fibers)
            {
                var posY = Math.Round(fiber.Pos.X, 2);
                var posZ = Math.Round(fiber.Pos.Y, 2);
                var fileName = $"{MomentCurvature.FiberStressFilePath}_{fiber.Index}.out";
                var recorder = $"recorder Element -file {fileName} -ele 1 section fiber {fiber.Pos.X} {fiber.Pos.Y} {type}";
                recorders.Add(recorder);
                i++;
            }

            return recorders;
        }

    }
}
