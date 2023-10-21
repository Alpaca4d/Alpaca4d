using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Grasshopper.Kernel.Types;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Drawing;
using System.Reflection;
using System.Windows.Forms;
using Grasshopper.GUI;
using Grasshopper.GUI.Canvas;
using Grasshopper.Kernel.Attributes;



namespace Alpaca4d.Gh
{
    public class ExplodeAnythingComponent : GH_Component, IGH_VariableParameterComponent
    {
        private string typeName;

        private FieldInfo[] fieldsArr;

        private PropertyInfo[] propertiesArr;

        private ExplodeAnythingComponentAttributes ThisAttribute
        {
            get
            {
                return this.m_attributes as ExplodeAnythingComponentAttributes;
            }
        }

        protected override Bitmap Icon
        {
            get
            {
                return null;
            }
        }

        public override Guid ComponentGuid
        {
            get
            {
                return new Guid("{1E68B376-F7AA-4C70-BE45-FBCD1BD9B356}");
            }
        }

        public ExplodeAnythingComponent() : base("Explode", "Explode", "Explode anything you want to peek inside", "Alpaca4d", "10_Utility")
        {
        }

        public override void CreateAttributes()
        {
            this.m_attributes = new ExplodeAnythingComponentAttributes(this)
            {
                ButtonResponder = new ExplodeAnythingComponentAttributes.ResponderEvent(this.MatchResponder),
                ButtonText = "BOOM",
                TextLine = new LongShortString
                {
                    Long = "NULL",
                    Short = "NULL"
                },
                TextFont = new Font(GH_FontServer.ScriptSmall, FontStyle.Bold)
            };
        }

        protected override void AppendAdditionalComponentMenuItems(ToolStripDropDown menu)
        {
            base.AppendAdditionalComponentMenuItems(menu);
            GH_DocumentObject.Menu_AppendItem(menu, "Match object Fields", new EventHandler(this.MatchResponder));
        }

        private void MatchResponder(object o, EventArgs e)
        {
            bool flag = this.fieldsArr == null || this.propertiesArr == null;
            if (!flag)
            {
                bool flag2 = base.Params.Output.Count == this.fieldsArr.Length + this.propertiesArr.Length + 1;
                if (!flag2)
                {
                    while (base.Params.Output.Count < this.fieldsArr.Length + this.propertiesArr.Length + 1)
                    {
                        base.Params.RegisterOutputParam(new Param_GenericObject());
                    }
                    while (base.Params.Output.Count > this.fieldsArr.Length + this.propertiesArr.Length + 1)
                    {
                        base.Params.UnregisterOutputParameter(base.Params.Output[base.Params.Output.Count - 1]);
                    }
                    base.Params.OnParametersChanged();
                    this.VariableParameterMaintenance();
                    this.ExpireSolution(true);
                }
            }
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("Object", "O", "Object to explode", 0);
            pManager[pManager.ParamCount - 1].Optional = true;
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.AddGenericParameter("Type", "T", "Object Type", 0);
            this.VariableParameterMaintenance();
        }

