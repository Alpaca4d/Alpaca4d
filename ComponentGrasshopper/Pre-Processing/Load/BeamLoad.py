import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp


def uniformLoad(Force = rg.Vector3d(0,0,0), Element = None, Orientation = 0):

    if Orientation == 0:        # Values on local Axis
        localForce = Force      # Input value in kN ---> Output kN 
    else:
        midPoint = Element.PointAtNormalizedLength(0.5)
        midParameter = Element.ClosestPoint(midPoint, 0.01)[1]
        perpFrame = Element.PerpendicularFrameAt(midParameter)[1]
        xForm = rg.Transform.ChangeBasis(rg.Plane.WorldXY, perpFrame )
        localForce = Force
        localForce.Transform(xForm)

    elementLoad = Element
    loadType = 'beamUniform'

    return [[elementLoad, localForce,  "leaveEmpty", loadType, perpFrame]]

beamUniformLoad = uniformLoad(Force, Element, Orientation)