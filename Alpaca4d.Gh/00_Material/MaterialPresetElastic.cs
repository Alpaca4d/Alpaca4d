using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using Alpaca4d.UIWidgets;
using Grasshopper.Kernel;
using Grasshopper.Kernel.Parameters;
using Newtonsoft.Json.Linq;
using System.Reflection;
using static Alpaca4d.Gh.ComponentMessage;

namespace Alpaca4d.Gh
{
	public class MaterialPresetElastic : GH_ExtendableComponent
	{
		private MenuDropDown modelDrop;
		private MenuDropDown typeDrop;
		private MenuDropDown gradeDrop;

		private Dictionary<string, List<string>> typeToGrades = new Dictionary<string, List<string>>();

		private static readonly object jsonLock = new object();
		private static JObject steelDb;
		private static JObject concreteDb;
		private static JObject timberDb;
		private static JObject plasticDb;

		private static JObject LoadJsonResourceOnce(ref JObject cache, string resourceName)
		{
			if (cache != null) return cache;
			lock (jsonLock)
			{
				if (cache != null) return cache;
				var coreAsm = typeof(Alpaca4d.Material.ElasticIsotropicMaterial).Assembly;
				using (var stream = coreAsm.GetManifestResourceStream(resourceName))
				{
					if (stream == null) throw new FileNotFoundException("Embedded resource not found", resourceName);
					using (var reader = new StreamReader(stream))
					{
						var json = reader.ReadToEnd();
						cache = JObject.Parse(json);
						return cache;
					}
				}
			}
		}

		private static double TryGetDouble(JObject obj, string key)
		{
			if (obj == null) return double.NaN;
			var token = obj[key];
			return token != null ? token.Value<double>() : double.NaN;
		}

		// Convert MPa to kN/m^2 (1 MPa = 1000 kN/m^2)
		private static double MPaTokN_m2(double xMpa) => double.IsNaN(xMpa) ? double.NaN : xMpa * 1000.0;

		private static double ComputeNuFromEG(double e, double g)
		{
			if (g <= 0 || e <= 0) return double.NaN;
			var nu = (e / (2.0 * g)) - 1.0;
			// Clamp to a physical range
			if (double.IsNaN(nu) || double.IsInfinity(nu)) return double.NaN;
			return Math.Max(0.0, Math.Min(0.4999, nu));
		}

		public override Guid ComponentGuid => new Guid("{F50A7B47-2E73-4B57-BF7A-DB6D7EAC91D6}");
		public override GH_Exposure Exposure => GH_Exposure.secondary;
		protected override Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Material_Library__Alpaca4d_;

		public MaterialPresetElastic()
			: base("Material Library (Elastic)", "Library",
			  "Select a material type and grade to create an Elastic Material",
			  "Alpaca4d", "00_Material")
        {
            // Draw a Description Underneath the component
            this.Message = MyMessage(this);
        }

		protected override void RegisterInputParams(GH_InputParamManager pManager)
		{
		}

		protected override void RegisterOutputParams(GH_OutputParamManager pManager)
		{
			pManager.RegisterParam(new Param_GenericObject(), "Material", "Material", "Material");
		}

		protected override void Setup(GH_ExtendableComponentAttributes attr)
		{
			var menu = new GH_ExtendableMenu(0, "Library");
			menu.Name = "Library";
			menu.Header = "Select model, type and grade";

			var panel = new MenuPanel(0, "Library");
			panel.Header = "Library";

			typeDrop = new MenuDropDown(0, "Type", "Type");
			typeDrop.VisibleItemCount = 6;
			typeDrop.ValueChanged += OnTypeChanged;

			gradeDrop = new MenuDropDown(1, "Grade", "Grade");
			gradeDrop.VisibleItemCount = 8;
			gradeDrop.ValueChanged += OnGradeChanged;
			
			modelDrop = new MenuDropDown(2, "Model", "Model");
			modelDrop.VisibleItemCount = 2;
			modelDrop.ValueChanged += OnModelChanged;

			panel.AddControl(typeDrop);
			panel.AddControl(gradeDrop);
			panel.AddControl(modelDrop);
			menu.AddControl(panel);
			menu.Expand();
			attr.AddMenu(menu);
			attr.MinWidth = 160f;

			InitializeModelOptions();
			InitializeTypeOptions();
			InitializeGradeOptions();
		}

		protected override void OnComponentLoaded()
		{
			base.OnComponentLoaded();
			InitializeModelOptions();
			InitializeTypeOptions();
			InitializeGradeOptions();
		}

		private void OnModelChanged(object sender, EventArgs e)
		{
			this.ExpireSolution(true);
		}

