import os
import System.Drawing.Color

import Rhino.Geometry as rg
import Rhino as rc
import ghpythonlib.components as ghcomp
from collections import OrderedDict
from collections import defaultdict

import math as mt
import subprocess


# VIEW MODEL
def ViewBeam( Model, type ):
    Beam = []
    for iBeam in Model.beams:
        curve = iBeam.Crv
        color = iBeam.Colour
        if type is True:
            start =  curve.PointAtNormalizedLength(0.0)
            parameter = curve.ClosestPoint(start , 0.01)[1]
            #rg.Curve.PerpendicularFrameAt( x, parameter )[1]
            len = curve.Line.Length
            section = iBeam.CrossSection.sectionBrep
            #Section at 0.0
            planeStart = curve.PerpendicularFrameAt(parameter)[1]
            trasfom1 = rg.Transform.PlaneToPlane( rg.Plane.WorldXY, planeStart )
            profileFace = rg.Brep.Duplicate( section )
            profileFace.Transform( trasfom1 )
            #SolidBeam
            solidBeam = rg.Brep.CreateFromOffsetFace( profileFace.Faces[0], len, 0.1, False, True )
            Beam.append( [solidBeam, color] )
        else:
            Beam.append([curve, color])
    return Beam 

def ViewShell(Model, type):
    Shell = []
    for item in Model.shells:
        shell = item.Mesh
        color = item.Colour
        if type is False: 
            Shell.append([shell, color])
        else:
            point = [ rg.Point3d( ipoint ) for ipoint in item.Mesh.Vertices ]
            shellExtrude = rg.Mesh()
            thick = item.CrossSection.height
            vt = shell.Vertices[0]
            shell.FaceNormals.ComputeFaceNormals()
            fid,MPt = shell.ClosestPoint(vt,0.01)
            normalFace = shell.FaceNormals[fid]
            vectormoltiplicate = rg.Vector3d.Multiply( normalFace, thick/2 )
            PointMesh1 = [rg.Point3d.Add( ipoint, -vectormoltiplicate ) for ipoint in shell.Vertices]
            PointMesh2 = [rg.Point3d.Add( ipoint, vectormoltiplicate ) for ipoint in shell.Vertices]
            PointMesh = PointMesh1 + PointMesh2
            for jpoint in PointMesh:
                shellExtrude.Vertices.Add( jpoint )
            if len(item.indexNodes) == 4 :
                shellExtrude.Faces.AddFace( 0, 1, 2, 3 )
                shellExtrude.Faces.AddFace( 4, 5, 6, 7 )
                shellExtrude.Faces.AddFace( 0, 1, 5, 4 )
                shellExtrude.Faces.AddFace( 2, 3, 7, 6 )
                shellExtrude.Faces.AddFace( 0, 3, 7, 4 )
                shellExtrude.Faces.AddFace( 1, 2, 6, 5 )
            else: 
                shellExtrude.Faces.AddFace( 0, 1, 2 )
                shellExtrude.Faces.AddFace( 3, 4, 5 )
                shellExtrude.Faces.AddFace( 0, 1, 4, 3 )
                shellExtrude.Faces.AddFace( 1, 2, 5, 4 )
                shellExtrude.Faces.AddFace( 2, 0, 3, 5 )
                   
            Shell.append([shellExtrude, color])
    return Shell

def ViewBrick(Model):
    Brick = []
    for item in Model.bricks:
        brick = item.Mesh
        color = item.Colour
        Brick.append([brick, color])
    return Brick

