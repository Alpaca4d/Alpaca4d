using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using System.Runtime.InteropServices;


namespace Alpaca4d
{
    public partial class Application
    {
        public static readonly List<string> Intro = new List<string>(){""};


        public static string assemblyLocation = Assembly.GetExecutingAssembly().Location;
        public static string GhAlpacaFolder = System.IO.Path.GetDirectoryName(assemblyLocation);

        
        //public static readonly string OpenSeesFolder = System.IO.Path.Combine(GhAlpacaFolder, @"OpenSees-Solvers/bin");

        public static string OpenSeesFolder
        {
            get
            {
                if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))
                {
                    return System.IO.Path.Combine(GhAlpacaFolder, @"OpenSees-Solvers/win/bin");
                }
                else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
                {
                    return System.IO.Path.Combine(GhAlpacaFolder, @"OpenSees-Solvers/mac/bin");
                }
                else
                {
                    throw new Exception("Linux is not supported!");
                }
            }
        }

        public static string OpenSees = System.IO.Path.Combine(OpenSeesFolder, @"OpenSees");

        public string CurrentDir { get; } = System.IO.Directory.GetCurrentDirectory();
        public string FileName { get; set; }

        public Application()
        {

        }

    }
}
