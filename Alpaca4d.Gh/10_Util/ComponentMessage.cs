using Grasshopper.Kernel;

namespace Alpaca4d.Gh
{
	internal static class ComponentMessage
	{
		public static string MyMessage(GH_Component component)
		{
			return $"{component.NickName}\n{component.Category}";
		}
	}
}