# VIEW SUPPORT
#TRONCO DI PIRAMIDE
def troncoPiramide(PointBase, width, height):
    z1 = PointBase.Z
    h = -height
    ztot = z1 + h
    c = 2
    brep = rg.Brep()
    point1 = rg.Point3d( width/2, width/2, z1 )
    point2 = rg.Point3d( -width/2, width/2, z1 )
    point3 = rg.Point3d( -width/2, -width/2, z1 )
    point4 = rg.Point3d( width/2, -width/2, z1 )
    point5 = rg.Point3d( width/2*c, width/2*c, ztot )
    point6 = rg.Point3d( -width/2*c, width/2*c, ztot )
    point7 = rg.Point3d( -width/2*c, -width/2*c, ztot )
    point8 = rg.Point3d( width/2*c, -width/2*c, ztot )
    surf1 = rg.Brep.CreateFromCornerPoints( point1, point2, point3, point4, 0.01)
    surf2 = rg.Brep.CreateFromCornerPoints( point5, point6, point7, point8, 0.01)
    surf3 = rg.Brep.CreateFromCornerPoints( point1, point2, point5, point6, 0.01)
    surf4 = rg.Brep.CreateFromCornerPoints( point2, point3, point6, point7, 0.01)
    surf5 = rg.Brep.CreateFromCornerPoints( point3, point4, point7, point8, 0.01)
    surf6 = rg.Brep.CreateFromCornerPoints( point4, point1, point8, point5, 0.01)
    breps = [surf1, surf2, surf3, surf4, surf5, surf6 ]
    solid = rg.Brep.CreateSolid(breps,0.1)
    return solid

#INCASTRO
def incastro():
    plane = rg.Plane.WorldXY
    b = 0.5
    h = b/3
    widthDomain = rg.Interval(-b/2,b/2)
    rectangle = rg.Rectangle3d.ToNurbsCurve(rg.Rectangle3d( plane, widthDomain, widthDomain ))
    surface = rg.Brep.CreatePlanarBreps( rectangle, 0.1 )[0]
    solidSupport = rg.Brep.CreateFromOffsetFace( surface.Faces[0], -h, 0.1, False, True )
    return solidSupport
#CERNIERA SFERICA
def cernieraXYZ():
    plane = rg.Plane.WorldXY
    radius = 0.15
    length = radius*3.50
    center =rg.Point3d(0.0, 0.0, -radius)
    # sfera
    solid1 = rg.Brep.CreateFromSphere(rg.Sphere( center, radius))
    #tronco di piramide
    b = 0.5
    h = 0.5
    solid2 = troncoPiramide(center, b, h)[0]
    solid = rg.Brep.CreateBooleanUnion( [solid1,solid2], 0.01)[0] 
    return solid
#CERNIERA LUNGO Y
def cernieraY():
    plane = rg.Plane.WorldXY
    radius = 0.15
    length = radius*3.00
    center = rg.Point3d(0.0, 0.0, -radius)
    # cilindro
    solid = rg.Brep()
    planeZX = rg.Plane.WorldZX
    vector = rg.Vector3d( 0, -length/2 , 0 ) 
    vectorTrasl = rg.Point3d.Add( center, vector )
    trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
    planeZX.Transform( trasl )
    circle = rg.Circle(planeZX, radius)
    solid1 = rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True )  
    #tronco di piramide
    b = 0.5
    h = 0.5
    solid2 = troncoPiramide(center, b, h)[0]
    solid.Append(solid1)
    solid.Append(solid2)
    return solid
#CERNIERA LUNGO X
def cernieraX():
    plane = rg.Plane.WorldXY
    radius = 0.15
    length = radius*3.00
    center = rg.Point3d(0.0, 0.0, -radius)
    # cilindro
    solid = rg.Brep()
    planeYZ = rg.Plane.WorldYZ
    vector = rg.Vector3d( -length/2, 0 , 0 ) 
    vectorTrasl = rg.Point3d.Add( center, vector )
    trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
    planeYZ.Transform( trasl )
    circle = rg.Circle(planeYZ, radius)
    solid1 = rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True ) 
    #tronco di piramide
    b = 0.5
    h = 0.5
    solid2 = troncoPiramide(center, b, h)[0]
    solid.Append(solid1)
    solid.Append(solid2)
    return solid
