using System;
using Rhino.Geometry;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Alpaca4d.Generic;

namespace Alpaca4d.Element
{
    public partial class Support : EntityBase, IStructure, ISerialize
    {
        public Point3d Pos { get; set; }
        public bool Tx { get; set; }
        public bool Ty { get; set; }
        public bool Tz { get; set; }
        public bool Rx { get; set; }
        public bool Ry { get; set; }
        public bool Rz { get; set; }
        public int? Id { get; set; }
        public int ndf { get; set; }

        private Plane plane = Plane.WorldXY;

        /// <summary>
        /// The frame Tx/Ty/Tz and Rx/Ry/Rz are read in. Its axes - not the world axes -
        /// are what each restraint refers to, so rotating the plane skews the support.
        /// The origin is the support location, mirrored by <see cref="Pos"/>.
        /// </summary>
        public Plane Plane
        {
            get { return this.plane.IsValid ? this.plane : Plane.WorldXY; }
            set { this.plane = value; }
        }

        /// <summary>
        /// The coincident node that carries the <c>fix</c> of a skewed support, and with
        /// it the reaction. Null while the support restrains global axes and needs no
        /// spring. Assigned by <see cref="Model"/> during assembly.
        /// </summary>
        public int? AuxiliaryNodeId { get; set; }

        /// <summary>Tag of the zeroLength element joining the support node to <see cref="AuxiliaryNodeId"/>.</summary>
        public int? SpringElementId { get; set; }

        /// <summary>Penalty material holding the restrained translations, set during assembly.</summary>
        public Alpaca4d.Material.UniaxialMaterialElastic TranslationSpring { get; set; }

        /// <summary>Penalty material holding the restrained rotations, set during assembly.</summary>
        public Alpaca4d.Material.UniaxialMaterialElastic RotationSpring { get; set; }

        /// <summary>
        /// Two frames count as the same one when their axes agree to this much. Well
        /// inside anything a user can dial in, and far outside the rounding a plane
        /// picks up being passed around Grasshopper.
        /// </summary>
        private const double AxisTolerance = 1e-9;

        /// <summary>
        /// True when the support frame is the world frame, so every restraint lands on a
        /// global degree of freedom and OpenSees' own <c>fix</c> can express it exactly.
        /// </summary>
        public bool IsAxisAligned
        {
            get
            {
                return this.Plane.XAxis.EpsilonEquals(Vector3d.XAxis, AxisTolerance)
                    && this.Plane.YAxis.EpsilonEquals(Vector3d.YAxis, AxisTolerance)
                    && this.Plane.ZAxis.EpsilonEquals(Vector3d.ZAxis, AxisTolerance);
            }
        }

        /// <summary>
        /// The restraints as zeroLength <c>-dir</c> indices: 1-3 translation along the
        /// plane's own axes, 4-6 rotation about them. A 3 ndf node - anything meshed out
        /// of bricks - carries no rotations, so Rx/Ry/Rz are dropped rather than written
        /// as directions the node does not have.
        /// </summary>
        public List<int> RestrainedDirections
        {
            get
            {
                var directions = new List<int>();

                if (this.Tx) directions.Add(1);
                if (this.Ty) directions.Add(2);
                if (this.Tz) directions.Add(3);

                if (this.ndf == 3)
                    return directions;

                if (this.Rx) directions.Add(4);
                if (this.Ry) directions.Add(5);
                if (this.Rz) directions.Add(6);

                return directions;
            }
        }

        /// <summary>True when this support is written as a penalty spring rather than a <c>fix</c>.</summary>
        public bool NeedsSpring
        {
            get { return !this.IsAxisAligned && this.RestrainedDirections.Count != 0; }
        }

        public dynamic Geometry
        {
            get
            {
                var symbol = this.SymbolGeometry;

                if (symbol is Mesh mesh && !this.IsAxisAligned)
                {
                    var oriented = mesh.DuplicateMesh();
                    oriented.Transform(Transform.PlaneToPlane(
                        Plane.WorldXY,
                        new Plane(Point3d.Origin, this.Plane.XAxis, this.Plane.YAxis)));
                    return oriented;
                }

                return symbol;
            }
        }

