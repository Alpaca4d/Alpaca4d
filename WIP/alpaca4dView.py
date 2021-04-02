import os
import System.Drawing.Color

import Rhino.Geometry as rg

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
            len = curve.Line.Length
            section = iBeam.CrossSection.sectionBrep
            #Section at 0.0
            planeStart = curve.PerpendicularFrameAt(0.0)[1]
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
    if scale is None:
        scale = 1
    if support.Tx == True and support.Ty == True and support.Tz == True and support.Rx == True and support.Ry == True and support.Rz == True:
        solid = incastro()
    elif support.Tx == True and support.Ty == True and support.Tz == True and support.Rx == False and support.Ry == False and support.Rz == False:
        solid = cernieraXYZ()
    elif support.Tx == True and support.Ty == True and support.Tz == True and support.Rx == True and support.Ry == False :
        solid = cernieraY()
    elif support.Tx == True and support.Ty == True and support.Tz == True and support.Rx == False and support.Ry == True :
        solid = cernieraX()
    elif support.Tx == False and support.Ty == True and support.Tz == True :
        solid = carrelloX()
    elif support.Tx == True and support.Ty == False and support.Tz == True :
        solid = carrelloY()
    elif support.Tx == True and support.Ty == True and support.Tz == False :
        solid = carrelloZ()
        
    trasl = rg.Transform.Translation( rg.Vector3d(support.Pos) )
    plane = rg.Plane(support.Pos, rg.Vector3d.ZAxis)
    solid.Transform(trasl)
    bb = rg.Transform.Scale( plane, scale, scale, scale)
    solid.Transform(bb)
    return solid