#CARRELLO LUNGO Y
def carrelloY():
    plane = rg.Plane.WorldXY
    radius = 0.15
    length = radius*3.00
    center = rg.Point3d(0.0, 0.0, -radius)
    h = 0.5
    # cilindro
    solid = rg.Brep()
    planeZX = rg.Plane.WorldZX
    vector = rg.Vector3d( 0, -length/2 , -h ) 
    vectorTrasl = rg.Point3d.Add( center, vector )
    trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
    planeZX.Transform( trasl )
    circle = rg.Circle(planeZX, radius)
    cylinder = rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True )
    solid1 = rg.Brep.DuplicateBrep(cylinder)
    traslc1 = rg.Transform.Translation( -length/2, 0, 0 )
    solid1.Transform( traslc1 )
    solid2 = rg.Brep.DuplicateBrep(cylinder)
    traslc2 = rg.Transform.Translation( length/2, 0, 0 )
    solid2.Transform( traslc2 )
    #tronco di piramide
    b = 0.5
    solid3 = troncoPiramide(rg.Point3d.Origin, b, h)[0]
    solid.Append(solid1)
    solid.Append(solid2)
    solid.Append(solid3)
    return solid
#CARRELLO LUNGO X
def carrelloX():
    plane = rg.Plane.WorldXY
    radius = 0.15
    length = radius*3.5
    center = rg.Point3d(0.0, 0.0, -radius)
    h = 0.5
    # cilindro
    solid = rg.Brep()
    planeZX = rg.Plane.WorldZX
    vector = rg.Vector3d( 0, -length/2 , -h ) 
    vectorTrasl = rg.Point3d.Add( center, vector )
    trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
    planeZX.Transform( trasl )
    circle = rg.Circle(planeZX, radius)
    cylinder = rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True )
    solid1 = rg.Brep.DuplicateBrep(cylinder)
    traslc1 = rg.Transform.Translation( -length/2, 0, 0 )
    solid1.Transform( traslc1 )
    solid2 = rg.Brep.DuplicateBrep(cylinder)
    traslc2 = rg.Transform.Translation( length/2, 0, 0 )
    solid2.Transform( traslc2 )
    #tronco di piramide
    b = 0.5
    solid3 = troncoPiramide(rg.Point3d.Origin, b, h)[0]
    solid.Append(solid1)
    solid.Append(solid2)
    solid.Append(solid3)
    return solid

#CARRELLO LUNGO Y
def carrelloY():
    plane = rg.Plane.WorldXY
    radius = 0.15
    length = radius*3.50
    center = rg.Point3d(0.0, 0.0, -radius)
    h = 0.5
    # cilindro
    solid = rg.Brep()
    planeYZ = rg.Plane.WorldYZ
    vector = rg.Vector3d( -length/2, 0, -h ) 
    vectorTrasl = rg.Point3d.Add( center, vector )
    trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
    planeYZ.Transform( trasl )
    circle = rg.Circle(planeYZ, radius)
    cylinder = rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True )
    solid1 = rg.Brep.DuplicateBrep(cylinder)
    traslc1 = rg.Transform.Translation( 0, -length/2, 0 )
    solid1.Transform( traslc1 )
    solid2 = rg.Brep.DuplicateBrep(cylinder)
    traslc2 = rg.Transform.Translation( 0, length/2, 0 )
    solid2.Transform( traslc2 )
    #tronco di piramide
    b = 0.5
    solid3 = troncoPiramide(rg.Point3d.Origin, b, h)[0]
    solid.Append(solid1)
    solid.Append(solid2)
    solid.Append(solid3)
    return solid

