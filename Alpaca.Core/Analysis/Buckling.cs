using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;

namespace Alpaca4d
{
    /// <summary>
    /// Linear buckling of an assembled model, the way Michael Scott shows it after Luigi Caglio
    /// ("Right under your nose", OpenSees Digital, 2021): OpenSees has no buckling analysis, but it
    /// prints its stiffness matrix. Printed once with no load it is K_mat; printed again under the
    /// reference load it is K_mat − K_geo, so K_geo is the difference, and the load factors λ that
    /// buckle the structure solve K_mat φ = λ K_geo φ (<see cref="BucklingSolver"/>).
    ///
    /// For that the deck is rewritten (<see cref="Rewrite"/>): beams get a PDelta transformation,
    /// which is what gives them a geometric stiffness, and may be split, because PDelta only sees
    /// the sway of each element's chord. Shells become ShellNLDKGQ / ShellNLDKGT: the corotational
    /// ASDShellQ4 and ASDShellT3 of OpenSees 3.8.0 leave the stress stiffness of membrane forces out
    /// of their tangent, so they would never buckle. Everything else in the deck stays as it was.
    ///
    /// Two runs. The first (<see cref="ExportDeck"/>) prints the matrices; the second
    /// (<see cref="ModesDeck"/>) writes the buckled shapes to an MPCO file as steps, one per mode,
    /// so Nodal Displacements and View Results read them as they read any static step.
    /// </summary>
    public static class Buckling
    {
        /// <summary>What the deck prints its findings behind, on lines of their own; see <see cref="Said"/>.</summary>
        public const string Label = "ALPACA4D_BUCKLING";

        /// <summary>
        /// The most equations the matrices are printed dense for. OpenSees 3.8.0 can only hand them
        /// over that way - a list of N² numbers - and Tcl holds the whole list at once: 4000
        /// equations are 16 million numbers, about a gigabyte on the way out.
        /// </summary>
        public const int DenseLimit = 4000;

        public enum TieKind { EqualDof, RigidBeam, RigidBar, RigidDiaphragm }

        public sealed class DeckNode
        {
            public int Tag;
            public double X, Y, Z;
            public int Ndf;
        }

        /// <summary>One of the elements a beam is split into, I end first.</summary>
        public sealed class Piece
        {
            public int Tag;
            public int Parent;
            public int INode, JNode;
        }

        /// <summary>A multi-point constraint of the deck, which the slave nodes' mode shapes are rebuilt from.</summary>
        public sealed class Tie
        {
            public TieKind Kind;
            public int Master;
            public int[] Slaves;
            /// <summary>The constrained dofs, from 1, for an equalDOF.</summary>
            public int[] Dofs;
            /// <summary>The direction normal to the plane of a rigidDiaphragm, 1 to 3.</summary>
            public int Perpendicular;
        }

        /// <summary>The deck as the buckling analysis runs it, and what it takes to read the results back.</summary>
        public sealed class Deck
        {
            /// <summary>Everything up to the load patterns.</summary>
            public List<string> Model { get; } = new List<string>();

            /// <summary>The load patterns, with element loads on split beams put on all their pieces.</summary>
            public List<string> Patterns { get; } = new List<string>();

            /// <summary>Every node of the deck by tag, the ones splitting added included.</summary>
            public Dictionary<int, DeckNode> Nodes { get; } = new Dictionary<int, DeckNode>();

            /// <summary>The nodes splitting added, in tag order.</summary>
            public List<DeckNode> SplitNodes { get; } = new List<DeckNode>();

            /// <summary>The pieces of each split beam, by the beam's tag. The first piece keeps the tag.</summary>
            public Dictionary<int, List<Piece>> Pieces { get; } = new Dictionary<int, List<Piece>>();

            public List<Tie> Ties { get; } = new List<Tie>();

            public int TransformsMadePDelta;
            public int QuadShellsReplaced;
            public int TriangleShellsReplaced;
            public int Solids;
            public int PatternsDropped;
            public List<string> Warnings { get; } = new List<string>();

            /// <summary>The two end nodes of every beam element of the deck, pieces included, by tag.</summary>
            public Dictionary<int, int[]> BeamEnds { get; } = new Dictionary<int, int[]>();

            /// <summary>
            /// Nodes tied twice over: the slave of one tie and the retained node of another, or the
            /// slave of two. The Transformation handler does not follow such a chain, and says nothing
            /// about it; <see cref="Analyse"/> uses the Penalty handler for a deck that has one.
            /// </summary>
            public List<int> ChainedNodes { get; } = new List<int>();
        }

