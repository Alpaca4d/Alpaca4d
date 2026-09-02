using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


using Rhino.Geometry;
using Grasshopper;
using Alpaca4d;
using Alpaca4d.Helper;
using PureHDF;
using Newtonsoft.Json.Linq;

namespace Alpaca4d.Result
{

    public enum ResultType
    {
        DISPLACEMENT,
        ROTATION,
        VELOCITY,
        ACCELERATION,
        REACTION_FORCE,
        REACTION_MOMENT,
        MODES_OF_VIBRATION_U,
        MODES_OF_VIBRATION_R
    }

    public enum ResultLocation
    {
        NODES,
        ELEMENTS,
    }

    public partial class Read
    {
        private const string ON_NODES = "/MODEL_STAGE[1]/RESULTS/ON_NODES";
        private const string ON_ELEMENTS = "/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS";
        private const string STEP_PREFIX = "STEP_";

        /// <summary>
        /// How many steps the recorder actually wrote, which is the count a caller needs to
        /// walk a whole time history.
        ///
        /// Read off the file rather than off Settings.AnalysisStep.NumIncr: a model can be
        /// run with no Settings at all, an analysis that stops early writes fewer steps than
        /// it was asked for, and a deserialised model carries no Settings to ask.
        ///
        /// A modal run nests its results as STEP_0/MODE_n instead, so this returns 1 there -
        /// modes are counted by the eigenvalue analysis, not by this.
        /// </summary>
        public static int StepCount(Model alpacaModel)
        {
            if (alpacaModel == null || alpacaModel.Recorders == null || !alpacaModel.Recorders.Any())
                return 0;

            string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);
            if (!System.IO.File.Exists(recorderPath))
                return 0;

            using var h5File = PureHDF.H5File.OpenRead(recorderPath);

            // Every recorded quantity is written for the same steps, so the first group that
            // holds any settles the count.
            foreach (var dataGroup in DataGroups(h5File))
            {
                int count = dataGroup.Children().Count(child => child.Name.StartsWith(STEP_PREFIX));
                if (count > 0)
                    return count;
            }

            return 0;
        }

        /// <summary>
        /// Every DATA group in the file: one per nodal quantity, and one per element class
        /// per element quantity. Laid out as ON_NODES/&lt;quantity&gt;/DATA and
        /// ON_ELEMENTS/&lt;quantity&gt;/&lt;class&gt;/DATA.
        /// </summary>
        private static IEnumerable<PureHDF.IH5Group> DataGroups(PureHDF.IH5Group h5File)
        {
            if (h5File.LinkExists(ON_NODES))
            {
                foreach (var quantity in h5File.Group(ON_NODES).Children().OfType<PureHDF.IH5Group>())
                {
                    if (quantity.LinkExists("DATA"))
                        yield return quantity.Group("DATA");
                }
            }

            if (h5File.LinkExists(ON_ELEMENTS))
            {
                foreach (var quantity in h5File.Group(ON_ELEMENTS).Children().OfType<PureHDF.IH5Group>())
                {
                    foreach (var elementClass in quantity.Children().OfType<PureHDF.IH5Group>())
                    {
                        if (elementClass.LinkExists("DATA"))
                            yield return elementClass.Group("DATA");
                    }
                }
            }
        }

        /// <summary>
        /// Methods to return nodal Displacement, Rotation, Velocity, Acceleration
        /// </summary>
        /// <param name="alpacaModel"></param>
        /// <param name="step"></param>
        /// <param name="resultType"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>
        public static IEnumerable<Rhino.Geometry.Vector3d> NodalOutput(Model alpacaModel, int step, ResultType resultType, List<int?> nodeIndex = null)
        {
            var dataOutput = Enumerable.Empty<Rhino.Geometry.Vector3d>();

            string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);

            using var h5File = PureHDF.H5File.OpenRead(recorderPath);           
            double[,] values;

            var _resultType = Alpaca4d.Helper.EnumHelper.ResultTypeConvert(resultType);
            if (alpacaModel.IsModal == false)
            {
                var dataset = h5File.Dataset($"/MODEL_STAGE[1]/RESULTS/ON_NODES/{_resultType}/DATA/STEP_{step}");
                var dimX = (long)dataset.Space.Dimensions[0];
                var dimY = (long)dataset.Space.Dimensions[1];

                values = dataset.Read<double>().ToArray2D(dimX, dimY);
            }
            else
            {
                var dataset = h5File.Dataset($"MODEL_STAGE[1]/RESULTS/ON_NODES/{_resultType}/DATA/STEP_0/MODE_{step}");
                var dimX = (long)dataset.Space.Dimensions[0];
                var dimY = (long)dataset.Space.Dimensions[1];

                values = dataset.Read<double>().ToArray2D(dimX, dimY);
            }


