using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Section
{
    public partial class FiberSection
    {
        public int? Id { get; set; }
        public List<PointFiber> PointFibers { get; set; } = new List<PointFiber>();
        public List<Patch> Patches { get; set; } = new List<Patch>();
        public List<Layer> Layers { get; set; } = new List<Layer>();
        public List<PointFiber> Fibers
        {
            get
            {
                // Point fibres, then layers, then patches - the order WriteTcl declares
                // them in, and so the order OpenSees holds them in and reports them in.
                // These two had layers and patches the other way round, which only stayed
                // invisible while every fibre had a recorder of its own to be matched by
                // coordinate.
                var fibers = new List<PointFiber>();
                fibers.AddRange(this.PointFibers);
                fibers.AddRange(this.Layers.SelectMany(x => x.Fibers));
                fibers.AddRange(this.Patches.SelectMany(x => x.Fibers));
                var i = 0;
                foreach(var fiber in fibers)
                {
                    fiber.Index = i;
                    i++;
                }
                return fibers;
            }
        }

        public double? GJ { get; set; }
        public FiberSection()
        {
        }

        public FiberSection(List<PointFiber> pointFibers, List<Layer> layers, List<Patch> patches, double gj)
        {
            this.PointFibers = pointFibers;
            this.Layers = layers;
            this.Patches = patches;
            this.GJ = gj;
        }

        public string WriteTcl()
        {
            return WriteTcl(null);
        }

        /// <summary>
        /// The section, under <paramref name="tag"/> in place of its own Id.
        ///
        /// A deck holding a single section - the moment-curvature one - wants a known
        /// tag, and used to get one by assigning to Id. That reached back into the object
        /// the upstream component still holds and hands to everything else downstream; a
        /// tag a caller needs for the length of one deck belongs to the call, not to the
        /// section.
        /// </summary>
        public string WriteTcl(int? tag)
        {
            var sb = new StringBuilder();

            sb.Append($"section Fiber {tag ?? this.Id} -GJ {TclNumber.Write(this.GJ)} {{\n");
            foreach (var element in PointFibers)
            {
                sb.Append(element.WriteTcl());
            }

            foreach (var element in Layers)
            {
                sb.Append(element.WriteTcl());
            }

            foreach (var element in Patches)
            {
                sb.Append(element.WriteTcl());
            }

            sb.Append("}\n");

            return sb.ToString();
        }
    }
}