        /// <summary>
        /// The deck of an assembled model rewritten for the buckling analysis.
        /// </summary>
        /// <param name="tcl">The model's Tcl, as Assemble wrote it.</param>
        /// <param name="patternStart">Where the load patterns begin in it; -1 to find them.</param>
        /// <param name="divisions">Elements each beam is split into; 1 leaves them whole.</param>
        public static Deck Rewrite(IList<string> tcl, int patternStart, int divisions)
        {
            if (patternStart < 0 || patternStart > tcl.Count)
                patternStart = FirstPattern(tcl);
            divisions = Math.Max(1, divisions);

            var deck = new Deck();

            // New nodes and elements are numbered past everything the deck already has, the
            // auxiliary nodes and springs of skewed supports included.
            int nextNode = 0, nextElement = 0;
            foreach (var entry in tcl)
                foreach (var line in Lines(entry))
                {
                    var t = Tokens(line);
                    if (t.Length > 1 && t[0] == "node" && int.TryParse(t[1], out int node))
                        nextNode = Math.Max(nextNode, node);
                    else if (t.Length > 2 && t[0] == "element" && int.TryParse(t[2], out int element))
                        nextElement = Math.Max(nextElement, element);
                }

            int ndf = 6;
            for (int e = 0; e < tcl.Count; e++)
            {
                var text = new StringBuilder();
                bool drop = false;

                foreach (var line in Lines(tcl[e]))
                {
                    var t = Tokens(line);
                    string indent = line.Substring(0, line.Length - line.TrimStart().Length);
                    if (t.Length == 0 || t[0].StartsWith("#"))
                    {
                        text.Append(line).Append('\n');
                        continue;
                    }

                    switch (t[0])
                    {
                        case "model":
                            int at = Array.IndexOf(t, "-ndf");
                            if (at >= 0 && at + 1 < t.Length && int.TryParse(t[at + 1], out int n))
                                ndf = n;
                            text.Append(line).Append('\n');
                            break;

                        case "node":
                            if (t.Length >= 5 && int.TryParse(t[1], out int tag))
                                deck.Nodes[tag] = new DeckNode { Tag = tag, X = Number(t[2]), Y = Number(t[3]), Z = Number(t[4]), Ndf = ndf };
                            text.Append(line).Append('\n');
                            break;

                        case "geomTransf":
                            if (t.Length > 1 && t[1] != "PDelta")
                            {
                                t[1] = "PDelta";
                                deck.TransformsMadePDelta++;
                            }
                            text.Append(indent).Append(string.Join(" ", t)).Append('\n');
                            break;

                        case "element":
                            text.Append(RewriteElement(deck, t, divisions, ref nextNode, ref nextElement, ref ndf));
                            break;

                        case "equalDOF":
                        case "rigidLink":
                        case "rigidDiaphragm":
                            var tie = ReadTie(t);
                            if (tie != null)
                                deck.Ties.Add(tie);
                            else
                                deck.Warnings.Add($"\"{line.Trim()}\" could not be read; the mode shapes of its nodes may be off.");
                            text.Append(line).Append('\n');
                            break;

                        case "eleLoad":
                            text.Append(RetargetElementLoad(deck, t, indent));
                            break;

                        case "pattern":
                            // A ground motion moves nothing in a static step.
                            if (t.Length > 1 && t[1] == "UniformExcitation")
                            {
                                drop = true;
                                deck.PatternsDropped++;
                            }
                            text.Append(line).Append('\n');
                            break;

                        default:
                            text.Append(line).Append('\n');
                            break;
                    }
                }

                if (drop)
                    continue;
                (e >= patternStart ? deck.Patterns : deck.Model).Add(text.ToString());
            }

            var slaves = deck.Ties.SelectMany(tie => tie.Slaves).ToList();
            var masters = new HashSet<int>(deck.Ties.Select(tie => tie.Master));
            deck.ChainedNodes.AddRange(slaves
                .GroupBy(s => s)
                .Where(g => g.Count() > 1 || masters.Contains(g.Key))
                .Select(g => g.Key)
                .OrderBy(s => s));

            return deck;
        }

        /// <summary>The first entry of the deck that defines a load pattern; the count when none does.</summary>
        public static int FirstPattern(IList<string> tcl)
        {
            for (int e = 0; e < tcl.Count; e++)
                foreach (var line in Lines(tcl[e]))
                {
                    var t = Tokens(line);
                    if (t.Length > 0 && t[0] == "pattern")
                        return e;
                }
            return tcl.Count;
        }

        private static string RewriteElement(Deck deck, string[] t, int divisions, ref int nextNode, ref int nextElement, ref int ndf)
        {
            string type = t.Length > 1 ? t[1] : "";
            switch (type)
            {
                case "ASDShellQ4":
                case "ShellDKGQ":
                case "ShellMITC4":
                    if (t.Length < 8) break;
                    deck.QuadShellsReplaced++;
                    return $"element ShellNLDKGQ {t[2]} {t[3]} {t[4]} {t[5]} {t[6]} {t[7]}\n";

                case "ASDShellT3":
                case "ShellDKGT":
                    if (t.Length < 7) break;
                    deck.TriangleShellsReplaced++;
                    return $"element ShellNLDKGT {t[2]} {t[3]} {t[4]} {t[5]} {t[6]}\n";

                case "SSPbrick":
                case "FourNodeTetrahedron":
                case "stdBrick":
                case "bbarBrick":
                    deck.Solids++;
                    break;

                case "forceBeamColumn":
                case "dispBeamColumn":
                    if (divisions > 1)
                        return SplitBeam(deck, t, divisions, ref nextNode, ref nextElement, ref ndf);
                    if (t.Length > 4 && int.TryParse(t[2], out int tag) && int.TryParse(t[3], out int i) && int.TryParse(t[4], out int j))
                        deck.BeamEnds[tag] = new[] { i, j };
                    break;
            }
            return string.Join(" ", t) + "\n";
        }

        /// <summary>
        /// element forceBeamColumn $tag $i $j $transf &lt;integration&gt; -mass $m, as n elements in a
        /// row along the chord. The transformation is shared: OpenSees gives every element its own
        /// copy of it.
        /// </summary>
        private static string SplitBeam(Deck deck, string[] t, int n, ref int nextNode, ref int nextElement, ref int ndf)
        {
            string whole = string.Join(" ", t) + "\n";
            if (t.Length < 7 || !int.TryParse(t[2], out int tag) || !int.TryParse(t[3], out int i) || !int.TryParse(t[4], out int j)
                || !deck.Nodes.TryGetValue(i, out var a) || !deck.Nodes.TryGetValue(j, out var b))
            {
                deck.Warnings.Add($"Element {(t.Length > 2 ? t[2] : "?")} could not be split and was left whole.");
                if (t.Length > 4 && int.TryParse(t[2], out int whole2) && int.TryParse(t[3], out int i2) && int.TryParse(t[4], out int j2))
                    deck.BeamEnds[whole2] = new[] { i2, j2 };
                return whole;
            }

            int end = 6;
            while (end < t.Length && !IsFlag(t[end]))
                end++;
            var integration = t.Skip(6).Take(end - 6).ToArray();
            var rest = t.Skip(end).ToArray();

            var pieces = new string[n][];
            for (int k = 0; k < n; k++)
            {
                pieces[k] = PieceIntegration(integration, k, n);
                if (pieces[k] == null)
                {
                    deck.Warnings.Add($"Element {tag} integrates by \"{string.Join(" ", integration)}\", which cannot be split; it was left whole.");
                    deck.BeamEnds[tag] = new[] { i, j };
                    return whole;
                }
            }

            var text = new StringBuilder();
            if (ndf != 6)
            {
                text.Append("model BasicBuilder -ndm 3 -ndf 6\n");
                ndf = 6;
            }

            var ends = new List<int> { i };
            for (int k = 1; k < n; k++)
            {
                double f = (double)k / n;
                var node = new DeckNode
                {
                    Tag = ++nextNode,
                    X = a.X + f * (b.X - a.X),
                    Y = a.Y + f * (b.Y - a.Y),
                    Z = a.Z + f * (b.Z - a.Z),
                    Ndf = 6,
                };
                deck.Nodes[node.Tag] = node;
                deck.SplitNodes.Add(node);
                ends.Add(node.Tag);
                text.Append($"node {node.Tag} {Write(node.X)} {Write(node.Y)} {Write(node.Z)}\n");
            }
            ends.Add(j);

            var list = new List<Piece>();
            for (int k = 0; k < n; k++)
            {
                var piece = new Piece { Tag = k == 0 ? tag : ++nextElement, Parent = tag, INode = ends[k], JNode = ends[k + 1] };
                list.Add(piece);
                deck.BeamEnds[piece.Tag] = new[] { piece.INode, piece.JNode };
                text.Append($"element {t[1]} {piece.Tag} {piece.INode} {piece.JNode} {t[5]} {string.Join(" ", pieces[k])}");
                if (rest.Length > 0)
                    text.Append(' ').Append(string.Join(" ", rest));
                text.Append('\n');
            }
            deck.Pieces[tag] = list;
            return text.ToString();
        }

