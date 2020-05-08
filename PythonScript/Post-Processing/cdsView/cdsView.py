import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import ghpythonlib.components as ghcomp
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
## node e nodeDisp son dictionary ##
def forceTimoshenkoBeam( ele, node, force, loadDict ):
    #---------------- WORLD PLANE -----------------------#
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
    axis3 = pointEnd - pointStart
    axis3.Unitize()
    axis1 =  rg.Vector3d( propSection[9][0], propSection[9][1], propSection[9][2]  )
    axis2 = rg.Vector3d.CrossProduct(axis3, axis1)
    versor = [ axis1, axis2, axis3 ]
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
    divideDistance = 0.5
    DivCurve = line.DivideByLength( divideDistance, True )
    if DivCurve == None:
        DivCurve = [ 0, Length]
        
    uniformLoad = loadDict.get( TagEle , [0,0,0])
    q1 = uniformLoad[0]
    q2 = uniformLoad[1]
    q3 = uniformLoad[2]
    pointLine = []
    N, V1, V2, Mt, M1, M2 = [], [], [], [], [], [] 
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        beamPoint = line.PointAt(DivCurve[index]) 
        pointLine.append( beamPoint )
        ## forza normale 3 ##
        Nx = F3I - q3*x
        N.append( Nx )
        ## Taglio in direzione 1 ##
        V1x = F1I - q1*x
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
        M2x = M2I + F1I*x - q1*x**2/2
        M2.append( M2x )
        
    eleForceValue = [ N, V1, V2, Mt, M1, M2, versor, pointLine ]
    return   eleForceValue 

## node e nodeDisp son dictionary ##
def forceTrussValue(  ele, node, force, loadDict ):
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
    axis3 = pointEnd - pointStart
    axis3.Unitize()
    axis1 =  rg.Vector3d( propSection[9][0], propSection[9][1], propSection[9][2]  )
    axis2 = rg.Vector3d.CrossProduct(axis3, axis1)
    versor = [ axis1, axis2, axis3 ]
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
    divideDistance = 0.5
    DivCurve = line.DivideByLength( divideDistance, True )
    if DivCurve == None:
        DivCurve = [ 0, Length]
        
    uniformLoad = loadDict.get( TagEle , [0,0,0])
    q1 = uniformLoad[0]
    q2 = uniformLoad[1]
    q3 = uniformLoad[2]
    pointLine = []
    N, V1, V2, Mt, M1, M2 = [], [], [], [], [], [] 
    #----------------------- local to global-------------------------#
    xform2 = xform.TryGetInverse()
    #----------------------------------------------------------------#
    for index, x in enumerate(DivCurve):
        beamPoint = line.PointAt(DivCurve[index]) 
        pointLine.append( beamPoint )
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
        
    eleForceValue = [ N, V1, V2, Mt, M1, M2, versor, pointLine ]
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
versorLine = []
linePoint = []
for ele in EleOut :
    eleTag = ele[0]
    eleType = ele[2][0]
    if eleType == 'ElasticTimoshenkoBeam' :
        valueTBeam = forceTimoshenkoBeam( ele, pointWrapperDict, forceWrapperDict, loadWrapperDict )
        N.append(valueTBeam[0])
        V1.append(valueTBeam[1])
        V2.append(valueTBeam[2])
        Mt.append(valueTBeam[3])
        M1.append(valueTBeam[4])
        M2.append(valueTBeam[5])
        versorLine.append(valueTBeam[6])
        linePoint.append(valueTBeam[7])
'''
    elif eleType == 'Truss' :
        valueTruss = forceTrussValue( ele, pointWrapperDict, forceWrapperDict, loadWrapperDict)
        N.append(valueTruss[0])
        V1.append(valueTruss[1])
        V2.append(valueTruss[2])
        Mt.append(valueTruss[3])
        M1.append(valueTruss[4])
        M2.append(valueTruss[5])
        versorLine.append(valueTruss[6])
        linePoint.append(valueTruss[7])
'''
#--------------------------------------------------------------#

Nmax = max(max(N))
Nmin = min(min(N))

M1max = max(max(M1))
M1min = min(min(M1))

V2max = max(max(V2))
V2min = min(min(V2))

M2max = max(max(M2))
M2min = min(min(M2))

V1max = max(max(V1))
v1min = min(min(V1))

Mtmax = max(max(Mt))
Mtmin = min(min(Mt))


def scaleAutomatic(lengthMax, valueMax, valueMin):
    if valueMax < 0.01 :
        return 0
    else :
        return lengthMax*0.2/(max( valueMax,mt.fabs(valueMin)))

