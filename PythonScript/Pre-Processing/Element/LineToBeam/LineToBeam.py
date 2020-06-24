import Rhino.Geometry as rg
from Rhino.RhinoMath import *
from System.Drawing import Color
import ghpythonlib.components as ghcomp
import Grasshopper as gh

def LineToBeam(Line, CrossSection, Colour):

    Line = Line
    if beamType == 1:
        elementType = "ElasticTimoshenkoBeam"
    else:
        elementType = "Truss"

    CrossSection = CrossSection
    
    midPoint =  Line.PointAtNormalizedLength(0.5)
    parameter = Line.ClosestPoint(midPoint, 0.01)[1]
    print( parameter )
    perpFrame = ghcomp.PerpFrame( Line, parameter )
    #perpFrame = line.PerpendicularFrameAt(parameter)[1]
    perpFrame.Rotate(ToRadians(orientSection), perpFrame.ZAxis, perpFrame.Origin)
    #axis1 = piano[1]
    #axis2 = piano[2]
    #axis3 = piano[3]

    #vecGeomTransfX = round(perpFrame.XAxis.X , 3 )
    #vecGeomTransfY = round(perpFrame.XAxis.Y , 3 )
    #vecGeomTransfZ = round(perpFrame.XAxis.Z , 3 )


    #vecGeomTransf = rg.Vector3d(vecGeomTransfX, vecGeomTransfY, vecGeomTransfZ)
    vecGeomTransf = [ perpFrame.XAxis, perpFrame.YAxis, perpFrame.ZAxis ]
    #print(vecGeomTransf )
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








