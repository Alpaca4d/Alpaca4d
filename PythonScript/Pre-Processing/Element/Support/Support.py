"""Generate support for the structure.
    Inputs:
        Pos: QuadMesh representing the structural element.
        Tx: Translation in X. TRUE if it is Fixed.
        Ty: Translation in Y. TRUE if it is Fixed.
        Tz: Translation in Z. TRUE if it is Fixed.
        Rx: Rotation about the X axis. TRUE if it is Fixed.
        Ry: Rotation about the Y axis. TRUE if it is Fixed.
        Rz: Rotation about the Z axis. TRUE if it is Fixed.
    Output:
       supportWrapper: Point with constraint properties.
       """

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
    msg = "input 'Pos' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    supportWrapper = SupportWrapper(Pos, Tx, Ty, Tz, Rx, Ry, Rz)