            try
            {
                // read all data base
                if (nodeIndex == null)
                {
                    for (int i = 0; i < alpacaModel.Nodes.Count; i++)
                    {
                        double x = (double)values.GetValue(i, 0);
                        double y = (double)values.GetValue(i, 1);
                        double z = (double)values.GetValue(i, 2);
                        dataOutput = dataOutput.Append(new Rhino.Geometry.Vector3d(x, y, z));
                    }
                    h5File.Dispose();
                }
                // read value only for selected nodes
                else
                {
                    foreach (int i in nodeIndex)
                    {
                        double x = (double)values.GetValue(i - 1, 0);
                        double y = (double)values.GetValue(i - 1, 1);
                        double z = (double)values.GetValue(i - 1, 2);
                        dataOutput = dataOutput.Append(new Rhino.Geometry.Vector3d(x, y, z));
                    }
                    h5File.Dispose();
                }
            }
            catch
            {
                h5File.Dispose();

                throw new Exception($"STEP_{step} not defined!");
            }

            return dataOutput;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="alpacaModel"></param>
        /// <param name="step"></param>
        /// <param name="resultType"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>
        public static (List<List<double>> n, List<List<double>> mz, List<List<double>> vy, List<List<double>> my, List<List<double>> vz, List<List<double>> t) ForceBeamColumn(Model alpacaModel, int step, string resultType = null)
        {
            // MPCORecorder names every element result group
            //     <classTag>-<className>[<integrationRule>:<customRuleIndex>:<headerIndex>]
            // (MPCORecorder.cpp, "create a name for this dataset using the following format").
            // forceBeamColumn always lands on integrationRule 1000 (CustomIntegrationRule), and
            // customRuleIndex is handed out in order of discovery, one per DISTINCT set of
            // normalised Gauss point locations - not one per integration type. So the index is
            // not a stable label: with NewtonCotes and HingeRadau in the same model, whichever
            // element the domain reaches first takes index 1. Worse, HingeRadau locations depend
            // on lpI/L and lpJ/L, so every distinct hinge length ratio spawns another group
            // ([1000:3:0], [1000:4:0], ...). Hard-coding a list of keys silently drops the beams
            // that fall outside it, so enumerate whatever the file actually holds and key the
            // rows by element ID, which is unique across the whole model.
            const string BASE = "/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/section.force";
            const string BEAM_CLASS = "ForceBeamColumn";
            const int SECTIONFORCES = 6;

            var nNested  = new List<List<double>>();
            var mzNested = new List<List<double>>();
            var vyNested = new List<List<double>>();
            var myNested = new List<List<double>>();
            var vzNested = new List<List<double>>();
            var tNested  = new List<List<double>>();

            string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);

            using var h5File = PureHDF.H5File.OpenRead(recorderPath);

            if (!h5File.LinkExists(BASE))
                throw new Exception(
                    "The recorder file holds no section forces. Switch \"section.force\" on in the Recorder component.");

            // Map: element ID -> row data (all columns for that element)
            var rowById = new Dictionary<int, double[]>();

            var beamGroups = h5File.Group(BASE)
                                   .Children()
                                   .OfType<PureHDF.IH5Group>()
                                   .Where(group => group.Name.Contains(BEAM_CLASS))
                                   .ToList();

            foreach (var group in beamGroups)
            {
                var stepGroup = group.Group("DATA");
                if (!stepGroup.LinkExists($"STEP_{step}"))
                    throw new Exception($"STEP_{step} not defined!");

                var idDataset   = group.Dataset("ID");
                var dataDataset = stepGroup.Dataset($"STEP_{step}");

                long rows = (long)dataDataset.Space.Dimensions[0];
                long cols = (long)dataDataset.Space.Dimensions[1];
                long idRows = (long)idDataset.Space.Dimensions[0];

                double[,] data = dataDataset.Read<double>().ToArray2D(rows, cols);
                int[,]    ids  = idDataset.Read<int>().ToArray2D(idRows, 1L);

                for (int r = 0; r < rows; r++)
                {
                    int elemId = ids[r, 0];
                    var rowData = new double[cols];
                    for (int c = 0; c < cols; c++)
                        rowData[c] = data[r, c];
                    rowById[elemId] = rowData;
                }
            }

