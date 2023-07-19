using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;

namespace Alpaca4d
{
    public partial class Application
    {
        public static readonly List<string> Intro = new List<string>(){""};


        public static readonly string assemblyLocation = Assembly.GetExecutingAssembly().Location;
        public static readonly string GhAlpacaFolder = System.IO.Path.GetDirectoryName(assemblyLocation);
        public static readonly string OpenSeesFolder = System.IO.Path.Combine(GhAlpacaFolder, @"OpenSees-Solvers\bin");

        public static readonly string OpenSees = System.IO.Path.Combine(OpenSeesFolder, @"OpenSees.exe");
        public static readonly string OpenSeesSP = System.IO.Path.Combine(OpenSeesFolder, @"openseessp.bat");
        public static readonly string OpenSeesMP = System.IO.Path.Combine(OpenSeesFolder, @"openseesmp.bat");

        public string CurrentDir { get; } = System.IO.Directory.GetCurrentDirectory();
        public string FileName { get; set; }

        public Application()
        {

        }

    }
}