def carrelloZ():
    plane = rg.Plane.WorldXY
    radius = 0.15
    length = radius*3.50
    center = rg.Point3d(0.0, 0.0, -radius)
    h = 0.5
    # cilindro
    solid = rg.Brep()
    planeYZ = rg.Plane.WorldYZ
    vector = rg.Vector3d( -length/2, -h-radius, +radius ) 
    vectorTrasl = rg.Point3d.Add( center, vector )
    trasl = rg.Transform.Translation( vectorTrasl.X, vectorTrasl.Y, vectorTrasl.Z ) 
    planeYZ.Transform( trasl )
    circle = rg.Circle(planeYZ, radius)
    cylinder = rg.Brep.CreateFromCylinder( rg.Cylinder(circle, length), True, True )
    solid1 = rg.Brep.DuplicateBrep(cylinder)
    traslc1 = rg.Transform.Translation( 0, 0, -length/2 )
    solid1.Transform( traslc1 )
    solid2 = rg.Brep.DuplicateBrep(cylinder)
    traslc2 = rg.Transform.Translation( 0, 0, length/2 )
    solid2.Transform( traslc2 )
    #tronco di piramide
    b = 0.5
    solid3 = troncoPiramide(rg.Point3d.Origin, b, h)[0]
    alpha = mt.radians( 90 )
    beta = mt.radians( 90 )
    gamma = mt.radians( 0)
    transf1 = rg.Transform.RotationZYZ( alpha, beta, gamma )
    solid3.Transform( transf1 )
    solid.Append(solid1)
    solid.Append(solid2)
    solid.Append(solid3)
    return solid


def Support( support, scale):
    vincoli = [ incastro(), cernieraXYZ(), cernieraY(), cernieraX(), carrelloX(), carrelloY(), carrelloZ()]
    if scale is None:
        scale = 1
    if support.Tx == True and support.Ty == True and support.Tz == True and support.Rx == True and support.Ry == True and support.Rz == True:
        solid = vincoli[0] #incastro()
    elif support.Tx == True and support.Ty == True and support.Tz == True and support.Rx == False and support.Ry == False and support.Rz == False:
        solid = vincoli[1] #cernieraXYZ()
    elif support.Tx == True and support.Ty == True and support.Tz == True and support.Rx == True and support.Ry == False :
        solid = vincoli[2] #cernieraY()
    elif support.Tx == True and support.Ty == True and support.Tz == True and support.Rx == False and support.Ry == True :
        solid = vincoli[3] #cernieraX()
    elif support.Tx == False and support.Ty == True and support.Tz == True :
        solid = vincoli[4] #carrelloX()
    elif support.Tx == True and support.Ty == False and support.Tz == True :
        solid = vincoli[5] #carrelloY()
    elif support.Tx == True and support.Ty == True and support.Tz == False :
        solid = vincoli[6] #carrelloZ()
        
    trasl = rg.Transform.Translation( rg.Vector3d(support.Pos) )
    plane = rg.Plane(support.Pos, rg.Vector3d.ZAxis)
    solid.Transform(trasl)
    bb = rg.Transform.Scale( plane, scale, scale, scale)
    solid.Transform(bb)
    return solid


def cdsMesh( beam, cdsVector, color_Positive, color_Negative):
    DivCurve = beam.Crv.DivideByCount( len(cdsVector)-1, True )
    beamPoint = [ beam.Crv.PointAt(DivCurve[index]) for index in range(len(DivCurve))]
    cdsPoint =  [ rg.Point3d.Add( ibeamPoint, icdsVector) for ibeamPoint, icdsVector in zip(beamPoint,cdsVector)]
    
    Mesh = rg.Mesh()
    for value in range( 1 , len(cdsVector)):
        mesh = rg.Mesh()
        
        corner1 = beamPoint[ value-1 ]
        corner4 = beamPoint[ value ]
        corner2 = cdsPoint[ value-1 ]
        corner3 = cdsPoint[ value ] 
        mesh.Vertices.Add( corner1 )
        mesh.Vertices.Add( corner2 )
        mesh.Vertices.Add( corner3 )
        mesh.Vertices.Add( corner4 )
        
        valor1 = cdsVector[value-1].X + cdsVector[value-1].Y + cdsVector[value-1].Z
        valor2 = cdsVector[value].X + cdsVector[value].Y + cdsVector[value].Z
        
        if valor1 >= 0:
            color1 = color_Negative
        else:
            color1 = color_Positive
            
        if valor2 > 0:
            color2 = color_Negative
        else:
            color2 = color_Positive
            
        mesh.VertexColors.Add(color1)
        mesh.VertexColors.Add(color1)
        mesh.VertexColors.Add(color2)
        mesh.VertexColors.Add(color2)
        mesh.Faces.AddFace( 0,1,2,3 )
        mesh.Normals.ComputeNormals()
        mesh.Compact()
        Mesh.Append( mesh )

    return Mesh, cdsPoint