		private void OnTypeChanged(object sender, EventArgs e)
		{
			InitializeGradeOptions();
			this.ExpireSolution(true);
		}

		private void OnGradeChanged(object sender, EventArgs e)
		{
			this.ExpireSolution(true);
		}

		private void InitializeModelOptions()
		{
			if (modelDrop == null) return;
			modelDrop.Clear();
			// Keep default as nD to preserve previous behavior
			modelDrop.AddItem("Uniaxial", "Uniaxial");
			modelDrop.AddItem("nD", "nD");
		}

		private void InitializeTypeOptions()
		{
			// Build the dynamic dictionary from embedded JSON resources
			typeToGrades = BuildTypeToGrades();

			// Repopulate type dropdown
			if (typeDrop == null) return;
			typeDrop.Clear();
			var types = typeToGrades.Keys.OrderBy(k => k).ToList();
			for (int i = 0; i < types.Count; i++)
			{
				var t = types[i];
				typeDrop.AddItem(t, t);
			}
		}

		private Dictionary<string, List<string>> BuildTypeToGrades()
		{
			var result = new Dictionary<string, List<string>>();

			void addFromDb(JObject db)
			{
				if (db == null) return;
				// Discover material_type from first entry and collect all names (keys)
				var first = db.Properties().Select(p => p.Value as JObject).FirstOrDefault(v => v != null);
				if (first == null) return;
				var matType = first["material_type"]?.Value<string>() ?? "Unknown";
				var names = db.Properties().Select(p => p.Name).OrderBy(n => n).ToList();
				if (names.Count == 0) return;
				if (!result.ContainsKey(matType)) result[matType] = new List<string>();
				foreach (var n in names)
				{
					if (!result[matType].Contains(n)) result[matType].Add(n);
				}
			}

			// Load each DB as needed
			try { addFromDb(LoadJsonResourceOnce(ref steelDb, "Alpaca4d.Resources.Material.steel_properties.json")); } catch { }
			try { addFromDb(LoadJsonResourceOnce(ref concreteDb, "Alpaca4d.Resources.Material.concrete_properties.json")); } catch { }
			try { addFromDb(LoadJsonResourceOnce(ref timberDb, "Alpaca4d.Resources.Material.timber_properties.json")); } catch { }
			try { addFromDb(LoadJsonResourceOnce(ref plasticDb, "Alpaca4d.Resources.Material.plastic_properties.json")); } catch { }

			return result;
		}

		private void InitializeGradeOptions()
		{
			if (typeDrop == null || gradeDrop == null) return;
			string selType = GetSelected(typeDrop, defaultName: "Steel");
			gradeDrop.Clear();
			if (typeToGrades.TryGetValue(selType, out var grades))
			{
				for (int i = 0; i < grades.Count; i++)
				{
					var g = grades[i];
					gradeDrop.AddItem(g, g);
				}
			}
		}

		private static string GetSelected(MenuDropDown dd, string defaultName)
		{
			if (dd.Items.Count == 0) return defaultName;
			int idx = Math.Max(0, Math.Min(dd.Value, dd.Items.Count - 1));
			return dd.Items[idx].name ?? dd.Items[idx].content ?? defaultName;
		}

		protected override void SolveInstance(IGH_DataAccess DA)
		{
			string selType = typeDrop != null ? GetSelected(typeDrop, "Steel") : "Steel";
			string selGrade = gradeDrop != null ? GetSelected(gradeDrop, "S235") : "S235";
			string selModel = modelDrop != null ? GetSelected(modelDrop, "nD") : "nD";

			// Compute properties in kN/m^2, unit system consistent with existing components (Force=kN, Length=m)
			double E, nu, rho;
			GetElasticParameters(selType, selGrade, out E, out nu, out rho);
			double G = E / (2.0 * (1.0 + nu));

			if (string.Equals(selModel, "Uniaxial", StringComparison.OrdinalIgnoreCase))
			{
				double eNeg = E;
				double eta = 0.0;
				var material = new Alpaca4d.Material.UniaxialMaterialElastic(selGrade, E, eNeg, eta, G, nu, rho);
				DA.SetData(0, material);
			}
			else
			{
				var material = new Alpaca4d.Material.ElasticIsotropicMaterial(selGrade, E, G, nu, rho);
				DA.SetData(0, material);
			}
		}

