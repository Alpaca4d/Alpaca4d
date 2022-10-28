using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel;
using System.Text.RegularExpressions;

using System.Drawing;
using Rhino.Geometry;
using Grasshopper;
using Grasshopper.Kernel.Data;


namespace Alpaca4d
{
    public class Utils
    {
        public static Plane AlignPlane(Plane plane, Vector3d vector)
        {
            double s;
            double t;
            plane.ClosestParameter(plane.Origin + vector, out s, out t);
            double num = Math.Atan2(s, t);
            plane.Rotate(-num + 1.5707963267948966, plane.ZAxis, plane.Origin);
            return plane;
        }
        public static List<int> RTreeSearch(Rhino.Geometry.RTree RTree, List<Point3d> searchPoint, double tol)
        {
            var closestIndexes = new List<int>();

            foreach (var item in searchPoint)
            {
                RTree.Search(new Sphere(item, tol), SearchCallback);
            }

            void SearchCallback(object sender, RTreeEventArgs e)
            {
                closestIndexes.Add(e.Id);
            }

            return closestIndexes;
        }
        public static DataTree<object> DataTreeFromNestedList(List<List<double>> nestedList)
        {
            GH_Path path;
            var tree = new DataTree<object>();

            for (int i = 0; i < nestedList.Count; i++)
            {
                var array = (List<double>)nestedList[i];
                for (int j = 0; j < array.Count; j++)
                {
                    path = new GH_Path(i);
                    tree.Add(array[j], new GH_Path(path));
                }
            }

            return tree;
        }
        public static DataTree<object> DataTreeFromNestedList(List<List<double>> nestedList, List<int?> indexes)
        {
            GH_Path path;
            var tree = new DataTree<object>();

            for (int i = 0; i < nestedList.Count; i++)
            {
                var array = (List<double>)nestedList[i];
                for (int j = 0; j < array.Count; j++)
                {
                    path = new GH_Path((int)indexes[i]);
                    tree.Add(array[j], new GH_Path(path));
                }
            }

            return tree;
        }
        public static DataTree<object> DataTreeFromNestedList(List<List<string>> nestedList)
        {
            GH_Path path;
            var tree = new DataTree<object>();

            for (int i = 0; i < nestedList.Count; i++)
            {
                var array = (List<string>)nestedList[i];
                for (int j = 0; j < array.Count; j++)
                {
                    path = new GH_Path(i);
                    tree.Add(array[j], new GH_Path(path));
                }
            }

            return tree;
        }
        public static List<Mesh> ExplodeMesh(Mesh mesh)
        {
            List<Mesh> list = new List<Mesh>(mesh.Faces.Count);
            for (int i = 0; i < mesh.Faces.Count; i++)
            {
                Mesh mesh2 = new Mesh();
                List<Color> list2 = new List<Color>();
                int a = mesh.Faces.GetFace(i).A;
                int b = mesh.Faces.GetFace(i).B;
                int c = mesh.Faces.GetFace(i).C;
                mesh2.Vertices.Add(mesh.Vertices.ElementAt(a));
                mesh2.Vertices.Add(mesh.Vertices.ElementAt(b));
                mesh2.Vertices.Add(mesh.Vertices.ElementAt(c));
                if (mesh.VertexColors.Count != 0)
                {
                    list2.Add(mesh.VertexColors.ElementAt(a));
                    list2.Add(mesh.VertexColors.ElementAt(b));
                    list2.Add(mesh.VertexColors.ElementAt(c));
                }
                if (mesh.Faces.GetFace(i).IsTriangle)
                {
                    mesh2.Faces.AddFace(0, 1, 2);
                }
                else
                {
                    int d = mesh.Faces.GetFace(i).D;
                    mesh2.Vertices.Add(mesh.Vertices.ElementAt(d));
                    if (mesh.VertexColors.Count != 0)
                    {
                        list2.Add(mesh.VertexColors.ElementAt(d));
                    }
                    mesh2.Faces.AddFace(0, 1, 2, 3);
                }
                if (mesh.VertexColors.Count != 0)
                {
                    mesh2.VertexColors.AppendColors(list2.ToArray());
                }
                list.Add(mesh2);
            }
            return list;
        }
        public static Plane PerpendicularFrame(Curve Curve)
        {
            double min = Curve.Domain.Min;
            double max = Curve.Domain.Max;
            double value = 0.5 * (min + max);

            double[] array = new double[2];
            if (value <= min + 1E-12)
            {
                array[0] = value;
                array[1] = 0.5 * (min + max);
            }
            else
            {
                array[0] = min;
                array[1] = value;
            }
            Plane[] perpendicularFrames = Curve.GetPerpendicularFrames(array);

            if (value <= min + 1E-12)
            {
                return perpendicularFrames[0];
            }
            return perpendicularFrames[1];
        }
        public static Mesh CreateLoft(IList<Polyline> polylines)
        {
            if (Enumerable.All(polylines, p => p.IsClosed))
                return CreateLoftClosed(polylines);
            else
                return CreateLoftOpen(polylines);
        }
        private static Mesh CreateLoftOpen(IList<Polyline> polylines)
        {
            Mesh result = new Mesh();
            var verts = result.Vertices;
            var faces = result.Faces;

            int ny = polylines.Count;
            int nx = Enumerable.Min(polylines, p => p.Count);
            int n;

            // add vertices
            for (int i = 0; i < ny; i++)
            {
                var poly = polylines[i];

                for (int j = 0; j < nx; j++)
                    verts.Add(poly[j]);
            }

            // add faces
            for (int i = 0; i < ny - 1; i++)
            {
                n = i * nx;

                for (int j = 0; j < nx - 1; j++)
                    faces.AddFace(n + j, n + j + 1, n + j + nx + 1, n + j + nx);
            }

            return result;
        }
        private static Mesh CreateLoftClosed(IList<Polyline> polylines)
        {
            Mesh result = new Mesh();
            var verts = result.Vertices;
            var faces = result.Faces;

            int ny = polylines.Count;
            int nx = Enumerable.Min(polylines, p => p.Count) - 1;
            int n;

            // add vertices
            for (int i = 0; i < ny; i++)
            {
                var poly = polylines[i];

                for (int j = 0; j < nx; j++)
                    verts.Add(poly[j]);
            }

            // add faces
            for (int i = 0; i < ny - 1; i++)
            {
                n = i * nx;

                for (int j0 = 0; j0 < nx; j0++)
                {
                    int j1 = (j0 + 1) % nx;
                    faces.AddFace(n + j0, n + j1, n + j1 + nx, n + j0 + nx);
                }
            }

            return result;
        }



