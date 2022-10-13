﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Alpaca4d.Generic;

namespace Alpaca4d.Section
{
    public partial class PlateFiberSection : ISerialize, IMultiDimensionSection
    {
        public string SectionName { get; set; }
        public double Thickness { get; set; }
        public IMultiDimensionMaterial Material { get; set; }
        public int? Id { get; set; }

        public PlateFiberSection(string sectionName, double thickness, IMultiDimensionMaterial material)
        {
            this.SectionName = sectionName;
            this.Thickness = thickness;
            this.Material = material;
        }

        public string WriteTcl()
        {
            return $"section PlateFiber {this.Id} {this.Material.Id} {this.Thickness}\n";
        }
    }
}
