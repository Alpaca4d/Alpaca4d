"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.
        Cds : Cds =  caratteristiche delle sollecitazioni ( Italian Name) - Is Stress characteristics .
        if you enter '0' view N ( forces in direction 3 ) ;
        if you enter '1' view V1  ( forces in direction 1 ).
        if you enter '2' view V2  ( forces in direction 2 ).
        if you enter '3' view M2 ( Moments in direction 2 ) ;
        if you enter '4' view M1  ( Moments in direction 1 ).
        if you enter '5' view Mt  ( Moments in direction 3 ).
        scale: number that multiplies the real forces.
        If you don't enter anything it will be automatically scaled. 
    Output:
       diagram : view mesh outputs which represents the trend of the chosen stress .
       """

import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
#import ghpythonlib.components as ghcomp
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
def scaleAutomatic( valueMax, valueMin):
    if max( valueMax,mt.fabs(valueMin)) < 0.000000001 :
        return 0
    else :
        return 2/(max( valueMax,mt.fabs(valueMin)))

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
        #modo elegante per spostare un punto
        corner2 = rg.Point3d.Add( corner1, cdsPoint[ value-1 ] )
        corner3 = rg.Point3d.Add( corner4, cdsPoint[ value ] ) 
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
    axis1 =  rg.Vector3d( propSection[9][0][0], propSection[9][0][1], propSection[9][0][2]  )
    axis2 =  rg.Vector3d( propSection[9][1][0], propSection[9][1][1], propSection[9][1][2]  )
    axis3 =  rg.Vector3d( propSection[9][2][0], propSection[9][2][1], propSection[9][2][2]  )
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
        
    eleForceValue = [ N, V1, V2, Mt, M1, M2, versor, pointLine ]
    return   eleForceValue 

## node e nodeDisp son dictionary ##
def forceTrussValue(  ele, node, force, loadDict ):
    #---------------- WORLD PLANE ----------------------#
    WorldPlane = rg.Plane.WorldXY
    #--------- Propriety TimoshenkoBeam  ---------------#
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
def cdsView( AlpacaStaticOutput, Cds, scale ):
        
    global diagram

    diplacementWrapper = AlpacaStaticOutput[0]
    EleOut = AlpacaStaticOutput[2]
    eleLoad = AlpacaStaticOutput[3]
    ForceOut = AlpacaStaticOutput[4]
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
    V1min = min(min(V1))

    Mtmax = max(max(Mt))
    Mtmin = min(min(Mt))

    if scale == None:
        scaleN = scaleAutomatic( Nmax, Nmin )
        scaleM1 = scaleAutomatic( M1max, M1min )
        scaleM2 = scaleAutomatic( M2max, M2min )
        scaleV1 = scaleAutomatic( V1max ,V1min )
        scaleV2 = scaleAutomatic( V2max ,V2min )
        scaleMt = scaleAutomatic( Mtmax, Mtmin )

    else :
        scaleN = scale
        scaleM1 = scale
        scaleM2 = scale
        scaleV1 = scale
        scaleV2 = scale
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

    for f3,f1,f2,m3,m1,m2,vector,pointDiv in zip( N, V1, V2, Mt, M1, M2 , versorLine, linePoint ):
        versor1 = vector[0]
        versor2 = vector[1]
        versor3 = vector[2]
        PointsDivLength = pointDiv
        #print( force )
        Nval = f3
        V1val = f1
        V2val = f2
        Mtval = m3
        M1val = m1
        M2val = m2
        
        NPoint = []
        M1Point = []
        V2Point = []
        M2Point = []
        V1Point = []
        MtPoint = []
        
        for value in range( 0, len(Nval) ):
            
            NPoint.append(scaleN*versor1*Nval[value])
            M1Point.append(scaleM1*versor2*M1val[value])
            V2Point.append(scaleV2*versor2*V2val[value])
            M2Point.append(scaleM2*versor1*M2val[value])
            V1Point.append(scaleV1*versor1*V1val[value])
            MtPoint.append(scaleMt*versor1*Mtval[value])
        Nmesh = cdsMesh( PointsDivLength , Nval, NPoint, blu, rosa)
        
        M2mesh = cdsMesh( PointsDivLength , M2val, M2Point, rosso, blu)
        
        T1mesh = cdsMesh( PointsDivLength , V1val, V1Point, rosso, rosso)
        
        M1mesh = cdsMesh( PointsDivLength , M1val, M1Point, rosa, celeste)
        
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

    return diagram

checkData = True

if not AlpacaStaticOutput:
    checkData = False
    msg = "input 'AlpacaStaticOutput' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if Cds is None:
    checkData = False
    msg = " input 'Cds' failed to collect data"  
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    diagram = cdsView( AlpacaStaticOutput, Cds, scale  )