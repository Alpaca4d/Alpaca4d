using Alpaca4d.TimeSeries;
using Grasshopper;
using Grasshopper.Kernel;
using Rhino.Geometry;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace Alpaca4d.Gh
{

    public class ModelView : GH_Component
    {
        private Alpaca4d.Model _model = null;

        private List<Mesh> _beamMeshes = new List<Mesh>();
        private List<Mesh> _shellMeshes = new List<Mesh>();
        private List<Mesh> _brickMeshes = new List<Mesh>();

        private bool? _extruded = false;
        private bool _loads = false;
        private bool _supports = false;
        private bool _constraints = false;

        private double _loadsScale = 1.0;
        private double _supportsScale = 1.0;

        public ModelView()
          : base("Model View (Alpaca4d)", "ModelView",
            "ModelView",
            "Alpaca4d", "09_Visualisation")
        {
            // Draw a Description Underneath the component
            this.Message = $"{this.Name}";
        }

        protected override void RegisterInputParams(GH_Component.GH_InputParamManager pManager)
        {
            pManager.AddGenericParameter("AlpacaModel", "AlpacaModel", "", GH_ParamAccess.item);
            pManager.AddBooleanParameter("Extruded", "Extruded", "", GH_ParamAccess.item, false);
            pManager.AddBooleanParameter("Load", "Load", "", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("LoadFactor", "LoadFactor", "", GH_ParamAccess.item, 1.0);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddBooleanParameter("Support", "Support", "", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;
            pManager.AddNumberParameter("SupportFactor", "SupportFactor", "", GH_ParamAccess.item, 1.0);
            pManager.AddBooleanParameter("Constraint", "Constraint", "", GH_ParamAccess.item, false);
            pManager[pManager.ParamCount - 1].Optional = true;
        }
        protected override void RegisterOutputParams(GH_Component.GH_OutputParamManager pManager)
        {
            pManager.Register_GenericParam("AlpacaModel", "AlpacaModel", "");
            pManager.Register_StringParam("Info", "Info", "");
        }
        protected override void SolveInstance(IGH_DataAccess DA)
        {
            DA.GetData(0, ref _model);
            DA.GetData(1, ref _extruded);
            DA.GetData(2, ref _loads);
            DA.GetData(3, ref _loadsScale);
            DA.GetData(4, ref _supports);
            DA.GetData(5, ref _supportsScale); 
            DA.GetData(6, ref _constraints);


            foreach (var item in _model.Beams)
            {
                var curve = item.Curve;
                var section = item.Section.Curves[0];

                var localY = item.GeomTransf.LocalY;
                var localZ = item.GeomTransf.LocalZ;
                var planeStart = new Rhino.Geometry.Plane(curve.PointAtStart, localZ, localY);
                var planeEnd = new Rhino.Geometry.Plane(curve.PointAtEnd, localZ, localY);

                var transfEnd = Rhino.Geometry.Transform.PlaneToPlane(Plane.WorldXY, planeStart);
                var transfStart = Rhino.Geometry.Transform.PlaneToPlane(Plane.WorldXY, planeEnd);

                var sectionStart = section.DuplicateCurve();
                var sectionEnd = section.DuplicateCurve();

                sectionStart.Transform(transfStart);
                sectionEnd.Transform(transfEnd);


                var polyStart = sectionStart.ToPolyline(0, 0, 0, 0).ToPolyline();
                var polyEnd = sectionEnd.ToPolyline(0, 0, 0, 0).ToPolyline();
                var sections = new List<Rhino.Geometry.Polyline> { polyStart, polyEnd };

                var beamMesh = Utils.CreateLoft(sections);
                beamMesh.VertexColors.CreateMonotoneMesh(item.Color);
                _beamMeshes.Add(beamMesh);
            }
            foreach (var item in _model.Shells)
            {
                var myMesh = new Mesh();

                var medialAxisMesh = item.Mesh;
                var meshTop = medialAxisMesh.Offset(item.Section.Thickness / 2, true);
                var meshBottom = medialAxisMesh.Offset(-item.Section.Thickness / 2, true);

                myMesh.Append(meshTop);
                myMesh.Append(meshBottom);
                myMesh.VertexColors.CreateMonotoneMesh(item.Color);

                _shellMeshes.Add(myMesh);
            }
            foreach (var item in _model.Bricks)
            {
                var brick = item.Mesh;
                brick.VertexColors.CreateMonotoneMesh(item.Color);

                _brickMeshes.Add(brick);
            }

            // Finally assign the spiral to the output parameter.
            DA.SetData(0, _model);
            DA.SetDataList(1, _model.Tcl);

            // Ensure viewport updates even if only preview content changed
            Rhino.RhinoDoc.ActiveDoc?.Views?.Redraw();
        }


        protected override void BeforeSolveInstance()
        {
            _beamMeshes.Clear();
            _shellMeshes.Clear();
            _brickMeshes.Clear();
        }


        public override void DrawViewportWires(IGH_PreviewArgs args)
        {
            base.DrawViewportWires(args);
            if (this.Hidden || this.Locked || _model == null) return;

            // Draw Point Fibers
            if(_loads == true)
            {
                var loadPatterns = _model.LoadPatterns.SelectMany(x => x.Load);

                var pointLoads = loadPatterns.OfType<Alpaca4d.Loads.PointLoad>();
                var meshLoads = loadPatterns.OfType<Alpaca4d.Loads.MeshLoad>();
                var lineLoads = loadPatterns.OfType<Alpaca4d.Loads.LineLoad>();


                foreach (var pointLoad in pointLoads)
                {
                    var point = pointLoad.Pos;
                    var magnitude = pointLoad.Force * _loadsScale;
                    VisualisePointLoad(args, point, magnitude);
                }

                //foreach (var pointLoad in _model.GravityPointLoad)
                //{
                //    var point = pointLoad.Pos;
                //    var magnitude = pointLoad.Force * _loadsScale;
                //    VisualisePointLoad(args, point, magnitude);
                //}

                // visualise MeshLoad
                foreach(var meshLoad in _model.MeshLoad)
                {
                    if (meshLoad.Element == null)
                    {
                        foreach (var shell in _model.Shells)
                        {
                            var meshGeometry = shell.Mesh; ;
                            var forceValue = meshLoad.GlobalForce.Length;
                            var unitVector = meshLoad.GlobalForce / forceValue;
                            VisualiseMeshLoad(args, meshGeometry, forceValue, unitVector);
                        }
                    }
                    else
                    {
                        var meshGeometry = meshLoad.Element.Mesh;
                        var forceValue = meshLoad.GlobalForce.Length;
                        var unitVector = meshLoad.GlobalForce / forceValue;
                        VisualiseMeshLoad(args, meshGeometry, forceValue, unitVector);
                    }
                }
                // visualise LineLoad
                foreach(var lineLoad in _model.LineLoad)
				{
                    if(lineLoad.Element != null)
                    {
                        var lineGeometry = lineLoad.Element.Curve;
                        var forceVector = lineLoad.GlobalForce;
                        VisualiseLineLoad(args, lineGeometry, forceVector);
                    }
                    else
                    {
                        foreach (var beam in _model.Beams)
                        {
                            var lineGeometry = beam.Curve;
                            var forceVector = lineLoad.GlobalForce;
                            VisualiseLineLoad(args, lineGeometry, forceVector);
                        }
                    }
                }
            }

            // Draw Supports
            if(_supports == true)
            {
                // Define Material
                var diffuse = System.Drawing.Color.White;
                var specular = System.Drawing.Color.White;
                var ambient = System.Drawing.Color.White;
                var emission = System.Drawing.Color.White;
                var shine = 1.00;
                var transparency = 0.00;

                var material = new Rhino.Display.DisplayMaterial(diffuse, specular, ambient, emission, shine, transparency);


                foreach (var support in _model.Supports)
                {
                    if (support.Geometry is Mesh) 
                    {
                        var supportGeometry = support.Geometry.DuplicateMesh();
                        var scale = Rhino.Geometry.Transform.Scale(Rhino.Geometry.Point3d.Origin, _supportsScale);
                    
                        supportGeometry.Transform(scale);
                        supportGeometry.Transform(Transform.Translation(new Rhino.Geometry.Vector3d(support.Pos)));

                        args.Display.DrawMeshShaded(supportGeometry, material);
                        args.Display.DrawMeshWires(supportGeometry, System.Drawing.Color.Black, 2);
                        args.Display.DrawMeshVertices(supportGeometry, System.Drawing.Color.White);
                    }
                    else if(support.Geometry is String)
                    {
                        args.Display.DrawDot(support.Pos, support.Geometry);
                    }
                }
            }

            // Draw Elements
            if(_extruded == true)
            {
                foreach (var mesh in _beamMeshes)
                {
                    args.Display.DrawMeshFalseColors(mesh);
                    args.Display.DrawMeshWires(mesh, System.Drawing.Color.Black, 2);
                    args.Display.DrawMeshVertices(mesh, System.Drawing.Color.Black);
                }
                foreach (var mesh in _shellMeshes)
                {
                    args.Display.DrawMeshFalseColors(mesh);
                    args.Display.DrawMeshWires(mesh, System.Drawing.Color.Black, 2);
                    args.Display.DrawMeshVertices(mesh, System.Drawing.Color.Black);
                }
                foreach (var mesh in _brickMeshes)
                {
                    args.Display.DrawMeshFalseColors(mesh);
                    args.Display.DrawMeshWires(mesh, System.Drawing.Color.Black, 2);
                    args.Display.DrawMeshVertices(mesh, System.Drawing.Color.Black);
                }
            }
            else if(_extruded == false)
            {
                var beams = _model.Beams;
                var shells = _model.Shells;
                var bricks = _model.Bricks;

                foreach (var beam in beams)
                {
                    var crv = beam.Curve;
                    var color = beam.Color;
                    args.Display.DrawCurve(crv, color);
                }
                foreach (var shell in shells)
                {
                    var mesh = shell.Mesh;
                    mesh.VertexColors.CreateMonotoneMesh(shell.Color);
                    args.Display.DrawMeshFalseColors(mesh);
                    args.Display.DrawMeshWires(mesh, System.Drawing.Color.Black, 2);
                    args.Display.DrawMeshVertices(mesh, System.Drawing.Color.Black);
                }
                foreach (var brick in bricks)
                {
                    var mesh = brick.Mesh;

                    args.Display.DrawMeshFalseColors(mesh);
                    args.Display.DrawMeshWires(mesh, System.Drawing.Color.Black, 2);
                    args.Display.DrawMeshVertices(mesh, System.Drawing.Color.Black);
                }
            }

            //// Draw Local Axis
            //var boundingBox = new Rhino.Geometry.BoundingBox(_fiberSection.Fibers.Select(x => x.Pos));
            //var center = boundingBox.Center;
            //var length = boundingBox.Diagonal.Length / 2;
            //var yLine = new Rhino.Geometry.Line(center, new Vector3d(0, length, 0));
            //var zLine = new Rhino.Geometry.Line(center, new Vector3d(-length, 0, 0));

            //args.Display.DrawLineArrow(yLine, System.Drawing.Color.Green, 3, 0.5);
            //args.Display.DrawLineArrow(zLine, System.Drawing.Color.Blue, 3, 0.5);

            //var yPos = (yLine.ToNurbsCurve().PointAtEnd - center) * 1.1;
            //var zPos = (zLine.ToNurbsCurve().PointAtEnd - center) * 1.1;

            //args.Display.Draw2dText("Y", System.Drawing.Color.Black, center + yPos, true, 36);
            //args.Display.Draw2dText("Z", System.Drawing.Color.Black, center + zPos, true, 36);
        }

        public override bool IsPreviewCapable => true;

        public override BoundingBox ClippingBox
        {
            get
            {
                return new BoundingBox(
                    new Point3d(-1e9, -1e9, -1e9),
                    new Point3d( 1e9,  1e9,  1e9)
                );
            }
        }

        private void VisualisePointLoad(IGH_PreviewArgs args, Point3d position, Vector3d magnitude)
        {
            if (magnitude.Length > 0)
            {
                var line = new Rhino.Geometry.Line(position, magnitude);
                var vector = new Vector3d(position.X - line.ToNurbsCurve().PointAtEnd.X, position.Y - line.ToNurbsCurve().PointAtEnd.Y, position.Z - line.ToNurbsCurve().PointAtEnd.Z);
                var translation = Rhino.Geometry.Transform.Translation(vector);
                line.Transform(translation);
                args.Display.DrawArrow(line, System.Drawing.Color.IndianRed, 24, 0);
            }
        }

        private void VisualiseLineLoad(IGH_PreviewArgs args, Curve lineGeometry, Vector3d forceVector)
        {
            var color = System.Drawing.Color.DarkSeaGreen;

            int division = 6;
            for (double value = 0.0; value <= 1.00; value += 1.0 / division)
            {
                var point = lineGeometry.PointAtNormalizedLength(value);
                var magnitude = forceVector * _loadsScale;
                var line = new Rhino.Geometry.Line(point, magnitude);
                var vector = new Vector3d(point.X - line.ToNurbsCurve().PointAtEnd.X, point.Y - line.ToNurbsCurve().PointAtEnd.Y, point.Z - line.ToNurbsCurve().PointAtEnd.Z);
                var translation = Rhino.Geometry.Transform.Translation(vector);
                line.Transform(translation);
                args.Display.DrawArrow(line, color, 24, 0);
            }
        }

        private void VisualiseMeshLoad(IGH_PreviewArgs args, Mesh meshGeometry, double forceValue, Vector3d unitVector)
        {
            var meshPos = meshGeometry.Offset(forceValue * _loadsScale, true, unitVector);
            meshPos.Faces.DeleteFaces(new List<int>(1));
            var color = System.Drawing.Color.OrangeRed;
            var material = new Rhino.Display.DisplayMaterial(color, color, color, color, 0.00, 0.80);

            args.Display.DrawMeshShaded(meshPos, material);
            args.Display.DrawMeshWires(meshPos, System.Drawing.Color.OrangeRed, 2);
            args.Display.DrawMeshVertices(meshPos, System.Drawing.Color.Black);
        }

        public override GH_Exposure Exposure => GH_Exposure.primary;
        protected override System.Drawing.Bitmap Icon => Alpaca4d.Gh.Properties.Resources.model_View__Alpaca4d_;
        public override Guid ComponentGuid => new Guid("{5EDB6364-D458-43D6-81E9-324DECA1FEA6}");
    }
}