        protected override void SolveInstance(IGH_DataAccess DA)
        {
            object obj = new object();
            bool flag = !DA.GetData<object>(0, ref obj);
            if (!flag)
            {
                bool flag2 = DA.Iteration < 1;
                if (flag2)
                {
                    this.typeName = obj.GetType().Name;
                }
                else
                {
                    bool flag3 = obj.GetType().Name != this.typeName;
                    if (flag3)
                    {
                        throw new Exception("Only same type of object can be explode");
                    }
                }
                Type type = obj.GetType();
                bool flag4 = type.Name.StartsWith("GH_");
                if (flag4)
                {
                    try
                    {
                        GH_ObjectWrapper gH_ObjectWrapper = (GH_ObjectWrapper)obj;
                        type = gH_ObjectWrapper.Value.GetType();
                        obj = gH_ObjectWrapper.Value;
                    }
                    catch
                    {
                        obj = obj.GetType().GetProperty("Value", BindingFlags.Instance | BindingFlags.Public | BindingFlags.FlattenHierarchy).GetValue(obj);
                        type = obj.GetType();
                    }
                }
                this.fieldsArr = type.GetFields(BindingFlags.Instance | BindingFlags.Public | BindingFlags.GetField);
                this.propertiesArr = type.GetProperties(BindingFlags.Instance | BindingFlags.Public | BindingFlags.GetProperty);
                int num = Math.Max(this.fieldsArr.Length + this.propertiesArr.Length, base.Params.Output.Count - 1);
                for (int i = 0; i < num; i++)
                {
                    bool flag5 = i >= this.fieldsArr.Length + this.propertiesArr.Length;
                    if (flag5)
                    {
                        base.Params.Output[i + 1].NickName = "--";
                    }
                    else
                    {
                        bool flag6 = i < this.fieldsArr.Length;
                        if (flag6)
                        {
                            try
                            {
                                bool flag7 = base.Params.Output[i + 1].NickName != this.fieldsArr[i].Name;
                                if (flag7)
                                {
                                    base.Params.Output[i + 1].NickName = this.fieldsArr[i].Name;
                                }
                                DA.SetData(i + 1, this.fieldsArr[i].GetValue(obj));
                            }
                            catch
                            {
                                this.AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Some fields were failed to explode, check answer carefully");
                            }
                        }
                        else
                        {
                            try
                            {
                                bool flag8 = base.Params.Output[i + 1].NickName != this.propertiesArr[i - this.fieldsArr.Length].Name;
                                if (flag8)
                                {
                                    base.Params.Output[i + 1].NickName = this.propertiesArr[i - this.fieldsArr.Length].Name;
                                }
                                bool flag9 = this.propertiesArr[i - this.fieldsArr.Length].Name == "Item" && (type.IsArray || (type.IsGenericType && type.GetGenericTypeDefinition() == typeof(List<>)));
                                if (flag9)
                                {
                                    IEnumerable enumerable = (IEnumerable)obj;
                                    DA.SetDataList(i + 1, enumerable);
                                }
                                else
                                {
                                    bool flag10 = type.Name.Contains("[]") && i == 3;
                                    if (flag10)
                                    {
                                        DA.SetDataList(i + 1, (IEnumerable)obj);
                                    }
                                    else
                                    {
                                        PropertyInfo propertyInfo = this.propertiesArr[i - this.fieldsArr.Length];
                                        bool flag11 = propertyInfo.GetIndexParameters().Length == 0;
                                        if (flag11)
                                        {
                                            DA.SetData(i + 1, propertyInfo.GetValue(obj));
                                        }
                                        else
                                        {
                                            bool flag12 = obj is IEnumerable;
                                            if (flag12)
                                            {
                                                DA.SetDataList(i + 1, (IEnumerable)obj);
                                            }
                                            else
                                            {
                                                DA.SetData(i + 1, obj);
                                            }
                                        }
                                    }
                                }
                            }
                            catch
                            {
                                this.AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Some fields were failed to explode, check answer carefully");
                            }
                        }
                    }
                }
                base.Params.Output[0].NickName = "Type";
                DA.SetData(0, type);
                this.ThisAttribute.TextLine = new LongShortString
                {
                    Long = type.FullName,
                    Short = type.Name
                };
            }
        }

        public bool CanInsertParameter(GH_ParameterSide side, int index)
        {
            return side == GH_ParameterSide.Output;
        }

        public bool CanRemoveParameter(GH_ParameterSide side, int index)
        {
            return side == GH_ParameterSide.Output;
        }

        public IGH_Param CreateParameter(GH_ParameterSide side, int index)
        {
            return new Param_GenericObject();
        }

        public bool DestroyParameter(GH_ParameterSide side, int index)
        {
            return true;
        }

        public void VariableParameterMaintenance()
        {
            bool flag = this.fieldsArr != null && this.propertiesArr != null;
            if (flag)
            {
                bool flag2 = base.Params.Output.Count > 0;
                if (flag2)
                {
                    for (int i = 0; i < this.fieldsArr.Length + this.propertiesArr.Length; i++)
                    {
                        bool flag3 = i < this.fieldsArr.Length;
                        if (flag3)
                        {
                            base.Params.Output[i].NickName = this.fieldsArr[i].Name;
                        }
                        else
                        {
                            base.Params.Output[i].NickName = this.propertiesArr[i - this.fieldsArr.Length].Name;
                        }
                    }
                }
            }
        }

