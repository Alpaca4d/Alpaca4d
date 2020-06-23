import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper
import ghpythonlib.components as ghcomp
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
## node e nodeDisp son dictionary ##
def forceTimoshenkoBeam( ele, node, force, loadDict, numberResults ):
    #---------------- WORLD PLANE ----------------------#
    WorldPlane = rg.Plane.WorldXY
    #--------- Propriety TimoshenkoBeam  ----------------#
    TagEle = ele[0]
    propSection = ele[2]
    indexStart = ele[1][0]
    indexEnd = ele[1][1]
    #---- traslation and rotation index start & end ------- #
    forceStart = force.get( TagEle , "never")[0]
    momentStart = force.get( TagEle , "never")[1]
    forceEnd = force.get( TagEle , "never")[2]
    momentEnd = force.get( TagEle , "never")[3]
    ##-------------------------------------------- ------------##
    pointStart = node.get( indexStart -1 , "never")
    pointEnd = node.get( indexEnd -1 , "never")
    line = rg.LineCurve( pointStart, pointEnd )
    #-------------------------versor ---------------------------#
    axis1 =  rg.Vector3d( propSection[9][0][0], propSection[9][0][1], propSection[9][0][2]  )
    axis2 =  rg.Vector3d( propSection[9][1][0], propSection[9][1][1], propSection[9][1][2]  )
    axis3 =  rg.Vector3d( propSection[9][2][0], propSection[9][2][1], propSection[9][2][2]  )
    #---------- WORLD PLANE on point start of line ---------------#
    traslPlane = rg.Transform.Translation( pointStart.X, pointStart.Y, pointStart.Z )
    WorldPlane.Transform( traslPlane )
    #-------------------------------------------------------------#
    planeStart = rg.Plane(pointStart, axis1, axis2 )
    #planeStart = rg.Plane(pointStart, axis3 )
    localPlane = planeStart
    xform = rg.Transform.ChangeBasis( WorldPlane, localPlane )
    localForceStart = rg.Point3d( forceStart )
    vectorTrasform = rg.Transform.TransformList( xform, [ forceStart, momentStart, forceEnd, momentEnd ] )
    #print( vectorTrasform[0] )
    localForceStart = vectorTrasform[0]
    F1I = localForceStart.X # spostamento in direzione dell'asse rosso 
    F2I = localForceStart.Y # spostamento in direzione dell'asse verde
    F3I = localForceStart.Z # spostamento linea d'asse
    localMomentStart = vectorTrasform[1]
    M1I = localMomentStart.X # 
    M2I = localMomentStart.Y # 
    M3I = localMomentStart.Z # 
    localForceEnd = vectorTrasform[2]
    F1J = localForceStart.X # spostamento in direzione dell'asse rosso 
    F2J = localForceStart.Y # spostamento in direzione dell'asse verde
    F3J = localForceStart.Z # spostamento linea d'asse
    localMomentEnd = vectorTrasform[3]
    M1J = localMomentStart.X # 
    M2J = localMomentStart.Y # 
    M3J = localMomentStart.Z # 
    ##------------------ displacement value -------------------------##
    Length = rg.Curve.GetLength( line )
    DivCurve = dg.linspace( 0, Length, numberResults )
    if numberResults == None:
        DivCurve = [ 0, Length]
        
    uniformLoad = loadDict.get( TagEle , [0,0,0])
    q1 = uniformLoad[0]
    q2 = uniformLoad[1]
    q3 = uniformLoad[2]
    
    N, V1, V2, Mt, M1, M2 = [], [], [], [], [], [] 
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        ## forza normale 3 ##
        Nx = F3I - q3*x
        N.append( Nx )
        ## Taglio in direzione 1 ##
        V1x = F1I + q1*x
        V1.append( V1x )
        ## Taglio in direzione 2 ##
        V2x = F2I - q2*x
        V2.append( V2x )
        ## momento torcente ##
        Mtx = M3I
        Mt.append( Mtx )
        ## Taglio in direzione 1 ##
        M1x = M1I + F2I*x - q2*x**2/2
        M1.append( M1x )
        ## Taglio in direzione 2 ##
        M2x = M2I - F1I*x - q1*x**2/2
        M2.append( M2x )
        
    eleForceValue = [ N, V1, V2, Mt, M1, M2 ]
    return   eleForceValue 

