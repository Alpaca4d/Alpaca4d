using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System;

using Rhino.Geometry;
using Alpaca4d.Element;
using Alpaca4d.Material;
using Alpaca4d.Generic;
using Alpaca4d;

namespace Alpaca4d
{
    public class Model
    {
        public int Ndm { get; set; }
        public int Ndf { get; set; }
        public List<Point3d> UniquePoints { get; set; }
        public List<Point3d> UniquePointsThreeNDF { get; set; } = new List<Point3d>();
        public List<Point3d> UniquePointsSixNDF { get; set; } = new List<Point3d>();
        public PointCloud PointCloud { get; set; }
        public PointCloud CloudPointThreeNDF { get; set; }
        public PointCloud CloudPointSixNDF { get; set; }
        public RTree RTreeCloudPoint { get; set; }
        public RTree RTreeCloudPointThreeNDF { get; set; }
        public RTree RTreeCloudPointSixNDF { get; set; }
        public static int NumberOfBeam { get; set; }
        public List<Node> Nodes { get; set; } = new List<Node> { };
        public List<IBeam> Beams { get; set; } = new List<IBeam> { };
        public List<IShell> Shells { get; set; } = new List<IShell> { };
        public List<IBrick> Bricks { get; set; } = new List<IBrick> { };
        public List<IElement> Elements { get; set; } = new List<IElement> { };
        public List<ForceBeamColumn> ForceBeamColumns { get; set; }
        public List<ILoad> Loads { get; set; } = new List<ILoad> { };
        public List<Alpaca4d.Loads.PointLoad> PointLoad
        {
            get
            {
                var pointLoadType = this.Loads.OfType<Alpaca4d.Loads.PointLoad>();
                return pointLoadType.ToList();
            }
        }
        public List<Alpaca4d.Loads.PointLoad> GravityPointLoad { get; set; } = new List<Alpaca4d.Loads.PointLoad> { };
        public List<Alpaca4d.Loads.LineLoad> LineLoad
        {
            get
            {
                var lineLoadType = this.Loads.OfType<Alpaca4d.Loads.LineLoad>();
                return lineLoadType.ToList();
            }
        }
        public List<Alpaca4d.Loads.MeshLoad> MeshLoad
        {
            get
            {
                var meshLoadType = this.Loads.OfType<Alpaca4d.Loads.MeshLoad>();
                return meshLoadType.ToList();
            }
        }
        public List<Alpaca4d.Loads.MassLoad> Mass { get; set; } = new List<Alpaca4d.Loads.MassLoad> { };
        public List<Support> Supports { get; set; } = new List<Support> { };
        public List<IConstraint> Constraint { get; set; } = new List<IConstraint> { };
        public List<IRecorder> Recorders { get; set; } = new List<IRecorder> { };


        public List<UniaxialMaterialElastic> UniaxialMaterialElastics { get; set; }
        public List<IMaterial> Materials { get; set; } = new List<IMaterial> { };
        public List<IUniaxialSection> ElasticSections { get; set; } = new List<IUniaxialSection> { };
        public double Tollerance { get; set; }
        public double? TotalMass
        {
            get
            {
                double? mass = 0.00;
                foreach (var item in this.Elements)
                {
                    if (item.Type == ElementType.Beam)
                    {
                        var beam = (IBeam)item;
                        var length = beam.Curve.GetLength();
                        var massDens = beam.Section.Area * beam.Section.Material.Rho;
                        mass += (massDens * length);
                    }

                    else if (item.Type == ElementType.Shell)
                    {
                        var shell = (IShell)item;

                        double meshArea = Rhino.Geometry.AreaMassProperties.Compute(shell.Mesh).Area;
                        var areaDensity = shell.Section.Thickness * (double)shell.Section.Material.Rho;
                        mass += areaDensity * meshArea;
                    }

                    else if (item.Type == ElementType.Brick)
                    {
                        var brick = (IBrick)item;
                        var meshVolume = Rhino.Geometry.VolumeMassProperties.Compute(brick.Mesh).Volume;
                        var density = (double)brick.Material.Rho;
                        mass += density * meshVolume;
                    }
                    else
                    {
                        throw new NotImplementedException($"{item.Type} has not been considered!");
                    }
                }

                foreach (var pointMass in this.Mass)
                {
                    mass += pointMass.TransMass.Z;
                }
                return mass;
            }
        }

