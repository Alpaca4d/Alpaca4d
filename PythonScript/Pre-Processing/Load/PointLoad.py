import Rhino.Geometry as rg

def pointLoad(Force, Moment, Pos):

    Pos = Pos
    Force = Force                   # Input value in kN ---> Output kN
    Moment = Moment                 # Input value in kNm ---> Output kNm
    loadType = "pointLoad"

    return [[Pos, Force, Moment, loadType]]

checkData = True

if Force is None:
    checkData = False
    msg = "input 'Force' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Moment is None:
    checkData = False
    msg = "input 'Moment' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Pos is None:
    checkData = False
    msg = "input 'Pos' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
	LoadWrapper = pointLoad(Force, Moment, Pos)