## node e nodeDisp son dictionary ##
def forceTrussValue(  ele, node, force, loadDict, numberResults ):
    #---------------- WORLD PLANE ----------------------#
    WorldPlane = rg.Plane.WorldXY
    #--------- Propriety TimoshenkoBeam  ----------------#
    TagEle = ele[0]
    propSection = ele[2]
    indexStart = ele[1][0]
    indexEnd = ele[1][1]
    #---- traslation and rotation index start & end ------- #
    forceStart = force.get( TagEle  , "never")[0]
    momentStart = force.get( TagEle  , "never")[1]
    forceEnd = force.get( TagEle , "never")[2]
    momentEnd = force.get( TagEle , "never")[3]
    ##-------------------------------------------- ------------##
    pointStart = node.get( indexStart -1 , "never")
    pointEnd = node.get( indexEnd -1 , "never")
    line = rg.LineCurve( pointStart, pointEnd )
    #-------------------------versor ---------------------------#
    axis1 =  rg.Vector3d( propSection[9][0][0], propSection[9][0][1], propSection[9][0][2]  )
    axis2 =  rg.Vector3d( propSection[9][1][0], propSection[9][1][1], propSection[9][1][2]  )
    axis3 =  rg.Vector3d( propSection[9][2][0], propSection[9][2][1], propSection[9][2][2]  )
    #---------- WORLD PLANE on point start of line ---------------#
    traslPlane = rg.Transform.Translation( pointStart.X, pointStart.Y, pointStart.Z )
    WorldPlane.Transform( traslPlane )
    #-------------------------------------------------------------#
    planeStart = rg.Plane(pointStart, axis1, axis2 )
    #planeStart = rg.Plane(pointStart, axis3 )
    localPlane = planeStart
    xform = rg.Transform.ChangeBasis( WorldPlane, localPlane )
    localForceStart = rg.Point3d( forceStart )
    vectorTrasform = rg.Transform.TransformList( xform, [ forceStart, momentStart, forceEnd, momentEnd ] )
    #print( vectorTrasform[0] )
    localForceStart = vectorTrasform[0]
    F1I = localForceStart.X # spostamento in direzione dell'asse rosso 
    F2I = localForceStart.Y # spostamento in direzione dell'asse verde
    F3I = localForceStart.Z # spostamento linea d'asse
    localMomentStart = vectorTrasform[1]
    M1I = localMomentStart.X # 
    M2I = localMomentStart.Y # 
    M3I = localMomentStart.Z # 
    localForceEnd = vectorTrasform[2]
    F1J = localForceStart.X # spostamento in direzione dell'asse rosso 
    F2J = localForceStart.Y # spostamento in direzione dell'asse verde
    F3J = localForceStart.Z # spostamento linea d'asse
    localMomentEnd = vectorTrasform[3]
    M1J = localMomentStart.X # 
    M2J = localMomentStart.Y # 
    M3J = localMomentStart.Z # 
    ##------------------ displacement value -------------------------##
    Length = rg.Curve.GetLength( line )
    DivCurve = dg.linspace( 0, Length, numberResults )
    if numberResults == None:
        DivCurve = [ 0, Length]
        
    uniformLoad = loadDict.get( TagEle , [0,0,0])
    q1 = uniformLoad[0]
    q2 = uniformLoad[1]
    q3 = uniformLoad[2]
    
    N, V1, V2, Mt, M1, M2 = [], [], [], [], [], [] 
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        ## forza normale 3 ##
        Nx = F3I - q3*x
        N.append( Nx )
        ## Taglio in direzione 1 ##
        V1x = F1I 
        V1.append( V1x )
        ## Taglio in direzione 2 ##
        V2x = F2I 
        V2.append( V2x )
        ## momento torcente ##
        Mtx = M3I
        Mt.append( Mtx )
        ## Taglio in direzione 1 ##
        M1x = M1I 
        M1.append( M1x )
        ## Taglio in direzione 2 ##
        M2x = M2I 
        M2.append( M2x )
        
    eleForceValue = [ N, V1, V2, Mt, M1, M2 ]
    return  eleForceValue

#--------------------------------------------------------------------------
diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]
eleLoad = openSeesOutputWrapper[3]
ForceOut = openSeesOutputWrapper[4]

pointWrapper = []
for index,item in enumerate(diplacementWrapper):
    pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
## Dict. for point ##
pointWrapperDict = dict( pointWrapper )

## Dict. for load ##
loadWrapperPaired = []

for item in eleLoad:
    loadWrapperPaired.append( [item[0], item[1:]] )

loadWrapperDict = dict( loadWrapperPaired )
####

forceWrapper = []
for item in ForceOut:
    index = item[0]
    if len(item[1]) == 12: # 6 nodo start e 6 nodo end
        Fi = rg.Point3d( item[1][0], item[1][1], item[1][2] ) # risultante nodo i
        Mi = rg.Point3d( item[1][3], item[1][4], item[1][5] )
        Fj = rg.Point3d( item[1][6], item[1][7], item[1][8] ) # risultante nodo j
        Mj = rg.Point3d( item[1][9], item[1][10], item[1][11] )
        forceWrapper.append( [index, [ Fi, Mi, Fj, Mj ]] )

## Dict. for force ##
forceWrapperDict = dict( forceWrapper )
####

N, V1, V2, Mt, M1, M2 = [],[],[],[],[],[]
tag = []

for ele in EleOut :
    eleTag = ele[0]
    eleType = ele[2][0]
    if eleType == 'ElasticTimoshenkoBeam' :
        tag.append( eleTag )
        valueTBeam = forceTimoshenkoBeam( ele, pointWrapperDict, forceWrapperDict, loadWrapperDict, numberResults )
        N.append(valueTBeam[0])
        V1.append(valueTBeam[1])
        V2.append(valueTBeam[2])
        Mt.append(valueTBeam[3])
        M1.append(valueTBeam[4])
        M2.append(valueTBeam[5])
    elif eleType == 'Truss' :
        tag.append( eleTag )
        valueTruss = forceTrussValue( ele, pointWrapperDict, forceWrapperDict, loadWrapperDict, numberResults )
        N.append(valueTruss[0])
        V1.append(valueTruss[1])
        V2.append(valueTruss[2])
        Mt.append(valueTruss[3])
        M1.append(valueTruss[4])
        M2.append(valueTruss[5])
        
tagElement = th.list_to_tree( tag )
N = th.list_to_tree( N )
V1 = th.list_to_tree( V1 )
V2 = th.list_to_tree( V2 )
Mt = th.list_to_tree( Mt )
M1 = th.list_to_tree( M1 )
M2 = th.list_to_tree( M2 )

