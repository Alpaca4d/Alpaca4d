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
        private readonly LegendConduit _conduit;
        private bool _preview = true;

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
          : base("Legend\n(Alpaca4d)", "Legend",
            "Draw a fixed on-screen legend with colors and labels",
            "Alpaca4d", "09_Visualisation")
        {
            this.Message = $"{this.Name}";
            _conduit = new LegendConduit();
            _conduit.SetShouldDrawProvider(() => !this.Hidden && !this.Locked);
        }

        protected override void RegisterInputParams(GH_InputParamManager pManager)
        {
            pManager.AddTextParameter("Title", "Title", "Legend title", GH_ParamAccess.item, "");
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("Data", "Data", "Numeric data to derive min/max labels", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddColourParameter("Colors", "Colors", "Legend colors (gradient steps)", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddIntegerParameter("Position", "Pos", "0: Left, 1: Right, 2: Bottom Center", GH_ParamAccess.item, 0);
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
                _colors = Alpaca4d.Colors.Gradient(0);
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

            // Update conduit state and request a redraw
            _conduit?.Update(
                _title,
                _colors,
                _min,
                _max,
                _pos,
                _scale,
                _fontFace,
                _black,
                !this.Hidden && !this.Locked
            );
            Rhino.RhinoDoc.ActiveDoc?.Views?.Redraw();
        }

        // DrawViewportWires is intentionally omitted; legend rendering is handled by a DisplayConduit in DrawForeground.

        public override void AddedToDocument(GH_Document document)
        {
            base.AddedToDocument(document);
            _conduit.Enabled = true;
        }

        public override void RemovedFromDocument(GH_Document document)
        {
            _conduit.Enabled = false;
            base.RemovedFromDocument(document);
        }

        public override BoundingBox ClippingBox
        {
            get
            {
                return new BoundingBox(
                    new Point3d(-1e9, -1e9, -1e9),
                    new Point3d( 1e9,  1e9,  1e9)
                );
            }
        }

        protected override void BeforeSolveInstance()
        {
            List<string> resultTypes = new List<string> { "Left", "Right", "Bottom" };
            List<int> values = new List<int> { 0, 1, 2 };
            ValueListUtils.UpdateValueLists(this, 3, resultTypes, values);
        }

        public override GH_Exposure Exposure => GH_Exposure.tertiary;
        public override bool IsPreviewCapable => true;
        protected override Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Legend__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{A6B3B5C9-DB8D-4B6A-9E7E-63C6D2E2F9F5}");

        private class LegendConduit : DisplayConduit
        {
            private string _title = string.Empty;
            private List<Color> _colors = new List<Color>();
            private double _min = -1.0;
            private double _max = 1.0;
            private int _pos = 2;
            private double _scale = 1.5;
            private string _fontFace = "Arial";
            private Color _stroke = Color.Black;
            private bool _shouldDraw = false;
            private Func<bool> _shouldDrawProvider;

            public void SetShouldDrawProvider(Func<bool> provider)
            {
                _shouldDrawProvider = provider;
            }

            public void Update(string title, List<Color> colors, double min, double max, int pos, double scale, string fontFace, Color stroke, bool shouldDraw)
            {
                _title = title ?? string.Empty;
                _colors = colors != null ? new List<Color>(colors) : new List<Color>();
                _min = min;
                _max = max;
                _pos = pos;
                _scale = scale > 0 ? scale : 1.5;
                _fontFace = string.IsNullOrWhiteSpace(fontFace) ? "Arial" : fontFace;
                _stroke = stroke;
                _shouldDraw = shouldDraw;
            }

            protected override void DrawForeground(DrawEventArgs e)
            {
                bool allow = _shouldDrawProvider != null ? _shouldDrawProvider() : _shouldDraw;
                if (!allow) return;
                if (_colors == null || _colors.Count == 0) return;

                // Viewport dimensions
                int left, right, bottom, top, near, far;
                e.Viewport.GetScreenPort(out left, out right, out bottom, out top, out near, out far);
                int width = right - left;
                int height = bottom - top;

                // Common constants and derived values
                const double topBottomMarginFactor = 0.075;   // 7.5% from top/bottom
                const double leftMarginFactor = 0.025;         // 2.5% from left
                const double rightMarginFactor = 0.075;        // 7.5% from right
                const int strokeThickness = 2;

                double baseUnit = 15.0 * _scale;
                double rectWidth = (_pos == 2) ? baseUnit * 3.5 : baseUnit;
                double rectHeight = (_pos == 2) ? baseUnit : baseUnit * 3.5;
                double textHeight = (baseUnit * 2.0) * 0.6;
                double titleHeight = (baseUnit * 2.0) * 0.9;

                int rectWidthPx = (int)Math.Round(rectWidth);
                int rectHeightPx = (int)Math.Round(rectHeight);
                int textHeightPx = (int)Math.Round(textHeight);
                int titleHeightPx = (int)Math.Round(titleHeight);

                // Label offsets (group repeated magic numbers)
                double titleYOffsetVertical = -(3.0 / 1.6) * textHeight;
                double labelYOffsetVertical = -(1.0 / (1.6 * 2.0)) * textHeight; // used for all vertical labels including max
                double titleYOffsetHorizontal = (2.5 / 1.6) * textHeight;
                double labelYOffsetHorizontal = -1.5 * textHeight;               // used for all horizontal labels
                double labelXOffsetHorizontal = -(1.0 / 1.6) * textHeight;       // value labels
                double labelXOffsetHorizontalMax = -(1.0 / 1.2) * textHeight;    // max label only

                // Anchor position based on desired legend position
                double anchorX;
                double anchorY = height * topBottomMarginFactor;
                if (_pos == 0)
                {
                    anchorX = width * leftMarginFactor;
                }
                else if (_pos == 1)
                {
                    anchorX = width * (1.0 - rightMarginFactor);
                }
                else
                {
                    anchorX = width * 0.5;
                    anchorY = height * (1.0 - topBottomMarginFactor);
                }

                // Small positional nudges per request
                if (_pos == 1)
                {
                    anchorX += rectWidth * 0.5; // move legend slightly right
                }
                else if (_pos == 2)
                {
                    anchorY += rectHeight * 0.5; // move legend slightly down
                }

                // Data range
                int colorCount = _colors.Count;
                double diff = _max - _min;
                int range = colorCount;

                if (_pos == 0 || _pos == 1)
                {
                    // Vertical layouts (left/right)
                    if (!string.IsNullOrWhiteSpace(_title))
                    {
                        var titlePt = new Point2d(anchorX, anchorY + titleYOffsetVertical);
                        e.Display.Draw2dText(_title, _stroke, titlePt, false, titleHeightPx, _fontFace);
                    }

                    for (int i = 0; i < colorCount; i++)
                    {
                        int rx = (int)Math.Round(anchorX);
                        int ry = (int)Math.Round(anchorY + i * rectHeight);
                        var rec2d = new Rectangle(rx, ry, rectWidthPx, rectHeightPx);
                        e.Display.Draw2dRectangle(rec2d, _stroke, strokeThickness, _colors[i]);

                        double value = diff * (double)i / range + _min;
                        string valueText = value.ToString("0.00", CultureInfo.InvariantCulture);
                        var pt = new Point2d(anchorX + 1.5 * rectWidth, anchorY + labelYOffsetVertical + i * rectHeight);
                        e.Display.Draw2dText(valueText, _stroke, pt, false, textHeightPx, _fontFace);
                    }

                    // Max value label
                    {
                        int i = colorCount;
                        var pt = new Point2d(anchorX + 1.5 * rectWidth, anchorY + labelYOffsetVertical + i * rectHeight);
                        string maxText = _max.ToString("0.00", CultureInfo.InvariantCulture);
                        e.Display.Draw2dText(maxText, _stroke, pt, false, textHeightPx, _fontFace);
                    }
                }
                else
                {
                    // Horizontal layout (bottom center)
                    if (!string.IsNullOrWhiteSpace(_title))
                    {
                        var titlePt = new Point2d(anchorX, anchorY + titleYOffsetHorizontal);
                        e.Display.Draw2dText(_title, _stroke, titlePt, false, titleHeightPx, _fontFace);
                    }

                    double startX = anchorX - 0.5 * colorCount * rectWidth;
                    for (int i = 0; i < colorCount; i++)
                    {
                        int rx = (int)Math.Round(startX + i * rectWidth);
                        int ry = (int)Math.Round(anchorY);
                        var rec2d = new Rectangle(rx, ry, rectWidthPx, rectHeightPx);
                        e.Display.Draw2dRectangle(rec2d, _stroke, strokeThickness, _colors[i]);

                        double value = diff * (double)i / range + _min;
                        string valueText = value.ToString("0.00", CultureInfo.InvariantCulture);
                        var pt = new Point2d(startX + labelXOffsetHorizontal + i * rectWidth, anchorY + labelYOffsetHorizontal);
                        e.Display.Draw2dText(valueText, _stroke, pt, false, textHeightPx, _fontFace);
                    }

                    // Max value label
                    {
                        int i = colorCount;
                        var pt = new Point2d(startX + labelXOffsetHorizontalMax + i * rectWidth, anchorY + labelYOffsetHorizontal);
                        string maxText = _max.ToString("0.00", CultureInfo.InvariantCulture);
                        e.Display.Draw2dText(maxText, _stroke, pt, false, textHeightPx, _fontFace);
                    }
                }
            }
        }
    }
}