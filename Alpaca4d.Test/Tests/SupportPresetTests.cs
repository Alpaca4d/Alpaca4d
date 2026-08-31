using System.Linq;
using NUnit.Framework;
using Rhino.Geometry;
using Alpaca4d.Element;

namespace Alpaca4d.Testing.Tests
{
    /// <summary>
    /// The seven predefined supports, checked against the table they were specified from
    /// rather than against each other. Every expectation here is written out by hand: a
    /// test that derived the states the same way the code does would agree with a wrong
    /// implementation.
    /// </summary>
    [TestFixture]
    public class SupportPresetTests
    {
        /// <summary>
        /// id, then Tx, Ty, Tz, Rx, Ry, Rz - true is restrained. In display order, left to
        /// right. Transcribed from the specification, not from SupportPreset.
        /// </summary>
        private static readonly object[] Table =
        {
            new object[] { 0, "fixed",      true,  true,  true,  true,  true,  true  },
            new object[] { 1, "hinged",     true,  true,  true,  false, false, false },
            new object[] { 2, "sliding-xy", false, false, true,  false, false, true  },
            new object[] { 3, "sliding-x",  false, true,  true,  false, false, true  },
            new object[] { 4, "sliding-y",  true,  false, true,  false, false, true  },
            new object[] { 5, "sliding-zy", true,  false, false, false, false, true  },
            new object[] { 6, "free",       false, false, false, false, false, false },
        };

        [Test]
        public void There_are_exactly_seven_presets()
        {
            Assert.That(SupportPreset.All, Has.Count.EqualTo(7));
        }

        [TestCaseSource(nameof(Table))]
        public void The_preset_at_each_position_holds_what_the_table_says(
            int position, string id, bool tx, bool ty, bool tz, bool rx, bool ry, bool rz)
        {
            var preset = SupportPreset.All[position];

            Assert.Multiple(() =>
            {
                Assert.That(preset.Id, Is.EqualTo(id), "left-to-right order");
                Assert.That(preset.Tx, Is.EqualTo(tx), "Tx");
                Assert.That(preset.Ty, Is.EqualTo(ty), "Ty");
                Assert.That(preset.Tz, Is.EqualTo(tz), "Tz");
                Assert.That(preset.Rx, Is.EqualTo(rx), "Rx");
                Assert.That(preset.Ry, Is.EqualTo(ry), "Ry");
                Assert.That(preset.Rz, Is.EqualTo(rz), "Rz");
            });
        }

        [Test]
        public void Every_preset_has_a_label_and_a_symbol_of_its_own()
        {
            Assert.Multiple(() =>
            {
                foreach (var preset in SupportPreset.All)
                {
                    Assert.That(preset.Label, Is.Not.Null.And.Not.Empty, preset.Id);
                    Assert.That(SupportSymbol.For(preset.Id), Is.Not.Null,
                        preset.Id + " has no symbol");
                }
            });
        }

        /// <summary>
        /// The symbol lookup is a switch on id, which is exactly the kind of thing that
        /// ends up one case short or one case crossed. Two presets sharing a symbol would
        /// mean one of them is drawn as the other.
        /// </summary>
        [Test]
        public void No_two_presets_share_a_symbol()
        {
            // Compare the vertices themselves, not counts and bounding boxes. Sliding in X
            // and Sliding in Y are the same rollers a quarter turn apart, so they agree on
            // vertex count, face count and - both being framed by the same square plates -
            // bounding box too. Only the positions tell them apart.
            var signatures = SupportPreset.All
                .Select(preset => new { preset.Id, Signature = Signature(SupportSymbol.For(preset.Id)) })
                .ToList();

            Assert.Multiple(() =>
            {
                foreach (var a in signatures)
                {
                    foreach (var b in signatures.Where(other => other.Id != a.Id))
                        Assert.That(a.Signature, Is.Not.EqualTo(b.Signature),
                            a.Id + " is drawn the same as " + b.Id);
                }
            });
        }

        /// <summary>Every vertex position, rounded and sorted, so order of assembly cannot matter.</summary>
        private static string Signature(Mesh mesh)
        {
            return string.Join(";", mesh.Vertices
                .Select(v => string.Format(System.Globalization.CultureInfo.InvariantCulture,
                    "{0:F4},{1:F4},{2:F4}", v.X, v.Y, v.Z))
                .OrderBy(text => text, System.StringComparer.Ordinal));
        }

