"""Generate a Timoshenko Beam element or a Truss element
    Inputs:
        Line: Straight line representing the structural element.
        CrossSection: Cross section of the element.
        Colour: Colour of the element.
        orientSection: Rotation angle in degrees about local X-axis.
        beamType:  0: Truss  1: Beam. Default is Beam.
    Output:
       beamWrapper: Beam with properties.
       """

import Rhino.Geometry as rg
from Rhino.RhinoMath import *
from System.Drawing import Color
import ghpythonlib.components as ghcomp
import Grasshopper as gh

def LineToBeam(Line, CrossSection, Colour):

    Line = Line
    if beamType == 1 or None:
        elementType = "ElasticTimoshenkoBeam"
    else:
        elementType = "Truss"

    CrossSection = CrossSection
    
    midPoint =  Line.PointAtNormalizedLength(0.5)
    parameter = Line.ClosestPoint(midPoint, 0.01)[1]
    print( parameter )
    perpFrame = ghcomp.PerpFrame( Line, parameter )
    perpFrame.Rotate(ToRadians(orientSection), perpFrame.ZAxis, perpFrame.Origin)
    vecGeomTransf = [ perpFrame.XAxis, perpFrame.YAxis, perpFrame.ZAxis ]

    colour = Colour
    Area = float(CrossSection[0])
    rho = float(CrossSection[6][4])
    massDens = Area * rho


    return [[Line, elementType, CrossSection, vecGeomTransf, colour, massDens,perpFrame]]

checkData = True

if Line is None:
    checkData = False
    msg = "input 'Line' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if CrossSection is None:
    checkData = False
    msg = "input 'CrossSection' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    beamWrapper = LineToBeam(Line, CrossSection, Colour )








