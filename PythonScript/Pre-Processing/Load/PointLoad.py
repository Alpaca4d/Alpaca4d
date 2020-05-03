import Rhino.Geometry as rg

def pointLoad(Force=rg.Vector3d(0, 0, 0), Moment=rg.Vector3d(0, 0, 0), Pos = None):

    Pos = Pos
    Force = Force                   # Input value in kN ---> Output kN
    Moment = Moment                 # Input value in kNm ---> Output kNm
    loadType = "pointLoad"

    return [[Pos, Force, Moment, loadType]]


LoadWrapper = pointLoad(Force, Moment, Pos)