#DEFORMED MODEL VIEW

def BeamVectorDef(Model, DictNodeDisp):
    vectorEle = []
    for item in Model.beams:
            iListvector = [ DictNodeDisp[item.iNode], DictNodeDisp[item.jNode] ]
            vectorEle.append( iListvector )
    return vectorEle
    
def ShellVectorDef(Model, DictNodeDisp):
    vectorEle = []
    for item in Model.shells:
            iListvector = [ DictNodeDisp[iIndex] for iIndex in item.indexNodes ]
            vectorEle.append( iListvector )
    return vectorEle

def BrickVectorDef(Model, DictNodeDisp):
    vectorEle = []
    for item in Model.bricks:
            iListvector = [ DictNodeDisp[iIndex] for iIndex in item.indexNodes ]
            vectorEle.append( iListvector )
    return vectorEle
#------------------------------------------------------------------------------------#
def BeamDef(Model, DictNodeDisp, c):
    beamDefModel = []
    for item in Model.beams:
        DefiNode = rg.Point3d.Add( item.Crv.PointAtStart, DictNodeDisp[item.iNode]*c )
        DefjNode = rg.Point3d.Add( item.Crv.PointAtEnd, DictNodeDisp[item.jNode]*c )
        beamDef = rg.LineCurve( DefiNode, DefjNode )
        beamDefModel.append(beamDef)
    return beamDefModel

def ShellDef(Model, DictNodeDisp, c):
    shellDefModel = []
    for item in Model.shells:
        point = [ rg.Point3d( ipoint ) for ipoint in item.Mesh.Vertices ]
        pointDef = [ rg.Point3d.Add( ipoint, DictNodeDisp[iIndex]*c ) for ipoint, iIndex in zip(point, item.indexNodes) ]
        shellDef = rg.Mesh()
        for iPointDef in pointDef:
            shellDef.Vertices.Add( iPointDef ) #0
                    
        if len(item.indexNodes) == 4 :
            shellDef.Faces.AddFace( 0, 1, 2, 3 )
        else:
            shellDef.Faces.AddFace( 0, 1, 2 )
                    
        shellDefModel.append(shellDef)
    return shellDefModel

def BrickDef(Model, DictNodeDisp, c):
    shellDefModel = []
    for item in Model.bricks:
        point = [ rg.Point3d( ipoint ) for ipoint in item.Mesh.Vertices ]
        pointDef = [ rg.Point3d.Add( ipoint, DictNodeDisp[iIndex]*c ) for ipoint, iIndex in zip(point, item.indexNodes) ]
        shellDef = rg.Mesh()
        for iPointDef in pointDef:
            shellDef.Vertices.Add( iPointDef ) #0
                    
        if len(item.indexNodes) == 8 :
            shellDef.Faces.AddFace( 0, 1, 2, 3 )
            shellDef.Faces.AddFace(0, 1, 2, 3)
            shellDef.Faces.AddFace(4, 5, 6, 7)
            shellDef.Faces.AddFace(0, 1, 5, 4)
            shellDef.Faces.AddFace(1, 2, 6, 5)
            shellDef.Faces.AddFace(2, 3, 7, 6)
            shellDef.Faces.AddFace(3, 0, 4, 7)
        else:
            shellDef.Faces.AddFace( 0, 1, 2 )
            shellDef.Faces.AddFace( 0, 1, 3 )
            shellDef.Faces.AddFace( 1, 2, 3 )
            shellDef.Faces.AddFace( 0, 2, 3 )      
        shellDefModel.append(shellDef)
    return shellDefModel
