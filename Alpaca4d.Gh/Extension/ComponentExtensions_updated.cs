using Grasshopper.Kernel;
using Grasshopper.Kernel.Special;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Runtime.CompilerServices;

// The following code has been taken from an open-source library

namespace Alpaca4d.Gh
{
	public static partial class ValueListUtils
	{
		private sealed class BracketC
		{
			public BracketC()
			{
			}

			public static readonly ValueListUtils.BracketC _nine = new ValueListUtils.BracketC();

			public static Func<GH_ValueListItem, string> _nine__0_0 = null;

			public static Func<GH_ValueListItem, string> _nine__0_1 = null;

			internal string b__0_0(GH_ValueListItem x)
			{
				return x.Name;
			}

			internal string b__0_1(GH_ValueListItem x)
			{
				return x.Name;
			}
		}


		public static void updateValueLists(GH_Component component, int input_ind, List<string> names, List<int> values = null, GH_ValueListMode list_mode = GH_ValueListMode.DropDown)
		{
			if (names.Count == 0)
			{
				return;
			}
			using (IEnumerator<IGH_Param> enumerator = component.Params.Input[input_ind].Sources.GetEnumerator())
			{
				while (enumerator.MoveNext())
				{
					GH_ValueList gH_ValueList = enumerator.Current as GH_ValueList;
					if (gH_ValueList != null)
					{
						IEnumerable<GH_ValueListItem> arg_62_0 = gH_ValueList.ListItems;
						Func<GH_ValueListItem, string> arg_62_1;

						if ((arg_62_1 = ValueListUtils.BracketC._nine__0_0) == null)
						{
							arg_62_1 = new Func<GH_ValueListItem, string>(new BracketC().b__0_0);
						}
						if (!names.SequenceEqual(arg_62_0.Select(arg_62_1)))
						{
							IEnumerable<GH_ValueListItem> arg_96_0 = gH_ValueList.SelectedItems;
							Func<GH_ValueListItem, string> arg_96_1;
							if ((arg_96_1 = ValueListUtils.BracketC._nine__0_1) == null)
							{
								arg_96_1 = new Func<GH_ValueListItem, string>(new BracketC().b__0_1);
							}
							IEnumerable<string> enumerable = arg_96_0.Select(arg_96_1);
							gH_ValueList.ListItems.Clear();
							int num = 0;
							if (values == null || values.Count != names.Count)
							{
								using (List<string>.Enumerator enumerator2 = names.GetEnumerator())
								{
									while (enumerator2.MoveNext())
									{
										string current = enumerator2.Current;
										gH_ValueList.ListItems.Add(new GH_ValueListItem(current, String.Format("\"{0}\"", current) ));
									}
									goto IL_158;
								}
							}
							goto IL_106;
						IL_158:
							foreach (string current2 in enumerable)
							{
								int num2 = names.IndexOf(current2);
								if (num2 != -1)
								{
									gH_ValueList.ToggleItem(num2);
								}
							}
							gH_ValueList.ListMode = list_mode;
							gH_ValueList.ExpireSolution(true);
							continue;
						IL_106:
							foreach (string current3 in names)
							{
								gH_ValueList.ListItems.Add(new GH_ValueListItem(current3, values[num++].ToString()));
							}
							goto IL_158;
						}
					}
				}
			}
		}
	}
}