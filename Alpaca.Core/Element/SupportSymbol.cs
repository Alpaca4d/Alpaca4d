using System;
using System.Collections.Generic;

using Rhino.Geometry;

namespace Alpaca4d.Element
{
    /// <summary>
    /// The picture drawn for each <see cref="SupportPreset"/>.
    ///
    /// Nothing structural is decided here. A symbol is a drawing of a preset and can be
    /// replaced wholesale - different primitives, different proportions, a different idiom
    /// entirely - without touching the degrees of freedom in <see cref="SupportPreset"/>,
    /// which are what the solver reads.
    ///
    /// Everything is built in a unit cell so that a caller only ever has to scale: one unit
    /// across in plan, centred on the node at the origin, and hanging below it - the node
    /// is the point being supported, so the symbol sits under it the way the real thing
    /// would. <see cref="Free"/> is the exception and straddles the node, having no ground
    /// to stand on.
    /// </summary>
    public static class SupportSymbol
    {
        /// <summary>Plan footprint of every symbol. Everything else is a fraction of it.</summary>
        public const double Size = 1.0;

        /// <summary>Thickness of the plates the symbols are built from.</summary>
        private const double PlateThickness = 0.09;

        /// <summary>Facets around a cylinder or sphere. One number, so the family stays even.</summary>
        private const int Facets = 16;

        /// <summary>
        /// The symbol for a preset id, or null if the id is not one of the seven.
        /// Ids come from <see cref="SupportPreset"/>; this switch is the one place the two
        /// halves meet.
        /// </summary>
        public static Mesh For(string presetId)
        {
            switch (presetId)
            {
                case SupportPreset.Fixed: return Fixed();
                case SupportPreset.Hinged: return Hinged();
                case SupportPreset.SlidingXY: return SlidingXY();
                case SupportPreset.SlidingX: return SlidingX();
                case SupportPreset.SlidingY: return SlidingY();
                case SupportPreset.SlidingZY: return SlidingZY();
                case SupportPreset.Free: return Free();
                default: return null;
            }
        }

        public static Mesh For(SupportPreset preset)
        {
            return preset == null ? null : For(preset.Id);
        }

        /// <summary>
        /// Rigid / Fixed - a solid block under a cap plate. No rollers, no ball, no gap:
        /// there is nothing in the drawing that could move, which is the whole statement.
        /// </summary>
        private static Mesh Fixed()
        {
            var symbol = new Mesh();

            symbol.Append(Plate(Size, Size, 0.0));
            symbol.Append(Block(Size, Size, 0.32, -PlateThickness));

            return Finish(symbol);
        }

        /// <summary>
        /// Hinged / Pinned - a pyramid balanced on its point at the node, with a ball at
        /// that point. The ball is the whole statement: a sphere turns freely about every
        /// axis, so the node is pinned in place and released in all three rotations. The
        /// five partial supports that do hold Rz are drawn with fins or rollers instead,
        /// never a sphere.
        /// </summary>
        private static Mesh Hinged()
        {
            var symbol = new Mesh();

            symbol.Append(Pyramid(Size, Size, 0.58, 0.0));
            symbol.Append(Ball(0.17, 0.0));

            return Finish(symbol);
        }

        /// <summary>
        /// Sliding in X and Y - an upright roller: whichever way the node is pushed in plan
        /// it can go, so the roller stands on end and the plate rests on it. The two
        /// upright fins are the Rz restraint.
        /// </summary>
        private static Mesh SlidingXY()
        {
            var symbol = new Mesh();

            const double roller = 0.21;
            const double height = 0.46;

            symbol.Append(Plate(Size, Size, 0.0));
            symbol.Append(Rod(new Point3d(0, 0, -PlateThickness - height), Vector3d.ZAxis, roller, height));
            symbol.Append(Block(Size * 0.9, 0.05, height, -PlateThickness));
            symbol.Append(Block(0.05, Size * 0.9, height, -PlateThickness));
            symbol.Append(Plate(Size, Size, -PlateThickness - height));

            return Finish(symbol);
        }

        /// <summary>
        /// Sliding in X - a plate on two rollers whose axes run along Y, so the only way it
        /// can travel is along X.
        /// </summary>
        private static Mesh SlidingX()
        {
            return Rollers(Vector3d.YAxis);
        }

        /// <summary>
        /// Sliding in Y - the same pair of rollers given a quarter turn: axes along X, so it
        /// travels along Y. Same family as <see cref="SlidingX"/> on purpose; the two
        /// supports differ by one degree of freedom and the drawings differ by one rotation.
        /// </summary>
        private static Mesh SlidingY()
        {
            return Rollers(Vector3d.XAxis);
        }