        private dynamic SymbolGeometry
        {
            get
            {
                if (Tx == true && Ty == true && Tz == true && Rx == true && Ry == true && Rz == true)
                {
                    return Support.Fix;
                }
                else if (Tx == true && Ty == true && Tz == true && Rx == false && Ry == false && Rz == false)
                {
                    return Support.Pinned;
                }
                else if (Tx == false && Ty == true && Tz == true && Rx == true && Ry == true && Rz == true)
                {
                    return Support.TranslateX;
                }
                else if (Tx == true && Ty == false && Tz == true && Rx == true && Ry == true && Rz == true)
                {
                    return Support.TranslateY;
                }
                else if (Tx == true && Ty == true && Tz == false && Rx == true && Ry == true && Rz == true)
                {
                    return Support.TranslateZ;
                }
                else if (Tx == true && Ty == true && Tz == true && Rx == false && Ry == true && Rz == true)
                {
                    return Support.RotateX;
                }
                else if (Tx == true && Ty == true && Tz == true && Rx == true && Ry == false && Rz == true)
                {
                    return Support.RotateY;
                }
                else if (Tx == true && Ty == true && Tz == true && Rx == true && Ry == true && Rz == false)
                {
                    return Support.RotateZ;
                }
                else
                {
                    var tx = this.Tx == true ? "x" : "";
                    var ty = this.Ty == true ? "y" : "";
                    var tz = this.Tz == true ? "z" : "";
                    var rx = this.Rx == true ? "xx" : "";
                    var ry = this.Ry == true ? "yy" : "";
                    var rz = this.Rz == true ? "zz" : "";
                    return $"{tx}{ty}{tz}-{rx}{ry}{rz}";
                }
            }
        }
        public Support(Point3d node, bool tx, bool ty, bool tz, bool rx, bool ry, bool rz)
            : this(new Plane(node, Vector3d.XAxis, Vector3d.YAxis), tx, ty, tz, rx, ry, rz)
        {
        }

        public Support(Plane frame, bool tx, bool ty, bool tz, bool rx, bool ry, bool rz)
        {
            this.Plane = frame;
            this.Pos = frame.Origin;
            this.Tx = tx;
            this.Ty = ty;
            this.Tz = tz;
            this.Rx = rx;
            this.Ry = ry;
            this.Rz = rz;
        }

        public Support(int index, bool tx, bool ty, bool tz, bool rx, bool ry, bool rz)
        {
            this.Id = index;
            this.Tx = tx;
            this.Ty = ty;
            this.Tz = tz;
            this.Rx = rx;
            this.Ry = ry;
            this.Rz = rz;
        }

        public override string WriteTcl()
        {
            // A support the model has not seen yet - the one a Grasshopper panel prints
            // straight off the component - has no node to name. Show it the way it always
            // has been shown rather than failing on a preview.
            if (this.ndf == 0 && this.Id == null)
                return this.WriteFixTcl(6);

            if (this.ndf != 3 && this.ndf != 6)
                throw new Exception($"The support at location {this.Pos.ToString()} is not part of the mdodel");

            return this.NeedsSpring ? this.WriteSpringTcl() : this.WriteFixTcl(this.ndf);
        }

        /// <summary>
        /// An axis-aligned support, written the way OpenSees means it: a single point
        /// constraint on global degrees of freedom, exact and free of any penalty.
        /// </summary>
        private string WriteFixTcl(int dofCount)
        {
            var translations = $"{Convert.ToInt16(this.Tx)} {Convert.ToInt16(this.Ty)} {Convert.ToInt16(this.Tz)}";

            if (dofCount == 3)
                return $"fix {this.Id} {translations}\n";

            return $"fix {this.Id} {translations} {Convert.ToInt16(this.Rx)} {Convert.ToInt16(this.Ry)} {Convert.ToInt16(this.Rz)}\n";
        }