        /// <summary>
        /// The integration of piece k of n. Sections and point counts carry over; a HingeRadau keeps
        /// its hinges at the ends of the beam, on the first and last piece, with the plastic hinge
        /// lengths shortened with the pieces so that they keep their share of the length. In between
        /// the "hinges" are the beam's own section. Null for a form that is not understood.
        /// </summary>
        private static string[] PieceIntegration(string[] integration, int k, int n)
        {
            if (integration.Length == 1 && int.TryParse(integration[0], out _))
                return integration; // a beamIntegration tag

            if (integration.Length == 6 && integration[0] == "HingeRadau")
            {
                string secI = integration[1], secJ = integration[3], secE = integration[5];
                string lpI = Write(Number(integration[2]) / n), lpJ = Write(Number(integration[4]) / n);
                return new[] { "HingeRadau", k == 0 ? secI : secE, lpI, k == n - 1 ? secJ : secE, lpJ, secE };
            }

            var simple = new[] { "Lobatto", "Legendre", "NewtonCotes", "Radau", "Trapezoidal", "CompositeSimpson" };
            if (integration.Length == 3 && Array.IndexOf(simple, integration[0]) >= 0)
                return integration;

            return null;
        }

        /// <summary>
        /// An element load, put on every piece of a split beam - and with its axial part, Wx of a
        /// -beamUniform, moved onto the element's two nodes, half each. PDelta takes the axial force of
        /// an element from one of its ends, so a load spread along the element leaves every element
        /// short of its mean axial force: a column buckling under its own weight converged as 1/n,
        /// 10 % too high with 32 pieces. As nodal loads each element carries its mean.
        /// </summary>
        private static string RetargetElementLoad(Deck deck, string[] t, string indent)
        {
            int at = Array.IndexOf(t, "-ele");
            if (at < 0)
            {
                if (Array.IndexOf(t, "-range") >= 0 && deck.Pieces.Count > 0)
                    deck.Warnings.Add($"\"{string.Join(" ", t)}\" names its elements by range; split pieces past the range get none of it.");
                return indent + string.Join(" ", t) + "\n";
            }

            var head = t.Take(at + 1).ToList();
            var tags = new List<string>();
            int k = at + 1;
            for (; k < t.Length && !IsFlag(t[k]); k++)
            {
                if (int.TryParse(t[k], out int tag) && deck.Pieces.TryGetValue(tag, out var pieces))
                    tags.AddRange(pieces.Select(p => p.Tag.ToString(CultureInfo.InvariantCulture)));
                else
                    tags.Add(t[k]);
            }
            var tail = t.Skip(k).ToList();

            int uniform = tail.IndexOf("-beamUniform");
            bool axial = uniform >= 0 && tail.Count == uniform + 4 && Number(tail[uniform + 3]) != 0.0 &&
                         tags.All(s => int.TryParse(s, out int e) && deck.BeamEnds.ContainsKey(e));
            if (!axial)
                return indent + string.Join(" ", head.Concat(tags).Concat(tail)) + "\n";

            double wx = Number(tail[uniform + 3]);
            var text = new StringBuilder();
            foreach (var s in tags)
            {
                var ends = deck.BeamEnds[int.Parse(s, CultureInfo.InvariantCulture)];
                var a = deck.Nodes[ends[0]];
                var b = deck.Nodes[ends[1]];
                double dx = b.X - a.X, dy = b.Y - a.Y, dz = b.Z - a.Z;
                // Wx per unit length along the element, from I to J: wx l / 2 at each end, along it.
                double half = 0.5 * wx;
                foreach (var node in new[] { a, b })
                    text.Append($"{indent}load {node.Tag} {Write(half * dx)} {Write(half * dy)} {Write(half * dz)}" +
                                (node.Ndf > 3 ? " 0 0 0" : "") + "\n");
            }

            tail.RemoveAt(uniform + 3);
            if (Number(tail[uniform + 1]) != 0.0 || Number(tail[uniform + 2]) != 0.0)
                text.Insert(0, indent + string.Join(" ", head.Concat(tags).Concat(tail)) + "\n");
            return text.ToString();
        }

        private static Tie ReadTie(string[] t)
        {
            var ints = new List<int>();
            switch (t[0])
            {
                case "equalDOF":
                    if (t.Length < 4) return null;
                    for (int k = 1; k < t.Length; k++)
                    {
                        if (!int.TryParse(t[k], out int v)) return null;
                        ints.Add(v);
                    }
                    return new Tie { Kind = TieKind.EqualDof, Master = ints[0], Slaves = new[] { ints[1] }, Dofs = ints.Skip(2).ToArray() };

                case "rigidLink":
                    if (t.Length < 4 || !int.TryParse(t[2], out int m) || !int.TryParse(t[3], out int s)) return null;
                    if (t[1] == "beam") return new Tie { Kind = TieKind.RigidBeam, Master = m, Slaves = new[] { s } };
                    if (t[1] == "bar") return new Tie { Kind = TieKind.RigidBar, Master = m, Slaves = new[] { s } };
                    return null;

                case "rigidDiaphragm":
                    if (t.Length < 4) return null;
                    for (int k = 1; k < t.Length; k++)
                    {
                        if (!int.TryParse(t[k], out int v)) return null;
                        ints.Add(v);
                    }
                    if (ints[0] < 1 || ints[0] > 3) return null;
                    return new Tie { Kind = TieKind.RigidDiaphragm, Perpendicular = ints[0], Master = ints[1], Slaves = ints.Skip(2).ToArray() };
            }
            return null;
        }