        /// <summary>
        /// A roller's end caps are rings of quads, not fans of triangles converging on the
        /// centre: at symbol scale a fan reads as a knot of noise. The plates and the
        /// pyramid are quads and triangles by nature, so only the rollers are checked.
        /// </summary>
        [TestCase(SupportPreset.SlidingX)]
        [TestCase(SupportPreset.SlidingY)]
        [TestCase(SupportPreset.SlidingXY)]
        public void A_roller_symbol_is_built_entirely_from_quads(string presetId)
        {
            var mesh = SupportSymbol.For(presetId);
            var triangles = mesh.Faces.Count(face => face.IsTriangle);

            TestContext.WriteLine(presetId + ": " + mesh.Faces.Count + " faces, " + triangles + " triangles");

            Assert.That(triangles, Is.Zero, "a fan cap would show up here");
        }

        /// <summary>
        /// CreateQuadSphere gives 6 * 4^level faces. Level 2 is 96, a quarter of the 384
        /// that level 3 was drawing, which was far denser than the symbol needs.
        /// </summary>
        [Test]
        public void The_pinned_ball_is_not_over_subdivided()
        {
            var faces = SupportSymbol.For(SupportPreset.Hinged).Faces.Count;
            TestContext.WriteLine("hinged symbol: " + faces + " faces");

            // The pyramid contributes 5; the rest is the ball.
            Assert.That(faces - 5, Is.EqualTo(96), "6 * 4^2");
        }

        /// <summary>
        /// A unit model, so a caller only has to scale. Everything sits inside a single
        /// unit cell.
        /// </summary>
        [Test]
        public void Every_symbol_fits_the_unit_cell()
        {
            Assert.Multiple(() =>
            {
                foreach (var preset in SupportPreset.All)
                {
                    var box = SupportSymbol.For(preset.Id).GetBoundingBox(true);

                    Assert.That(box.Diagonal.X, Is.LessThanOrEqualTo(1.001), preset.Id + " width");
                    Assert.That(box.Diagonal.Y, Is.LessThanOrEqualTo(1.001), preset.Id + " depth");
                    Assert.That(box.Diagonal.Z, Is.LessThanOrEqualTo(1.001), preset.Id + " height");
                }
            });
        }

        /// <summary>
        /// The support symbol hangs under the node it supports - except Free, which holds
        /// nothing, has no ground to stand on and straddles the node instead.
        /// </summary>
        [Test]
        public void Symbols_hang_below_the_node_and_the_star_straddles_it()
        {
            Assert.Multiple(() =>
            {
                foreach (var preset in SupportPreset.All.Where(p => p.Id != SupportPreset.Free))
                {
                    var box = SupportSymbol.For(preset.Id).GetBoundingBox(true);
                    Assert.That(box.Max.Z, Is.LessThanOrEqualTo(1e-9), preset.Id + " reaches above the node");
                }

                var star = SupportSymbol.For(SupportPreset.Free).GetBoundingBox(true);
                Assert.That(star.Max.Z, Is.GreaterThan(0.1), "the star reaches above the node");
                Assert.That(star.Min.Z, Is.LessThan(-0.1), "and below it");
            });
        }

        /// <summary>
        /// Free is the one that is easiest to leave out, being the support that supports
        /// nothing. Six spokes on three axes, and a reach on every one of them.
        /// </summary>
        [Test]
        public void The_free_support_is_a_star_reaching_along_all_three_axes()
        {
            var preset = SupportPreset.All.Last();
            var box = SupportSymbol.For(SupportPreset.Free).GetBoundingBox(true);

            Assert.Multiple(() =>
            {
                Assert.That(preset.Id, Is.EqualTo(SupportPreset.Free), "seventh, and last");
                Assert.That(preset.Dof, Is.All.False, "a free support holds nothing");
                Assert.That(box.Diagonal.X, Is.GreaterThan(0.5), "spokes along X");
                Assert.That(box.Diagonal.Y, Is.GreaterThan(0.5), "spokes along Y");
                Assert.That(box.Diagonal.Z, Is.GreaterThan(0.5), "spokes along Z");
            });
        }