		private void GetElasticParameters(string type, string grade, out double E, out double nu, out double rho)
		{
			SetDefaultElastic(out E, out nu, out rho);
			switch (type)
			{
				case "Steel":
					GetSteelParameters(grade, out E, out nu, out rho);
					break;
				case "Concrete":
					GetConcreteParameters(grade, out E, out nu, out rho);
					break;
				case "Timber":
					GetTimberParameters(grade, out E, out nu, out rho);
					break;
				case "Plastic":
					GetPlasticParameters(grade, out E, out nu, out rho);
					break;
				default:
					// keep defaults
					break;
			}
		}

		private static void SetDefaultElastic(out double E, out double nu, out double rho)
		{
			// Sensible defaults if JSON lookups fail
			E = 210000000;   // kN/m^2
			nu = 0.30;
			rho = 7850;      // kg/m^3
		}

		private void GetSteelParameters(string grade, out double E, out double nu, out double rho)
		{
			SetDefaultElastic(out E, out nu, out rho);
			var db = LoadJsonResourceOnce(ref steelDb, "Alpaca4d.Resources.Material.steel_properties.json");
			var entry = db?[grade] as JObject;
			if (entry == null) return;

			var eMpa = TryGetDouble(entry, "E");
			var gMpa = TryGetDouble(entry, "G");
			var rhoVal = TryGetDouble(entry, "rho");
			if (!double.IsNaN(eMpa)) E = MPaTokN_m2(eMpa);
			if (!double.IsNaN(rhoVal)) rho = rhoVal;
			var nuComputed = ComputeNuFromEG(MPaTokN_m2(eMpa), MPaTokN_m2(gMpa));
			if (!double.IsNaN(nuComputed)) nu = nuComputed;
		}

		private void GetConcreteParameters(string grade, out double E, out double nu, out double rho)
		{
			SetDefaultElastic(out E, out nu, out rho);
			var db = LoadJsonResourceOnce(ref concreteDb, "Alpaca4d.Resources.Material.concrete_properties.json");
			var entry = db?[grade] as JObject;
			if (entry == null)
			{
				nu = 0.20;
				return;
			}

			var eMpa = TryGetDouble(entry, "E_mean");
			var gMpa = TryGetDouble(entry, "G_mean");
			var rhoMean = TryGetDouble(entry, "rho_mean");
			var rhoK = TryGetDouble(entry, "rho_k");

			if (!double.IsNaN(eMpa)) E = MPaTokN_m2(eMpa);
			if (!double.IsNaN(rhoMean)) rho = rhoMean;
			else if (!double.IsNaN(rhoK)) rho = rhoK;

			var nuComputed = ComputeNuFromEG(MPaTokN_m2(eMpa), MPaTokN_m2(gMpa));
			nu = !double.IsNaN(nuComputed) ? nuComputed : 0.20;
		}

		private void GetTimberParameters(string grade, out double E, out double nu, out double rho)
		{
			SetDefaultElastic(out E, out nu, out rho);
			var db = LoadJsonResourceOnce(ref timberDb, "Alpaca4d.Resources.Material.timber_properties.json");
			var entry = db?[grade] as JObject;
			if (entry == null)
			{
				nu = 0.35;
				rho = 500;
				return;
			}

			var eMpa = TryGetDouble(entry, "E_mean");
			var gMpa = TryGetDouble(entry, "G_mean");
			var rhoMean = TryGetDouble(entry, "rho_mean");
			var rhoK = TryGetDouble(entry, "rho_k");

			if (!double.IsNaN(eMpa)) E = MPaTokN_m2(eMpa);
			if (!double.IsNaN(rhoMean)) rho = rhoMean;
			else if (!double.IsNaN(rhoK)) rho = rhoK;

			var nuComputed = ComputeNuFromEG(MPaTokN_m2(eMpa), MPaTokN_m2(gMpa));
			nu = !double.IsNaN(nuComputed) ? nuComputed : 0.35;
		}

		private void GetPlasticParameters(string grade, out double E, out double nu, out double rho)
		{
			SetDefaultElastic(out E, out nu, out rho);
			var db = LoadJsonResourceOnce(ref plasticDb, "Alpaca4d.Resources.Material.plastic_properties.json");
			var entry = db?[grade] as JObject;
			if (entry == null)
			{
				nu = 0.40;
				return;
			}

			var eMpa = TryGetDouble(entry, "E");
			var gMpa = TryGetDouble(entry, "G");
			var rhoVal = TryGetDouble(entry, "rho");

			if (!double.IsNaN(eMpa)) E = MPaTokN_m2(eMpa);
			if (!double.IsNaN(rhoVal)) rho = rhoVal;

			var nuComputed = ComputeNuFromEG(MPaTokN_m2(eMpa), MPaTokN_m2(gMpa));
			nu = !double.IsNaN(nuComputed) ? nuComputed : 0.40;
		}
	}
}

