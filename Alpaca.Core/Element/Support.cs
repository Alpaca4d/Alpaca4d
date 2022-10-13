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
        public dynamic Geometry
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
        {
            this.Pos = node;
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
            string tclText;

            if(this.ndf == 6)
            {
                tclText = $"fix {this.Id} {Convert.ToInt16(this.Tx)} {Convert.ToInt16(this.Ty)} {Convert.ToInt16(this.Tz)} {Convert.ToInt16(this.Rx)} {Convert.ToInt16(this.Ry)} {Convert.ToInt16(this.Rz)}\n";
            }
            else if(this.ndf == 3)
            {
                tclText = $"fix {this.Id} {Convert.ToInt16(this.Tx)} {Convert.ToInt16(this.Ty)} {Convert.ToInt16(this.Tz)}\n";
            }
            else if(this.ndf == 0 && this.Id == null)
            {
                tclText = $"fix {this.Id} {Convert.ToInt16(this.Tx)} {Convert.ToInt16(this.Ty)} {Convert.ToInt16(this.Tz)} {Convert.ToInt16(this.Rx)} {Convert.ToInt16(this.Ry)} {Convert.ToInt16(this.Rz)}\n";
            }
			else
			{
                throw new Exception($"The support at location {this.Pos.ToString()} is not part of the mdodel");
            }
            return tclText;
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