            try
            {
                foreach (var beam in alpacaModel.Beams)
                {
                    var n  = new List<double>();
                    var mz = new List<double>();
                    var vy = new List<double>();
                    var my = new List<double>();
                    var vz = new List<double>();
                    var t  = new List<double>();

                    if (rowById.TryGetValue(beam.Id.Value, out double[] row))
                    {
                        // Derive the number of integration points from the column count
                        int numIP = row.Length / SECTIONFORCES;
                        for (int j = 0; j < SECTIONFORCES * numIP; j += SECTIONFORCES)
                        {
                            n.Add(row[j + 0]);
                            mz.Add(row[j + 1]);
                            vy.Add(row[j + 2]);
                            my.Add(row[j + 3]);
                            vz.Add(row[j + 4]);
                            t.Add(row[j + 5]);
                        }
                    }

                    nNested.Add(n);
                    mzNested.Add(mz);
                    vyNested.Add(vy);
                    myNested.Add(my);
                    vzNested.Add(vz);
                    tNested.Add(t);
                }
                h5File.Dispose();
            }
            catch
            {
                h5File.Dispose();
                throw new Exception($"STEP_{step} not defined!");
            }

            return (nNested, mzNested, vyNested, myNested, vzNested, tNested);
        }

        public static (List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>) ASDQ4Forces(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "203-ASDShellQ4[201:0:0]";
            var fxxNested = new List<List<double>>();
            var fyyNested = new List<List<double>>();
            var fxyNested = new List<List<double>>();
            var mxxNested = new List<List<double>>();
            var myyNested = new List<List<double>>();
            var mxyNested = new List<List<double>>();
            var vxzNested = new List<List<double>>();
            var vyzNested = new List<List<double>>();

            string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);

            using var h5File = PureHDF.H5File.OpenRead(recorderPath);
            double[,] values;

            var dataset = h5File.Dataset($"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/section.force/{resultType}/DATA/STEP_{step}");
            var dimX = (long)dataset.Space.Dimensions[0];
            var dimY = (long)dataset.Space.Dimensions[1];

            values = dataset.Read<double>().ToArray2D(dimX, dimY);

            var asdq4ShellNumber = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ASDShellQ4).Count();

            try
            {
                for (int i = 0; i < asdq4ShellNumber; i++)
                {
                    var fxx = new List<double>();
                    var fyy = new List<double>();
                    var fxy = new List<double>();
                    var mxx = new List<double>();
                    var myy = new List<double>();
                    var mxy = new List<double>();
                    var vxz = new List<double>();
                    var vyz = new List<double>();

                    int NUMBER_COMPONENTS = 8;
                    int NUMBER_NODES = 4;
                    for (int j = 0; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fxx.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 1; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fyy.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 2; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fxy.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 3; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        mxx.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 4; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        myy.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 5; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        mxy.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 6; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        vxz.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 7; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        vyz.Add((double)values.GetValue(i, j));
                    }

                    fxxNested.Add(fxx);
                    fyyNested.Add(fyy);
                    fxyNested.Add(fxy);
                    mxxNested.Add(mxx);
                    myyNested.Add(myy);
                    mxyNested.Add(mxy);
                    vxzNested.Add(vxz);
                    vyzNested.Add(vyz);
                }

                h5File.Dispose();
            }
            catch
            {
                h5File.Dispose();
                throw new Exception($"STEP_{step} not defined!");
            }

            return (fxxNested, fyyNested, fxyNested, mxxNested, myyNested, mxyNested, vxzNested, vyzNested);
        }

        public static (List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>) DKGTForces(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "167-ShellDKGT[103:0:0]"; // DKGT
            //resultType = "168-UnknownMovableObject[103:0:0]"; // NLDKGT
            var fxxNested = new List<List<double>>();
            var fyyNested = new List<List<double>>();
            var fxyNested = new List<List<double>>();
            var mxxNested = new List<List<double>>();
            var myyNested = new List<List<double>>();
            var mxyNested = new List<List<double>>();
            var vxzNested = new List<List<double>>();
            var vyzNested = new List<List<double>>();

            string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);

            using var h5File = PureHDF.H5File.OpenRead(recorderPath);
            double[,] values;

            var dataset = h5File.Dataset($"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/section.force/{resultType}/DATA/STEP_{step}");
            var dimX = (long)dataset.Space.Dimensions[0];
            var dimY = (long)dataset.Space.Dimensions[1];

            values = dataset.Read<double>().ToArray2D(dimX, dimY);

            var dkgtShellNumber = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ShellDKGT).Count();

            try
            {
                for (int i = 0; i < dkgtShellNumber; i++)
                {
                    var fxx = new List<double>();
                    var fyy = new List<double>();
                    var fxy = new List<double>();
                    var mxx = new List<double>();
                    var myy = new List<double>();
                    var mxy = new List<double>();
                    var vxz = new List<double>();
                    var vyz = new List<double>();

                    int NUMBER_COMPONENTS = 8;
                    int NUMBER_NODES = 3;
                    for (int j = 0; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fxx.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 1; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fyy.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 2; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fxy.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 3; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        mxx.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 4; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        myy.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 5; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        mxy.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 6; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        vxz.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 7; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        vyz.Add((double)values.GetValue(i, j));
                    }

                    fxxNested.Add(fxx);
                    fyyNested.Add(fyy);
                    fxyNested.Add(fxy);
                    mxxNested.Add(mxx);
                    myyNested.Add(myy);
                    mxyNested.Add(mxy);
                    vxzNested.Add(vxz);
                    vyzNested.Add(vyz);
                }

                h5File.Dispose();
            }
            catch
            {
                h5File.Dispose();
                throw new Exception($"STEP_{step} not defined!");
            }

            return (fxxNested, fyyNested, fxyNested, mxxNested, myyNested, mxyNested, vxzNested, vyzNested);
        }

        public static (List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>) ASDT3Forces(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "204-ASDShellT3[102:0:0]"; // ASDShellT3
            var fxxNested = new List<List<double>>();
            var fyyNested = new List<List<double>>();
            var fxyNested = new List<List<double>>();
            var mxxNested = new List<List<double>>();
            var myyNested = new List<List<double>>();
            var mxyNested = new List<List<double>>();
            var vxzNested = new List<List<double>>();
            var vyzNested = new List<List<double>>();

            string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);

            using var h5File = PureHDF.H5File.OpenRead(recorderPath);
            double[,] values;

            var dataset = h5File.Dataset($"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/section.force/{resultType}/DATA/STEP_{step}");
            var dimX = (long)dataset.Space.Dimensions[0];
            var dimY = (long)dataset.Space.Dimensions[1];

            values = dataset.Read<double>().ToArray2D(dimX, dimY);

            var asdt3ShellNumber = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ASDShellT3).Count();

            try
            {
                for (int i = 0; i < asdt3ShellNumber; i++)
                {
                    var fxx = new List<double>();
                    var fyy = new List<double>();
                    var fxy = new List<double>();
                    var mxx = new List<double>();
                    var myy = new List<double>();
                    var mxy = new List<double>();
                    var vxz = new List<double>();
                    var vyz = new List<double>();

                    int NUMBER_COMPONENTS = 8;
                    int NUMBER_NODES = 3;
                    for (int j = 0; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fxx.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 1; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fyy.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 2; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        fxy.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 3; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        mxx.Add((double)values.GetValue(i, j));
                    }

                    for (int j = 4; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        myy.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 5; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        mxy.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 6; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        vxz.Add((double)values.GetValue(i, j));
                    }
                    for (int j = 7; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
                    {
                        vyz.Add((double)values.GetValue(i, j));
                    }

                    fxxNested.Add(fxx);
                    fyyNested.Add(fyy);
                    fxyNested.Add(fxy);
                    mxxNested.Add(mxx);
                    myyNested.Add(myy);
                    mxyNested.Add(mxy);
                    vxzNested.Add(vxz);
                    vyzNested.Add(vyz);
                }

                h5File.Dispose();
            }
            catch
            {
                h5File.Dispose();
                throw new Exception($"STEP_{step} not defined!");
            }

            return (fxxNested, fyyNested, fxyNested, mxxNested, myyNested, mxyNested, vxzNested, vyzNested);
        }


        /// <summary>
        /// 
        /// </summary>
        /// <param name="alpacaModel"></param>
        /// <param name="step"></param>
        /// <param name="resultType"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>
        public static (List<double>, List<double>, List<double>, List<double>, List<double>, List<double>) TetrahedronStress(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "179-FourNodeTetrahedron[300:0:0]";
            var sigma11 = new List<double>();
            var sigma22 = new List<double>();
            var sigma33 = new List<double>();
            var sigma12 = new List<double>();
            var sigma23 = new List<double>();
            var sigma13 = new List<double>();


            string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);

            using var h5File = PureHDF.H5File.OpenRead(recorderPath);
            double[,] values;

            var dataset = h5File.Dataset($"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/stresses/{resultType}/DATA/STEP_{step}");
            var dimX = (long)dataset.Space.Dimensions[0];
            var dimY = (long)dataset.Space.Dimensions[1];

            values = dataset.Read<double>().ToArray2D(dimX, dimY);


            var tetrahedronBrickNumber = alpacaModel.Bricks.Where(x => x.ElementClass == Element.ElementClass.FourNodeTetrahedron).Count();
            try
            {
                for (int i = 0; i < tetrahedronBrickNumber; i++)
                {

                    sigma11.Add((double)values.GetValue(i, 0));
                    sigma22.Add((double)values.GetValue(i, 1));
                    sigma33.Add((double)values.GetValue(i, 2));
                    sigma12.Add((double)values.GetValue(i, 3));
                    sigma23.Add((double)values.GetValue(i, 4));
                    sigma13.Add((double)values.GetValue(i, 5));
                }

                h5File.Dispose();
            }
            catch
            {
                h5File.Dispose();
                throw new Exception($"STEP_{step} not defined!");
            }

            return (sigma11, sigma22, sigma33, sigma12, sigma23, sigma13);
        }


        public static (List<double>, List<double>, List<double>, List<double>, List<double>, List<double>) SSPBrickStress(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "121-SSPbrick[400:0:0]";
            var sigma11 = new List<double>();
            var sigma22 = new List<double>();
            var sigma33 = new List<double>();
            var sigma12 = new List<double>();
            var sigma23 = new List<double>();
            var sigma13 = new List<double>();

            string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);

            using var h5File = PureHDF.H5File.OpenRead(recorderPath);
            double[,] values;

            var dataset = h5File.Dataset($"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/stresses/{resultType}/DATA/STEP_{step}");
            var dimX = (long)dataset.Space.Dimensions[0];
            var dimY = (long)dataset.Space.Dimensions[1];

            values = dataset.Read<double>().ToArray2D(dimX, dimY);

            var sspBrickNumber = alpacaModel.Bricks.Where(x => x.ElementClass == Element.ElementClass.SSPBrick).Count();
            try
            {
                for (int i = 0; i < sspBrickNumber; i++)
                {

                    sigma11.Add((double)values.GetValue(i, 0));
                    sigma22.Add((double)values.GetValue(i, 1));
                    sigma33.Add((double)values.GetValue(i, 2));
                    sigma12.Add((double)values.GetValue(i, 3));
                    sigma23.Add((double)values.GetValue(i, 4));
                    sigma13.Add((double)values.GetValue(i, 5));
                }

                h5File.Dispose();
            }
            catch
            {
                h5File.Dispose();
                throw new Exception($"STEP_{step} not defined!");
            }

            return (sigma11, sigma22, sigma33, sigma12, sigma23, sigma13);
        }


        /// <summary>
        /// Every fibre's stress and strain history, from a "section fiberData" recorder
        /// file. Each line is one analysis step and carries five numbers per fibre -
        /// y, z, area, stress, strain - in the section's own fibre order.
        /// </summary>
        /// <param name="fiberCount">
        /// How many fibres the section has. The file is read against this rather than
        /// inferred from it, so a step written short - the solver killed mid-write - is
        /// dropped instead of silently shifting every fibre after it.
        /// </param>
        public static List<(List<double> Stress, List<double> Strain)> FiberData(string filePath, int fiberCount)
        {
            const int ValuesPerFiber = 5;
            const int StressOffset = 3;
            const int StrainOffset = 4;

            var histories = new List<(List<double> Stress, List<double> Strain)>(fiberCount);
            for (var i = 0; i < fiberCount; i++)
                histories.Add((new List<double>(), new List<double>()));

            if (fiberCount <= 0 || !System.IO.File.Exists(filePath))
                return histories;

            foreach (var line in System.IO.File.ReadAllLines(filePath))
            {
                var values = line.Split(new char[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);

                if (values.Length < fiberCount * ValuesPerFiber)
                    continue;

                for (var i = 0; i < fiberCount; i++)
                {
                    var at = i * ValuesPerFiber;
                    histories[i].Stress.Add(TclNumber.Read(values[at + StressOffset]));
                    histories[i].Strain.Add(TclNumber.Read(values[at + StrainOffset]));
                }
            }

            return histories;
        }

    }

    // Class Created to wrap an object in a single output for Grasshopper
    public partial class PointFiberResult
    {
        public DataTree<double> Stress { get; set; } = new DataTree<double>();
        public DataTree<double> Strain { get; set; } = new DataTree<double>();
        public DataTree<Alpaca4d.Section.PointFiber> Fibers { get; set; } = new DataTree<Alpaca4d.Section.PointFiber>();

        public PointFiberResult()
        {
        }
    }
}
