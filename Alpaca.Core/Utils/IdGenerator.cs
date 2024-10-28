using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Alpaca4d.Core.Utils
{
    public static class IdGenerator
    {
        private static int _counter = 0;

        public static int GenerateId()
        {
            return ++_counter;
        }
    }
}
