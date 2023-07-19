using PureHDF;


namespace Alpaca4d.Test.HDF5
{
    [TestClass]
    public class ReadHDF5
    {

        //https://github.com/Apollo3zehn/PureHDF/issues/36

        [TestMethod]
        public void TestMethod1()
        {

            using var h5File = PureHDF.H5File.OpenRead(@"HDF5\recorder.hdf5");


            // get nested group
            var SPATIAL_DIM = h5File.Dataset("/INFO/SPATIAL_DIM").Read<int>();


            var nodes = h5File.Group("/MODEL_STAGE[1]/MODEL/NODES");

            var COORDINATES = h5File.Dataset("/MODEL_STAGE[1]/MODEL/NODES/COORDINATES").Read<double>();

            var DISPLACEMENT = h5File.Dataset("/MODEL_STAGE[1]/RESULTS/ON_NODES/DISPLACEMENT/DATA/STEP_0").Read<double>().ToArray2D(264, 3);


            var dataset = h5File.Dataset("/MODEL_STAGE[1]/RESULTS/ON_NODES/DISPLACEMENT/DATA/STEP_0");
            var dimX = (long)dataset.Space.Dimensions[0];
            var dimY = (long)dataset.Space.Dimensions[1];

            var values = dataset.Read<double>().ToArray2D(dimX, dimY);
        }
    }
}