        // ----------------------------------------------------------------- the two runs

        /// <summary>Where the first run leaves the matrices and the equation numbers of the nodes.</summary>
        public sealed class Files
        {
            public string KMat, KT, DofsMat, DofsT;

            public static Files In(string folder, string stem, bool sparse)
            {
                string ext = sparse ? ".mtx" : ".txt";
                return new Files
                {
                    KMat = Path.Combine(folder, stem + "_Kmat" + ext),
                    KT = Path.Combine(folder, stem + "_Kt" + ext),
                    DofsMat = Path.Combine(folder, stem + "_dofs_mat.txt"),
                    DofsT = Path.Combine(folder, stem + "_dofs_t.txt"),
                };
            }

            public IEnumerable<string> All => new[] { KMat, KT, DofsMat, DofsT };
        }

        /// <summary>
        /// The first run: the model, a step with no load in which K_mat is printed, the load
        /// patterns, and a first-order step to the reference load - pseudo-time 1, which is load
        /// factor 1 - in which K_mat − K_geo is printed. First order, so the axial forces are the
        /// ones the buckling problem is defined with, and nothing has to converge.
        /// </summary>
        /// <param name="constraints">The constraint handler. Transformation folds tied dofs into the
        /// retained node exactly; Penalty keeps every dof an equation of its own, at the price of
        /// large numbers next to the small K_geo is made of.</param>
        public static List<string> ExportDeck(Deck deck, Files files, bool sparse, string constraints = "Transformation")
        {
            var lines = new List<string>(deck.Model);
            bool measure = constraints.Trim() == "Penalty";
            string analysis =
                // One Newton iteration: a single solve from no load, so the state is first order,
                // as the buckling problem defines it - and then the resisting forces at that state,
                // which Linear never asks for. ShellNLDKGQ only updates its stresses there; after a
                // Linear step it would commit the stresses of before it and have no K_geo at all.
                "numberer Plain\n" +
                "test FixedNumIter 1 0\n" +
                "algorithm Newton\n" +
                "integrator LoadControl 0.0\n" +
                "analysis Static\n";
            if (measure)
                lines.Add(
                    "\n# ---- the penalty number, from the stiffness of the model ----\n" +
                    "system FullGeneral\n" +
                    "constraints Transformation\n" +
                    analysis +
                    "catch {analyze 1}\n" +
                    "set alpaca4dN [systemSize]\n" +
                    $"if {{$alpaca4dN > {DenseLimit}}} {{ puts \"{Label} equations $alpaca4dN\"; puts \"{Label} too-large $alpaca4dN\"; exit }}\n" +
                    "set alpaca4dK [printA -ret]\n" +
                    "set alpaca4dMax 0.0\n" +
                    "for {set i 0} {$i < $alpaca4dN} {incr i} {\n" +
                    "    set d [expr {abs([lindex $alpaca4dK [expr {$i * $alpaca4dN + $i}]])}]\n" +
                    "    if {$d > $alpaca4dMax} { set alpaca4dMax $d }\n" +
                    "}\n" +
                    "unset alpaca4dK\n" +
                    "wipeAnalysis\n" +
                    $"set alpaca4dPenalty [expr {{{Write(DensePenaltyScale)} * $alpaca4dMax}}]\n" +
                    $"puts \"{Label} penalty $alpaca4dPenalty\"\n");
            lines.Add(
                "\n# ---- linear buckling: K_mat with no load ----\n" +
                "proc alpaca4dDofs {path} {\n" +
                "    set f [open $path w]\n" +
                "    foreach n [getNodeTags] { puts $f \"$n [nodeDOFs $n]\" }\n" +
                "    close $f\n" +
                "}\n" +
                $"system {(sparse ? "SparseGeneral" : "FullGeneral")}\n" +
                (measure ? "constraints Penalty $alpaca4dPenalty $alpaca4dPenalty\n" : $"constraints {constraints}\n") +
                analysis +
                $"if {{[analyze 1] != 0}} {{ puts \"{Label} failed unloaded\"; exit }}\n" +
                "set alpaca4dN [systemSize]\n" +
                $"puts \"{Label} equations $alpaca4dN\"\n" +
                (sparse ? "" : $"if {{$alpaca4dN > {DenseLimit}}} {{ puts \"{Label} too-large $alpaca4dN\"; exit }}\n") +
                PrintMatrix(files.KMat, sparse) +
                $"alpaca4dDofs {TclPath.Write(files.DofsMat)}\n" +
                "# ---- the reference load ----\n");
            lines.AddRange(deck.Patterns);
            lines.Add(
                "\n# ---- linear buckling: K_mat - K_geo under the reference load ----\n" +
                "integrator LoadControl 1.0\n" +
                $"if {{[analyze 1] != 0}} {{ puts \"{Label} failed loaded\"; exit }}\n" +
                PrintMatrix(files.KT, sparse) +
                $"alpaca4dDofs {TclPath.Write(files.DofsT)}\n" +
                $"puts \"{Label} done\"\n" +
                "wipe\n");
            return lines;
        }

        private static string PrintMatrix(string path, bool sparse)
        {
            return sparse
                ? $"printA -file {TclPath.Write(path)} -sparse 1 -precision 16\n"
                : $"set f [open {TclPath.Write(path)} w]; puts $f [printA -ret]; close $f\n";
        }

        /// <summary>
        /// A deck of two nodes that prints its matrix sparse. Builds of OpenSees after 3.8.0 write
        /// it; 3.8.0 itself writes nothing, without a word, and its version reads the same either
        /// way - so asking is the only test. See <see cref="PrintsSparse"/>.
        /// </summary>
        public static string SparseProbeDeck(string path)
        {
            return "wipe\n" +
                   "model BasicBuilder -ndm 1 -ndf 1\n" +
                   "node 1 0.0\n" +
                   "node 2 1.0\n" +
                   "fix 1 1\n" +
                   "uniaxialMaterial Elastic 1 1.0\n" +
                   "element truss 1 1 2 1.0 1\n" +
                   "system SparseGeneral\n" +
                   "constraints Plain\n" +
                   "numberer Plain\n" +
                   "algorithm Linear\n" +
                   "integrator LoadControl 0.0\n" +
                   "analysis Static\n" +
                   "analyze 1\n" +
                   $"catch {{printA -file {TclPath.Write(path)} -sparse 1 -precision 16}}\n" +
                   "wipe\n";
        }

