using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Eto;
using Eto.Forms;
using Eto.Drawing;

namespace Alpaca4d.Forms
{
    public partial class Advertise
    {
        public static int NumberOfElements = 10;
        public Advertise()
        {
            var windows = new Eto.Forms.Form();
            windows.Size = new Eto.Drawing.Size(800, 450);
            windows.Maximizable = false;
            windows.Minimizable = false;
            windows.Resizable = false;
            windows.Padding = new Eto.Drawing.Padding(5, 5, 5, 5);
            windows.BackgroundColor = new Eto.Drawing.Color(1, 1, 1);

            var centerScreen = Eto.Forms.Screen.DisplayBounds.Center;
            windows.Location = new Eto.Drawing.Point((int)centerScreen.X - windows.Size.Width / 2, (int)centerScreen.Y - windows.Size.Height / 2);
            windows.Icon = new Eto.Drawing.Icon(@"C:\GitHub\Alpaca4d\Alpaca4d.Gh\Resources\Tab.png");

            var imageView = new Eto.Forms.ImageView();
            var imagePaths = System.IO.Directory.GetFiles(Alpaca4d.Application.GhAlpacaFolder, "*_adv.png", System.IO.SearchOption.AllDirectories);
            var index = new Random().Next(imagePaths.Count());

            imageView.Image = new Eto.Drawing.Bitmap(imagePaths.ElementAt(index));

            windows.Content = imageView;
            windows.Show();
        }
    }
}