        //public override void DrawViewportMeshes(IGH_PreviewArgs args)
        //{
        //}

        //public override void DrawViewportWires(IGH_PreviewArgs args)
        //{
        //}
    }




    internal class ExplodeAnythingComponentAttributes : GH_ComponentAttributes
    {
        public delegate void ResponderEvent(object o, EventArgs e);

        private readonly GH_Component attributeOwner;

        private Rectangle textRectangle;

        private Rectangle buttonRectangle;

        public string ButtonText
        {
            get;
            set;
        }

        public LongShortString TextLine
        {
            get;
            set;
        }

        public Font TextFont
        {
            get;
            set;
        }

        public ExplodeAnythingComponentAttributes.ResponderEvent ButtonResponder
        {
            get;
            set;
        }

        public ExplodeAnythingComponentAttributes(GH_Component owner) : base(owner)
        {
            this.attributeOwner = owner;
            this.TextLine = new LongShortString
            {
                Long = "",
                Short = ""
            };
            this.TextFont = GH_FontServer.Standard;
            this.ButtonText = "Button";
        }

        protected override void Layout()
        {
            base.Layout();
            Rectangle r = GH_Convert.ToRectangle(this.Bounds);
            r.Height += 36;
            this.Bounds = r;
            this.buttonRectangle = r;
            this.buttonRectangle.Y = this.buttonRectangle.Bottom - 20;
            this.buttonRectangle.Height = 20;
            this.buttonRectangle.Inflate(-2, -2);
            this.textRectangle = r;
            this.textRectangle.Y = this.buttonRectangle.Bottom - 36;
            this.textRectangle.Height = 16;
        }

        protected override void Render(GH_Canvas canvas, Graphics graphics, GH_CanvasChannel channel)
        {
            base.Render(canvas, graphics, channel);
            bool flag = channel == GH_CanvasChannel.Objects;
            if (flag)
            {
                GH_Capsule gH_Capsule = GH_Capsule.CreateTextCapsule(this.buttonRectangle, this.buttonRectangle, GH_Palette.Grey, this.ButtonText);
                gH_Capsule.Render(graphics, this.Selected, this.attributeOwner.Locked, false);
                gH_Capsule.Dispose();
                StringFormat format = new StringFormat
                {
                    Alignment = StringAlignment.Center,
                    LineAlignment = StringAlignment.Center,
                    Trimming = StringTrimming.EllipsisCharacter
                };
                bool flag2 = (float)GH_FontServer.StringWidth(this.TextLine.Long, this.TextFont) < this.Bounds.Width;
                if (flag2)
                {
                    graphics.DrawString(this.TextLine.Long, this.TextFont, Brushes.Black, this.textRectangle, format);
                }
                else
                {
                    graphics.DrawString(this.TextLine.Short, this.TextFont, Brushes.Black, this.textRectangle, format);
                }
            }
        }

        public override GH_ObjectResponse RespondToMouseUp(GH_Canvas sender, GH_CanvasMouseEvent e)
        {
            bool flag = e.Button == MouseButtons.Left;
            GH_ObjectResponse result;
            if (flag)
            {
                bool flag2 = this.buttonRectangle.Contains( new System.Drawing.Point((int)e.CanvasLocation.X, (int)e.CanvasLocation.Y));
                if (flag2)
                {
                    bool flag3 = this.ButtonResponder != null;
                    if (flag3)
                    {
                        this.ButtonResponder(sender, e);
                        result = GH_ObjectResponse.Handled;
                        return result;
                    }
                }
            }
            result = base.RespondToMouseDown(sender, e);
            return result;
        }
    }



    internal class LongShortString
    {
        public string Long
        {
            get;
            set;
        }

        public string Short
        {
            get;
            set;
        }
    }




}