        /// <summary>Whether the probe deck left a sparse matrix with an entry in it.</summary>
        public static bool PrintsSparse(string path)
        {
            if (!File.Exists(path))
                return false;
            return File.ReadLines(path)
                .Select(l => l.Trim())
                .Where(l => l.Length > 0 && !l.StartsWith("%"))
                .Skip(1)
                .Any();
        }

        /// <summary>What the deck said behind <see cref="Label"/>: each word after it, with what follows.</summary>
        public static Dictionary<string, string> Said(string output)
        {
            var said = new Dictionary<string, string>();
            foreach (var raw in (output ?? "").Split('\n'))
            {
                var line = raw.Trim();
                if (!line.StartsWith(Label + " ", StringComparison.Ordinal))
                    continue;
                var rest = line.Substring(Label.Length + 1).Trim();
                int space = rest.IndexOf(' ');
                if (space < 0) said[rest] = "";
                else said[rest.Substring(0, space)] = rest.Substring(space + 1).Trim();
            }
            return said;
        }

        // ----------------------------------------------------------------- reading the matrices

        /// <summary>K_mat and K_geo by equation, and the equations of every node.</summary>
        public sealed class Matrices
        {
            public SparseMatrix KMat, KGeo;
            public Dictionary<int, int[]> Dofs;
            public int Equations => KMat.Size;
            public double Asymmetry;
        }

        public static Matrices Read(Files files, bool sparse)
        {
            var kMat = sparse ? ReadSparse(files.KMat) : ReadDense(files.KMat);
            var kT = sparse ? ReadSparse(files.KT) : ReadDense(files.KT);
            var dofsMat = ReadDofs(files.DofsMat);
            var dofs = ReadDofs(files.DofsT);
            if (kMat.Size != kT.Size)
                throw new InvalidDataException($"K_mat has {kMat.Size} equations and K_mat − K_geo {kT.Size}.");

            // Adding the load patterns tells the analysis the domain changed, and it numbers the
            // equations again. The Plain numberer numbers them the same, but should they move, K_mat
            // is put in the numbering of the loaded step rather than subtracted from it misaligned.
            var map = Renumbering(dofsMat, dofs, kMat.Size);
            if (map != null)
                kMat = kMat.Renumbered(map);

            // The dense matrices come with 11 significant digits, the sparse ones with 16: what K_mat
            // and K_mat − K_geo differ by below that is the printing, not the load.
            var kGeo = SparseMatrix.Difference(kMat, kT, sparse ? 1e-13 : 1e-9);

            return new Matrices
            {
                Asymmetry = Math.Max(kMat.Asymmetry(), kGeo.Asymmetry()),
                KMat = kMat.Symmetrised(),
                KGeo = kGeo.Symmetrised(),
                Dofs = dofs,
            };
        }

        private static int[] Renumbering(Dictionary<int, int[]> from, Dictionary<int, int[]> to, int size)
        {
            bool same = from.Count == to.Count && from.All(kv => to.TryGetValue(kv.Key, out var other) && Enumerable.SequenceEqual(other, kv.Value));
            if (same)
                return null;

            var map = Enumerable.Repeat(-1, size).ToArray();
            foreach (var kv in from)
            {
                if (!to.TryGetValue(kv.Key, out var other) || other.Length != kv.Value.Length)
                    throw new InvalidDataException($"Node {kv.Key} changed its degrees of freedom between the two steps.");
                for (int d = 0; d < other.Length; d++)
                    if (kv.Value[d] >= 0 && other[d] >= 0)
                        map[kv.Value[d]] = other[d];
            }
            if (map.Any(m => m < 0) || map.Distinct().Count() != size)
                throw new InvalidDataException("The equations were numbered differently in the two steps.");
            return map;
        }

        /// <summary>A matrix printA wrote with -sparse 1: MatrixMarket coordinates, from 1.</summary>
        public static SparseMatrix ReadSparse(string path)
        {
            int size = -1, count = 0;
            int[] rows = null, cols = null;
            double[] vals = null;
            foreach (var raw in File.ReadLines(path))
            {
                var line = raw.Trim();
                if (line.Length == 0 || line.StartsWith("%"))
                    continue;
                var t = Tokens(line);
                if (size < 0)
                {
                    size = int.Parse(t[0], CultureInfo.InvariantCulture);
                    int nnz = int.Parse(t[2], CultureInfo.InvariantCulture);
                    rows = new int[nnz]; cols = new int[nnz]; vals = new double[nnz];
                    continue;
                }
                if (count == rows.Length)
                    throw new InvalidDataException($"{Path.GetFileName(path)} has more entries than its header says.");
                rows[count] = int.Parse(t[0], CultureInfo.InvariantCulture) - 1;
                cols[count] = int.Parse(t[1], CultureInfo.InvariantCulture) - 1;
                vals[count] = Number(t[2]);
                count++;
            }
            if (size < 0)
                throw new InvalidDataException($"{Path.GetFileName(path)} holds no matrix.");
            return SparseMatrix.FromEntries(size, rows, cols, vals, count);
        }

        /// <summary>A matrix printA -ret gave as a Tcl list, row by row, written out on one line.</summary>
        public static SparseMatrix ReadDense(string path)
        {
            var rows = new List<int>();
            var cols = new List<int>();
            var vals = new List<double>();
            long index = 0;
            var token = new StringBuilder(32);

            void Take()
            {
                if (token.Length == 0) return;
                double v = Number(token.ToString());
                token.Clear();
                if (v != 0.0)
                {
                    rows.Add((int)index);   // the row and column are only known once the size is
                    vals.Add(v);
                }
                index++;
            }

            using (var reader = new StreamReader(path))
            {
                var buffer = new char[1 << 16];
                int read;
                while ((read = reader.Read(buffer, 0, buffer.Length)) > 0)
                    for (int k = 0; k < read; k++)
                    {
                        char c = buffer[k];
                        if (char.IsWhiteSpace(c) || c == '{' || c == '}') Take();
                        else token.Append(c);
                    }
                Take();
            }

            int size = (int)Math.Round(Math.Sqrt(index));
            if ((long)size * size != index)
                throw new InvalidDataException($"{Path.GetFileName(path)} holds {index} numbers, which is no square matrix.");
            for (int k = 0; k < rows.Count; k++)
            {
                long at = rows[k];
                rows[k] = (int)(at / size);
                cols.Add((int)(at % size));
            }
            return SparseMatrix.FromEntries(size, rows.ToArray(), cols.ToArray(), vals.ToArray(), vals.Count);
        }

