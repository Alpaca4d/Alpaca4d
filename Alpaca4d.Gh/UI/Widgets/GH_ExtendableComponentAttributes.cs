using GH_IO.Serialization;
using Grasshopper.GUI;
using Grasshopper.GUI.Canvas;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Attributes;
using System;
using System.Drawing;
using System.Windows.Forms;

namespace Alpaca4d.UIWidgets
{
	[Serializable]
	public class GH_ExtendableComponentAttributes : GH_ComponentAttributes
	{
		private float _minWidth;

		private GH_Attr_Widget _activeToolTip;

		private GH_MenuCollection _collection;

		private const bool RENDER_OVERLAY_OVERWIDGETS = true;

		public float MinWidth
		{
			get
			{
				return _minWidth;
			}
			set
			{
				_minWidth = value;
			}
		}

		public GH_ExtendableComponentAttributes(IGH_Component nComponent)
			: base(nComponent)
		{
			_collection = new GH_MenuCollection();
		}

		public void AddMenu(GH_ExtendableMenu _menu)
		{
			_collection.AddMenu(_menu);
		}

		public override bool Write(GH_IWriter writer)
		{
			try
			{
				_collection.Write(writer);
			}
			catch (Exception)
			{
			}
			return base.Write(writer);
		}

		public override bool Read(GH_IReader reader)
		{
			try
			{
				_collection.Read(reader);
			}
			catch (Exception)
			{
			}
			return base.Read(reader);
		}

		protected override void PrepareForRender(GH_Canvas canvas)
		{
			base.PrepareForRender(canvas);
			LayoutStyle();
		}

		protected override void Layout()
		{
			Pivot = GH_Convert.ToPoint(Pivot);
			base.Layout();
			FixLayout();
			LayoutMenu();
		}

		protected void FixLayout()
		{
			_ = Bounds.Width;
			float num = Math.Max(_collection.GetMinLayoutSize().Width, _minWidth);
			float num2 = 0f;
			if (num > Bounds.Width)
			{
				num2 = num - Bounds.Width;
				Bounds = new RectangleF(Bounds.X - num2 / 2f, Bounds.Y, num, Bounds.Height);
			}
			foreach (IGH_Param item in base.Owner.Params.Output)
			{
				PointF pivot = item.Attributes.Pivot;
				RectangleF bounds = item.Attributes.Bounds;
				item.Attributes.Pivot = new PointF(pivot.X, pivot.Y);
				item.Attributes.Bounds = new RectangleF(bounds.Location.X, bounds.Location.Y, bounds.Width + num2 / 2f, bounds.Height);
			}
			foreach (IGH_Param item2 in base.Owner.Params.Input)
			{
				PointF pivot2 = item2.Attributes.Pivot;
				RectangleF bounds2 = item2.Attributes.Bounds;
				item2.Attributes.Pivot = new PointF(pivot2.X - num2 / 2f, pivot2.Y);
				item2.Attributes.Bounds = new RectangleF(bounds2.Location.X - num2 / 2f, bounds2.Location.Y, bounds2.Width + num2 / 2f, bounds2.Height);
			}

		}

		private void LayoutStyle()
		{
			_collection.Palette = GH_CapsuleRenderEngine.GetImpliedPalette(base.Owner);
			_collection.Style = GH_CapsuleRenderEngine.GetImpliedStyle(_collection.Palette, Selected, base.Owner.Locked, base.Owner.Hidden);
			_collection.Layout();
		}

		protected void LayoutMenu()
		{
			_collection.Width = Bounds.Width;
			_collection.Pivot = new PointF(Bounds.Left, Bounds.Bottom);
			LayoutStyle();
			Bounds = new RectangleF(Bounds.X, Bounds.Y, Bounds.Width, Bounds.Height + _collection.Height);

		}

		protected override void Render(GH_Canvas iCanvas, Graphics graph, GH_CanvasChannel iChannel)
		{

			if (iChannel == GH_CanvasChannel.First)
			{
				iCanvas.CanvasPostPaintWidgets -= RenderPostWidgets;
				iCanvas.CanvasPostPaintWidgets += RenderPostWidgets;
			}
			base.Render(iCanvas, graph, iChannel);
			if (iChannel != GH_CanvasChannel.Objects)
			{
				_ = 30;
			}
			else
			{
				_collection.Render(new WidgetRenderArgs(iCanvas, WidgetChannel.Object));
			}


		}