        public string FileName { get; set; }
        public string ModalAnalysisReportFile { get; set; }

        public List<IStructure> ThreeNdfModel { get; set; } = new List<IStructure> { };
        public List<IStructure> SixNdfModel { get; set; } = new List<IStructure> { };

        public Analysis Analysis { get; set; }
        public Settings Settings { get; set; }
        public bool IsAnalysed { get; set; }
        public bool IsStatic { get; set; }
        public bool IsTransient { get; set; }
        public bool IsModal { get; set; }
        public int NumberOfModes { get; set; }

        public List<string> Tcl { get; set; } = new List<string> { };

        public bool HasSSpBrick
        {
            get
            {
                bool hasSSpBrick = false;
                foreach(var brick in this.Bricks)
                {
                    if(brick.ElementClass == ElementClass.SSPBrick)
                    {
                        hasSSpBrick = true;
                        break;
                    }
                }
                return hasSSpBrick;
            }
        }

        public bool HasTetrahedron
        {
            get
            {
                bool hasTetrahedron = false;
                foreach (var brick in this.Bricks)
                {
                    if (brick.ElementClass == ElementClass.FourNodeTetrahedron)
                    {
                        hasTetrahedron = true;
                        break;
                    }
                }
                return hasTetrahedron;
            }
        }

        public bool HasTriShell
        {
            get
            {
                bool hasTriShell = false;
                foreach (var shell in this.Shells)
                {
                    if (shell.ElementClass == ElementClass.ShellDKGT || shell.ElementClass == ElementClass.ShellNLDKGT)
                    {
                        hasTriShell = true;
                        break;
                    }
                }
                return hasTriShell;
            }
        }

        public bool HasQuadShell
        {
            get
            {
                bool hasQuadShell = false;
                foreach (var shell in this.Shells)
                {
                    if (shell.ElementClass == ElementClass.ASDShellQ4)
                    {
                        hasQuadShell = true;
                        break;
                    }
                }
                return hasQuadShell;
            }
        }

        public Dictionary<int?, Vector3d> NodalDisplacements(int step)
        {
            Dictionary<int?, Vector3d> result = new Dictionary<int?, Vector3d>();
            var _resultType = this.IsModal == false ? Result.ResultType.DISPLACEMENT : Result.ResultType.MODES_OF_VIBRATION_U;
            var dispVector = Alpaca4d.Result.Read.NodalOutput(this, step, _resultType);
            foreach(var node in this.Nodes)
            {
                result.Add(node.Id, dispVector.ElementAt( (int)node.Id - 1));
            }
            return result;
        }


        public List<Curve> DeformedBeam(int step, double scale)
        {
            var dispDictionary = this.NodalDisplacements(step);

            var beamDefModel = new List<Curve>();

            foreach(var beam in this.Beams)
            {
                var beamCurve = beam.Curve;

                var startVector = new Rhino.Geometry.Vector3d(dispDictionary[(int)beam.INode]) * scale;
                var endvector = new Rhino.Geometry.Vector3d(dispDictionary[(int)beam.JNode]) * scale;

               beamDefModel.Add( new Rhino.Geometry.LineCurve(beamCurve.PointAtStart + startVector, beamCurve.PointAtEnd + endvector) );
            }
            return beamDefModel;
        }