        /// <summary>"tag eq eq eq ..." per node, as alpaca4dDofs writes them.</summary>
        public static Dictionary<int, int[]> ReadDofs(string path)
        {
            var dofs = new Dictionary<int, int[]>();
            foreach (var raw in File.ReadLines(path))
            {
                var t = Tokens(raw);
                if (t.Length < 2 || !int.TryParse(t[0], out int tag))
                    continue;
                dofs[tag] = t.Skip(1).Select(s => int.Parse(s, CultureInfo.InvariantCulture)).ToArray();
            }
            return dofs;
        }

        // ----------------------------------------------------------------- mode shapes

        /// <summary>
        /// The displacement of every node of the deck in a mode, by node tag: translations and,
        /// for a six-dof node, rotations.
        ///
        /// A node's equations are what nodeDOFs gives, one per dof, -1 where it is fixed - except
        /// for a node a constraint ties to another. The Transformation handler folds those into the
        /// retained node, and nodeDOFs then lists the slave's own free dofs followed by the retained
        /// node's equations. So the free dofs of a slave are read in order and the tied ones are
        /// worked out from the retained node, the way the constraint ties them.
        /// </summary>
        /// <param name="folded">Whether the ties were folded by the Transformation handler; under
        /// Penalty every node has an equation per dof and nothing is rebuilt.</param>
        public static Dictionary<int, double[]> ModeShape(Deck deck, Dictionary<int, int[]> dofs, double[] mode, bool folded = true)
        {
            var tied = new Dictionary<int, List<(Tie tie, int[] dofs)>>();
            foreach (var tie in folded ? deck.Ties : new List<Tie>())
                foreach (int slave in tie.Slaves)
                {
                    if (!tied.TryGetValue(slave, out var list))
                        tied[slave] = list = new List<(Tie, int[])>();
                    list.Add((tie, TiedDofs(tie, NdfOf(deck, slave))));
                }

            var shape = new Dictionary<int, double[]>();
            foreach (var node in deck.Nodes.Values)
            {
                var u = new double[node.Ndf];
                if (dofs.TryGetValue(node.Tag, out var eqs))
                {
                    if (tied.TryGetValue(node.Tag, out var ties))
                    {
                        var constrained = new HashSet<int>(ties.SelectMany(x => x.dofs));
                        int at = 0;
                        for (int d = 0; d < node.Ndf; d++)
                        {
                            if (constrained.Contains(d)) continue;
                            if (at < eqs.Length && eqs[at] >= 0 && eqs[at] < mode.Length)
                                u[d] = mode[eqs[at]];
                            at++;
                        }
                    }
                    else
                    {
                        for (int d = 0; d < node.Ndf && d < eqs.Length; d++)
                            if (eqs[d] >= 0 && eqs[d] < mode.Length)
                                u[d] = mode[eqs[d]];
                    }
                }
                shape[node.Tag] = u;
            }

            // Retained nodes first; a chain of ties takes a pass per link.
            var done = new HashSet<int>(deck.Nodes.Keys.Where(t => !tied.ContainsKey(t)));
            for (int pass = 0; pass < 8 && done.Count < deck.Nodes.Count; pass++)
                foreach (var kv in tied)
                {
                    if (done.Contains(kv.Key) || !shape.ContainsKey(kv.Key)) continue;
                    if (kv.Value.Any(x => !done.Contains(x.tie.Master) || !shape.ContainsKey(x.tie.Master))) continue;
                    foreach (var (tie, _) in kv.Value)
                        Follow(deck, tie, kv.Key, shape[tie.Master], shape[kv.Key]);
                    done.Add(kv.Key);
                }

            return shape;
        }

        private static int NdfOf(Deck deck, int tag) => deck.Nodes.TryGetValue(tag, out var node) ? node.Ndf : 6;

        /// <summary>The dofs of a slave a tie constrains, from 0.</summary>
        private static int[] TiedDofs(Tie tie, int ndf)
        {
            switch (tie.Kind)
            {
                case TieKind.EqualDof:
                    return tie.Dofs.Select(d => d - 1).Where(d => d >= 0 && d < ndf).ToArray();
                case TieKind.RigidBeam:
                    return Enumerable.Range(0, ndf).ToArray();
                case TieKind.RigidBar:
                    return Enumerable.Range(0, Math.Min(3, ndf)).ToArray();
                case TieKind.RigidDiaphragm:
                    int p = tie.Perpendicular - 1;
                    var list = new List<int> { (p + 1) % 3, (p + 2) % 3 };
                    if (ndf > 3) list.Add(3 + p);
                    return list.ToArray();
            }
            return new int[0];
        }

        /// <summary>The tied dofs of the slave, from the retained node's displacement.</summary>
        private static void Follow(Deck deck, Tie tie, int slave, double[] master, double[] u)
        {
            var m = deck.Nodes[tie.Master];
            var s = deck.Nodes[slave];
            double[] r = { s.X - m.X, s.Y - m.Y, s.Z - m.Z };
            double Rot(int d) => master.Length > 3 + d ? master[3 + d] : 0.0;

            switch (tie.Kind)
            {
                case TieKind.EqualDof:
                    foreach (int d in tie.Dofs.Select(d => d - 1))
                        if (d >= 0 && d < u.Length && d < master.Length)
                            u[d] = master[d];
                    break;

                case TieKind.RigidBeam:
                    // u_s = u_m + θ_m × r, θ_s = θ_m
                    u[0] = master[0] + Rot(1) * r[2] - Rot(2) * r[1];
                    u[1] = master[1] + Rot(2) * r[0] - Rot(0) * r[2];
                    u[2] = master[2] + Rot(0) * r[1] - Rot(1) * r[0];
                    for (int d = 3; d < u.Length; d++)
                        u[d] = Rot(d - 3);
                    break;

                case TieKind.RigidBar:
                    for (int d = 0; d < 3 && d < u.Length; d++)
                        u[d] = master[d];
                    break;

                case TieKind.RigidDiaphragm:
                    // In the plane normal to p, the slave turns with the retained node about p.
                    int p = tie.Perpendicular - 1, a = (p + 1) % 3, b = (p + 2) % 3;
                    double theta = Rot(p);
                    u[a] = master[a] - theta * r[b];
                    u[b] = master[b] + theta * r[a];
                    if (u.Length > 3) u[3 + p] = theta;
                    break;
            }
        }

