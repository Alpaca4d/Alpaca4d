using System;
using System.Collections.Generic;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;

using Grasshopper.Kernel;

// Writes what the docs images need about every component shown in the toolbar - names, tab,
// inputs and outputs, message - as JSON, and its 24 px icon as a PNG.
class Export
{
    static void Main(string[] args)
    {
        var gha = Assembly.LoadFrom(args[0]);
        string outDir = args[1];
        Directory.CreateDirectory(Path.Combine(outDir, "icons"));
        var entries = new List<string>();
        foreach (var type in Types(gha).Where(t => !t.IsAbstract && typeof(GH_Component).IsAssignableFrom(t) && t.GetConstructor(Type.EmptyTypes) != null).OrderBy(t => t.Name))
        {
            var c = (GH_Component)Activator.CreateInstance(type);
            if (c.Exposure == GH_Exposure.hidden) continue;
            string icon = "";
            try
            {
                if (c.Icon_24x24 != null)
                {
                    icon = "icons/" + type.Name + ".png";
                    c.Icon_24x24.Save(Path.Combine(outDir, icon), ImageFormat.Png);
                }
            }
            catch (Exception) { icon = ""; }
            Func<IGH_Param, string> param = p => $"{{\"name\":{Q(p.Name)},\"nick\":{Q(p.NickName)},\"optional\":{(p.Optional ? "true" : "false")}}}";
            entries.Add("{" +
                $"\"type\":{Q(type.Name)},\"name\":{Q(c.Name)},\"nick\":{Q(c.NickName)},\"category\":{Q(c.Category)},\"subcategory\":{Q(c.SubCategory)}," +
                $"\"message\":{Q(c.Message ?? "")},\"icon\":{Q(icon)}," +
                $"\"inputs\":[{string.Join(",", c.Params.Input.Select(param))}],\"outputs\":[{string.Join(",", c.Params.Output.Select(param))}]," +
                $"\"menus\":[{string.Join(",", MenusOf(c))}],\"button\":{Q(ButtonOf(c))}" +
                "}");
        }
        File.WriteAllText(Path.Combine(outDir, "components.json"), "[\n" + string.Join(",\n", entries) + "\n]\n", new UTF8Encoding(false));
        Console.WriteLine($"{entries.Count} components");
    }

    // The fold-out menus of an extendable component: each menu, the inputs and outputs it holds,
    // and the controls it shows when placed, flattened out of their panels. "folds" is true when
    // the menu's inputs and outputs are drawn only in it, and so are hidden while it is closed.
    static IEnumerable<string> MenusOf(GH_Component c)
    {
        c.CreateAttributes();
        var menus = new List<string>();
        var collection = MenuCollection(c.Attributes, out bool folds);
        if (collection == null) return menus;
        foreach (var menu in (System.Collections.IEnumerable)collection.GetType().GetProperty("Menus").GetValue(collection))
        {
            Func<string, IEnumerable<string>> plugs = side => ((System.Collections.IEnumerable)Get(menu, side)).Cast<object>()
                .Select(p => Q(((IGH_Param)Get(p, "Parameter")).NickName));
            var controls = new List<string>();
            foreach (var control in (System.Collections.IEnumerable)Get(menu, "Controlls")) Flatten(control, controls);
            menus.Add($"{{\"name\":{Q((string)Get(menu, "Name"))},\"header\":{Q((string)Get(menu, "Header"))},\"expanded\":{((bool)Get(menu, "Expanded") ? "true" : "false")}," +
                      $"\"folds\":{(folds ? "true" : "false")},\"plugs\":[{string.Join(",", plugs("Inputs"))}],\"outputs\":[{string.Join(",", plugs("Outputs"))}],\"controls\":[{string.Join(",", controls)}]}}");
        }
        return menus;
    }