        // 3d visualisation
        // WIP
        public List<Mesh> DeformedBeam(int step, double scale, List<System.Drawing.Color> colors, double min, double max)
        {
            var dispDictionary = this.NodalDisplacements(step);

            var beamDefModel = new List<Mesh>();

            foreach (var beam in this.Beams)
            {
                var beamCurve = beam.Curve;

                var startVctr = new Rhino.Geometry.Vector3d(dispDictionary[(int)beam.INode]);
                var endVctr = new Rhino.Geometry.Vector3d(dispDictionary[(int)beam.JNode]);

                var startVector = new Rhino.Geometry.Vector3d(dispDictionary[(int)beam.INode]) * scale;
                var endvector = new Rhino.Geometry.Vector3d(dispDictionary[(int)beam.JNode]) * scale;
                

                var beamDeformed = new Rhino.Geometry.LineCurve(beamCurve.PointAtStart + startVector, beamCurve.PointAtEnd + endvector);

                var curve = beamDeformed;
                var section = beam.Section.Curves[0];

                var localY = beam.GeomTransf.LocalY;
                var localZ = beam.GeomTransf.LocalZ;
                var planeStart = new Rhino.Geometry.Plane(curve.PointAtStart, localZ, localY);
                var planeEnd = new Rhino.Geometry.Plane(curve.PointAtEnd, localZ, localY);

                var transfStart = Rhino.Geometry.Transform.PlaneToPlane(Plane.WorldXY, planeStart);
                var transfEnd = Rhino.Geometry.Transform.PlaneToPlane(Plane.WorldXY, planeEnd);

                var sectionStart = section.DuplicateCurve();
                var sectionEnd = section.DuplicateCurve();

                sectionStart.Transform(transfStart);
                sectionEnd.Transform(transfEnd);


                var polyStart = sectionStart.ToPolyline(0, 0, 0, 0).ToPolyline();
                var polyEnd = sectionEnd.ToPolyline(0, 0, 0, 0).ToPolyline();
                var sections = new List<Rhino.Geometry.Polyline> { polyStart, polyEnd };

                var beamMesh = Alpaca4d.Utils.CreateLoft(sections, new List<double> { startVctr.Length, endVctr.Length }, colors, min, max);

                beamDefModel.Add(beamMesh);
            }


            return beamDefModel;
        }

        public List<Mesh> DeformedShell(int step, double scale, List<System.Drawing.Color> colors, double min, double max)
        {
            var dispDictionary = this.NodalDisplacements(step);

            // find the total range of displacement
            var disp = dispDictionary.Values.Select(x => x.Length);

            var d = new SortedDictionary<double, System.Drawing.Color>();

            var numberOfColors = colors.Count;
            var diff = (max - min) / (numberOfColors-1);

            var start = min;
            foreach (var color in colors)
			{
                if(!d.ContainsKey(start))
                {
                    d.Add(start, color);
                    start += diff;
                }
			}

            var shellDefModel = new List<Mesh>();

            foreach (var item in this.Shells)
            {
                var points = item.Mesh.Vertices.Select(x => new Rhino.Geometry.Point3d(x));
                var pointDef = new List<Point3d>();
                var defValues = new List<double>();
                 
                int i = 0;
                foreach(var point in points)
                {
                    var indexNode = item.IndexNodes[i];
                    pointDef.Add(point + dispDictionary[indexNode] * scale);
                    defValues.Add(dispDictionary[indexNode].Length);
                    i++;
                }

                var shellDef = new Rhino.Geometry.Mesh();
                shellDef.Vertices.AddVertices(pointDef);

                var myColors = defValues.Select(x => (Colors.GetColor(x, d)));

                shellDef.VertexColors.SetColors(myColors.ToArray());


                if (item.IndexNodes.Count == 4)
                    shellDef.Faces.AddFace(0, 1, 2, 3);
                else
                    shellDef.Faces.AddFace(0, 1, 2);

                shellDefModel.Add(shellDef);
            }

            return shellDefModel;
        }

        public List<Mesh> DeformedBrick(int step, double scale, List<System.Drawing.Color> colors, double min, double max)
        {
            var dispDictionary = this.NodalDisplacements(step);

            // find the total range of displacement
            var disp = dispDictionary.Values.Select(x => x.Length);

            var d = new SortedDictionary<double, System.Drawing.Color>();

            var numberOfColors = colors.Count;
            var diff = (max - min) / (numberOfColors - 1);

            var start = min;
            foreach (var color in colors)
            {
                if (!d.ContainsKey(start))
                {
                    d.Add(start, color);
                    start += diff;
                }
            }


            var brickDefModel = new List<Mesh>();

            foreach (var item in this.Bricks)
            {
                var points = item.Mesh.Vertices.Select(x => new Rhino.Geometry.Point3d(x));
                var pointDef = new List<Point3d>();
                var defValues = new List<double>();

                int i = 0;
                foreach (var point in points)
                {
                    var indexNode = item.IndexNodes[i];
                    pointDef.Add(point + dispDictionary[(int)indexNode] * scale);
                    defValues.Add(dispDictionary[(int)indexNode].Length);
                    i++;
                }

                var brickDef = new Rhino.Geometry.Mesh();
                brickDef.Vertices.AddVertices(pointDef);

                var myColors = defValues.Select(x => (Colors.GetColor(x, d)));

                brickDef.VertexColors.SetColors(myColors.ToArray());

                if (item.IndexNodes.Count == 8)
                {
                    brickDef.Faces.AddFace(0, 3, 2, 1);
                    brickDef.Faces.AddFace(4, 5, 6, 7);
                    brickDef.Faces.AddFace(0, 1, 5, 4);
                    brickDef.Faces.AddFace(1, 2, 6, 5);
                    brickDef.Faces.AddFace(2, 3, 7, 6);
                    brickDef.Faces.AddFace(3, 0, 4, 7);
                }
                else
                {
                    brickDef.Faces.AddFace(0, 1, 2);
                    brickDef.Faces.AddFace(0, 1, 3);
                    brickDef.Faces.AddFace(1, 2, 3);
                    brickDef.Faces.AddFace(0, 2, 3);
                }

                brickDefModel.Add(brickDef);
            }

            return brickDefModel;
        }