        /// <summary>
        /// The shape scaled so that its largest translation is 1, in model length units, and points
        /// the positive way - a buckling mode has no size of its own.
        /// </summary>
        public static void Normalise(Dictionary<int, double[]> shape)
        {
            double largest = 0.0, signed = 0.0;
            foreach (var u in shape.Values)
                for (int d = 0; d < Math.Min(3, u.Length); d++)
                    if (Math.Abs(u[d]) > largest)
                    {
                        largest = Math.Abs(u[d]);
                        signed = u[d];
                    }
            if (largest == 0.0)
                return;
            double scale = 1.0 / signed;
            foreach (var u in shape.Values)
                for (int d = 0; d < u.Length; d++)
                    u[d] *= scale;
        }

        /// <summary>
        /// The tag a deck node has in the model the analysis hands on: the model's own nodes keep
        /// theirs, the nodes splitting added follow them, and anything else - the auxiliary nodes of
        /// skewed supports - is not in it (0). The results are read by row, a node per row in tag
        /// order, so the model's nodes and the split ones have to come without a gap.
        /// </summary>
        public static int OutputTag(Deck deck, int tag, int modelNodes)
        {
            if (tag >= 1 && tag <= modelNodes)
                return tag;
            int at = deck.SplitNodes.FindIndex(n => n.Tag == tag);
            return at >= 0 ? modelNodes + 1 + at : 0;
        }

        /// <summary>
        /// The second run: the nodes alone, in the numbering of <see cref="OutputTag"/>, an MPCO
        /// recorder, and each mode set on them and recorded as a step - step 0 the first mode.
        /// </summary>
        public static List<string> ModesDeck(Deck deck, int modelNodes, IList<Dictionary<int, double[]>> shapes, string recorderPath)
        {
            var nodes = deck.Nodes.Values
                .Select(n => (node: n, tag: OutputTag(deck, n.Tag, modelNodes)))
                .Where(x => x.tag > 0)
                .OrderBy(x => x.tag)
                .ToList();

            var text = new StringBuilder();
            text.Append("wipe\n");
            int ndf = 0;
            foreach (var (node, tag) in nodes)
            {
                if (node.Ndf != ndf)
                {
                    text.Append($"model BasicBuilder -ndm 3 -ndf {node.Ndf}\n");
                    ndf = node.Ndf;
                }
                text.Append($"node {tag} {Write(node.X)} {Write(node.Y)} {Write(node.Z)}\n");
            }
            text.Append($"recorder mpco {TclPath.Write(recorderPath)} -N displacement rotation\n");

            var lines = new List<string> { text.ToString() };
            Dictionary<int, double[]> previous = null;
            for (int m = 0; m < shapes.Count; m++)
            {
                var step = new StringBuilder($"# mode {m + 1}\n");
                foreach (var (node, tag) in nodes)
                {
                    shapes[m].TryGetValue(node.Tag, out var u);
                    double[] before = null;
                    previous?.TryGetValue(node.Tag, out before);
                    for (int d = 0; d < node.Ndf; d++)
                    {
                        double v = u != null && d < u.Length ? u[d] : 0.0;
                        double was = before != null && d < before.Length ? before[d] : 0.0;
                        if (v != 0.0 || was != 0.0)
                            step.Append($"setNodeDisp {tag} {d + 1} {Write(v)} -commit\n");
                    }
                }
                step.Append("record\n");
                lines.Add(step.ToString());
                previous = shapes[m];
            }
            lines.Add("wipe\n");
            return lines;
        }

        // ----------------------------------------------------------------- the whole analysis

        /// <summary>What a buckling analysis came to.</summary>
        public sealed class Outcome
        {
            public Deck Deck;
            public bool Sparse;
            public int Equations;
            public double Asymmetry;
            public BucklingSolver.Result Solution;

            /// <summary>The shapes by deck node tag, largest translation 1; one per factor.</summary>
            public List<Dictionary<int, double[]>> Shapes = new List<Dictionary<int, double[]>>();

            /// <summary>What OpenSees printed, both runs.</summary>
            public string Log = "";

            /// <summary>Why there are no load factors; null when there are, or when the load buckles nothing.</summary>
            public string Failure;

            public double[] Factors => Solution?.Factors ?? new double[0];

            /// <summary>The constraint handler the analysis ran with.</summary>
            public string Constraints;
        }

        /// <summary>
        /// Runs OpenSees on the deck file it is given and returns what it printed and its exit code.
        /// </summary>
        public delegate (string output, string error, int exitCode) OpenSeesRunner(string deckPath);

        /// <summary>
        /// Whether this OpenSees prints a matrix sparse, which is what lifts <see cref="DenseLimit"/>.
        /// </summary>
        public static bool CanPrintSparse(string folder, OpenSeesRunner run)
        {
            string matrix = Path.Combine(folder, "alpaca4d_sparse_probe.mtx");
            string deck = Path.Combine(folder, "alpaca4d_sparse_probe.tcl");
            try
            {
                if (File.Exists(matrix)) File.Delete(matrix);
                File.WriteAllText(deck, SparseProbeDeck(matrix));
                run(deck);
                return PrintsSparse(matrix);
            }
            catch (Exception)
            {
                return false;
            }
            finally
            {
                TryDelete(matrix);
                TryDelete(deck);
            }
        }

