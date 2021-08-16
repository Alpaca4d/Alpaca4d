"""Generate a point load.
    Inputs:
        Force: Input force vector [kN].
        Moment: Input moment vector [kN].
        Pos: Point to apply the loads.
    Output:
       LoadWrapper: Load element.
       """

import Rhino.Geometry as rg
import Grasshopper as gh

def pointLoad(Force, Moment, Pos):

    Pos = Pos
    Force = rg.Vector3d(0,0,0) if Force is None else Force                   # Input value in kN ---> Output kN
    Moment = rg.Vector3d(0,0,0) if Moment is None else Moment                 # Input value in kNm ---> Output kNm
    loadType = "pointLoad"

    return [[Pos, Force, Moment, loadType]]

checkData = True

if Pos is None:
    checkData = False
    msg = "input 'Pos' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    LoadWrapper = pointLoad(Force, Moment, Pos)