        //Constructor
        public Model()
        {

        }

        public Model(List<IElement> elements, List<Support> supports, List<ILoad> loads, List<IConstraint> constraints, List<IRecorder> recorders)
        {
            this.Elements = elements;
            this.Supports = supports;
            this.Loads = loads;
            this.Constraint = constraints;
            this.Recorders = recorders;
        }

        public Model ShallowCopy()
        {
            return (Model)this.MemberwiseClone();
        }

        public void GetUniquePoints(List<IBeam> beams, List<IShell> shells, List<IBrick> bricks, List<IConstraint> constraints)
        {
            var threeNdfPoints = new List<Point3d>();
            var sixNdfPoints = new List<Point3d>();

            foreach (var beam in beams)
            {
                var PointAtStart = beam.Curve.PointAtStart;
                var PointAtEnd = beam.Curve.PointAtEnd;
                sixNdfPoints.Add(PointAtStart);
                sixNdfPoints.Add(PointAtEnd);
            }

            foreach (var shell in shells)
            {
                var points = shell.Mesh.Vertices.ToPoint3dArray();
                sixNdfPoints.AddRange(points);

            }

            foreach (var brick in bricks)
            {
                var points = brick.Mesh.Vertices.ToPoint3dArray();
                threeNdfPoints.AddRange(points);
            }

            foreach (var constraint in constraints)
            {
                if(constraint.ConstraintType == Constraints.ConstraintType.RigidDiaphgram)
                {
                    var rigid = (Alpaca4d.Constraints.RigidDiaphragm)constraint;
                    sixNdfPoints.Add((Point3d)rigid.MasterNode);
                    sixNdfPoints.AddRange(rigid.SlaveNodes);
                }
                else if (constraint.ConstraintType == Constraints.ConstraintType.EqualDof)
                {
                    var equalDOF = (Alpaca4d.Constraints.EqualDOF)constraint;
                    sixNdfPoints.Add((Point3d)equalDOF.MasterNode);
                    sixNdfPoints.Add(equalDOF.SlaveNode);
                }
            }

            if (threeNdfPoints.Any())
            {
                this.UniquePointsThreeNDF = Rhino.Geometry.Point3d.CullDuplicates(threeNdfPoints, this.Tollerance).ToList();
                this.CloudPointThreeNDF = new Rhino.Geometry.PointCloud(this.UniquePointsThreeNDF);
                this.RTreeCloudPointThreeNDF = Rhino.Geometry.RTree.CreateFromPointArray(this.UniquePointsThreeNDF);
            }

            if (sixNdfPoints.Any())
            {
                this.UniquePointsSixNDF = Rhino.Geometry.Point3d.CullDuplicates(sixNdfPoints, this.Tollerance).ToList();
                this.CloudPointSixNDF = new Rhino.Geometry.PointCloud(this.UniquePointsSixNDF);
                this.RTreeCloudPointSixNDF = Rhino.Geometry.RTree.CreateFromPointArray(this.UniquePointsSixNDF);
            }

            if (!this.UniquePointsThreeNDF.Any())
                this.UniquePoints = this.UniquePointsSixNDF;
            else if (!this.UniquePointsSixNDF.Any())
            {
                this.UniquePoints = this.UniquePointsThreeNDF;
            }
            else
            {
                this.UniquePoints = this.UniquePointsThreeNDF.Concat(this.UniquePointsSixNDF).ToList();
            }


        }

