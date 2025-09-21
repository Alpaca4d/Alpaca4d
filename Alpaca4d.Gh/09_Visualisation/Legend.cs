using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Display;
using Rhino.Geometry;
using System;
using System.Collections.Generic;
using System.Drawing;

namespace Alpaca4d.Gh
{
    public class Legend : GH_Component
    {
        private List<Color> _colors = new List<Color>();
        private List<string> _labels = new List<string>();

        // UI options
        private int _itemHeight = 18;       // px
        private int _itemWidth = 18;        // px
        private int _itemSpacing = 6;       // px vertical spacing
        private int _padding = 10;          // px inset from border and between box/text
        private int _fontHeight = 12;       // px
        private string _fontFace = "Arial";
        private string _title = string.Empty;

        public Legend()
          : base("Legend (Alpaca4d)", "Legend",
            "Draw a fixed on-screen legend with colors and labels",
            "Alpaca4d", "09_Visualisation")
        {
            this.Message = $"{this.Name}";
        }

        protected override void RegisterInputParams(GH_InputParamManager pManager)
        {
            pManager.AddColourParameter("Colors", "C", "Legend colors (one per item)", GH_ParamAccess.list);
            pManager.AddTextParameter("Labels", "T", "Legend labels (aligned with colors)", GH_ParamAccess.list);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddTextParameter("Title", "Title", "Optional legend title", GH_ParamAccess.item, "");
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        protected override void RegisterOutputParams(GH_OutputParamManager pManager)
        {
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            _colors.Clear();
            _labels.Clear();

            DA.GetDataList(0, _colors);
            DA.GetDataList(1, _labels);
            DA.GetData(2, ref _title);

            // if labels shorter, pad with empty strings
            if (_labels.Count < _colors.Count)
            {
                int missing = _colors.Count - _labels.Count;
                for (int i = 0; i < missing; i++) _labels.Add(string.Empty);
            }
        }

        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            base.DrawViewportWires(args);
            if (this.Hidden || this.Locked) return;
            if (_colors.Count == 0) return;

            // Get viewport screen rectangle
            int left, right, bottom, top;
            args.Viewport.GetScreenPort(out left, out right, out bottom, out top);

            // Position legend near right side centered vertically
            int totalItems = _colors.Count;
            int blockHeight = totalItems * _itemHeight + (totalItems - 1) * _itemSpacing;
            int titleExtra = string.IsNullOrWhiteSpace(_title) ? 0 : (_itemHeight + _itemSpacing);

            int legendWidth = _padding + _itemWidth + _padding + 200; // reserve room for text
            int legendHeight = _padding + titleExtra + blockHeight + _padding;

            int startX = right - legendWidth - 20; // 20 px from right border
            int startY = top + 20;                 // 20 px from top border

            // Background panel
            var bgRect = new System.Drawing.Rectangle(startX, startY, legendWidth, legendHeight);
            args.Display.Draw2dRectangle(bgRect, System.Drawing.Color.FromArgb(180, 245, 245, 255), true);
            args.Display.Draw2dRectangle(bgRect, System.Drawing.Color.FromArgb(180, 120, 120, 120), false);

            int cursorX = startX + _padding;
            int cursorY = startY + _padding;

            // Title
            if (!string.IsNullOrWhiteSpace(_title))
            {
                var titlePoint = new Point2d(cursorX, cursorY + _itemHeight * 0.75);
                args.Display.Draw2dText(_title, System.Drawing.Color.Black, titlePoint, false, _fontHeight + 2, _fontFace);
                cursorY += _itemHeight + _itemSpacing;
            }

            // Items
            for (int i = 0; i < _colors.Count; i++)
            {
                var rect = new System.Drawing.Rectangle(cursorX, cursorY, _itemWidth, _itemHeight);
                args.Display.Draw2dRectangle(rect, _colors[i], true);
                args.Display.Draw2dRectangle(rect, System.Drawing.Color.Black, false);

                var textPoint = new Point2d(cursorX + _itemWidth + _padding, cursorY + _itemHeight * 0.75);
                var label = i < _labels.Count ? _labels[i] : string.Empty;
                args.Display.Draw2dText(label, System.Drawing.Color.Black, textPoint, false, _fontHeight, _fontFace);

                cursorY += _itemHeight + _itemSpacing;
            }
        }

        public override GH_Exposure Exposure => GH_Exposure.tertiary;
        protected override Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Legend__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{A6B3B5C9-DB8D-4B6A-9E7E-63C6D2E2F9F5}");
    }
}