        /// <summary>
        /// A skewed support. OpenSees has no notion of a nodal coordinate system - `fix`
        /// only ever speaks global degrees of freedom - so the restraint is carried by a
        /// zeroLength element between the support node and a coincident node that is
        /// fixed outright. `-orient` hands that element the support plane, and from then
        /// on its `-dir` indices count along the plane's own axes: 1-3 translation, 4-6
        /// rotation. Directions left out of `-dir` carry no stiffness at all, so a
        /// release along a local axis is exact; only the restrained ones are a penalty.
        ///
        /// The reaction ends up on the auxiliary node, in global components, because that
        /// is where the point constraint lives - see the reaction reader.
        /// </summary>
        private string WriteSpringTcl()
        {
            var directions = this.RestrainedDirections;
            var materials = directions.Select(direction =>
                direction <= 3 ? this.TranslationSpring.Id : this.RotationSpring.Id);

            var x = this.Plane.XAxis;
            var y = this.Plane.YAxis;

            var tcl = new StringBuilder();

            if (directions.Any(direction => direction <= 3))
                tcl.Append(this.TranslationSpring.WriteTcl());
            if (directions.Any(direction => direction > 3))
                tcl.Append(this.RotationSpring.WriteTcl());

            tcl.Append($"node {this.AuxiliaryNodeId} {this.Pos.X} {this.Pos.Y} {this.Pos.Z}\n");
            tcl.Append(this.ndf == 3
                ? $"fix {this.AuxiliaryNodeId} 1 1 1\n"
                : $"fix {this.AuxiliaryNodeId} 1 1 1 1 1 1\n");
            tcl.Append($"element zeroLength {this.SpringElementId} {this.AuxiliaryNodeId} {this.Id}" +
                       $" -mat {string.Join(" ", materials)}" +
                       $" -dir {string.Join(" ", directions)}" +
                       $" -orient {x.X} {x.Y} {x.Z} {y.X} {y.Y} {y.Z}\n");

            return tcl.ToString();
        }
        public void SetNodeTag(Model model)
        {
            if(this.ndf == 3)
            {
                this.Id = model.CloudPointThreeNDF.ClosestPoint(this.Pos) + 1;
            }
            else // ndf == 6
            {
                this.Id = model.CloudPointSixNDF.ClosestPoint(this.Pos) + 1 + model.UniquePointsThreeNDF.Count();
            }
        }
        private static Mesh Fix
        {
            get
            {
                var radius = 0.25;
                var gondenRatio = 1.61803398875;
                var boxLength = radius * 2 * gondenRatio;

                var bbox = new Rhino.Geometry.BoundingBox(-boxLength / 2, -boxLength / 2, -boxLength / 2, boxLength / 2, boxLength / 2, boxLength / 2);
                bbox.Transform(Transform.Translation(new Vector3d(0, 0, -boxLength / 2)));
                var fixSupport = Rhino.Geometry.Mesh.CreateFromBox(bbox, 1, 1, 1);
                return fixSupport;
            }
        }
        private static Mesh Pinned
        {
            get
            {
                var radius = 0.25;
                var pinnedMesh = new Rhino.Geometry.Mesh();

                // Create Sphere
                var center = new Rhino.Geometry.Point3d(0, 0, 0);
                var sphere = new Rhino.Geometry.Sphere(center, radius);
                var icoSphere = Rhino.Geometry.Mesh.CreateQuadSphere(sphere, 2);
                icoSphere.Transform(Transform.Translation(new Vector3d(0, 0, -radius)));

                // Create Box
                var fix = Support.Fix.DuplicateMesh();
                fix.Transform(Transform.Translation(new Vector3d(0, 0, -radius/1.2)));

                // Collect Geometries
                pinnedMesh.Append(icoSphere);
                pinnedMesh.Append(fix);

                return pinnedMesh;
            }
        }
        private static Mesh Translate
        {
            get
            {
                var radius = 0.25;
                var gondenRatio = 1.61803398875;
                var boxLength = radius * 2 * gondenRatio;
                var TranslateGeometry = new Rhino.Geometry.Mesh();

                // box geometry
                var box = Support.Fix;

                // cylinder geometries
                var circle = new Rhino.Geometry.Circle(Rhino.Geometry.Plane.WorldZX, radius);
                var cylinder = new Rhino.Geometry.Cylinder(circle, boxLength);
                var cylinderMesh = Rhino.Geometry.Mesh.CreateFromCylinder(cylinder, 2, 12);

                var cylinderOne = cylinderMesh.DuplicateMesh();
                var cylinderTwo = cylinderMesh.DuplicateMesh();
                cylinderOne.Translate(new Vector3d(- boxLength / 2, -boxLength/2, -boxLength - radius));
                cylinderTwo.Translate(new Vector3d(+ boxLength / 2, -boxLength/2, -boxLength - radius));


                // Collect Geometries
                TranslateGeometry.Append(box);
                TranslateGeometry.Append(cylinderOne);
                TranslateGeometry.Append(cylinderTwo);

                return TranslateGeometry;
            }
        }
        private static Mesh TranslateX
        {
            get
            {
                var TranslateGeometryX = Support.Translate;
                // Orient Geometry
                // it is not required as it is already in the correct orientation
                return TranslateGeometryX;
            }
        }
        private static Mesh TranslateY
        {
            get
            {
                var TranslateGeometryY = Support.Translate;
                // Orient Geometry

                var orient = Rhino.Geometry.Transform.PlaneToPlane(Plane.WorldXY, Plane.WorldYZ);
                TranslateGeometryY.Transform(orient);
                return TranslateGeometryY;
            }
        }
        private static Mesh TranslateZ
        {
            get
            {
                var TranslateGeometryZ = Support.Translate;
                // Orient Geometry

                var orient = Rhino.Geometry.Transform.PlaneToPlane(Plane.WorldXY, Plane.WorldZX);
                TranslateGeometryZ.Transform(orient);
                return TranslateGeometryZ;
            }
        }
        private static Mesh Rotate
        {
            get
            {
                var radius = 0.25;
                var gondenRatio = 1.61803398875;
                var boxLength = radius * 2 * gondenRatio;
                var rotateGeometry = new Rhino.Geometry.Mesh();

                // box geometry
                var box = Support.Fix;
                box.Translate(new Vector3d(0, 0, -radius));

                // cylinder geometries
                var circle = new Rhino.Geometry.Circle(Rhino.Geometry.Plane.WorldXY, radius);
                var cylinder = new Rhino.Geometry.Cylinder(circle, radius);
                var cylinderMesh = Rhino.Geometry.Mesh.CreateFromCylinder(cylinder, 2, 12);

                var cylinderOne = cylinderMesh.DuplicateMesh();
                cylinderOne.Translate(new Vector3d(0, 0, - radius));

                // Collect Geometries
                rotateGeometry.Append(box);
                rotateGeometry.Append(cylinderOne);

                return rotateGeometry;
            }
        }
        private static Mesh RotateX
        {
            get
            {
                var RotateGeometryX = Support.Rotate;
                // Orient Geometry
                var orient = Rhino.Geometry.Transform.PlaneToPlane(Plane.WorldXY, Plane.WorldYZ);
                RotateGeometryX.Transform(orient);
                return RotateGeometryX;
            }
        }
        private static Mesh RotateY
        {
            get
            {
                var rotateGeometryY = Support.Rotate;
                // Orient Geometry
                var orient = Rhino.Geometry.Transform.PlaneToPlane(Plane.WorldXY, Plane.WorldZX);
                rotateGeometryY.Transform(orient);
                return rotateGeometryY;
            }
        }
        private static Mesh RotateZ
        {
            get
            {
                var rotateGeometryZ = Support.Rotate;
                // Orient Geometry
                return rotateGeometryZ;
            }
        }
    }
}
