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
                var fibers = new List<PointFiber>();
                fibers.AddRange(this.PointFibers);
                fibers.AddRange(this.Patches.SelectMany(x => x.Fibers));
                fibers.AddRange(this.Layers.SelectMany(x => x.Fibers));
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
            string tcl = "";

            tcl += $"section Fiber {this.Id} -GJ {this.GJ} {{\n";
            foreach (var element in PointFibers)
            {
                tcl += element.WriteTcl();
            }

            foreach (var element in Layers)
            {
                tcl += element.WriteTcl();
            }

            foreach (var element in Patches)
            {
                tcl += element.WriteTcl();
            }

            tcl += "}\n";

            return tcl;
        }
    }
}
