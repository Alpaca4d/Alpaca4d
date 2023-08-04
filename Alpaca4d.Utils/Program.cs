using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.License;

namespace CreateLicense
{
    internal class Program
    {
        static void Main()
        {
            var jsonFilePath = "data.json";
            var binaryFilePath = @"../../data.bin";

            var binary = License.SerializeJsonToBinary(jsonFilePath);
            License.SerializeBinaryToFile(binaryFilePath, binary);
            Console.WriteLine("data.bin created");
        }
    }
}