        /// <summary>Round trip through the id, which is all that needs to be serialised.</summary>
        [TestCaseSource(nameof(Table))]
        public void A_preset_survives_a_round_trip_through_its_id(
            int position, string id, bool tx, bool ty, bool tz, bool rx, bool ry, bool rz)
        {
            Assert.That(SupportPreset.FromId(id), Is.SameAs(SupportPreset.All[position]));
        }

        /// <summary>
        /// The link back the other way: a support built from a preset has to be recognised
        /// as that preset, or the symbol drawn for it would be someone else's.
        /// </summary>
        [TestCaseSource(nameof(Table))]
        public void A_support_built_from_a_preset_is_matched_back_to_it(
            int position, string id, bool tx, bool ty, bool tz, bool rx, bool ry, bool rz)
        {
            var support = SupportPreset.FromId(id).At(new Point3d(1, 2, 3));

            Assert.Multiple(() =>
            {
                Assert.That(support.Preset, Is.SameAs(SupportPreset.All[position]));
                Assert.That(support.Pos.DistanceTo(new Point3d(1, 2, 3)), Is.LessThan(1e-12));
                Assert.That(SupportPreset.Match(tx, ty, tz, rx, ry, rz).Id, Is.EqualTo(id));
            });
        }

        /// <summary>
        /// The Type input is the only practical way to reach most of the seven. Five of
        /// them need Rx and Ry off and Rz on as well as the translations, so flipping the
        /// one boolean a user would think to flip lands outside the set and draws the text
        /// tag instead of a symbol.
        /// </summary>
        [TestCaseSource(nameof(Table))]
        public void Picking_a_type_on_the_component_gives_that_preset_and_a_symbol(
            int position, string id, bool tx, bool ty, bool tz, bool rx, bool ry, bool rz)
        {
            var result = ComponentHarness.For<Alpaca4d.Gh.Support>()
                                         .Set("Position", new Point3d(1, 2, 3))
                                         .Set("Type", position)
                                         .Solve();

            Assert.That(result.Errors, Is.Empty, result.Describe());

            var support = result.Get<Alpaca4d.Element.Support>(0);
            TestContext.WriteLine(support.Description);

            Assert.Multiple(() =>
            {
                Assert.That(support.Preset, Is.Not.Null, "type " + position + " matched no preset");
                Assert.That(support.Preset.Id, Is.EqualTo(id));
                // Geometry is dynamic; asserting on it directly would need the C# runtime
                // binder, which this project does not reference.
                Assert.That((object)support.Geometry, Is.InstanceOf<Mesh>(),
                    "a preset must draw a symbol, not fall through to the text tag");
            });
        }

        /// <summary>Left alone, the component still reads the six booleans as it always did.</summary>
        [Test]
        public void Leaving_the_type_alone_reads_the_six_booleans()
        {
            var result = ComponentHarness.For<Alpaca4d.Gh.Support>()
                                         .Set("Position", new Point3d(1, 2, 3))
                                         .Set("Tx", false)
                                         .Solve();

            var support = result.Get<Alpaca4d.Element.Support>(0);

            Assert.Multiple(() =>
            {
                Assert.That(result.Errors, Is.Empty, result.Describe());
                Assert.That(support.Tx, Is.False);
                Assert.That(support.Ty, Is.True);
                Assert.That(support.Rz, Is.True);
                Assert.That(support.Preset, Is.Null,
                    "one translation off with every rotation still held is not one of the seven");
            });
        }

        [Test]
        public void A_combination_outside_the_seven_matches_nothing()
        {
            // Held in translation and about X, free about Y and Z. A support someone
            // could reasonably build, and deliberately not one of the seven.
            Assert.That(SupportPreset.Match(true, true, true, true, false, false), Is.Null);
        }

        [Test]
        public void A_label_reads_the_states_in_the_order_they_are_always_read()
        {
            var described = SupportPreset.FromId(SupportPreset.SlidingX).Describe();
            TestContext.WriteLine(described);

            Assert.Multiple(() =>
            {
                Assert.That(described, Does.Contain("Sliding in X"));
                Assert.That(described, Does.Match("Tx .*Ty .*Tz .*Rx .*Ry .*Rz"));
                Assert.That(described, Does.Contain("Tx free"), "X slides");
                Assert.That(described, Does.Contain("Rz \U0001F512"), "Rz is held");
            });
        }
    }
}
