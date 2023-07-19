//using Alpaca4d.Element;
//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;
//using fd = FemDesign;
//using FemDesign.Utils;
//using FemDesign;

//namespace Alpaca4d
//{
//    public static class Export
//    {
//        public static fd.Model ToFEM_Design(Alpaca4d.Model model)
//        {
//            var elements = new List<fd.GenericClasses.IStructureElement>();
//            var loads = new List<fd.GenericClasses.ILoadElement>();

//            // create supports
//            foreach (var support in model.Supports)
//            {
//                var pos = new fd.Geometry.Point3d(support.Pos.X, support.Pos.Y, support.Pos.Z);

//                var fdSupport = new fd.Supports.PointSupport(pos, support.Tx, support.Ty, support.Tz, support.Rx, support.Ry, support.Rz);

//                elements.Add(fdSupport);
//            }



//            foreach (var beam in model.Beams)
//            {
                
//                var ptStart = beam.Curve.PointAtStart;
//                var ptEnd = beam.Curve.PointAtStart;

//                var start = new fd.Geometry.Point3d(ptStart.X, ptStart.Y, ptStart.Z);
//                var end = new fd.Geometry.Point3d(ptEnd.X, ptEnd.Y, ptEnd.Z);

//                var edge = new fd.Geometry.Edge(start, end);

//                // material
//                var uniaxial = beam.Section.Material;
//                var mass = (double)uniaxial.Rho;
//                var e_0 = uniaxial.E;
//                var nu_0 = uniaxial.Nu;
//                var alpha_0 = 0.0;
//                var fdMaterial = fd.Materials.Material.CustomUniaxialMaterial(uniaxial.Id.ToString(), mass, e_0, nu_0, alpha_0);
//                //section
//                var section = beam.Section;

                

//                var type = "";
//                var groupName = "groupName";
//                var typeName = "typeName";
//                var sizeName = "sizeName";

//                // convert geometry
//                List<FemDesign.Geometry.Region> regions = new List<FemDesign.Geometry.Region> { section.Brep.FromRhino() };

//                // create region group
//                FemDesign.Geometry.RegionGroup regionGroup = new FemDesign.Geometry.RegionGroup(regions);


//                var fdSection = new FemDesign.Sections.Section(regionGroup, type, fd.Materials.MaterialTypeEnum.Undefined, groupName, typeName, sizeName);

                
//                var fdBeam = new fd.Bars.Beam(edge, fdMaterial, fdSection);
//                elements.Add(fdBeam);
//            }


//            var fdModel = new fd.Model(fd.Country.COMMON, elements, loads);

//            return fdModel;
//        }




//        public static fd.Geometry.Region FromRhino(this Rhino.Geometry.Brep obj)
//        {
//            // check if brep contains more than 1 surface
//            if (obj.Surfaces.Count != 1)
//            {
//                throw new System.ArgumentException("Brep contains more than 1 surface.");
//            }

//            // check if brep surface is planar
//            if (!obj.Surfaces[0].IsPlanar())
//            {
//                throw new System.ArgumentException("Brep surface is not planar. This problem might occur due to tolerance error - if your model space is in millimeters try to change to meters.");
//            }

//            // Reconstruct Brep to make sure that boundaries are Atomic.
//            var innerNakedCurves = obj.DuplicateNakedEdgeCurves(true, false);
//            var outerNakedCurves = obj.DuplicateNakedEdgeCurves(false, true);
//            var nakedCurves = innerNakedCurves.Concat(outerNakedCurves);
//            var outerCurves = new List<Rhino.Geometry.Curve>();
//            foreach (var curve in nakedCurves)
//            {
//                var curves = Alpaca4d.Utils.Explode(curve);
//                outerCurves.AddRange(curves);
//            }
//            obj = Rhino.Geometry.Brep.CreatePlanarBreps(outerCurves, Tolerance.Brep)[0];

//            // get outline curves
//            var container = new List<List<Rhino.Geometry.Curve>>();
//            var loopCurves = new List<Rhino.Geometry.Curve>();

//            foreach (Rhino.Geometry.BrepLoop loop in obj.Loops)
//            {
//                foreach (Rhino.Geometry.BrepTrim trim in loop.Trims)
//                {
//                    loopCurves.Add(trim.Edge.EdgeCurve);
//                }
//                container.Add(new List<Rhino.Geometry.Curve>(loopCurves));
//                loopCurves.Clear();
//            }

