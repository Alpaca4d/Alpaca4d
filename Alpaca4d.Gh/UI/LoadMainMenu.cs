using System.Threading;
using System.Windows.Forms;

using Alpaca4d.UI;
using Grasshopper.GUI;
using Grasshopper.GUI.Canvas;
using System.Diagnostics;
using System.Security.Policy;
using System.IO;
using System.Reflection;
using System;
using GH_IO.Serialization;
using Grasshopper.Kernel;

namespace Alpaca4d.Menu
{
    public class MenuLoad
    {
        private static ToolStripMenuItem alpacaMenu;

        internal static void OnStartup(GH_Canvas canvas)
        {
            alpacaMenu = new ToolStripMenuItem("Alpaca4d")
            {
                Name = "Alpaca4d",
            };

            PopulateSub(alpacaMenu);

            GH_DocumentEditor editor = null;

            while (editor == null)
            {
                editor = Grasshopper.Instances.DocumentEditor;
                Thread.Sleep(321);
            }

            if (!editor.MainMenuStrip.Items.ContainsKey("Alpaca4d"))
            {
                editor.MainMenuStrip.Items.Add(alpacaMenu);
            }
            else
            {
                alpacaMenu = (ToolStripMenuItem)editor.MainMenuStrip.Items["Alpaca4d"];
                lock (alpacaMenu)
                {
                    alpacaMenu.DropDown.Items.Add(new ToolStripSeparator());
                    PopulateSub(alpacaMenu);
                }
            }

            Grasshopper.Instances.CanvasCreated -= OnStartup;
        }

        private static void PopulateSub(ToolStripMenuItem menuItem)
        {
            // Add Documentation
            menuItem.DropDown.Items.Add("Documentation", null, 
                (sender, e) => OpenBrowser(sender, e, "https://alpaca4d.gitbook.io/docs"));

            // Add Templates
            // add a sub menu for a toolstripmenu item
            ToolStripMenuItem subMenu = new ToolStripMenuItem("Examples");
            subMenu.DropDown.Items.Add("Construct Model", null, (sender, e) => OpenGhFile(sender, e));
            subMenu.DropDown.Items.Add("Analysis", null, (sender, e) => OpenGhFile(sender, e));
            subMenu.DropDown.Items.Add("Results", null, (sender, e) => OpenGhFile(sender, e));

            menuItem.DropDown.Items.Add(subMenu);

            menuItem.DropDown.Items.Add(new ToolStripSeparator());
            //----------------------

            // Add License Management
            ToolStripMenuItem subMenuLicense = new ToolStripMenuItem("License");
            subMenuLicense.DropDown.Items.Add("Activate License", null, ShowLicenseManagement);
            subMenuLicense.DropDown.Items.Add("License Terms", null,
                (sender, e) => OpenBrowser(sender, e, "https://alpaca4d.gitbook.io/docs/references/license"));

            menuItem.DropDown.Items.Add(subMenuLicense);

            // Add Help
            ToolStripMenuItem subMenuHelp = new ToolStripMenuItem("Help");
            subMenuHelp.DropDown.Items.Add("Help", null,
                (sender, e) => OpenBrowser(sender, e, "https://github.com/Alpaca4d/Alpaca4d/issues/new"));
                
            menuItem.DropDown.Items.Add(subMenu);
        }

        // create an event handler that opens up a sub-window
        private static void OpenForm(object sender, System.EventArgs e)
        {
            //new Form1().ShowDialog();
        }

        // create an event handler that opens up a browser window
        private static void OpenBrowser(object sender, System.EventArgs e, string url)
        {
            Process.Start(new ProcessStartInfo { FileName = url, UseShellExecute = true });
        }

        // create an event handler that opens up a Grasshopper template document 
        private static void OpenGhFile(object sender, EventArgs e, string fileName = null)
        {
            string assemblyPath = Assembly.GetExecutingAssembly().Location;
            string folderAssembly = System.IO.Path.GetDirectoryName(assemblyPath);
            

            string templateFile = System.IO.Path.Combine(folderAssembly, "Assets", fileName);

            PasteGrasshopperFile(templateFile);
        }

        private static void PasteGrasshopperFile(string filePath)
        {
            GH_Document currentDoc = Grasshopper.Instances.ActiveCanvas.Document;
            if (currentDoc == null)
            {
                MessageBox.Show("No active Grasshopper document found.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            GH_Archive archive = new GH_Archive();
            archive.ReadFromFile(filePath);
            
            GH_Document newDoc = new GH_Document();
            if (archive.ExtractObject(newDoc, "Definition"))
            {
                currentDoc.MergeDocument(newDoc);
                Grasshopper.Instances.ActiveCanvas.Refresh();
                Grasshopper.Instances.ActiveCanvas.Update();
            }
            else
            {
                MessageBox.Show("Failed to extract the Grasshopper document from the archive.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        // create an event handler for showing the license management form
        private static void ShowLicenseManagement(object sender, EventArgs e)
        {
            try
            {
                Alpaca4d.UI.LicenseManagementForm.ShowForm();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error opening license management: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}