        public static Mesh CreateLoft(IList<Polyline> polylines, List<double> deformation = null, List<Color> iColors = null, double? min = null, double? max = null)
        {
            if (Enumerable.All(polylines, p => p.IsClosed))
                return CreateLoftClosed(polylines, deformation, iColors, min, max);
            else
                return CreateLoftOpen(polylines, deformation, iColors, min, max);
        }
        private static Mesh CreateLoftClosed(IList<Polyline> polylines, List<double> deformation, List<Color> iColors, double? min, double? max)
        {
            // find the total range of displacement

            var d = new SortedDictionary<double, System.Drawing.Color>();

            var numberOfColors = iColors.Count;

            var diff = (max - min) / (numberOfColors - 1);

            var start = min;
            foreach (var color in iColors)
            {
                d.Add((double)start, color);
                start += diff;
            }


            Mesh result = new Mesh();
            var verts = result.Vertices;
            var faces = result.Faces;
            var clrs = result.VertexColors;

            int ny = polylines.Count;
            int nx = Enumerable.Min(polylines, p => p.Count) - 1;
            int n;

            // add vertices
            for (int i = 0; i < ny; i++)
            {
                var poly = polylines[i];

                for (int j = 0; j < nx; j++)
                {
                    verts.Add(poly[j]);
                    var clr = Alpaca4d.Colors.GetColor(deformation[i], d);
                    clrs.Add(clr);
                }
            }

            // add faces
            for (int i = 0; i < ny - 1; i++)
            {
                n = i * nx;

                for (int j0 = 0; j0 < nx; j0++)
                {
                    int j1 = (j0 + 1) % nx;
                    faces.AddFace(n + j0, n + j1, n + j1 + nx, n + j0 + nx);
                }
            }

            return result;
        }
        private static Mesh CreateLoftOpen(IList<Polyline> polylines, List<double> deformation, List<Color> iColors, double? min, double? max)
        {

            var d = new SortedDictionary<double, System.Drawing.Color>();

            var numberOfColors = iColors.Count;
            var range = max - max;
            var diff = (max - min) / (numberOfColors - 1);

            var start = min;
            foreach (var color in iColors)
            {
                d.Add((double)start, color);
                start += diff;
            }

            Mesh result = new Mesh();
            var verts = result.Vertices;
            var faces = result.Faces;
            var clrs = result.VertexColors;

            int ny = polylines.Count;
            int nx = Enumerable.Min(polylines, p => p.Count);
            int n;

            // add vertices
            for (int i = 0; i < ny; i++)
            {
                var poly = polylines[i];

                for (int j = 0; j < nx; j++)
                {
                    verts.Add(poly[j]);
                    var clr = Alpaca4d.Colors.GetColor(deformation[i], d);
                    clrs.Add(clr);
                }
            }

            // add faces
            for (int i = 0; i < ny - 1; i++)
            {
                n = i * nx;

                for (int j = 0; j < nx - 1; j++)
                    faces.AddFace(n + j, n + j + 1, n + j + nx + 1, n + j + nx);
            }

            return result;
        }

