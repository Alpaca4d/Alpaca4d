using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using Alpaca4d;
using System.Collections.Generic;
using System.ComponentModel;

using Alpaca4d.TimeSeries;

namespace Alpaca4d.Gh
{
	public class Deserialize : GH_Component
	{
		public Deserialize()
		  : base("Deserialise (Alpaca4d)", "Deserialize",
			"Geometry representation of an OpenSeesFile. Not all the elements have been implemented!",
			"Alpaca4d", "10_Utility")
		{
			// Draw a Description Underneath the component
			this.Message = Alpaca4d.Gh.ComponentMessage.MyMessage(this);
		}

		/// <summary>
		/// Registers all the input parameters for this component.
		/// </summary>
		protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
		{
			pManager.AddTextParameter("FilePath", "FilePath", "", GH_ParamAccess.item);
			pManager[pManager.ParamCount - 1].Optional = true;
			pManager.AddTextParameter("Text", "Text", "", GH_ParamAccess.list);
			pManager[pManager.ParamCount - 1].Optional = true;

		}

		/// <summary>
		/// Registers all the output parameters for this component.
		/// </summary>
		protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
		{
			pManager.Register_GenericParam("Points", "Points", "");
			pManager.Register_GenericParam("Supports", "Supports", "");
			pManager.Register_GenericParam("Lines", "Lines", "");
			pManager.Register_GenericParam("ShellMesh", "ShellMesh", "");
			pManager.Register_GenericParam("BrickMesh", "BrickMesh", "");
		}

		/// <summary>
		/// This is the method that actually does the work.
		/// </summary>
		/// <param name="DA">The DA object can be used to retrieve data from input parameters and 
		/// to store data in output parameters.</param>
		protected override void SolveInstance(IGH_DataAccess DA)
		{
			string filePath = null;
			DA.GetData(0, ref filePath);

			var textFile = new List<string>();
			DA.GetDataList(1, textFile);

			if (textFile.Count != 0)
			{
				var model = Alpaca4d.Utils.TextToGeometry(textFile);
				// Finally assign the spiral to the output parameter.
				DA.SetDataList(0, model.points);
				DA.SetDataList(1, model.supports);
				DA.SetDataList(2, model.beamCurves);
				DA.SetDataList(3, model.shellMeshes);
				DA.SetDataList(4, model.brickMeshes);
			}
			else if (filePath != null)
			{
				var model = Alpaca4d.Utils.TextToGeometry(filePath);

				DA.SetDataList(0, model.points);
				DA.SetDataList(1, model.supports);
				DA.SetDataList(2, model.beamCurves);
				DA.SetDataList(3, model.shellMeshes);
				DA.SetDataList(4, model.brickMeshes);
			}
			else
			{
				AddRuntimeMessage(GH_RuntimeMessageLevel.Warning, "FilePath or Text failed to collect data");
				return;
			}
		}

		public override GH_Exposure Exposure => GH_Exposure.tertiary;
		protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.Deserialize__Alpaca4d_;
		public override Guid ComponentGuid => new Guid("{D5309B00-6784-42E9-9219-1B68B6D3320F}");
	}
}