#------------------------------------------------------------------------------------#
def meshLoft( point ):
    meshEle = rg.Mesh()
    pointSection1 = point
    for i in range(0,len(pointSection1)):
        for j in range(0, len(pointSection1[0])):
            vertix = pointSection1[i][j]
            meshEle.Vertices.Add( vertix ) 
    k = len(pointSection1[0])
    for i in range(0,len(pointSection1)-1):
        for j in range(0, len(pointSection1[0])):
            if j < k-1:
                index1 = i*k + j
                index2 = (i+1)*k + j
                index3 = index2 + 1
                index4 = index1 + 1
            elif j == k-1:
                index1 = i*k + j
                index2 = (i+1)*k + j
                index3 = (i+1)*k
                index4 = i*k
            meshEle.Faces.AddFace(index1, index2, index3, index4)
            #rs.ObjectColor(scyl,(255,0,0))
    #colour = rs.CreateColor( color[0], color[1], color[2] )
    #meshEle.VertexColors.CreateMonotoneMesh( colour )
    meshElement = meshEle
    #meshElement.IsClosed(True)
    return meshElement

def BeamDefExtrude(Model, DictNodeDisp, c):
    beamDefExtrudeModel = []
    for item in Model.beams:
        pointSection = []
        DefiNode = rg.Point3d.Add( item.Crv.PointAtStart, DictNodeDisp[item.iNode]*c )
        DefjNode = rg.Point3d.Add( item.Crv.PointAtEnd, DictNodeDisp[item.jNode]*c )
        beamDef = rg.LineCurve( DefiNode, DefjNode )
        start =  beamDef.PointAtNormalizedLength(0.0)
        end =  beamDef.PointAtNormalizedLength(1)
        section = item.CrossSection.crv
        #Section at 0.0
        parameter = beamDef.ClosestPoint(start , 0.01)[1]
        planeStart = beamDef.PerpendicularFrameAt(parameter)[1]
        trasfom1 = rg.Transform.PlaneToPlane( rg.Plane.WorldXY, planeStart )
        profileFace1 = rg.Curve.Duplicate(section)
        profileFace1.Transform( trasfom1 )
        pointSection.append( rg.NurbsCurve.GrevillePoints( profileFace1, True))
        #Section at 1
        parameter = beamDef.ClosestPoint(end , 0.01)[1]
        planeEnd = beamDef.PerpendicularFrameAt(parameter)[1]
        trasfom2 = rg.Transform.PlaneToPlane( rg.Plane.WorldXY, planeEnd )
        profileFace2 = rg.Curve.Duplicate(section)
        profileFace2.Transform( trasfom2 )
        pointSection.append( rg.NurbsCurve.GrevillePoints( profileFace2, True))
        MeshBeam = meshLoft( pointSection )
        beamDefExtrudeModel.append(MeshBeam)
    return beamDefExtrudeModel