		private void RenderPostWidgets(GH_Canvas sender)
		{
			_collection.Render(new WidgetRenderArgs(sender, WidgetChannel.Overlay));
		}

		public override GH_ObjectResponse RespondToMouseUp(GH_Canvas sender, GH_CanvasMouseEvent e)
		{
			GH_ObjectResponse gH_ObjectResponse = _collection.RespondToMouseUp(sender, e);
			switch (gH_ObjectResponse)
			{
				case GH_ObjectResponse.Capture:
					ExpireLayout();
					sender.Invalidate();
					return gH_ObjectResponse;
				default:
					ExpireLayout();
					sender.Invalidate();
					return GH_ObjectResponse.Release;
				case GH_ObjectResponse.Ignore:
					return base.RespondToMouseUp(sender, e);
			}
		}

		public override GH_ObjectResponse RespondToMouseDoubleClick(GH_Canvas sender, GH_CanvasMouseEvent e)
		{
			GH_ObjectResponse gH_ObjectResponse = _collection.RespondToMouseDoubleClick(sender, e);
			if (gH_ObjectResponse != 0)
			{
				ExpireLayout();
				sender.Refresh();
				return gH_ObjectResponse;
			}
			return base.RespondToMouseDoubleClick(sender, e);

		}

		public override GH_ObjectResponse RespondToKeyDown(GH_Canvas sender, KeyEventArgs e)
		{
			GH_ObjectResponse gH_ObjectResponse = _collection.RespondToKeyDown(sender, e);
			if (gH_ObjectResponse != 0)
			{
				ExpireLayout();
				sender.Refresh();
				return gH_ObjectResponse;
			}
			return base.RespondToKeyDown(sender, e);


		}

		public override GH_ObjectResponse RespondToMouseMove(GH_Canvas sender, GH_CanvasMouseEvent e)
		{
			GH_ObjectResponse gH_ObjectResponse = _collection.RespondToMouseMove(sender, e);
			if (gH_ObjectResponse != 0)
			{
				ExpireLayout();
				sender.Refresh();
				return gH_ObjectResponse;
			}
			return base.RespondToMouseMove(sender, e);
		}

		public override GH_ObjectResponse RespondToMouseDown(GH_Canvas sender, GH_CanvasMouseEvent e)
		{
			try
			{
				GH_ObjectResponse gH_ObjectResponse = _collection.RespondToMouseDown(sender, e);
				if (gH_ObjectResponse != 0)
				{
					ExpireLayout();
					sender.Refresh();
					return gH_ObjectResponse;
				}
				return base.RespondToMouseDown(sender, e);
			}
			catch (Exception)
			{
				return base.RespondToMouseDown(sender, e);
			}
		}

		public override bool IsTooltipRegion(PointF pt)
		{
			_activeToolTip = null;
			bool flag = base.IsTooltipRegion(pt);
			if (flag)
			{
				return flag;
			}
			if (base.m_innerBounds.Contains(pt))
			{
				GH_Attr_Widget gH_Attr_Widget = _collection.IsTtipPoint(pt);
				if (gH_Attr_Widget != null)
				{
					_activeToolTip = gH_Attr_Widget;
					return true;
				}
			}
			return false;
		}

		public bool GetActiveTooltip(PointF pt)
		{
			GH_Attr_Widget gH_Attr_Widget = _collection.IsTtipPoint(pt);
			if (gH_Attr_Widget != null)
			{
				_activeToolTip = gH_Attr_Widget;
				return true;
			}
			return false;
		}

		public override void SetupTooltip(PointF canvasPoint, GH_TooltipDisplayEventArgs e)
		{
			GetActiveTooltip(canvasPoint);
			if (_activeToolTip != null)
			{
				_activeToolTip.TooltipSetup(canvasPoint, e);
				return;
			}
			e.Title = PathName;
			e.Text = base.Owner.Description;
			e.Description = base.Owner.InstanceDescription;
			e.Icon = base.Owner.Icon_24x24;
			if (base.Owner is IGH_Param)
			{
				IGH_Param obj = (IGH_Param)base.Owner;
				string text = obj.TypeName;
				if (obj.Access == GH_ParamAccess.list)
				{
					text += "[…]";
				}
				if (obj.Access == GH_ParamAccess.tree)
				{
					text += "{…;…;…}";
				}
				e.Title = $"{PathName} ({text})";
			}
		}

		public string GetMenuDescription()
		{
			return _collection.GetMenuDescription();
		}
	}
}
