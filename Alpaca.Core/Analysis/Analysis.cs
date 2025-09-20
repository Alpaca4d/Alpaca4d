using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d
{
    public partial class Settings : EntityBase
    {
        public Constraint Constraint { get; set; }
        public Numberer Numberer { get; set; }
        public SystemEquation SystemEquation { get; set; }
        public Test Test { get; set; }
        public Algorithm Algorithm { get; set; }
        public Integrator Integrator { get; set; }
        public Analysis Analysis { get; set; }
        public AnalysisStep AnalysisStep { get; set; }
        public Damping Damping { get; set; }

        public Settings()
        {

        }

        public Settings(Constraint constraint, Numberer numberer, SystemEquation systemEquation, Test test, Algorithm algorithm, Integrator integrator, Analysis analysis, AnalysisStep analysisSteps, Damping damping = null)
        {
            this.Constraint = constraint;
            this.Numberer = numberer;
            this.SystemEquation = systemEquation;
            this.Test = test;
            this.Algorithm = algorithm;
            this.Integrator = integrator;
            this.Analysis = analysis;
            this.AnalysisStep = analysisSteps;
            this.Damping = damping;
        }

        public override string WriteTcl()
        {
            string tclText = "";
            if(Damping != null)
                tclText += this.Damping.WriteTcl();
            tclText += this.Constraint.WriteTcl();
            tclText += this.Numberer.WriteTcl();
            tclText += this.SystemEquation.WriteTcl();
            tclText += this.Test.WriteTcl();
            tclText += this.Algorithm.WriteTcl();
            tclText += this.Integrator.WriteTcl();
            tclText += this.Analysis.WriteTcl();
            tclText += this.AnalysisStep.WriteTcl();
            return tclText;
        }
    }
    public class Constraint
    {
        public ConstraintType Type { get; set; } = ConstraintType.Transformation;
        public enum ConstraintType
        {
            Plain,
            Transformation
        }
        public Constraint(string type)
        {
            this.Type = (ConstraintType) Enum.Parse(typeof(ConstraintType), type, true);
        }
        public string WriteTcl()
        {
            return $"constraints {Type}\n";
        }
    }

    public class Numberer
    {
        public NumbererType Type { get; set; }
        public enum NumbererType
        {
            RCM,
            AMD,
            Plain,
            ParallelPlain,
            ParallelRCM
        }
        public Numberer(string type)
        {
            this.Type = (NumbererType) Enum.Parse(typeof(NumbererType), type, true);
        }

        public string WriteTcl()
        {
            return $"numberer {Type}\n";
        }
    }

    public class SystemEquation
    {
        public SystemType Type { get; set; }
        public enum SystemType
        {
            BandGen,
            BandSPD,
            ProfileSPD,
            SuperLU,
            UmfPack,
            FullGeneral,
            SparseSYM
        }

        public SystemEquation(string type)
        {
            this.Type = (SystemType) Enum.Parse(typeof(SystemType), type, true);
        }

        public string WriteTcl()
        {
            return $"system {Type}\n";
        }

    }

    public class Test
    {
        public TestType Type { get; set; }
        public double Tol { get; set; }
        public double? TolR { get; set; }
        public int Iter { get; set; }
        public NormType Norm { get; set; } = NormType.TwoNorm;
        public FlagType Flag { get; set; } = FlagType.Nothing;
        public int? MaxIncr { get; set; }

        public enum TestType
        {
            NormUnbalance,
            NormDispIncr,
            EnergyIncr,
            NormDispAndUnbalance,
            NormDispOrUnbalance,
            RelativeNormUnbalance,
            RelativeNormDispIncr,
            RelativeTotalNormDispIncr,
            RelativeEnergyIncr,
            FixedNumIter,
        }
        public enum NormType
        {
            MaxNorm,
            OneNorm,
            TwoNorm
        }
        public enum FlagType
        {
            Nothing = 0,
            EachTime = 1,
            Successful = 2,
            EachStep = 4,
            ErrorMessage = 5
        }

        public Test()
        {
        }
        public Test(TestType testType , double tol = 1e-8, int iter = 10, FlagType flag = FlagType.Nothing, NormType norm = NormType.TwoNorm, int? maxIncr = null)
        {
            this.Type = testType;
            this.Tol = tol;
            this.Iter = iter;
            this.Flag = flag;
            this.Norm = norm;
            this.MaxIncr = maxIncr;
        }
        public static Test EnergyIncr(double tol = 1e-8, int iter = 10, FlagType flag = FlagType.Nothing, NormType norm = NormType.TwoNorm, int? maxIncr = null)
        {
            var test = new Test();
            test.Type = TestType.EnergyIncr;
            test.Tol = tol;
            test.Iter = iter;
            test.Flag = flag;
            test.Norm = norm;
            test.MaxIncr = maxIncr;
            return test;
        }

        public static Test NormUnbalance(double tol = 1e-8, int iter = 10, FlagType flag = FlagType.Nothing, NormType norm = NormType.TwoNorm, int? maxIncr = null)
        {
            var test = new Test();
            test.Type = TestType.NormUnbalance;
            test.Tol = tol;
            test.Iter = iter;
            test.Flag = flag;
            test.Norm = norm;
            test.MaxIncr = maxIncr;
            return test;
        }
        public static Test NormDispAndUnbalance(double tolIncr = 1e-8, double tolR = 1e-8, int iter = 10, FlagType flag = FlagType.Nothing, NormType norm = NormType.TwoNorm, int? maxIncr = null)
        {
            var test = new Test();
            test.Type = TestType.NormDispAndUnbalance;
            test.Tol = tolIncr;
            test.TolR = tolR;
            test.Iter = iter;
            test.Flag = flag;
            test.Norm = norm;
            test.MaxIncr = maxIncr;
            return test;
        }
        public static Test NormDispOrUnbalance(double tolIncr = 1e-8, double tolR = 1e-8, int iter = 10, FlagType flag = FlagType.Nothing, NormType norm = NormType.TwoNorm, int? maxIncr = null)
        {
            var test = new Test();
            test.Type = TestType.NormDispOrUnbalance;
            test.Tol = tolIncr;
            test.TolR = tolR;
            test.Iter = iter;
            test.Flag = flag;
            test.Norm = norm;
            test.MaxIncr = maxIncr;
            return test;
        }


        public string WriteTcl()
        {
            if (this.Type == TestType.NormDispAndUnbalance || this.Type == TestType.NormDispOrUnbalance)
                return $"test {Type} {Tol} {TolR} {Iter} {(int)Flag} {(int)Norm} {MaxIncr}\n";
            else
                return $"test {Type} {Tol} {Iter} {(int)Flag} {(int)Norm} {MaxIncr}\n";
        }

    }

    public class Algorithm
    {
        public AlgorithmType Type { get; set; }
        public enum AlgorithmType
        {
            Linear,
            Newton,
            NewtonLineSearch,
            ModifiedNewton,
            KrylovNewton,
            SecantNewton,
            BFGS,
            Broyden
        }

        public Algorithm(string type)
        {
            this.Type = (AlgorithmType) Enum.Parse(typeof(AlgorithmType), type, true);
        }
        public string WriteTcl()
        {
            return $"algorithm {Type}\n";
        }

    }

    public class Integrator
    {
        public IntegratorType Type { get; set; }
        public double? Lambda { get; set; }
        public int? NumIter { get; set; }
        public double? MinLambda { get; set; }
        public double? MaxLambda { get; set; }
        public double? Gamma { get; set; }
        public double? Beta { get; set; }

        public enum IntegratorType
        {
            LoadControl,
            Newmark,
            CentralDifference
        }
        public Integrator()
        {

        }

        public Integrator(double lambda, int numIter, double minLambda, double maxLambda)
        {
            this.Lambda = lambda;
            this.NumIter = numIter;
            this.MinLambda = minLambda;
            this.MaxLambda = maxLambda;
        }

        public static Integrator LoadControl(double lambda, int? numIter = null, double? minLambda = null, double? maxLambda = null)
        {
            var integrator = new Integrator();
            integrator.Type = IntegratorType.LoadControl;
            integrator.Lambda = lambda;
            integrator.MaxLambda = maxLambda;
            integrator.NumIter = numIter;
            integrator.MinLambda = minLambda;
            return integrator;
        }
        public static Integrator Newmark(double gamma, double beta)
        {
            var integrator = new Integrator();
            integrator.Type = IntegratorType.Newmark;
            integrator.Gamma = gamma;
            integrator.Beta = beta;
            return integrator;
        }

        public static Integrator CentralDifference()
        {
            var integrator = new Integrator();
            integrator.Type = IntegratorType.CentralDifference;
            return integrator;
        }

        public string WriteTcl()
        {
            if (this.Type == IntegratorType.LoadControl)
                return $"integrator {Type} {Lambda} {NumIter} {MinLambda} {MaxLambda}\n";
            else if (this.Type == IntegratorType.Newmark)
                return $"integrator {Type} {Gamma} {Beta}\n";
            else if (this.Type == IntegratorType.CentralDifference)
                return $"integrator {Type}\n";
            else
                throw new Exception($"Integrator {Type} does not exist");
        }

    }

    public partial class Analysis
    {
        public AnalysisType Type { get; set; }
        public enum AnalysisType
        {
            Static,
            Transient
        }

        public enum Solver
        {
            genBandArpack,
            symmBandLapack,
            fullGenLapack,
		}

        public Analysis()
        {
        }

        public Analysis(string type)
        {
            this.Type = (AnalysisType) Enum.Parse(typeof(AnalysisType), type, true);
        }

        public string WriteTcl()
        {
            return $"analysis {Type}\n";
        }
    }

    public partial class AnalysisStep
    {
        public int NumIncr { get; set; }
        public double? Dt { get; set; }
        public double? DtMin { get; set; }
        public double? DtMax { get; set; }
        public int? Jd { get; set; }

        public AnalysisStep()
        {

        }

        public AnalysisStep(int numIncr, double? dt = null, double? dtMin = null, double? dtMax = null, int? jD = null)
        {
            this.NumIncr = numIncr;
            this.Dt = dt;
            this.DtMin = dtMin;
            this.DtMax = dtMax;
            this.Jd = jD;
        }

        public AnalysisStep(string text)
        {
            string[] values = text.Split(' ');
            try
            {
                this.NumIncr = int.Parse(values[0]);
                this.Dt = int.Parse(values[1]);
                this.DtMin = int.Parse(values[2]);
                this.DtMax = int.Parse(values[3]);
                this.Jd = int.Parse(values[4]);
            }
            catch
            {

            }
        }

        public AnalysisStep(int numIncr)
        {
            this.NumIncr = numIncr;
        }

        public string WriteTcl()
        {
            return $"analyze {NumIncr} {Dt} {DtMin} {DtMax} {Jd}";
        }
    }

    public partial class Damping
    {
        public double AlphaM { get; set; }
        public double BetaKCurr { get; set; }
        public double BetaKInit { get; set; }
        public double BetaKComm { get; set; }

        public Damping(double alphaM, double betaKCurr, double betaKInit, double betaKcomm)
        {
            this.AlphaM = alphaM;
            this.BetaKCurr = betaKCurr;
            this.BetaKInit = betaKInit;
            this.BetaKCurr = betaKcomm;
        }

        public string WriteTcl()
        {
            return $"rayleigh {this.AlphaM} {this.BetaKCurr} {this.BetaKInit} {this.BetaKComm}\n";
        }
    }
}