def ShellDefExtrude(Model, DictNodeDisp, c):
    shellDefExtrudeModel = []
    for item in Model.shells:
        point = [ rg.Point3d( ipoint ) for ipoint in item.Mesh.Vertices ]
        pointDef = [ rg.Point3d.Add( ipoint, DictNodeDisp[iIndex]*c ) for ipoint, iIndex in zip(point, item.indexNodes) ]
        shellDef = rg.Mesh()
        for iPointDef in pointDef:
            shellDef.Vertices.Add( iPointDef ) #0
                    
        if len(item.indexNodes) == 4 :
            shellDef.Faces.AddFace( 0, 1, 2, 3 )
        else:
            shellDef.Faces.AddFace( 0, 1, 2 )
                    
        shellExtrude = rg.Mesh()
        thick = item.CrossSection.height
        vt = shellDef.Vertices[0]
        shellDef.FaceNormals.ComputeFaceNormals()
        fid,MPt = shellDef.ClosestPoint(vt,0.01)
        normalFace = shellDef.FaceNormals[fid]
        vectormoltiplicate = rg.Vector3d.Multiply( normalFace, thick/2 )
        PointMesh1 = [rg.Point3d.Add( ipoint, -vectormoltiplicate ) for ipoint in shellDef.Vertices]
        PointMesh2 = [rg.Point3d.Add( ipoint, vectormoltiplicate ) for ipoint in shellDef.Vertices]
        PointMesh = PointMesh1 + PointMesh2
        for jpoint in PointMesh:
            shellExtrude.Vertices.Add( jpoint )
        if len(item.indexNodes) == 4 :
            shellExtrude.Faces.AddFace( 0, 1, 2, 3 )
            shellExtrude.Faces.AddFace( 4, 5, 6, 7 )
            shellExtrude.Faces.AddFace( 0, 1, 5, 4 )
            shellExtrude.Faces.AddFace( 2, 3, 7, 6 )
            shellExtrude.Faces.AddFace( 0, 3, 7, 4 )
            shellExtrude.Faces.AddFace( 1, 2, 6, 5 )
        else: 
            shellExtrude.Faces.AddFace( 0, 1, 2 )
            shellExtrude.Faces.AddFace( 3, 4, 5 )
            shellExtrude.Faces.AddFace( 0, 1, 4, 3 )
            shellExtrude.Faces.AddFace( 1, 2, 5, 4 )
            shellExtrude.Faces.AddFace( 2, 0, 3, 5 )
            
        shellDefExtrudeModel.append(shellExtrude)
    return shellDefExtrudeModel
        
            
def boundsDef( ListVector, type = None ):
    if type == None:
        type = 3
    valorList = []
    for i in ListVector:
        if type <= 0:
            valor = i.X
        elif type == 1:
            valor = i.Y
        elif type == 2:
            valor = i.Z
        elif type >= 3:
            valor = i.SquareLength #i.Length
                    
        valorList.append(valor)
    bounds = [min(valorList),max(valorList)]
    return bounds
        
def sampleColor( colorsList, value ):
    
    if value <= 0.0 :
        return colorsList[0]
    elif value >= 1.0:
        return colorsList[-1]
    else:
        tSpectrum = value*(len(colorsList)-1)
        colorID = int(mt.floor(tSpectrum))
        tLocal = tSpectrum-colorID
        
        cA = rc.Display.Color4f(colorsList[colorID])
        cB = rc.Display.Color4f(colorsList[colorID+1])
        cC = cA.BlendTo( tLocal, cB)
        blendColor = cC.AsSystemColor()
        
        return blendColor

def ColorBeamDef( BeamDef, defEleVector, bounds, ListColor, type):
    #tDomain = ghcomp.ConstructDomain( -1, 1 ) #[-1,1]
    t1 = abs(bounds[0])
    t2 = abs(bounds[1])
    modelBeamDef = []
    colorBeam = []
    for ele, vector in zip(BeamDef,defEleVector):
        n = 2 #len(defEleVector)
        divide = ele.DivideByCount( n, True )
        segmentCurve = rg.Curve.Split(ele, divide)
        modelBeamDef.append( segmentCurve )
        listColor = []
        for ivector in vector:
            if type == 0:
                valor = ivector.X
            elif type == 1:
                valor = ivector.Y
            elif type == 2:
                valor = ivector.Z
            elif type == 3:
                valor = ivector.SquareLength #ivector.Length
            Valor = (valor + t1)/(t1+t2)
            #color = ghcomp.Interpolatedata( ListColor, Valor)
            #color = rs.CreateColor( 255, 255, 0 )
            color = alpacaView.sampleColor( ListColor, Valor )
            listColor.append( color )
        colorBeam.append( listColor )
        
    return modelBeamDef, colorBeam
    