        /// <summary>
        /// The buckling analysis of an assembled deck, start to end: the deck rewritten, the
        /// matrices printed, the problem solved, the shapes rebuilt and written to
        /// <paramref name="recorderPath"/> as steps.
        /// </summary>
        /// <param name="modelNodes">How many nodes the model itself has; see <see cref="OutputTag"/>.</param>
        /// <param name="stem">What the files of this run are called, in <paramref name="folder"/>.</param>
        public static Outcome Analyse(IList<string> tcl, int patternStart, int divisions, int modes, int modelNodes,
                                      string folder, string stem, string recorderPath, bool sparse, OpenSeesRunner run,
                                      string constraints = null)
        {
            var outcome = new Outcome { Sparse = sparse };
            var deck = outcome.Deck = Rewrite(tcl, patternStart, divisions);

            if (constraints == null)
            {
                constraints = deck.ChainedNodes.Count > 0 ? Penalty(sparse) : "Transformation";
                if (deck.ChainedNodes.Count > 0)
                    deck.Warnings.Add(
                        $"Node{(deck.ChainedNodes.Count > 1 ? "s" : "")} {string.Join(", ", deck.ChainedNodes.Take(10))}" +
                        $"{(deck.ChainedNodes.Count > 10 ? ", ..." : "")} {(deck.ChainedNodes.Count > 1 ? "are" : "is")} tied twice over, " +
                        "which OpenSees's Transformation handler gets wrong without a word, so the ties were enforced by penalty." +
                        (sparse ? "" : " With the matrices printed dense that costs some accuracy on the tied nodes."));
            }
            outcome.Constraints = constraints;

            var files = Files.In(folder, stem, sparse);
            foreach (var file in files.All)
                TryDelete(file);

            string exportPath = Path.Combine(folder, stem + ".tcl");
            WriteDeck(exportPath, ExportDeck(deck, files, sparse, constraints));
            var (output, error, _) = run(exportPath);
            outcome.Log = error + output;

            var said = Said(error + "\n" + output);
            if (said.TryGetValue("equations", out var n) && int.TryParse(n, out int equations))
                outcome.Equations = equations;

            if (said.ContainsKey("too-large"))
            {
                outcome.Failure =
                    $"The model has {outcome.Equations} equations. This OpenSees can only hand the stiffness matrices over " +
                    $"dense, {outcome.Equations}² numbers, and that is too much above {DenseLimit} equations. A build of OpenSees " +
                    "newer than 3.8.0 prints them sparse, with no such limit.";
                return outcome;
            }
            if (said.TryGetValue("failed", out var step))
            {
                outcome.Failure = step == "unloaded"
                    ? "OpenSees could not solve the model with no load: its stiffness matrix is singular. The model is a " +
                      "mechanism, or a support is missing. See log."
                    : "OpenSees could not solve the step to the reference load. See log.";
                return outcome;
            }
            if (!said.ContainsKey("done") || !File.Exists(files.KT))
            {
                outcome.Failure = "OpenSees stopped before printing the stiffness matrices. See log.";
                return outcome;
            }

            var matrices = Read(files, sparse);
            outcome.Asymmetry = matrices.Asymmetry;
            foreach (var file in files.All)
                TryDelete(file);

            try
            {
                outcome.Solution = BucklingSolver.Solve(matrices.KMat, matrices.KGeo, modes);
            }
            catch (NotPositiveDefiniteException ex)
            {
                outcome.Failure = "The stiffness matrix with no load is not positive definite" + Where(deck, matrices.Dofs, ex.Equation) +
                                  ": the model is a mechanism there, or a support is missing.";
                return outcome;
            }

            foreach (var mode in outcome.Solution.Modes)
            {
                var shape = ModeShape(deck, matrices.Dofs, mode, constraints.StartsWith("Transformation"));
                Normalise(shape);
                outcome.Shapes.Add(shape);
            }

            if (outcome.Shapes.Count > 0 && recorderPath != null)
            {
                TryDelete(recorderPath);
                string modesPath = Path.Combine(folder, stem + "_modes.tcl");
                WriteDeck(modesPath, ModesDeck(deck, modelNodes, outcome.Shapes, recorderPath));
                var (output2, error2, exit2) = run(modesPath);
                outcome.Log += error2 + output2;
                if (exit2 != 0 || !File.Exists(recorderPath))
                    outcome.Failure = "The load factors were found, but OpenSees could not write the buckled shapes. See log.";
            }

            return outcome;
        }

        /// <summary>
        /// The Penalty handler, for a deck with chained ties. The penalty number sits on the tied
        /// dofs of K_mat and K_mat − K_geo alike, and K_geo there is what is left of it in their
        /// difference. Printed to 16 digits a large number costs nothing. Printed dense, to 11, it
        /// has to be large next to the model's stiffness, to hold the tie, and small enough to leave
        /// the geometric stiffness its digits: "Penalty" alone has the deck measure the stiffness
        /// first and take <see cref="DensePenaltyScale"/> times its largest diagonal entry. On four
        /// columns under a rigid diaphragm, one of them offset by a rigid link, 10 times was 0.002 %
        /// off, 100 times 0.04 %, and 10⁴ times 4 %.
        /// </summary>
        public static string Penalty(bool sparse) => sparse ? "Penalty 1.0e12 1.0e12" : "Penalty";

        /// <summary>See <see cref="Penalty"/>.</summary>
        public const double DensePenaltyScale = 30.0;

        /// <summary>" at node 12, dof 3" for an equation, when a node has it as its own.</summary>
        private static string Where(Deck deck, Dictionary<int, int[]> dofs, int equation)
        {
            foreach (var kv in dofs.OrderBy(kv => kv.Key))
            {
                int d = Array.IndexOf(kv.Value, equation);
                if (d < 0) continue;
                if (deck.Nodes.TryGetValue(kv.Key, out var node))
                    return $" at node {kv.Key} ({Write(node.X)}, {Write(node.Y)}, {Write(node.Z)}), dof {d + 1}";
                return $" at node {kv.Key}, dof {d + 1}";
            }
            return "";
        }

        private static void WriteDeck(string path, IEnumerable<string> lines)
        {
            using (var file = new StreamWriter(File.Create(path)))
                foreach (var line in lines)
                    file.WriteLine(line);
        }

        private static void TryDelete(string path)
        {
            try
            {
                if (path != null && File.Exists(path))
                    File.Delete(path);
            }
            catch (IOException) { }
            catch (UnauthorizedAccessException) { }
        }

        // ----------------------------------------------------------------- text

        private static IEnumerable<string> Lines(string entry)
        {
            return (entry ?? "").Replace("\r", "").Split('\n').Where(l => l.Length > 0);
        }

        private static string[] Tokens(string line)
        {
            return line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
        }

        /// <summary>A flag such as -mass, as against a negative number.</summary>
        private static bool IsFlag(string token)
        {
            return token.Length > 1 && token[0] == '-' && char.IsLetter(token[1]);
        }

        private static double Number(string text)
        {
            if (double.TryParse(text, NumberStyles.Float, CultureInfo.InvariantCulture, out double v))
                return v;
            switch (text.ToLowerInvariant())
            {
                case "inf": case "+inf": return double.PositiveInfinity;
                case "-inf": return double.NegativeInfinity;
            }
            throw new FormatException($"\"{text}\" is not a number.");
        }

        private static string Write(double value)
        {
            return value.ToString("R", CultureInfo.InvariantCulture);
        }
    }
}
