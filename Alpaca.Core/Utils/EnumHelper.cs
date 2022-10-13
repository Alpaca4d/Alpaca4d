using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


using Rhino.Geometry;
using Grasshopper;
using Alpaca4d;
using HDF5CSharp;
using HDF5CSharp.DataTypes;
using Alpaca4d.Result;

namespace Alpaca4d.Helper
{
	public static class EnumHelper
	{
		public static string ResultTypeConvert(ResultType resultType)
		{
            string _resultType = "";

            if (resultType == ResultType.MODES_OF_VIBRATION_R)
            {
                _resultType = "MODES_OF_VIBRATION(R)";
            }
            else if (resultType == ResultType.MODES_OF_VIBRATION_U)
            {
                _resultType = "MODES_OF_VIBRATION(U)";
            }
            else _resultType = resultType.ToString();

            return _resultType;
        }
	}
}
