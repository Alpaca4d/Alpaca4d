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

    public partial class Read
    {
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
            //TabularData<double> table;

            var _resultType = Alpaca4d.Helper.EnumHelper.ResultTypeConvert(resultType);
            if (alpacaModel.IsModal == false)
            {
                //groupId = Hdf5.CreateOrOpenGroup(fileId, $"/MODEL_STAGE[1]/RESULTS/ON_NODES/{_resultType}/DATA/");
                var dataset = h5File.Dataset($"/MODEL_STAGE[1]/RESULTS/ON_NODES/{_resultType}/DATA/STEP_{step}");
                var dimX = (long)dataset.Space.Dimensions[0];
                var dimY = (long)dataset.Space.Dimensions[1];

                values = dataset.Read<double>().ToArray2D(dimX, dimY);
            }
            else
            {
                var dataset = h5File.Dataset($"/MODEL_STAGE[1]/RESULTS/ON_NODES/DISPLACEMENT/DATA/STEP_0");
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
            resultType = "74-ForceBeamColumn3d[1000:1:0]";
            var nNested = new List<List<double>>();
            var mzNested = new List<List<double>>();
            var vyNested = new List<List<double>>();
            var myNested = new List<List<double>>();
            var vzNested = new List<List<double>>();
            var tNested = new List<List<double>>();

            //string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);
            //long fileId = Hdf5.OpenFile(recorderPath, true);
            //string name = $"STEP_{step}";
            //long groupId;
            //TabularData<double> table;

            //// READ DATA
            //groupId = Hdf5.CreateOrOpenGroup(fileId, $"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/section.force/{resultType}/DATA/");

            //table = Hdf5.Read2DTable<double>(groupId, name);
            //try
            //{
            //    for (int i = 0; i < alpacaModel.Beams.Count; i++)
            //    {
            //        var n = new List<double>();
            //        var mz = new List<double>();
            //        var vy = new List<double>();
            //        var my = new List<double>();
            //        var vz = new List<double>();
            //        var t = new List<double>();

            //        int SECTIONFORCES = 6;
            //        int integrationPoint = alpacaModel.Beams[i].BeamIntegration.IntegrationPoint;
            //        for (int j = 0; j < SECTIONFORCES * alpacaModel.Beams[i].BeamIntegration.IntegrationPoint; j += 6)
            //        {
            //            n.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 1; j < SECTIONFORCES * alpacaModel.Beams[i].BeamIntegration.IntegrationPoint; j += 6)
            //        {
            //            mz.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 2; j < SECTIONFORCES * alpacaModel.Beams[i].BeamIntegration.IntegrationPoint; j += 6)
            //        {
            //            vy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 3; j < SECTIONFORCES * alpacaModel.Beams[i].BeamIntegration.IntegrationPoint; j += 6)
            //        {
            //            my.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 4; j < SECTIONFORCES * alpacaModel.Beams[i].BeamIntegration.IntegrationPoint; j += 6)
            //        {
            //            vz.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 5; j < SECTIONFORCES * alpacaModel.Beams[i].BeamIntegration.IntegrationPoint; j += 6)
            //        {
            //            t.Add((double)table.Data.GetValue(i, j));
            //        }

            //        nNested.Add(n);
            //        mzNested.Add(mz);
            //        vyNested.Add(vy);
            //        myNested.Add(my);
            //        vzNested.Add(vz);
            //        tNested.Add(t);
            //    }

            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);
            //}
            //catch
            //{
            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);

            //    throw new Exception($"STEP_{step} not defined!");
            //}

            return (nNested, mzNested, vyNested, myNested, vzNested, tNested);
        }

        public static (List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>) ASDQ4Forces(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "203-UnknownMovableObject[201:0:0]";
            var fxxNested = new List<List<double>>();
            var fyyNested = new List<List<double>>();
            var fxyNested = new List<List<double>>();
            var mxxNested = new List<List<double>>();
            var myyNested = new List<List<double>>();
            var mxyNested = new List<List<double>>();
            var vxzNested = new List<List<double>>();
            var vyzNested = new List<List<double>>();

            //string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);
            //long fileId = Hdf5.OpenFile(recorderPath, true);
            //string name = $"STEP_{step}";
            //long groupId;
            //TabularData<double> table;

            //// READ DATA
            //groupId = Hdf5.CreateOrOpenGroup(fileId, $"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/section.force/{resultType}/DATA/");

            //table = Hdf5.Read2DTable<double>(groupId, name);
            //var asdq4ShellNumber = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ASDShellQ4).Count();

            //try
            //{
            //    for (int i = 0; i < asdq4ShellNumber; i++)
            //    {
            //        var fxx = new List<double>();
            //        var fyy = new List<double>();
            //        var fxy = new List<double>();
            //        var mxx = new List<double>();
            //        var myy = new List<double>();
            //        var mxy = new List<double>();
            //        var vxz = new List<double>();
            //        var vyz = new List<double>();

            //        int NUMBER_COMPONENTS = 8;
            //        int NUMBER_NODES = 4;
            //        for (int j = 0; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fxx.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 1; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fyy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 2; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fxy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 3; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            mxx.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 4; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            myy.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 5; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            mxy.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 6; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            vxz.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 7; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            vyz.Add((double)table.Data.GetValue(i, j));
            //        }

            //        fxxNested.Add(fxx);
            //        fyyNested.Add(fyy);
            //        fxyNested.Add(fxy);
            //        mxxNested.Add(mxx);
            //        myyNested.Add(myy);
            //        mxyNested.Add(mxy);
            //        vxzNested.Add(vxz);
            //        vyzNested.Add(vyz);
            //    }

            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);
            //}
            //catch
            //{
            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);

            //    throw new Exception($"STEP_{step} not defined!");
            //}

            return (fxxNested, fyyNested, fxyNested, mxxNested, myyNested, mxyNested, vxzNested, vyzNested);
        }

        public static (List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>) ASDQ4Stresses(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "203-UnknownMovableObject[201:0:0]";
            var pxxNested = new List<List<double>>();
            var pyyNested = new List<List<double>>();
            var pxyNested = new List<List<double>>();
            var mxxNested = new List<List<double>>();
            var myyNested = new List<List<double>>();
            var mxyNested = new List<List<double>>();
            var vxzNested = new List<List<double>>();
            var vyzNested = new List<List<double>>();

            //string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);
            //long fileId = Hdf5.OpenFile(recorderPath, true);
            //string name = $"STEP_{step}";
            //long groupId;
            //TabularData<double> table;

            //// READ DATA
            //groupId = Hdf5.CreateOrOpenGroup(fileId, $"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/stresses/{resultType}/DATA/");

            //table = Hdf5.Read2DTable<double>(groupId, name);
            //var asdq4ShellNumber = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ASDShellQ4).Count();

            //try
            //{
            //    for (int i = 0; i < asdq4ShellNumber; i++)
            //    {
            //        var pxx = new List<double>();
            //        var pyy = new List<double>();
            //        var pxy = new List<double>();
            //        var mxx = new List<double>();
            //        var myy = new List<double>();
            //        var mxy = new List<double>();
            //        var vxz = new List<double>();
            //        var vyz = new List<double>();

            //        int NUMBER_COMPONENTS = 8;
            //        int NUMBER_NODES = 4;
            //        for (int j = 0; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            pxx.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 1; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            pyy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 2; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            pxy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 3; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            mxx.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 4; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            myy.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 5; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            mxy.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 6; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            vxz.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 7; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            vyz.Add((double)table.Data.GetValue(i, j));
            //        }

            //        pxxNested.Add(pxx);
            //        pyyNested.Add(pyy);
            //        pxyNested.Add(pxy);
            //        mxxNested.Add(mxx);
            //        myyNested.Add(myy);
            //        mxyNested.Add(mxy);
            //        vxzNested.Add(vxz);
            //        vyzNested.Add(vyz);
            //    }

            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);
            //}
            //catch
            //{
            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);

            //    throw new Exception($"STEP_{step} not defined!");
            //}

            return (pxxNested, pyyNested, pxyNested, mxxNested, myyNested, mxyNested, vxzNested, vyzNested);
        }

        public static (List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>) DKGTForces(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "167-UnknownMovableObject[103:0:0]"; // DKGT
            //resultType = "168-UnknownMovableObject[103:0:0]"; // NLDKGT
            var fxxNested = new List<List<double>>();
            var fyyNested = new List<List<double>>();
            var fxyNested = new List<List<double>>();
            var mxxNested = new List<List<double>>();
            var myyNested = new List<List<double>>();
            var mxyNested = new List<List<double>>();
            var vxzNested = new List<List<double>>();
            var vyzNested = new List<List<double>>();

            //string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);
            //long fileId = Hdf5.OpenFile(recorderPath, true);
            //string name = $"STEP_{step}";
            //long groupId;
            //TabularData<double> table;
            //// READ DATA
            //groupId = Hdf5.CreateOrOpenGroup(fileId, $"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/section.force/{resultType}/DATA/");

            //table = Hdf5.Read2DTable<double>(groupId, name);
            //var dkgtShellNumber = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ShellDKGT).Count();

            //try
            //{
            //    for (int i = 0; i < dkgtShellNumber; i++)
            //    {
            //        var fxx = new List<double>();
            //        var fyy = new List<double>();
            //        var fxy = new List<double>();
            //        var mxx = new List<double>();
            //        var myy = new List<double>();
            //        var mxy = new List<double>();
            //        var vxz = new List<double>();
            //        var vyz = new List<double>();

            //        int NUMBER_COMPONENTS = 8;
            //        int NUMBER_NODES = 4;
            //        for (int j = 0; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fxx.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 1; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fyy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 2; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fxy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 3; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            mxx.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 4; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            myy.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 5; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            mxy.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 6; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            vxz.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 7; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            vyz.Add((double)table.Data.GetValue(i, j));
            //        }

            //        fxx.RemoveAt(0);
            //        fyy.RemoveAt(0);
            //        fxy.RemoveAt(0);
            //        mxx.RemoveAt(0);
            //        myy.RemoveAt(0);
            //        mxy.RemoveAt(0);
            //        vxz.RemoveAt(0);
            //        vyz.RemoveAt(0);

            //        fxxNested.Add(fxx);
            //        fyyNested.Add(fyy);
            //        fxyNested.Add(fxy);
            //        mxxNested.Add(mxx);
            //        myyNested.Add(myy);
            //        mxyNested.Add(mxy);
            //        vxzNested.Add(vxz);
            //        vyzNested.Add(vyz);
            //    }

            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);
            //}
            //catch
            //{
            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);

            //    throw new Exception($"STEP_{step} not defined!");
            //}

            return (fxxNested, fyyNested, fxyNested, mxxNested, myyNested, mxyNested, vxzNested, vyzNested);
        }

        public static (List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>, List<List<double>>) DKGTStresses(Model alpacaModel, int step, string resultType = null)
        {
            resultType = "167-UnknownMovableObject[103:0:0]"; // DKGT
            //resultType = "168-UnknownMovableObject[103:0:0]"; // NLDKGT
            var fxxNested = new List<List<double>>();
            var fyyNested = new List<List<double>>();
            var fxyNested = new List<List<double>>();
            var mxxNested = new List<List<double>>();
            var myyNested = new List<List<double>>();
            var mxyNested = new List<List<double>>();
            var vxzNested = new List<List<double>>();
            var vyzNested = new List<List<double>>();

            //string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);
            //long fileId = Hdf5.OpenFile(recorderPath, true);
            //string name = $"STEP_{step}";
            //long groupId;
            //TabularData<double> table;
            //// READ DATA
            //groupId = Hdf5.CreateOrOpenGroup(fileId, $"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/stresses/{resultType}/DATA/");

            //table = Hdf5.Read2DTable<double>(groupId, name);
            //var dkgtShellNumber = alpacaModel.Shells.Where(x => x.ElementClass == Element.ElementClass.ShellDKGT).Count();

            //try
            //{
            //    for (int i = 0; i < dkgtShellNumber; i++)
            //    {
            //        var fxx = new List<double>();
            //        var fyy = new List<double>();
            //        var fxy = new List<double>();
            //        var mxx = new List<double>();
            //        var myy = new List<double>();
            //        var mxy = new List<double>();
            //        var vxz = new List<double>();
            //        var vyz = new List<double>();

            //        int NUMBER_COMPONENTS = 8;
            //        int NUMBER_NODES = 4;
            //        for (int j = 0; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fxx.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 1; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fyy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 2; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            fxy.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 3; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            mxx.Add((double)table.Data.GetValue(i, j));
            //        }

            //        for (int j = 4; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            myy.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 5; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            mxy.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 6; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            vxz.Add((double)table.Data.GetValue(i, j));
            //        }
            //        for (int j = 7; j < NUMBER_COMPONENTS * NUMBER_NODES; j += NUMBER_COMPONENTS)
            //        {
            //            vyz.Add((double)table.Data.GetValue(i, j));
            //        }

            //        // remove first item as it is the force/stress in the center of the shell

            //        fxx.RemoveAt(0);
            //        fyy.RemoveAt(0);
            //        fxy.RemoveAt(0);
            //        mxx.RemoveAt(0);
            //        myy.RemoveAt(0);
            //        mxy.RemoveAt(0);
            //        vxz.RemoveAt(0);
            //        vyz.RemoveAt(0);

            //        fxxNested.Add(fxx);
            //        fyyNested.Add(fyy);
            //        fxyNested.Add(fxy);
            //        mxxNested.Add(mxx);
            //        myyNested.Add(myy);
            //        mxyNested.Add(mxy);
            //        vxzNested.Add(vxz);
            //        vyzNested.Add(vyz);
            //    }

            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);
            //}
            //catch
            //{
            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);

            //    throw new Exception($"STEP_{step} not defined!");
            //}

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

            //string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);
            //long fileId = Hdf5.OpenFile(recorderPath, true);
            //string name = $"STEP_{step}";
            //long groupId;
            //TabularData<double> table;

            //// READ DATA
            //groupId = Hdf5.CreateOrOpenGroup(fileId, $"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/stresses/{resultType}/DATA/");

            //table = Hdf5.Read2DTable<double>(groupId, name);
            //var tetrahedronBrickNumber = alpacaModel.Bricks.Where(x => x.ElementClass == Element.ElementClass.FourNodeTetrahedron).Count();
            //try
            //{
            //    for (int i = 0; i < tetrahedronBrickNumber; i++)
            //    {

            //        sigma11.Add((double)table.Data.GetValue(i, 0));
            //        sigma22.Add((double)table.Data.GetValue(i, 1));
            //        sigma33.Add((double)table.Data.GetValue(i, 2));
            //        sigma12.Add((double)table.Data.GetValue(i, 3));
            //        sigma23.Add((double)table.Data.GetValue(i, 4));
            //        sigma13.Add((double)table.Data.GetValue(i, 5));
            //    }

            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);
            //}
            //catch
            //{
            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);

            //    throw new Exception($"STEP_{step} not defined!");
            //}

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

            //string recorderPath = System.IO.Path.GetFullPath(alpacaModel.Recorders.First().FileName);
            //long fileId = Hdf5.OpenFile(recorderPath, true);
            //string name = $"STEP_{step}";
            //long groupId;
            //TabularData<double> table;

            //// READ DATA
            //groupId = Hdf5.CreateOrOpenGroup(fileId, $"/MODEL_STAGE[1]/RESULTS/ON_ELEMENTS/stresses/{resultType}/DATA/");

            //table = Hdf5.Read2DTable<double>(groupId, name);
            //var sspBrickNumber = alpacaModel.Bricks.Where(x => x.ElementClass == Element.ElementClass.SSPBrick).Count();
            //try
            //{
            //    for (int i = 0; i < sspBrickNumber; i++)
            //    {

            //        sigma11.Add((double)table.Data.GetValue(i, 0));
            //        sigma22.Add((double)table.Data.GetValue(i, 1));
            //        sigma33.Add((double)table.Data.GetValue(i, 2));
            //        sigma12.Add((double)table.Data.GetValue(i, 3));
            //        sigma23.Add((double)table.Data.GetValue(i, 4));
            //        sigma13.Add((double)table.Data.GetValue(i, 5));
            //    }

            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);
            //}
            //catch
            //{
            //    Hdf5.CloseGroup(groupId);
            //    Hdf5.CloseFile(fileId);

            //    throw new Exception($"STEP_{step} not defined!");
            //}

            return (sigma11, sigma22, sigma33, sigma12, sigma23, sigma13);
        }


        public static (List<double>, List<double>) FiberStress(string filePath)
        {
            var stress = new List<double>();
            var strain = new List<double>();

            var lines = System.IO.File.ReadAllLines(filePath);

            foreach(var line in lines)
            {
                var splittedLine = line.Split(new char[] { ' ' });
                var stressValue = splittedLine[0];
                var strainValue = splittedLine[1];

                strain.Add(Double.Parse(strainValue));
                stress.Add(Double.Parse(stressValue));
            }

            return (stress, strain);
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
