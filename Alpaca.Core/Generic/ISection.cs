﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alpaca4d.Generic
{
    public interface ISection : ISerialize
    {
        public int? Id { get; set; }
    }
}