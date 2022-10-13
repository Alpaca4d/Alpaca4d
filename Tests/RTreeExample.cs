using System;
using System.Collections.Generic;
using System.Linq;

using HDF5CSharp;
using HDF5CSharp.DataTypes;

namespace Tests
{

    public partial class Coordinates
    {
        [Hdf5EntryName("COORDINATES")]  public double[,] Table { get; set; }
    }
    public class Steps
    {
        [Hdf5EntryName("STEP_0")] public double[,] STEP0 { get; set; }
        [Hdf5EntryName("STEP_1")] public double[,] STEP1 { get; set; }
        [Hdf5EntryName("STEP_2")] public double[,] STEP2 { get; set; }
        [Hdf5EntryName("STEP_3")] public double[,] STEP3 { get; set; }
        [Hdf5EntryName("STEP_4")] public double[,] STEP4 { get; set; }
        [Hdf5EntryName("STEP_5")] public double[,] STEP5 { get; set; }
        [Hdf5EntryName("STEP_6")] public double[,] STEP6 { get; set; }
    }

    class RTreeExample
    {
        public static void Main(string[] args)
        {

            string fileName = @"C:\GitHub\Alpaca4d\Tests\Gh\recorder.mpco";
            var displacement = new Steps();

            long fileId = -1;
            bool readok = true;
            Dictionary<string, TabularData<double>> data = new Dictionary<string, TabularData<double>>();
            fileId = Hdf5.OpenFile(fileName, true);
            var groupId = Hdf5.CreateOrOpenGroup(fileId, "/MODEL_STAGE[1]/RESULTS/ON_NODES/DISPLACEMENT/DATA/");
            int step = 0;
            do
            {
                string name = $"STEP_{step++}";
                TabularData<double> disp = Hdf5.Read2DTable<double>(groupId, name);
                if (disp.Data != null)
                {
                    data.Add(name, disp);
                }
                else
                {
                    readok = false;
                }
            } while (readok);

        }


    }
}