    // An extendable component keeps its menus in _collection, and its menus' inputs on the body
    // with the others. A switcher component composes them, in the order it draws them, from its
    // active unit's menus, its own, and the drop-down that picks the unit when there is more than
    // one; OnSwitchUnit composes them and sets that drop-down to the active unit, as placing the
    // component on the canvas does. Its body has only the inputs and outputs of no menu.
    static object MenuCollection(IGH_Attributes attributes, out bool folds)
    {
        const BindingFlags any = BindingFlags.Instance | BindingFlags.NonPublic;
        folds = false;
        for (var t = attributes.GetType(); t != null; t = t.BaseType)
        {
            var extendable = t.GetField("_collection", any);
            if (extendable != null) return extendable.GetValue(attributes);
            var composed = t.GetField("composedCollection", any);
            if (composed != null)
            {
                try { t.GetMethod("OnSwitchUnit")?.Invoke(attributes, null); }
                catch (TargetInvocationException) { t.GetMethod("ComposeMenu", any)?.Invoke(attributes, null); }
                folds = true;
                return composed.GetValue(attributes);
            }
        }
        return null;
    }

    static void Flatten(object control, List<string> into)
    {
        var children = control.GetType().GetField("_controls", BindingFlags.Instance | BindingFlags.NonPublic)?.GetValue(control) as System.Collections.IEnumerable;
        string kind = control.GetType().Name;
        if (children != null && kind == "MenuPanel")
        {
            foreach (var child in children) Flatten(child, into);
            return;
        }
        string visible = (bool)(Get(control, "Visible") ?? true) ? "true" : "false";
        switch (kind)
        {
            case "MenuCheckBox":
                into.Add($"{{\"kind\":\"check\",\"text\":{Q((string)Get(control, "Tag"))},\"checked\":{((bool)Get(control, "Active") ? "true" : "false")},\"visible\":{visible}}}");
                break;
            case "MenuDropDown":
                var items = ((System.Collections.IEnumerable)Get(control, "Items")).Cast<object>().Select(i => Q((string)i.GetType().GetField("content").GetValue(i)));
                into.Add($"{{\"kind\":\"dropdown\",\"items\":[{string.Join(",", items)}],\"selected\":{Get(control, "Value")},\"visible\":{visible}}}");
                break;
            case "MenuSlider":
                into.Add($"{{\"kind\":\"slider\",\"name\":{Q((string)Get(control, "Name"))},\"value\":{Num(Get(control, "Value"))},\"min\":{Num(Get(control, "MinValue"))},\"max\":{Num(Get(control, "MaxValue"))},\"decimals\":{Get(control, "NumDecimals")},\"visible\":{visible}}}");
                break;
            case "MenuStaticText":
                into.Add($"{{\"kind\":\"text\",\"text\":{Q((string)Get(control, "Text"))},\"visible\":{visible}}}");
                break;
            default:
                into.Add($"{{\"kind\":{Q(kind)},\"visible\":{visible}}}");
                break;
        }
    }

    /// <summary>The caption of a button a component draws under itself, such as Explorer Inputs' Fly.</summary>
    static string ButtonOf(GH_Component c)
    {
        return c.GetType().GetProperty("ButtonText", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public)?.GetValue(c) as string ?? "";
    }

    static object Get(object o, string name) => o.GetType().GetProperty(name)?.GetValue(o);

    static string Num(object v) => Convert.ToDouble(v).ToString(System.Globalization.CultureInfo.InvariantCulture);

    static string Q(string s)
    {
        var b = new StringBuilder("\"");
        foreach (char ch in s ?? "")
        {
            if (ch == '"' || ch == '\\') b.Append('\\').Append(ch);
            else if (ch == '\n') b.Append("\\n");
            else if (ch < 32) b.Append($"\\u{(int)ch:x4}");
            else b.Append(ch);
        }
        return b.Append('"').ToString();
    }

    static IEnumerable<Type> Types(Assembly a)
    {
        try { return a.GetTypes(); } catch (ReflectionTypeLoadException e) { return e.Types.Where(t => t != null); }
    }
}
