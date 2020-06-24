import Rhino.Geometry as rg
import Grasshopper as gh


def MassLoad(Pos, NodalMass):

    NodalMass = rg.Point3d(NodalMass, NodalMass, NodalMass)
    return [[Pos, NodalMass]]

checkData = True

if Pos is None:
    checkData = False
    msg = "input 'Pos' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if NodalMass is None:
    checkData = False
    msg = "input 'NodalMass' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
	Mass = MassLoad(Pos, NodalMass)