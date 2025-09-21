using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Display;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Globalization;

namespace Alpaca4d.Gh
{
    public class Legend : GH_Component
    {
        private List<Color> _colors = new List<Color>();
        private List<double> _data = new List<double>();

        // UI options / state
        private double _scale = 1.5;        // scale factor
        private int _pos = 2;               // 0: left vertical, 1: right vertical, 2: bottom center horizontal
        private string _title = string.Empty;
        private readonly string _fontFace = "Arial";
        private readonly Color _black = Color.Black;
        private double _min = -1.0;
        private double _max = 1.0;
        private double _diff = 2.0;
        private int _range = 0;             // colors.Count + 1

        public Legend()
          : base("Legend (Alpaca4d)", "Legend",
            "Draw a fixed on-screen legend with colors and labels",
            "Alpaca4d", "09_Visualisation")
        {
            this.Message = $"{this.Name}";
        }

        protected override void RegisterInputParams(GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Title", "Title", "Legend title", GH_ParamAccess.item, "");
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Data", "Data", "Numeric data to derive min/max labels", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddColourParameter("Colors", "C", "Legend colors (gradient steps)", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Position", "Pos", "0: Left, 1: Right, 2: Bottom Center", GH_ParamAccess.item, 2);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Scale", "Scale", "Size scale factor", GH_ParamAccess.item, 1.5);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        protected override void RegisterOutputParams(GH_OutputParamManager pManager)
        {
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            _colors.Clear();
            _data.Clear();

            DA.GetData(0, ref _title);
            DA.GetDataList(1, _data);
            DA.GetDataList(2, _colors);
            DA.GetData(3, ref _pos);
            DA.GetData(4, ref _scale);

            if (_scale <= 0) _scale = 1.5;

            if (_colors.Count == 0)
            {
                _colors = new List<Color>
                {
                    Color.FromArgb(255,  51,  51),
                    Color.FromArgb(255, 170,  51),
                    Color.FromArgb(255, 255,  51),
                    Color.FromArgb(170, 255, 125),
                    Color.FromArgb( 51, 255, 231),
                    Color.FromArgb( 51, 170, 255),
                    Color.FromArgb( 51,  51, 255)
                };
            }

            if (_data != null && _data.Count > 0)
            {
                _min = double.MaxValue;
                _max = double.MinValue;
                foreach (var v in _data)
                {
                    if (v < _min) _min = v;
                    if (v > _max) _max = v;
                }
            }
            else
            {
                _min = -1.0;
                _max = 1.0;
            }

            _diff = _max - _min;
            _range = _colors.Count;
        }

        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            base.DrawViewportWires(args);
            if (this.Hidden || this.Locked) return;
            if (_colors.Count == 0) return;

            // Determine viewport size
            int left, right, bottom, top, near, far;
            args.Viewport.GetScreenPort(out left, out right, out bottom, out top, out near, out far);
            int width = right - left;
            int height = bottom - top;

            // Anchor position
            double anchorX;
            double anchorY = height * 0.075;
            if (_pos == 0)
            {
                anchorX = width * 0.025;
            }
            else if (_pos == 1)
            {
                anchorX = width * (1.0 - 0.125);
            }
            else // _pos == 2
            {
                anchorX = width * 0.5;
                anchorY = height * (1.0 - 0.125);
            }

            // Sizes
            double rectX = 20.0 * _scale;
            double rectY = 20.0 * _scale;
            double textHeight = rectY * 0.6;
            double titleHeight = rectY * 0.9;

            // Title
            int titleHeightPx = (int)Math.Round(titleHeight);
            if (!string.IsNullOrWhiteSpace(_title))
            {
                var titlePt = new Point2d(anchorX, anchorY - 3.0 / 1.6 * textHeight);
                args.Display.Draw2dText(_title, _black, titlePt, false, titleHeightPx, _fontFace);
            }

            // Vertical gradient (left/right)
            if (_pos == 0 || _pos == 1)
            {
                int textHeightPx = (int)Math.Round(textHeight);
                for (int i = 0; i < _colors.Count; i++)
                {
                    int rx = (int)Math.Round(anchorX);
                    int ry = (int)Math.Round(anchorY + i * rectY);
                    int rw = (int)Math.Round(rectX);
                    int rh = (int)Math.Round(rectY);
                    var rec2d = new Rectangle(rx, ry, rw, rh);
                    args.Display.Draw2dRectangle(rec2d, _black, 3, _colors[i]);

                    double value = _diff * (double)i / _range + _min;
                    string valueText = value.ToString("0.0", CultureInfo.InvariantCulture);
                    var pt = new Point2d(anchorX + 1.5 * rectX, anchorY - 1.0 / (1.6 * 2.0) * textHeight + i * rectY);
                    args.Display.Draw2dText(valueText, _black, pt, false, textHeightPx, _fontFace);
                }

                // Max label at the end
                {
                    int i = _colors.Count;
                    var pt = new Point2d(anchorX + 1.5 * rectX, anchorY - 1.0 / (1.6 * 2.0) * textHeight + i * rectY);
                    string maxText = _max.ToString("0.0", CultureInfo.InvariantCulture);
                    args.Display.Draw2dText(maxText, _black, pt, false, textHeightPx, _fontFace);
                }
            }
            else // Horizontal gradient (bottom center)
            {
                int textHeightSmallPx = (int)Math.Round(textHeight / 1.4);
                for (int i = 0; i < _colors.Count; i++)
                {
                    int rx = (int)Math.Round(anchorX + i * rectX);
                    int ry = (int)Math.Round(anchorY);
                    int rw = (int)Math.Round(rectX);
                    int rh = (int)Math.Round(rectY);
                    var rec2d = new Rectangle(rx, ry, rw, rh);
                    args.Display.Draw2dRectangle(rec2d, _black, 3, _colors[i]);

                    double value = _diff * (double)i / _range + _min;
                    string valueText = value.ToString("0.0", CultureInfo.InvariantCulture);
                    var pt = new Point2d(anchorX - 1.0 / 1.6 * textHeight + i * rectX, anchorY + 3.0 / 1.2 * textHeight);
                    args.Display.Draw2dText(valueText, _black, pt, false, textHeightSmallPx, _fontFace);
                }

                // Max label at the end
                {
                    int i = _colors.Count;
                    var pt = new Point2d(anchorX - 1.0 / 1.2 * textHeight + i * rectX, anchorY + 3.0 / 1.2 * textHeight);
                    string maxText = _max.ToString("0.0", CultureInfo.InvariantCulture);
                    args.Display.Draw2dText(maxText, _black, pt, false, textHeightSmallPx, _fontFace);
                }
            }
        }

        public override GH_Exposure Exposure => GH_Exposure.tertiary;
        public override bool IsPreviewCapable => true;
        protected override Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Legend__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{A6B3B5C9-DB8D-4B6A-9E7E-63C6D2E2F9F5}");
    }
}


