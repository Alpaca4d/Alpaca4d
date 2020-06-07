import Grasshopper as gh



def SupportWrapper(Pos, Tx, Ty, Tz, Rx, Ry, Rz):

    Pos = Pos

    Tx = int(False) if Tx is None else Tx
    Ty = int(False) if Ty is None else Ty
    Tz = int(False) if Tz is None else Tz
    Rx = int(False) if Rx is None else Rx
    Ry = int(False) if Ry is None else Ry
    Rz = int(False) if Rz is None else Rz

    return [[Pos, Tx, Ty, Tz, Rx, Ry, Rz]]

checkData = True

if Pos is None:
    checkData = False
    msg = "input Pos failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    supportWrapper = SupportWrapper(Pos, Tx, Ty, Tz, Rx, Ry, Rz)

