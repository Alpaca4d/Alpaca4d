"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.
    Output:
       tagElement : number of the tag of Beam or Truss element .
       Fx : Forces in direction X  of the Shell nodes .
       Fy : Forces in direction Y of the Shell nodes .
       Fz : Forces in direction Z  of the Shell nodes .
       Mx : Moments in direction X  of the Shell nodes .
       My : Moments in direction Y  of the Shell nodes .
       Mz : Moments in direction Z  of the Shell nodes .
       """

import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper as gh
#import System as sy #DV
import sys
import rhinoscriptsyntax as rs
from scriptcontext import doc

'''
ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name
folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
fileName = userObjectFolder + 'Alpaca'
'''
fileName = r'C:\GitHub\Alpaca4d\PythonScript\function'
sys.path.append(fileName)
# importante mettere import 'import Rhino.Geometry as rg' prima di importatre DomeFunc
import DomeFunc as dg 
#---------------------------------------------------------------------------------------#
def shellForces( AlpacaStaticOutput ):

    global tagElement
    global Fx
    global Fy
    global Fz
    global Mx
    global My
    global Mz

    diplacementWrapper = AlpacaStaticOutput[0]
    EleOut = AlpacaStaticOutput[2]
    ForceOut = AlpacaStaticOutput[4]

    pointWrapper = []
    for index,item in enumerate(diplacementWrapper):
        pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
    ## Dict. for point ##
    pointWrapperDict = dict( pointWrapper )

    forceWrapper = []
    for item in ForceOut:
        index = item[0]
        if len(item[1]) == 24: #6* numo nodi = 24 elementi quadrati
            Fi = rg.Vector3d( item[1][0], item[1][1], item[1][2] ) # risultante nodo i
            Mi = rg.Vector3d( item[1][3], item[1][4], item[1][5] )
            Fj = rg.Vector3d( item[1][6], item[1][7], item[1][8] ) # risultante nodo j
            Mj = rg.Vector3d( item[1][9], item[1][10], item[1][11] )
            Fk = rg.Vector3d( item[1][12], item[1][13], item[1][14] ) # risultante nodo k
            Mk = rg.Vector3d( item[1][15], item[1][16], item[1][17] )
            Fw = rg.Vector3d( item[1][18], item[1][19], item[1][20] ) # risultante nodo w
            Mw = rg.Vector3d( item[1][21], item[1][22], item[1][23] )
            forceOut = [[ Fi.X, Fj.X, Fk.X, Fw.X ],
                        [ Fi.Y, Fj.Y, Fk.Y, Fw.Y ],
                        [ Fi.Z, Fj.Z, Fk.Z, Fw.Z ],
                        [ Mi.X, Mj.X,  Mk.X, Mw.X ],
                        [ Mi.Y, Mj.Y, Mk.Y, Mw.Y ],
                        [ Mi.Z, Mj.Z, Mk.Z, Mw.Z ]]
            forceWrapper .append( [index, forceOut ])

        if len(item[1]) == 18: #6* numo nodi = 18 elementi quadrati
            Fi = rg.Vector3d( item[1][0], item[1][1], item[1][2] ) # risultante nodo i
            Mi = rg.Vector3d( item[1][3], item[1][4], item[1][5] )
            Fj = rg.Vector3d( item[1][6], item[1][7], item[1][8] ) # risultante nodo j
            Mj = rg.Vector3d( item[1][9], item[1][10], item[1][11] )
            Fk = rg.Vector3d( item[1][12], item[1][13], item[1][14] ) # risultante nodo k
            Mk = rg.Vector3d( item[1][15], item[1][16], item[1][17] )
            forceOut = [[ Fi.X, Fj.X, Fk.X ],
                        [ Fi.Y, Fj.Y, Fk.Y ],
                        [ Fi.Z, Fj.Z, Fk.Z ],
                        [ Mi.X, Mj.X,  Mk.X ],
                        [ Mi.Y, Mj.Y, Mk.Y ],
                        [ Mi.Z, Mj.Z, Mk.Z ]]
            forceWrapper .append( [index, forceOut ])

    ## Dict. for force ##
    forceWrapperDict = dict( forceWrapper )
    ####
    Fx, Fy, Fz, Mx, My, Mz = [],[],[],[],[],[]
    tag = []

    for ele in EleOut :
        eleTag = ele[0]
        eleType = ele[2][0]
        if eleType == "ShellDKGQ" :
            tag.append( eleTag )
            outputForce = forceWrapperDict.get( eleTag )
            Fx.append( outputForce[0] )
            Fy.append( outputForce[1] )
            Fz.append( outputForce[2] )
            Mx.append( outputForce[3] )
            My.append( outputForce[4] )
            Mz.append( outputForce[5] )
        elif eleType == "ShellDKGT" :
            tag.append( eleTag )
            outputForce = forceWrapperDict.get( eleTag )
            Fx.append( outputForce[0] )
            Fy.append( outputForce[1] )
            Fz.append( outputForce[2] )
            Mx.append( outputForce[3] )
            My.append( outputForce[4] )
            Mz.append( outputForce[5] )
            
    tagElement = th.list_to_tree( tag )
    Fx = th.list_to_tree( Fx )
    Fy = th.list_to_tree( Fy )
    Fz = th.list_to_tree( Fz )
    Mx = th.list_to_tree( Mx )
    My = th.list_to_tree( My )
    Mz = th.list_to_tree( Mz )

    return tagElement, Fx, Fy, Fz, Mx, My, Mz

checkData = True

if not AlpacaStaticOutput:
    checkData = False
    msg = "input 'AlpacaStaticOutput' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False:
    tagElement, Fx, Fy, Fz, Mx, My, Mz = shellForces( AlpacaStaticOutput )




