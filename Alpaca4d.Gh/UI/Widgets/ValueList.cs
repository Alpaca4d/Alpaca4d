using Grasshopper.Kernel;
using Grasshopper.Kernel.Special;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;


namespace Alpaca4d.UIWidgets
{
    public static class ValueList
    {
        public static void UpdateValueLists(GH_Component component, int inputIndex, List<string> names, List<int> values = null, GH_ValueListMode listMode = GH_ValueListMode.DropDown, int toggleIndex = 1)
        {
            if (names.Count == 0)
            {
                return;
            }

            foreach (var source in component.Params.Input[inputIndex].Sources.OfType<GH_ValueList>())
            {
                if (!names.SequenceEqual(source.ListItems.Select(x => x.Name)))
                {
                    source.ListItems.Clear();
                    int num = 0;

                    if (values == null || values.Count != names.Count)
                    {
                        foreach (var name in names)
                        {
                            source.ListItems.Add(new GH_ValueListItem(name, $"\"{name}\""));
                        }
                    }
                    else
                    {
                        foreach (var name in names)
                        {
                            source.ListItems.Add(new GH_ValueListItem(name, values[num++].ToString()));
                        }
                    }

                    source.ListMode = listMode;
                    source.ToggleItem(toggleIndex);
                    source.ExpireSolution(true);
                }
            }
        }
    }
}