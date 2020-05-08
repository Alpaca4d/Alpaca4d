import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper
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

#--------------------------------------------------------------------------
diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]
ForceOut = openSeesOutputWrapper[4]

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
        forceWrapper.append( [index, [[ Fi, Fj, Fk, Fw],[Mi, Mj,  Mk,  Mw ] ]])
    if len(item[1]) == 18: #6* numo nodi = 18 elementi quadrati
        Fi = rg.Vector3d( item[1][0], item[1][1], item[1][2] ) # risultante nodo i
        Mi = rg.Vector3d( item[1][3], item[1][4], item[1][5] )
        Fj = rg.Vector3d( item[1][6], item[1][7], item[1][8] ) # risultante nodo j
        Mj = rg.Vector3d( item[1][9], item[1][10], item[1][11] )
        Fk = rg.Vector3d( item[1][12], item[1][13], item[1][14] ) # risultante nodo k
        Mk = rg.Vector3d( item[1][15], item[1][16], item[1][17] )
        forceWrapper.append( [index, [[ Fi, Fj, Fk ],[Mi, Mj,  Mk] ]])

## Dict. for force ##
forceWrapperDict = dict( forceWrapper )
####

F, M = [],[]
tag = []

for ele in EleOut :
    eleTag = ele[0]
    eleType = ele[2][0]
    if eleType == "ShellDKGQ" :
        tag.append( eleTag )
        outputForce = forceWrapperDict.get( eleTag )
        F.append( outputForce[0] )
        M.append( outputForce[1] )
    elif eleType == "ShellDKGT" :
        tag.append( eleTag )
        outputForce = forceWrapperDict.get( eleTag )
        F.append( outputForce[0] )
        M.append( outputForce[1] )
        
tagElement = th.list_to_tree( tag )
nodalForce = th.list_to_tree( F )
nodalMoment = th.list_to_tree( M )