if scale == None:
    scaleN = scaleAutomatic( lengthMax, Nmax, Nmin )
    scaleM = scaleAutomatic( lengthMax, max(M1max, M2max), min(M1min, M2min) )
    scaleT = scaleAutomatic( lengthMax, max(T1max, T2max), min(T1min, T2min) )
    scaleMt = scaleAutomatic( lengthMax, Mtmax, Mtmin )

else :
    scaleN = scale
    scaleT = scale
    scaleM = scale
    scaleMt = scale


########################################################

Nsurf = []
M1surf = []
V2surf = []
M2surf = []
V1surf = []
Mtsurf = []

## COLORI ##

rosa = rs.CreateColor(232,101,81)
blu = rs.CreateColor(0,0,255)
celeste = rs.CreateColor(26,180,214)
rosso = rs.CreateColor(255,0,0)
giallo = rs.CreateColor(168,232,58)
verde = rs.CreateColor(0,255,0)

## colore ##
def color( value, color1, color2 ):
    if value <= 0 :
        return color1
    else :
        return color2

## funzione che fa le mesh ##
def cdsMesh( strucPoint , cdsValue, cdsPoint, color1, color2):

    Mesh = rg.Mesh()
    for value in range( 1 , len(cdsPoint) ):
        mesh = rg.Mesh()
        
        corner1 = strucPoint[value-1]
        corner4 = strucPoint[value]
        corner2 = ghcomp.Move( corner1, cdsPoint[ value-1 ])[0]
        corner3 = ghcomp.Move( corner4, cdsPoint[ value ])[0]

        mesh.Vertices.Add( corner1 )
        mesh.Vertices.Add( corner2 )
        mesh.Vertices.Add( corner3 )
        mesh.Vertices.Add( corner4 )
        
        mesh.VertexColors.Add(color(cdsValue[ value-1 ], color1, color2))
        mesh.VertexColors.Add(color(cdsValue[ value-1 ], color1, color2))
        mesh.VertexColors.Add(color(cdsValue[ value ], color1, color2))
        mesh.VertexColors.Add(color(cdsValue[ value ], color1, color2))
        
        mesh.Faces.AddFace( 0, 1, 2,3)
        mesh.Normals.ComputeNormals()
        mesh.Compact()
        Mesh.Append( mesh)
    return Mesh

for force,vector,pointDiv in zip( [N, V1, V2, Mt, M1, M2], versorLine, linePoint ):
    versor1 = vector[0]
    versor2 = vector[1]
    versor3 = vector[2]
    PointsDivLength = pointDiv
    Nval = force[0]
    V1val = force[1]
    V2val = force[2]
    Mtval = force[3]
    M1val = force[4]
    M2val = force[5]
    
    NPoint = []
    M1Point = []
    V2Point = []
    M2Point = []
    V1Point = []
    MtPoint = []
    
    for value in range( 0, len(Nval) ):
        
        NPoint.append(scaleN*versor1*Nval[value])
        M1Point.append(scaleM*versor2*M1val[value])
        V2Point.append(scaleT*versor2*V2val[value])
        M2Point.append(scaleM*versor1*M2val[value])
        V1Point.append(scaleT*versor1*V1val[value])
        MtPoint.append(scaleMt*versor1*Mtval[value])
    Nmesh = cdsMesh( PointsDivLength , Nval, NPoint, rosa, blu)
    
    M2mesh = cdsMesh( PointsDivLength , M2val, M2Point, blu, rosso)
    
    T1mesh = cdsMesh( PointsDivLength , V1val, V1Point, rosso, rosso)
    
    M1mesh = cdsMesh( PointsDivLength , M1val, M1Point, celeste, rosa)
    
    T2mesh = cdsMesh( PointsDivLength , V2val, V2Point, giallo, giallo)
    
    Mtmesh = cdsMesh( PointsDivLength , Mtval, MtPoint, verde, verde)

## PLOT N ##
    Nsurf.append( Nmesh )    
## PLOT M2 ##
    M2surf.append( M2mesh )
## PLOT T1 ##
    V1surf.append( T1mesh )
## PLOT M1 ##
    M1surf.append( M1mesh )
## PLOT T2 ##
    V2surf.append( T2mesh )
## PLOT Mt ##
    Mtsurf.append( Mtmesh )
    
if Cds == 0:
    diagram = th.list_to_tree( Nsurf )
elif Cds == 1:
    diagram = th.list_to_tree( V1surf )
elif Cds == 2:
    diagram = th.list_to_tree( V2surf )
elif Cds == 3:
    diagram = th.list_to_tree( M2surf )
elif Cds == 4:
    diagram = th.list_to_tree( M1surf )
elif Cds == 5:
    diagram = th.list_to_tree( Mtsurf )