def ColorBeamDefExtrude( BeamDef, defEleVector, bounds, ListColor, type):
    #tDomain = ghcomp.ConstructDomain( -1, 1 ) #[-1,1]
    t1 = abs(bounds[0])
    t2 = abs(bounds[1])
    modelBeamDefColor = []
    for ele, vector in zip(BeamDef,defEleVector):
        nVertices = range(len(ele.Vertices))
        ele.VertexColors.Clear()
        nDivide = len(vector)
        n = int(len(nVertices)/nDivide)
        list = []
        for i in range(nDivide):
            list.append( nVertices[n*i:n*(i+1)])
            
        listColor = []
        for ivector in vector:
            if type == 0:
                valor = ivector.X
            elif type == 1:
                valor = ivector.Y
            elif type == 2:
                valor = ivector.Z
            elif type == 3:
                valor = ivector.SquareLength #ivector.Length
            Valor = (valor + t1)/(t1+t2)
            #color = ghcomp.Interpolatedata( ListColor, Valor)
            #color = rs.CreateColor( 255, 255, 0 )
            color = sampleColor( ListColor, Valor )
            listColor.append( color )
            
        for icolor, iList in zip(listColor, list):
            for iPoint in iList:
                ele.VertexColors.Add( icolor )
        modelBeamDefColor.append( ele)
    return modelBeamDefColor

def ColorShellDef( shellDef, defEleVector, bounds, ListColor, type, extrudeModel ):
    #tDomain = ghcomp.ConstructDomain( -1, 1 ) #[-1,1]
    t1 = abs(bounds[0])
    t2 = abs(bounds[1])
    modelShellDefColor = []
    for ele, vector in zip(shellDef,defEleVector):
        ele.VertexColors.Clear()
        listColor = []
        for ivector in vector:
            if type == 0:
                valor = ivector.X
            elif type == 1:
                valor = ivector.Y
            elif type == 2:
                valor = ivector.Z
            elif type == 3:
                valor = ivector.SquareLength #ivector.Length
            Valor = (valor + t1)/(t1+t2)
            #color = ghcomp.Interpolatedata( ListColor, Valor)
            #color = rs.CreateColor( 255, 255, 0 )
            color = sampleColor( ListColor, Valor )
            listColor.append( color )
        if extrudeModel is True:
            EleColor = listColor + listColor
        else:
            EleColor = listColor
        for icolor in EleColor:
            ele.VertexColors.Add( icolor )
        modelShellDefColor.append( ele)
    return modelShellDefColor

def ColorBrickDef( brickDef, defEleVector, bounds, ListColor, type):
    #tDomain = ghcomp.ConstructDomain( -1, 1 ) #[-1,1]
    t1 = abs(bounds[0])
    t2 = abs(bounds[1])
    modelBrickDefColor = []
    for ele, vector in zip(brickDef,defEleVector):
        ele.VertexColors.Clear()
        listColor = []
        for ivector in vector:
            if type == 0:
                valor = ivector.X
            elif type == 1:
                valor = ivector.Y
            elif type == 2:
                valor = ivector.Z
            elif type == 3:
                valor = ivector.SquareLength #ivector.Length
            Valor = (valor + t1)/(t1+t2)
            #color = ghcomp.Interpolatedata( ListColor, Valor)
            #color = rs.CreateColor( 255, 255, 0 )
            color = sampleColor( ListColor, Valor )
            listColor.append( color )
            EleColor = listColor
        for icolor in EleColor:
            ele.VertexColors.Add( icolor )
        modelBrickDefColor.append( ele)
    return modelBrickDefColor