        private static List<Mesh> MeshToShell(Mesh mesh)
        {
            mesh.Unweld(0, true);
            var myMesh = mesh.ExplodeAtUnweldedEdges();

            var newMeshes = new List<Mesh>();
            foreach(var explodedMesh in myMesh)
            {
                newMeshes.Add(explodedMesh);
            }
            return newMeshes;
        }
        public static List<Mesh> MeshSeriesToBrick(List<Mesh> MeshList)
        {
            var meshExpl = new List<List<Mesh>>();
            var solid = new List<Mesh>();

            var a = MeshList[0].DuplicateMesh();


            a.Unweld(0, true);
            var b = a.ExplodeAtUnweldedEdges();
            if(b.Count() > 0)
            {
                foreach(var Mesh in MeshList)
                {
                    var shellWrapper = MeshToShell(Mesh);
                    meshExpl.Add(shellWrapper);
                }

                for(int index1 = 0; index1 < MeshList.Count()-1; index1++)
                {
                    for (int index2 = 0; index2 < meshExpl[0].Count(); index2++)
                    {
                        if(meshExpl[index1][index2].Vertices.Count == 4)
                        {
                            var vertix1 = meshExpl[index1][index2].Vertices[0];
                            var vertix2 = meshExpl[index1][index2].Vertices[1];
                            var vertix3 = meshExpl[index1][index2].Vertices[2];
                            var vertix4 = meshExpl[index1][index2].Vertices[3];
                            var vertix5 = meshExpl[index1 + 1][index2].Vertices[0];
                            var vertix6 = meshExpl[index1 + 1][index2].Vertices[1];
                            var vertix7 = meshExpl[index1 + 1][index2].Vertices[2];
                            var vertix8 = meshExpl[index1 + 1][index2].Vertices[3];


                            var ele = new Rhino.Geometry.Mesh();

                            ele.Vertices.Add(vertix1);
                            ele.Vertices.Add(vertix2);
                            ele.Vertices.Add(vertix3);
                            ele.Vertices.Add(vertix4);
                            ele.Vertices.Add(vertix5);
                            ele.Vertices.Add(vertix6);
                            ele.Vertices.Add(vertix7);
                            ele.Vertices.Add(vertix8);

                            ele.Faces.AddFace(0, 1, 2, 3);
                            ele.Faces.AddFace(4, 5, 6, 7);
                            ele.Faces.AddFace(0, 1, 5, 4);
                            ele.Faces.AddFace(3, 2, 6, 7);
                            ele.Faces.AddFace(1, 5, 6, 2);
                            ele.Faces.AddFace(0, 4, 7, 3);
                            solid.Add(ele);

                        }
                    }
                }
            }
            else
            {
                for (int index1 = 0; index1 < MeshList.Count() - 1; index1++)
                {
                    var vertix1 = MeshList[index1].Vertices[0];
                    var vertix2 = MeshList[index1].Vertices[1];
                    var vertix3 = MeshList[index1].Vertices[2];
                    var vertix4 = MeshList[index1].Vertices[3];
                    var vertix5 = MeshList[index1 + 1].Vertices[0];
                    var vertix6 = MeshList[index1 + 1].Vertices[1];
                    var vertix7 = MeshList[index1 + 1].Vertices[2];
                    var vertix8 = MeshList[index1 + 1].Vertices[3];

                    var ele = new Rhino.Geometry.Mesh();

                    ele.Vertices.Add(vertix1);
                    ele.Vertices.Add(vertix2);
                    ele.Vertices.Add(vertix3);
                    ele.Vertices.Add(vertix4);
                    ele.Vertices.Add(vertix5);
                    ele.Vertices.Add(vertix6);
                    ele.Vertices.Add(vertix7);
                    ele.Vertices.Add(vertix8);

                    ele.Faces.AddFace(0, 1, 2, 3);
                    ele.Faces.AddFace(4, 5, 6, 7);
                    ele.Faces.AddFace(0, 1, 5, 4);
                    ele.Faces.AddFace(3, 2, 6, 7);
                    ele.Faces.AddFace(1, 5, 6, 2);
                    ele.Faces.AddFace(0, 4, 7, 3);

                    solid.Add(ele);
                }
            }
            return solid;
        }
        public static Vector3d PlaceCoordinates(Point3d point, Plane localPlane)
        {
            localPlane.ClosestParameter(point, out double s, out double t);
            double w = localPlane.DistanceTo(point);
            return new Vector3d(-1.0 * w, t, s);
        }
        public static (List<Point3d> points, List<Point3d> supports, List<Curve> beamCurves, List<Mesh> shellMeshes, List<Mesh> brickMeshes) TextToGeometry(string filepath)
        {
            var lines = System.IO.File.ReadAllLines(filepath);
            (var points, var supports, var lineGeometry, var meshShell, var meshBrick) = Utils.TextToGeometry(lines.ToList());
            
            return (points, supports, lineGeometry, meshShell, meshBrick);
        }

