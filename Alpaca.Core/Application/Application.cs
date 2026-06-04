using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using System.Runtime.InteropServices;
using System.IO;
using System.Diagnostics;


namespace Alpaca4d
{
    public partial class Application
    {
        public static string assemblyLocation = Assembly.GetExecutingAssembly().Location;
        public static string GhAlpacaFolder = System.IO.Path.GetDirectoryName(assemblyLocation);

        public static string OpenSees
        {
            get
            {
                string openSeesPath = AlpacaSettings.OpenSeesPath;

                // Ensure execute permissions on Unix-like systems
                if (!string.IsNullOrEmpty(openSeesPath) &&
                    !RuntimeInformation.IsOSPlatform(OSPlatform.Windows) &&
                    File.Exists(openSeesPath))
                {
                    EnsureExecutePermissions(openSeesPath);
                }

                return openSeesPath;
            }
        }

        /// <summary>
        /// Ensures that the OpenSees executable has execute permissions on Unix-like systems
        /// </summary>
        /// <param name="filePath">Path to the executable file</param>
        private static void EnsureExecutePermissions(string filePath)
        {
            try
            {
                // Use chmod command to set execute permissions (755)
                var processInfo = new ProcessStartInfo
                {
                    FileName = "chmod",
                    Arguments = $"755 \"{filePath}\"",
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                };

                using (var process = Process.Start(processInfo))
                {
                    process?.WaitForExit();
                }
            }
            catch (Exception)
            {
                // If chmod fails, we'll continue anyway - the user can manually set permissions
                // This prevents the application from crashing due to permission issues
            }
        }
    }
}