        /// <summary>
        /// A plate carried on two rollers lying along <paramref name="axis"/>. The rollers
        /// sit either side of the node, spaced along the direction they let it travel.
        /// </summary>
        private static Mesh Rollers(Vector3d axis)
        {
            var symbol = new Mesh();

            const double radius = 0.185;
            const double spacing = 0.25;

            // A roller lying along `axis` rolls at right angles to it, in plan.
            var travel = Vector3d.CrossProduct(axis, Vector3d.ZAxis);
            travel.Unitize();

            var centreZ = -PlateThickness - radius;

            symbol.Append(Plate(Size, Size, 0.0));

            foreach (var offset in new[] { -spacing, spacing })
            {
                var centre = new Point3d(travel.X * offset, travel.Y * offset, centreZ);
                symbol.Append(Rod(centre - axis * (Size * 0.34), axis, radius, Size * 0.68));
            }

            symbol.Append(Plate(Size, Size, centreZ - radius));

            return Finish(symbol);
        }

        /// <summary>
        /// Sliding in Z and Y - two plates with air between them. The upper one carries the
        /// node and is free to slide along Y and to lift away in Z; only X is still held,
        /// which is why the plates are cut back on the Y faces and not on the X ones.
        /// </summary>
        private static Mesh SlidingZY()
        {
            var symbol = new Mesh();

            symbol.Append(Plate(Size, Size, 0.0));
            symbol.Append(Plate(Size, Size, -PlateThickness - 0.12));

            return Finish(symbol);
        }

        /// <summary>
        /// Free - nothing is held at all, so there is no ground to draw and no plate to rest
        /// on. Six spokes reach out along every axis the node is free to move on, which
        /// makes the one support that restrains nothing the one symbol that points
        /// everywhere. It straddles the node rather than hanging below it.
        /// </summary>
        private static Mesh Free()
        {
            var symbol = new Mesh();

            const double radius = 0.075;
            const double reach = 0.42;

            foreach (var axis in new[] { Vector3d.XAxis, Vector3d.YAxis, Vector3d.ZAxis })
                symbol.Append(Rod(Point3d.Origin - axis * reach, axis, radius, 2.0 * reach));

            symbol.Append(Ball(0.13, 0.0));

            return Finish(symbol);
        }

        /// <summary>A thin plate of the standard thickness, hanging from <paramref name="topZ"/>.</summary>
        private static Mesh Plate(double width, double depth, double topZ)
        {
            return Block(width, depth, PlateThickness, topZ);
        }

        /// <summary>A box centred on the Z axis, hanging from <paramref name="topZ"/>.</summary>
        private static Mesh Block(double width, double depth, double height, double topZ)
        {
            var box = new BoundingBox(
                -width / 2.0, -depth / 2.0, topZ - height,
                 width / 2.0, depth / 2.0, topZ);

            return Mesh.CreateFromBox(box, 1, 1, 1);
        }

        /// <summary>A capped cylinder running from <paramref name="start"/> along <paramref name="axis"/>.</summary>
        private static Mesh Rod(Point3d start, Vector3d axis, double radius, double length)
        {
            var circle = new Circle(new Plane(start, axis), radius);

            return Mesh.CreateFromCylinder(new Cylinder(circle, length), 1, Facets);
        }

        private static Mesh Ball(double radius, double centreZ)
        {
            return Mesh.CreateQuadSphere(new Sphere(new Point3d(0, 0, centreZ), radius), 3);
        }

        /// <summary>
        /// A square pyramid standing on its point, apex at <paramref name="apexZ"/> on the
        /// Z axis and base square below it.
        /// </summary>
        private static Mesh Pyramid(double width, double depth, double height, double apexZ)
        {
            var mesh = new Mesh();
            var baseZ = apexZ - height;

            mesh.Vertices.Add(-width / 2.0, -depth / 2.0, baseZ);
            mesh.Vertices.Add(width / 2.0, -depth / 2.0, baseZ);
            mesh.Vertices.Add(width / 2.0, depth / 2.0, baseZ);
            mesh.Vertices.Add(-width / 2.0, depth / 2.0, baseZ);
            mesh.Vertices.Add(0.0, 0.0, apexZ);

            mesh.Faces.AddFace(3, 2, 1, 0);
            mesh.Faces.AddFace(0, 1, 4);
            mesh.Faces.AddFace(1, 2, 4);
            mesh.Faces.AddFace(2, 3, 4);
            mesh.Faces.AddFace(3, 0, 4);

            return mesh;
        }

        private static Mesh Finish(Mesh symbol)
        {
            symbol.Normals.ComputeNormals();
            symbol.Compact();

            return symbol;
        }
    }
}