//            // Change direction of EdgeCurves if necessary.
//            // Circular Edge in Contour (id est the only Edge in that Contour) should have a normal in the opposite direction from any other type of Contour in Region (id est the direction of the Contour should be opposite).
//            // EndPoint of EdgeCurve[idx] should be equal to StartPoint of EdgeCurve[idx + 1] in a Contour.
//            foreach (List<Rhino.Geometry.Curve> items in container)
//            {
//                // if Contour consists of one curve
//                if (items.Count == 1)
//                {
//                    // check if curve is a Circle
//                    Rhino.Geometry.Curve curve = items[0];
//                    if (curve.IsArc() && curve.IsClosed)
//                    {
//                        // check if Circle is planar
//                        if (curve.IsPlanar())
//                        {
//                            curve.TryGetPlane(out Rhino.Geometry.Plane plane);
//                            // compare Contour and Surface normals
//                            if (obj.Surfaces[0].NormalAt(0, 0).IsParallelTo(plane.Normal, Tolerance.Point3d) == 1)
//                            {
//                                // reverse direction of Circle
//                                curve.Reverse();
//                            }
//                        }
//                        else
//                        {
//                            throw new System.ArgumentException("Curve is not planar");
//                        }
//                    }

//                    // if curve for some reason is not a Circle
//                    else
//                    {
//                        // if the curve can not be represented by a circle then direction is irrelevant.
//                        // pass
//                    }
//                }

//                // if Contour consists of more than one curve (i.e. is not a Circle)
//                else
//                {
//                    Rhino.Geometry.Point3d pA0, pA1, pB0, pB1;
//                    for (int idx = 0; idx < items.Count - 1; idx++)
//                    {
//                        // curve a = items[idx]
//                        // curve b = items[idx + 1]
//                        pA0 = items[idx].PointAtStart;
//                        pA1 = items[idx].PointAtEnd;
//                        pB0 = items[idx + 1].PointAtStart;
//                        pB1 = items[idx + 1].PointAtEnd;

//                        if (pA0.EpsilonEquals(pB0, Tolerance.Point3d))
//                        {
//                            if (idx == 0)
//                            {
//                                items[idx].Reverse();
//                            }
//                            else
//                            {
//                                throw new System.ArgumentException("pA0 == pB0 even though idx != 0. Bad outline.");
//                            }
//                        }

//                        else if (pA0.EpsilonEquals(pB1, Tolerance.Point3d))
//                        {
//                            if (idx == 0)
//                            {
//                                items[idx].Reverse();
//                                items[idx + 1].Reverse();
//                            }
//                            else
//                            {
//                                throw new System.ArgumentException("pA0 == pB1 even though idx != 0. Bad outline.");
//                            }
//                        }

//                        else if (pA1.EpsilonEquals(pB0, Tolerance.Point3d))
//                        {
//                            // pass
//                        }

//                        else if (pA1.EpsilonEquals(pB1, Tolerance.Point3d))
//                        {
//                            items[idx + 1].Reverse();
//                        }

//                        else
//                        {
//                            throw new System.ArgumentException("Can't close outline. Bad outline.");
//                        }
//                    }

//                    // check if outline is closed.
//                    pA1 = items[items.Count - 1].PointAtEnd;
//                    pB0 = items[0].PointAtStart;
//                    if (pA1.EpsilonEquals(pB0, Tolerance.Point3d))
//                    {

//                    }

//                    else
//                    {
//                        throw new System.ArgumentException("Can't close outline. Bad outline. Boundary Edge Directions should perform a close loop.");
//                    }
//                }
//            }

//            // Create contours
//            List<fd.Geometry.Edge> edges = new List<fd.Geometry.Edge>();
//            List<fd.Geometry.Contour> contours = new List<fd.Geometry.Contour>();

//            foreach (List<Rhino.Geometry.Curve> items in container)
//            {
//                foreach (Rhino.Geometry.Curve curve in items)
//                {
//                    foreach (fd.Geometry.Edge edge in curve.FromRhinoBrep())
//                    {
//                        edges.Add(edge);
//                    }
//                }
//                contours.Add(new fd.Geometry.Contour(new List<fd.Geometry.Edge>(edges)));
//                edges.Clear();
//            }

//            // Get LCS
//            FemDesign.Geometry.Plane cs = obj.Surfaces[0].FromRhinoSurface();

//            // return
//            return new fd.Geometry.Region(contours, cs);
//        }






//    }
//}