        public static (List<Point3d> points, List<Point3d> supports, List<Curve> beamCurves, List<Mesh> shellMeshes, List<Mesh> brickMeshes) TextToGeometry(List<string> lines)
        {
            Model model = new Model();

            var splittedLines = lines.Select(x => x.Split(new char[] { ' ', '\t', '\n' }, StringSplitOptions.RemoveEmptyEntries)).ToList();


            var monoDimensionalObject = new List<string> { "truss", "corotTruss", "elasticBeamColumn", "ElasticTimoshenkoBeam", "dispBeamColumn", "forceBeamColumn", "twoNodeLink" };
            var biDimensionalObject = new List<string> { "ShellMITC4", "ASDShellQ4", "ShellDKGQ", "ShellNLDKGQ" };
            var triDimensionalObject = new List<string> { "SSPbrick", "stdBrick", "FourNodeTetrahedron" };

            var nodeDictionary = new Dictionary<int, Alpaca4d.Element.Node>();
            var supportDictionary = new Dictionary<int, Alpaca4d.Element.Support>();
            var stickDictionary = new Dictionary<int, Curve>();
            var shellGeometryDictionary = new Dictionary<int, Mesh>();
            var brickGeometryDictionary = new Dictionary<int, Mesh>();

            foreach (var line in splittedLines)
            {
                // create only Node, Material, Section and Geometric Transformation
                if (Regex.IsMatch(line[0], "node"))
                {
                    int index = int.Parse(line[1]);
                    double x = double.Parse(line[2]);
                    double y = double.Parse(line[3]);
                    double z = double.Parse(line[4]);

                    var node = new Alpaca4d.Element.Node(index, x, y, z);
                    nodeDictionary.Add(index, node);
                }
            }

            foreach (var line in splittedLines)
            {
                if (Regex.IsMatch(line[0], "fix"))
                {
                    var index = int.Parse(line[1]);

                    if (line.Length == 8)
                    {
                        var x = Convert.ToBoolean(int.Parse(line[2]));
                        var y = Convert.ToBoolean(int.Parse(line[3]));
                        var z = Convert.ToBoolean(int.Parse(line[4]));
                        var xx = Convert.ToBoolean(int.Parse(line[5]));
                        var yy = Convert.ToBoolean(int.Parse(line[6]));
                        var zz = Convert.ToBoolean(int.Parse(line[7]));
                        var supportNode = nodeDictionary[index];
                        var support = new Alpaca4d.Element.Support(supportNode.Pos, x, y, z, xx, yy, zz);
                        support.ndf = 6;

                        supportDictionary.Add(index, support);
                    }
                    else if (line.Length == 5)
                    {
                        var x = Convert.ToBoolean(int.Parse(line[2]));
                        var y = Convert.ToBoolean(int.Parse(line[3]));
                        var z = Convert.ToBoolean(int.Parse(line[4]));
                        var supportNode = nodeDictionary[index];
                        var support = new Alpaca4d.Element.Support(supportNode.Pos, x, y, z, false, false, false);
                        support.ndf = 3; // it is require because WriteTcl read the ndf to correctly serialise

                        supportDictionary.Add(index, support);
                    }
                    else
                    {
                        throw new Exception("Support element is not ndf 3 or 6!");
                    }
                }
                else if (Regex.IsMatch(line[0], "element"))
                {
                    if (monoDimensionalObject.Contains(line[1]))
                    {
                        var index = int.Parse(line[2]);
                        var startIndex = int.Parse(line[3]);
                        var endIndex = int.Parse(line[4]);

                        var startNode = nodeDictionary[startIndex];
                        var endNode = nodeDictionary[endIndex];
                        var stickElement = new Rhino.Geometry.LineCurve(startNode.Pos, endNode.Pos);
                        stickDictionary.Add(index, stickElement);
                    }
                    if (biDimensionalObject.Contains(line[1]))
                    {
                        if (line[1] == "ASDShellQ4" || line[1] == "ShellMITC4")
                        {
                            var index = int.Parse(line[2]);
                            var nodeId_0 = int.Parse(line[3]);
                            var nodeId_1 = int.Parse(line[4]);
                            var nodeId_2 = int.Parse(line[5]);
                            var nodeId_3 = int.Parse(line[6]);
                            var nodeId = new List<int> { nodeId_0, nodeId_1, nodeId_2, nodeId_3 };
                            var flatMesh = new Rhino.Geometry.Mesh();
                            foreach (var id in nodeId)
                                flatMesh.Vertices.Add(nodeDictionary[id].Pos);
                            flatMesh.Faces.AddFace(0, 1, 2, 3);
                            shellGeometryDictionary.Add(index, flatMesh);
                        }
                        else if (line[1] == "ShellNLDKGQ" || line[1] == "ShellDKGQ")
                        {
                            var index = int.Parse(line[2]);
                            var nodeId_0 = int.Parse(line[3]);
                            var nodeId_1 = int.Parse(line[4]);
                            var nodeId_2 = int.Parse(line[5]);
                            var nodeId = new List<int> { nodeId_0, nodeId_1, nodeId_2 };
                            var flatMesh = new Rhino.Geometry.Mesh();
                            foreach (var id in nodeId)
                                flatMesh.Vertices.Add(nodeDictionary[id].Pos);
                            flatMesh.Faces.AddFace(0, 1, 2);
                            shellGeometryDictionary.Add(index, flatMesh);
                        }
                    }
                    if (triDimensionalObject.Contains(line[1]))
                    {
                        if (line[1] == "FourNodeTetrahedron")
                        {
                            var index = int.Parse(line[2]);
                            var nodeId_0 = int.Parse(line[3]);
                            var nodeId_1 = int.Parse(line[4]);
                            var nodeId_2 = int.Parse(line[5]);
                            var nodeId_3 = int.Parse(line[6]);
                            var nodeId = new List<int> { nodeId_0, nodeId_1, nodeId_2, nodeId_3 };
                            var solidMesh = new Rhino.Geometry.Mesh();
                            foreach (var id in nodeId)
                                solidMesh.Vertices.Add(nodeDictionary[id].Pos);
                            solidMesh.Faces.AddFace(0, 1, 2);
                            solidMesh.Faces.AddFace(1, 3, 2);
                            solidMesh.Faces.AddFace(0, 2, 3);
                            solidMesh.Faces.AddFace(0, 3, 2);
                            brickGeometryDictionary.Add(index, solidMesh);
                        }
                        else if (line[1] == "SSPbrick" || line[1] == "stdBrick")
                        {
                            var index = int.Parse(line[2]);
                            var nodeId_0 = int.Parse(line[3]);
                            var nodeId_1 = int.Parse(line[4]);
                            var nodeId_2 = int.Parse(line[5]);
                            var nodeId_3 = int.Parse(line[6]);
                            var nodeId_4 = int.Parse(line[7]);
                            var nodeId_5 = int.Parse(line[8]);
                            var nodeId_6 = int.Parse(line[9]);
                            var nodeId_7 = int.Parse(line[10]);
                            var nodeId = new List<int> { nodeId_0, nodeId_1, nodeId_2, nodeId_3, nodeId_4, nodeId_5, nodeId_6, nodeId_7 };
                            var solidMesh = new Rhino.Geometry.Mesh();
                            foreach (var id in nodeId)
                                solidMesh.Vertices.Add(nodeDictionary[id].Pos);
                            solidMesh.Faces.AddFace(0, 1, 2, 3);
                            solidMesh.Faces.AddFace(4, 5, 6, 7);
                            solidMesh.Faces.AddFace(1, 2, 6, 5);
                            solidMesh.Faces.AddFace(4, 7, 3, 0);
                            solidMesh.Faces.AddFace(0, 1, 5, 4);
                            solidMesh.Faces.AddFace(2, 3, 7, 6);
                            brickGeometryDictionary.Add(index, solidMesh);
                        }
                    }
                }
            }

            var points = nodeDictionary.Values.Select(x => x.Pos).ToList();
            var supports = supportDictionary.Values.Select(x => x.Pos).ToList();
            var lineGeometry = stickDictionary.Values.ToList();
            var meshShell = shellGeometryDictionary.Values.ToList();
            var meshBrick = brickGeometryDictionary.Values.ToList();

            return (points, supports, lineGeometry, meshShell, meshBrick);
        }
    }
}