import Rhino.Geometry as rg
from Rhino.RhinoMath import *
from System.Drawing import Color
import ghpythonlib.components as ghcomp

def LineToBeam(Line, CrossSection, Colour):

    line = Line
    if beamType == 1:
        elementType = "ElasticTimoshenkoBeam"
    else:
        elementType = "Truss"
        #print( elementType )
    CrossSection = CrossSection
    
    midPoint =  line.PointAtNormalizedLength(0.5)
    parameter = line.ClosestPoint(midPoint, 0.01)[1]
    print( parameter )
    perpFrame = ghcomp.PerpFrame( line, parameter )
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


    return [[line, elementType, CrossSection, vecGeomTransf, colour, massDens,perpFrame]]

beamWrapper = LineToBeam(Line, CrossSection, Colour )