        public override string ToString()
        {
            return "<Class Model>";
        }

        public static string Initialise3ndf()
        {
            return "model BasicBuilder -ndm 3 -ndf 3\n";
        }

        public static string Initialise6ndf()
        {
            return "model BasicBuilder -ndm 3 -ndf 6\n";
        }

        public void WriteTcl()
        {
            // write a method to store the text file
            // in a tcl property
        }

        public (string, string) RunOpenSees()
        {
            string openSeesPath = Application.OpenSees;


            Process process = new Process();
            // Configure the process using the StartInfo properties.
            process.StartInfo.FileName = openSeesPath;
            process.StartInfo.Arguments = "\"" + this.FileName + "\"";
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.CreateNoWindow = true;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;
            process.Start();

            string output = process.StandardOutput.ReadToEnd().Trim();
            string error = process.StandardError.ReadToEnd().Trim();
            process.WaitForExit();
            this.IsAnalysed = true;
            return (output, error);
        }

        public void Serialise()
        {
            string filePath = System.IO.Path.GetFullPath(this.FileName);

            if (File.Exists(filePath))
            {
                File.Delete(filePath);
                if(this.Recorders.Count != 0)
                    File.Delete(System.IO.Path.GetFullPath( this.Recorders.First().FileName));
            }

            using (var file = new StreamWriter(File.Create(filePath)))
            {
                foreach(var line in this.Tcl)
                {
                    file.WriteLine(line);
                }
            }
        }

        private void GetElements()
        {
            foreach (var element in this.Elements)
            {
                if (element.Type == ElementType.Beam)
                {
                    this.Beams.Add((IBeam)element);
                }
                else if (element.Type == ElementType.Shell)
                {
                    this.Shells.Add((IShell)element);
                }
                else if (element.Type == ElementType.Brick)
                    this.Bricks.Add((IBrick)element);
            }
        }

        private void CreateNodes()
        {
            if (this.UniquePointsThreeNDF.Count != 0)
            {
                this.Tcl.Add(Model.Initialise3ndf());
                foreach (var point in this.UniquePointsThreeNDF)
                {
                    var node = new Alpaca4d.Element.Node(point);
                    node.Ndf = 3;
                    node.SetNodeTag(this); // it can accept a list
                    this.Nodes.Add(node);

                    this.Tcl.Add(node.WriteTcl());
                }
            }

            if (this.UniquePointsSixNDF.Count != 0)
            {
                this.Tcl.Add(Model.Initialise6ndf());
                foreach (var point in this.UniquePointsSixNDF)
                {
                    var node = new Alpaca4d.Element.Node(point);
                    node.Ndf = 6;
                    node.SetNodeTag(this);
                    this.Nodes.Add(node);

                    this.Tcl.Add(node.WriteTcl());
                }
            }
        }

        private void CreateSupports()
        {
            Rhino.Geometry.Point3d closestPointInThreeNDF = Rhino.Geometry.Point3d.Origin;
            Rhino.Geometry.Point3d closestPointInSixNDF = Rhino.Geometry.Point3d.Origin;

            //var uniquePoints = this.Supports.Select(x => x.Pos).ToHashSet();

            //if (uniquePoints.Count != this.Supports.Count)
            //{
            //    var diff = this.Supports.Count - uniquePoints.Count;
            //    throw new Exception($"{diff} duplicate support points found!");
            //}


            foreach (var supportNode in this.Supports)
            {
                if (this.UniquePointsThreeNDF.Count != 0)
                {
                    closestPointInThreeNDF = Rhino.Collections.Point3dList.ClosestPointInList(this.UniquePointsThreeNDF, supportNode.Pos);
                    if (supportNode.Pos.DistanceTo(closestPointInThreeNDF) < this.Tollerance)
                    {
                        supportNode.ndf = 3;
                        this.ThreeNdfModel.Add(supportNode);
                        supportNode.SetNodeTag(this);
                    }
                    else
                        throw new Exception($"Support node at location '{supportNode.Pos}' is not part of the model!");
                }

                if (this.UniquePointsSixNDF.Count != 0)
                {
                    closestPointInSixNDF = Rhino.Collections.Point3dList.ClosestPointInList(this.UniquePointsSixNDF, supportNode.Pos);
                    if (supportNode.Pos.DistanceTo(closestPointInSixNDF) <= this.Tollerance)
                    {
                        supportNode.ndf = 6;
                        this.SixNdfModel.Add(supportNode);
                        supportNode.SetNodeTag(this);
                    }
                    else
                        throw new Exception($"Support node at location '{supportNode.Pos}' is not part of the model!");
                }

                this.Tcl.Add(supportNode.WriteTcl());
            }
        }

