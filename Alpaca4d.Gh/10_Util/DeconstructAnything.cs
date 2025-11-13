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
    public class DeconstructAnything : GH_Component, IGH_VariableParameterComponent
    {
        private string typeName;

        private FieldInfo[] fieldsArr;

        private PropertyInfo[] propertiesArr;

        // Prevent stacking multiple scheduled parameter resizes
        private bool isParameterResizeScheduled;

        protected override Bitmap Icon => Properties.Resources.Deconstruct__Alpaca4d_;

        public override Guid ComponentGuid
        {
            get
            {
                return new Guid("{1E68B376-F7AA-4C70-BE45-FBCD1BD9B356}");
            }
        }

        public DeconstructAnything() : base("Deconstruct (Alpaca4d)", "Deconstruct", "Deconstruct any object", "Alpaca4d", "10_Utility")
        {
            this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
        }

        public override GH_Exposure Exposure => GH_Exposure.primary;

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("object", "object", "Object to explode", 0);
        }

        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            // Start with no outputs; they will be added dynamically when input is provided
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
                // Auto-match outputs to fields + properties without requiring button click
                int desiredOutputCount = this.fieldsArr.Length + this.propertiesArr.Length + 1; // +1 for class output
                if (base.Params.Output.Count != desiredOutputCount)
                {
                    if (!this.isParameterResizeScheduled)
                    {
                        GH_Document doc = this.OnPingDocument();
                        if (doc != null)
                        {
                            this.isParameterResizeScheduled = true;
                            int targetCount = desiredOutputCount;
                            doc.ScheduleSolution(1, (d) =>
                            {
                                try
                                {
                                    // Ensure the class output exists at index 0 first
                                    if (this.Params.Output.Count == 0)
                                    {
                                        this.Params.RegisterOutputParam(new Param_GenericObject { NickName = "Object Class" });
                                    }
                                    while (this.Params.Output.Count < targetCount)
                                    {
                                        this.Params.RegisterOutputParam(new Param_GenericObject());
                                    }
                                    while (this.Params.Output.Count > targetCount)
                                    {
                                        this.Params.UnregisterOutputParameter(this.Params.Output[this.Params.Output.Count - 1]);
                                    }
                                    this.Params.OnParametersChanged();
                                    this.VariableParameterMaintenance();
                                    this.ExpireSolution(false);
                                }
                                finally
                                {
                                    this.isParameterResizeScheduled = false;
                                }
                            });
                        }
                    }
                    return;
                }
                int availableSlots = Math.Max(0, base.Params.Output.Count - 1);
                int num = Math.Min(this.fieldsArr.Length + this.propertiesArr.Length, availableSlots);
                for (int i = 0; i < num; i++)
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
                            object fieldValue = this.fieldsArr[i].GetValue(obj);
                            bool isEnumerableField = fieldValue is IEnumerable && !(fieldValue is string);
                            if (isEnumerableField)
                            {
                                DA.SetDataList(i + 1, (IEnumerable)fieldValue);
                            }
                            else
                            {
                                DA.SetData(i + 1, fieldValue);
                            }
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
                                PropertyInfo propertyInfo = this.propertiesArr[i - this.fieldsArr.Length];
                                bool flag11 = propertyInfo.GetIndexParameters().Length == 0;
                                if (flag11)
                                {
                                    object propertyValue = propertyInfo.GetValue(obj);
                                    bool isEnumerableProp = propertyValue is IEnumerable && !(propertyValue is string);
                                    if (isEnumerableProp)
                                    {
                                        DA.SetDataList(i + 1, (IEnumerable)propertyValue);
                                    }
                                    else
                                    {
                                        DA.SetData(i + 1, propertyValue);
                                    }
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
                        catch
                        {
                            this.AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "Some fields were failed to explode, check answer carefully");
                        }
                    }
                }
                // Clear any extra output slots beyond current fields+properties
                for (int j = num; j < availableSlots; j++)
                {
                    if ((j + 1) < base.Params.Output.Count)
                    {
                        base.Params.Output[j + 1].NickName = "--";
                        DA.SetData(j + 1, null);
                    }
                }

                if (base.Params.Output.Count > 0)
                {
                    DA.SetData(0, type);
                    base.Params.Output[0].NickName = "Object Class";
                }
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
            bool hasMembers = this.fieldsArr != null && this.propertiesArr != null;
            if (!hasMembers) return;
            if (base.Params.Output.Count <= 1) return;

            int availableSlots = base.Params.Output.Count - 1;
            int num = Math.Min(this.fieldsArr.Length + this.propertiesArr.Length, availableSlots);
            for (int i = 0; i < num; i++)
            {
                if (i < this.fieldsArr.Length)
                {
                    base.Params.Output[i + 1].NickName = this.fieldsArr[i].Name;
                }
                else
                {
                    base.Params.Output[i + 1].NickName = this.propertiesArr[i - this.fieldsArr.Length].Name;
                }
            }
            for (int j = num; j < availableSlots; j++)
            {
                base.Params.Output[j + 1].NickName = "--";
            }
        }

        public override void DrawViewportMeshes(IGH_PreviewArgs args)
        {
        }

        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
        }
    }
}