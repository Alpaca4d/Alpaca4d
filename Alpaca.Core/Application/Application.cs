using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alpaca4d
{
    public partial class Application
    {
        public static readonly List<string> Intro = new List<string>(){""};

        public static readonly string GhCompFolder = Grasshopper.Folders.DefaultAssemblyFolder;
        public static readonly string GhAlpacaFolder = System.IO.Path.Combine(GhCompFolder, @"Alpaca4d");
        public static readonly string OpenSeesFolder = System.IO.Path.Combine(GhAlpacaFolder, @"OpenSees-Solvers");

        public static readonly string OpenSees = System.IO.Path.Combine(OpenSeesFolder, @"opensees.bat");
        public static readonly string OpenSeesSP = System.IO.Path.Combine(OpenSeesFolder, @"openseessp.bat");
        public static readonly string OpenSeesMP = System.IO.Path.Combine(OpenSeesFolder, @"openseesmp.bat");

        public string CurrentDir { get; } = System.IO.Directory.GetCurrentDirectory();
        public string FileName { get; set; }

        public Application()
        {

        }
        public static string ReadLicense()
        {
            string openSeesPath = System.IO.Path.Combine(Application.OpenSeesFolder, @"License.txt");
            var license = System.IO.File.ReadAllText(openSeesPath);

            return license;
        }

    }
}