        private void CreateGravityLoad(Alpaca4d.Loads.Gravity gravityLoad = null)
        {
            double? mass = 0.00;
            foreach (var item in this.Elements)
            {
                if (item.Type == ElementType.Beam)
                {
                    var beam = (IBeam)item;
                    var length = beam.Curve.GetLength();
                    var massDens = beam.Section.Area * beam.Section.Material.Rho;
                    mass += (massDens * length);
                    if (gravityLoad != null)
                    {
                        var gravityPointLoadStart = new Alpaca4d.Loads.PointLoad((int)beam.INode, gravityLoad.GFactor * new Rhino.Geometry.Vector3d(0, 0, (double)-(massDens * length / 2)), new Rhino.Geometry.Vector3d(0, 0, 0), gravityLoad.TimeSeries);
                        var gravityPointLoadEnd = new Alpaca4d.Loads.PointLoad((int)beam.JNode, gravityLoad.GFactor * new Rhino.Geometry.Vector3d(0, 0, (double)-(massDens * length / 2)), new Rhino.Geometry.Vector3d(0, 0, 0), gravityLoad.TimeSeries);

                        gravityPointLoadStart.Ndf = 6;
                        gravityPointLoadEnd.Ndf = 6;
                        gravityPointLoadStart.Pos = this.UniquePoints[(int)beam.INode-1];
                        gravityPointLoadEnd.Pos = this.UniquePoints[(int)beam.JNode-1];
                        this.GravityPointLoad.Add(gravityPointLoadStart);
                        this.GravityPointLoad.Add(gravityPointLoadEnd);
                    }
                }

                if (item.Type == ElementType.Shell)
                {
                    var shell = (IShell)item;

                    double meshArea = Rhino.Geometry.AreaMassProperties.Compute(shell.Mesh).Area;
                    var areaDensity = shell.Section.Thickness * (double)shell.Section.Material.Rho;
                    mass += areaDensity * meshArea;
                    if (gravityLoad != null)
                    {
                        foreach (var index in shell.IndexNodes)
                        {
                            var gravityPointLoad = new Alpaca4d.Loads.PointLoad(index, gravityLoad.GFactor * new Rhino.Geometry.Vector3d(0, 0, -(areaDensity * meshArea / (shell.Mesh.Vertices.Count))), new Rhino.Geometry.Vector3d(0, 0, 0), gravityLoad.TimeSeries);
                            gravityPointLoad.Ndf = 6;
                            gravityPointLoad.Pos = this.UniquePoints[(int)index -1];
                            this.GravityPointLoad.Add(gravityPointLoad);

                        }
                    }
                    //if item.CrossSection.__class__.__name__ != "LayeredShell":
                    //    areaDensity = item.CrossSection.thickness * item.CrossSection.material.rho
                    //    Mass += areaDensity * meshArea
                    //    if IsGravity:
                    //        for vertex in item.Mesh.Vertices.ToPoint3dArray():
                    //            gravityPointLoad = alpaca.PointLoad(vertex, g_factor * rg.Vector3d(0, 0, -(areaDensity * meshArea / len(item.Mesh.Vertices))) * GravityLoad.GravityFactor, rg.Vector3d(0, 0, 0), GravityLoad.TimeSeries)
                    //            AlpacaModel.loads.append(gravityPointLoad)
                    //else:
                    //    for thickness, material in zip(item.CrossSection.thickness, item.CrossSection.material):
                    //        areaDensity = thickness * material.rho
                    //        Mass += areaDensity * meshArea
                    //        if IsGravity:
                    //            for vertex in item.Mesh.Vertices.ToPoint3dArray():
                    //                gravityPointLoad = alpaca.PointLoad(vertex, g_factor * rg.Vector3d(0, 0, -(areaDensity * meshArea / len(item.Mesh.Vertices))) * GravityLoad.GravityFactor, rg.Vector3d(0, 0, 0), GravityLoad.TimeSeries)
                    //                AlpacaModel.loads.append(gravityPointLoad)
                }

                if (item.Type == ElementType.Brick)
                {
                    var brick = (IBrick)item;
                    var meshVolume = Rhino.Geometry.VolumeMassProperties.Compute(brick.Mesh).Volume;
                    var density = (double)brick.Material.Rho;
                    mass += density * meshVolume;
                    if (gravityLoad != null)
                    {
                        foreach (var index in brick.IndexNodes)
                        {
                            var gravityPointLoad = new Alpaca4d.Loads.PointLoad(index, gravityLoad.GFactor * new Rhino.Geometry.Vector3d(0, 0, -(density * meshVolume / (brick.Mesh.Vertices.Count))), new Rhino.Geometry.Vector3d(0, 0, 0), gravityLoad.TimeSeries);
                            gravityPointLoad.Ndf = 3;
                            gravityPointLoad.Pos = this.UniquePoints[(int)index -1];
                            this.GravityPointLoad.Add(gravityPointLoad);

                        }
                    }
                }
            }
        }

        public void Assemble()
        {
            this.GetElements();
            
            this.GetUniquePoints(this.Beams, this.Shells, this.Bricks, this.Constraint);

            this.CreateNodes();

            this.CreateSupports();

            //////////////////
            // Create Constraint
            //////////////////
            foreach (var constraint in this.Constraint)
            {
                constraint.SetTopologyRTree(this);
            }

            // create equalDOF when the model has 3df and 6df together
            // TODO

            var Id = new List<int>();
            var IdB = new List<int>();

            void SearchCallback(object sender, RTreeEventArgs e)
            {
                Id.Add(e.Id);
                IdB.Add(e.IdB);
            }


            var lenThreeNDF = this.UniquePointsThreeNDF.Count;
            var lenSixNDF = this.UniquePointsSixNDF.Count;

            if(lenThreeNDF != 0 && lenSixNDF != 0)
            {
                Console.WriteLine("brick and beam together");
                Rhino.Geometry.RTree.SearchOverlaps(this.RTreeCloudPointThreeNDF, this.RTreeCloudPointSixNDF, this.Tollerance, SearchCallback);

                int i = 0;
                for(i = 0; i < Id.Count; i++)
                {
                    Console.WriteLine($"{Id[i]} {IdB[i]}");
                    var node_i = this.UniquePointsThreeNDF[Id[i]];
                    var node_j = this.UniquePointsSixNDF[IdB[i]];

                    var equalConstraint = new Alpaca4d.Constraints.EqualDOF(node_i, node_j, true, true, true, false, false, false);
                    equalConstraint.MasterNodeId = this.CloudPointThreeNDF.ClosestPoint(node_i) + 1;
                    equalConstraint.SlaveNodeId = this.CloudPointSixNDF.ClosestPoint(node_j) + 1 + (this.UniquePointsThreeNDF.Count);
                    this.Tcl.Add(equalConstraint.WriteTcl());
                }
            }



            var crossSections = new List<ISection>();
            var materials = new List<IMaterial>();


            foreach (var item in this.Elements)
            {
                if (item.Type == ElementType.Beam)
                {
                    crossSections.Add(((IBeam)item).Section);
                    materials.Add(((IBeam)item).Section.Material);
                }
                else if (item.Type == ElementType.Shell)
                {
                    crossSections.Add(((IShell)item).Section);
                    materials.Add(((IShell)item).Section.Material);
                }
                else
                    materials.Add(((IBrick)item).Material);
            }


            var uniqueSections = crossSections.Distinct().ToList();
            var uniqueMaterials = materials.Distinct().ToList();

            int index = 1;
            foreach (var material in uniqueMaterials)
            {
                material.Id = index;
                index++;
                this.Tcl.Add(material.WriteTcl());
            }

            index = 1;
            foreach (var section in uniqueSections)
            {
                section.Id = index;
                index++;
                this.Tcl.Add(section.WriteTcl());
            }

            // assign tag and node Index to element and shell
            index = 1;
            foreach(var element in this.Elements)
            {
                element.SetTopologyRTree(this);
                element.Id = index;
                element.SetTags();
                index++;
            }

            foreach(var item in this.Elements)
            {
                this.Tcl.Add(item.WriteTcl());
            }


            foreach(var item in this.Constraint)
            {
                this.Tcl.Add(item.WriteTcl());
            }

            /////////
            /// Loads
            /////////
            var myLoads = new List<ILoad>();

            foreach (var item in this.Loads)
            {
                if (item.Type == Alpaca4d.Loads.LoadType.Gravity)
                {
                    // Gravity Load will be use later to calculate the equivalent Gravity Load
                    this.CreateGravityLoad( (Alpaca4d.Loads.Gravity)item );
                }
                else if (item.Type == Alpaca4d.Loads.LoadType.PointLoad)
                {
                    myLoads.Add((Loads.PointLoad)item);
                }
                else if (item.Type == Alpaca4d.Loads.LoadType.DistributedLoad)
                {
                    var lineLoad = (Alpaca4d.Loads.LineLoad)item;
                    // Assign the load to all the elements if the user does not specify the elements.
                    if(lineLoad.Element == null)
                    {
                        foreach(var beam in this.Beams)
                        {
                            lineLoad = new Alpaca4d.Loads.LineLoad(beam, lineLoad.GlobalForce, lineLoad.TimeSeries);
                            myLoads.Add(lineLoad);
                        }
                    }
                    else
                        myLoads.Add(lineLoad);
                }
                else if (item.Type == Alpaca4d.Loads.LoadType.MeshLoad)
                {
                    var meshLoad = (Alpaca4d.Loads.MeshLoad)item;
                    // Assign the load to all the elements if the user does not specify the elements.
                    if (meshLoad.Element == null)
                    {
                        foreach (var mesh in this.Shells)
                        {
                            meshLoad = new Alpaca4d.Loads.MeshLoad(mesh, meshLoad.GlobalForce, meshLoad.TimeSeries);
                            myLoads.Add(meshLoad);
                        }
                    }
                    else
                        myLoads.Add(meshLoad);
                }
                else if (item.Type == Alpaca4d.Loads.LoadType.Mass)
                    this.Mass.Add((Loads.MassLoad)item);
                else if (item.Type == Alpaca4d.Loads.LoadType.UniformExcitation)
                    continue;
                else
                    throw new Exception("Type of Load not found");
            }


            foreach (var item in this.Mass)
            {
                item.SetTag(this);
                this.Tcl.Add(item.WriteTcl());
            }

            foreach (var item in myLoads)
            {
                if (item.Type == Alpaca4d.Loads.LoadType.PointLoad || item.Type == Alpaca4d.Loads.LoadType.DistributedLoad || item.Type == Alpaca4d.Loads.LoadType.MeshLoad)
                {
                    item.SetTag(this);
                }
            }


            // Group by TimeSeries
            var totalLoads = myLoads.Concat(this.GravityPointLoad);

            var timeSeriesGroup = totalLoads.GroupBy(s => s.TimeSeries);

            foreach(var group in timeSeriesGroup)
            {
                var timeSeries = group.Key;
                if (timeSeries == null) { continue; }
                timeSeries.Id = index;
                var loadPattern = new Alpaca4d.Loads.LoadPattern(Alpaca4d.Loads.PatternType.Plain, timeSeries, group.ToList());
                this.Tcl.Add(loadPattern.WriteTcl());
            }


            #region UNIFORM EXCITATION
            var uniformExcitationLoads = this.Loads.OfType<Alpaca4d.Loads.UniformExcitation>().ToList();

            if (uniformExcitationLoads.Count > 1)
            {
                throw new Exception("Only one UniformExcitation is allowed!");
            }
            else if (uniformExcitationLoads.Count == 1)
            {
                var uniformExcitation = uniformExcitationLoads.FirstOrDefault();
                uniformExcitation.TimeSeries.Id = index;

                this.Tcl.Add(uniformExcitation.TimeSeries.WriteTcl());
                this.Tcl.Add(uniformExcitation.WriteTcl());
            }
            #endregion


        }
    }
}