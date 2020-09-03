"""Visualize the Modal Shapes
    Inputs:
        AlpacaModalOutput: Analysed Alpaca Model.
        numberMode: number of mode to visualize.
        speed: 
        Animate: True - Animate the model.
        Reset:
        scale: Factor to multiply the modal shapes.
        direction : view relative color of the traslation:
            '0' view traslation X.
            '1' view traslation Y.
            '2' view traslation Z.
        modelExtrude: True - view extruded model.
        colorList: optional color list to remap number to colors.
    Output:
        ModelDisp: Deformed model for the selected modal shape.
"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, AlpacaModalOutput, numberMode, speed, Animate, Reset, scale, direction, modelExtrude, colorList):
        import Rhino as rc
        import Rhino.Geometry as rg
        import math as mt
        import ghpythonlib.treehelpers as th # per data tree
        import Grasshopper as gh
        import sys
        import rhinoscriptsyntax as rs
        import Rhino.Display as rd
        from scriptcontext import sticky as st
        import System.Drawing.Color
        import scriptcontext as sc
        #----------------------------------------------------------------------#
                
        def alphat( E, G, I, At ):
            return (E*I)/(G*At)
    
        ## Spostamenti e rotazioni ##
        def spostu( x, L, uI, uJ ):
            return -(-L*uI + uI*x - uJ*x)/L
            
        def spostv( x, L, vI, vJ, thetaI, thetaJ, alphay ):
            return (L**3*thetaI*x + L**3*vI - 2*L**2*thetaI*x**2 - L**2*thetaJ*x**2 + 6*L*alphay*thetaI*x - 6*L*alphay*thetaJ*x + 12*L*alphay*vI + L*thetaI*x**3 + L*thetaJ*x**3 - 3*L*vI*x**2 + 3*L*vJ*x**2 - 6*alphay*thetaI*x**2 + 6*alphay*thetaJ*x**2 - 12*alphay*vI*x + 12*alphay*vJ*x + 2*vI*x**3 - 2*vJ*x**3)/(L*(L**2 + 12*alphay))
            
        def spostw( x, L, wI, wJ, psiI, psiJ, alphaz ):
            return -(L**3*psiI*x - L**3*wI - 2*L**2*psiI*x**2 - L**2*psiJ*x**2 - 6*L*alphaz*psiI*x + 6*L*alphaz*psiJ*x + 12*L*alphaz*wI + L*psiI*x**3 + L*psiJ*x**3 + 3*L*wI*x**2 - 3*L*wJ*x**2 + 6*alphaz*psiI*x**2 - 6*alphaz*psiJ*x**2 - 12*alphaz*wI*x + 12*alphaz*wJ*x - 2*wI*x**3 + 2*wJ*x**3)/(L*(L**2 - 12*alphaz))
            
        def thetaz(x, L, vI, vJ, thetaI, thetaJ, alphay): 
            return (L**3*thetaI - 4*L**2*thetaI*x - 2*L**2*thetaJ*x + 12*L*alphay*thetaI + 3*L*thetaI*x**2 + 3*L*thetaJ*x**2 - 6*L*vI*x + 6*L*vJ*x - 12*alphay*thetaI*x + 12*alphay*thetaJ*x + 6*vI*x**2 - 6*vJ*x**2)/(L*(L**2 + 12*alphay))
            
        def phix(x, L, phiI, phiJ):
            return -(-L*phiI + phiI*x - phiJ*x)/L
    
        def psiy(x, L, wI, wJ, psiI, psiJ, alphaz): 
            return (L**3*psiI - 4*L**2*psiI*x - 2*L**2*psiJ*x - 12*L*alphaz*psiI + 3*L*psiI*x**2 + 3*L*psiJ*x**2 + 6*L*wI*x - 6*L*wJ*x + 12*alphaz*psiI*x - 12*alphaz*psiJ*x - 6*wI*x**2 + 6*wJ*x**2)/(L*(L**2 - 12*alphaz))
            
        def gammay( L, vI, vJ, thetaI, thetaJ, alphay): 
    
            return (L*thetaI + L*thetaJ + 2*vI - 2*vJ)/(L*(L**2 + 12*alphay))
            
        def gammaz( L, wI, wJ, psiI, psiJ, alphaz):
    
            return -(L*psiI + L*psiJ - 2*wI + 2*wJ)/(L*(L**2 - 12*alphaz))
    
        ##------------------------------------------------------------------------- --##
    
        def scaleAutomatic( Num , Den ):
            if Den < 0.1 :
                return Num
            else :
                return Num*1/Den
    
        def linspace(a, b, n=100):
            if n < 2:
                return b
            diff = (float(b) - a)/(n - 1)
            return [diff * i + a  for i in range(n)]
    
        ## Funzione rettangolo ##
        def AddRectangleFromCenter(plane, width, height):
            a = plane.PointAt(-width * 0.5, -height * 0.5 )
            b = plane.PointAt(-width * 0.5,  height * 0.5 )
            c = plane.PointAt( width * 0.5,  height * 0.5 )
            d = plane.PointAt( width * 0.5,  -height * 0.5 )
            #rectangle = rg.PolylineCurve( [a, b, c, d, a] )
            rectangle  = [a, b, c, d] 
            return rectangle
            
        ## Funzione cerchio ##
        def AddCircleFromCenter( plane, radius):
            t = linspace( 0 , 1.80*mt.pi, 15 )
            a = []
            for ti in t:
                x = radius*mt.cos(ti)
                y = radius*mt.sin(ti)
                a.append( plane.PointAt( x, y ) )
            #circle = rg.PolylineCurve( a )
            circle  = a 
            return circle
    
        def AddIFromCenter(plane, Bsup, tsup, Binf, tinf, H, ta, yg):
    
            p1 = plane.PointAt( -(yg - tinf), ta/2 )
            p2 = plane.PointAt( -(yg - tinf), Binf/2 )
            p3 = plane.PointAt( -yg, Binf/2 )
            p4 = plane.PointAt( -yg, -Binf/2 )
            p5 = plane.PointAt( -(yg - tinf), -Binf/2 ) 
            p6 = plane.PointAt( -(yg - tinf), -ta/2 )
            p7 = plane.PointAt( (H - yg - tsup), -ta/2)
            p8 = plane.PointAt( (H - yg - tsup), -Bsup/2 )
            p9 = plane.PointAt( (H - yg ), -Bsup/2 )
            p10 = plane.PointAt( (H - yg ), Bsup/2 )
            p11 = plane.PointAt( (H - yg - tsup), Bsup/2 )
            p12 = plane.PointAt( (H - yg - tsup), ta/2 )
    
            wirframe  = [ p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12 ] 
            return wirframe
            
        def defShellQuad( ele, node, nodeDisp, scaleDef ):
            
            eleTag = ele[0]
            eleNodeTag = ele[1]
            color = ele[2][2]
            thick = ele[2][1]
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            index4 = eleNodeTag[3]
            
            trasl1 = nodeDisp.get( index1 -1 , "never")[0]
            rotate1 = nodeDisp.get( index1 -1 , "never")[1]
            
            trasl2 = nodeDisp.get( index2 -1 , "never")[0]
            rotate2 = nodeDisp.get( index2 -1 , "never")[1]
            
            trasl3 = nodeDisp.get( index3 -1 , "never")[0]
            rotate3 = nodeDisp.get( index3 -1 , "never")[1]
            
            trasl4 = nodeDisp.get( index4 -1 , "never")[0]
            rotate4 = nodeDisp.get( index4 -1 , "never")[1]
            
            ## CREO IL MODELLO DEFORMATO  ##
            
            pointDef1 = rg.Vector3d.Clone( node.get( index1 -1 , "never") )
            pointDef2 = rg.Vector3d.Clone( node.get( index2 -1 , "never") )
            pointDef3 = rg.Vector3d.Clone( node.get( index3 -1 , "never") )
            pointDef4 = rg.Vector3d.Clone( node.get( index4 -1 , "never") )
            vectortrasl1 = rg.Transform.Translation( rg.Vector3d(trasl1.X, trasl1.Y, trasl1.Z)*scaleDef )
            pointDef1.Transform( vectortrasl1 )
            vectortrasl2 = rg.Transform.Translation( rg.Vector3d(trasl2.X, trasl2.Y, trasl2.Z)*scaleDef )
            pointDef2.Transform( vectortrasl2 )
            vectortrasl3 = rg.Transform.Translation( rg.Vector3d(trasl3.X, trasl3.Y, trasl3.Z)*scaleDef )
            pointDef3.Transform( vectortrasl3 )
            vectortrasl4 = rg.Transform.Translation( rg.Vector3d(trasl4.X, trasl4.Y, trasl4.Z)*scaleDef )
            pointDef4.Transform( vectortrasl4 )
            shellDefModel = rg.Mesh()
            shellDefModel.Vertices.Add( pointDef1 ) #0
            shellDefModel.Vertices.Add( pointDef2 ) #1
            shellDefModel.Vertices.Add( pointDef3 ) #2
            shellDefModel.Vertices.Add( pointDef4 ) #3
            
            
            shellDefModel.Faces.AddFace(0, 1, 2, 3)
            colour = rs.CreateColor( color[0], color[1], color[2] )
            shellDefModel.VertexColors.CreateMonotoneMesh( colour )
    
            vt = shellDefModel.Vertices
            shellDefModel.FaceNormals.ComputeFaceNormals()
            fid,MPt = shellDefModel.ClosestPoint(vt[0],0.01)
            normalFace = shellDefModel.FaceNormals[fid]
            vectormoltiplicate = rg.Vector3d.Multiply( -normalFace, thick/2 )
            trasl = rg.Transform.Translation( vectormoltiplicate )
            moveShell = rg.Mesh.DuplicateMesh(shellDefModel)
            moveShell.Transform( trasl )
            extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
            return  [shellDefModel,[trasl1, trasl2, trasl3, trasl4], [rotate1, rotate2, rotate3, rotate4], extrudeShell ]
    
        def defShellTriangle( ele, node, nodeDisp, scaleDef ):
            
            eleTag = ele[0]
            eleNodeTag = ele[1]
            color = ele[2][2]
            thick = ele[2][1]
            
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            
            trasl1 = nodeDisp.get( index1 -1 , "never")[0]
            rotate1 = nodeDisp.get( index1 -1 , "never")[1]
            
            trasl2 = nodeDisp.get( index2 -1 , "never")[0]
            rotate2 = nodeDisp.get( index2 -1 , "never")[1]
            
            trasl3 = nodeDisp.get( index3 -1 , "never")[0]
            rotate3 = nodeDisp.get( index3 -1 , "never")[1]
            
            ## CREO IL MODELLO DEFORMATO  ##
            pointDef1 = rg.Point3d.Clone( node.get( index1 -1 , "never") )
            pointDef2 = rg.Point3d.Clone( node.get( index2 -1 , "never") )
            pointDef3 = rg.Point3d.Clone( node.get( index3 -1 , "never") )
            vectortrasl1 = rg.Transform.Translation( rg.Vector3d(trasl1.X, trasl1.Y, trasl1.Z)*scaleDef )
            pointDef1.Transform( vectortrasl1 )
            vectortrasl2 = rg.Transform.Translation( rg.Vector3d(trasl2.X, trasl2.Y, trasl2.Z)*scaleDef )
            pointDef2.Transform( vectortrasl2 )
            vectortrasl3 = rg.Transform.Translation( rg.Vector3d(trasl3.X, trasl3.Y, trasl3.Z)*scaleDef )
            pointDef3.Transform( vectortrasl3 )
            shellDefModel = rg.Mesh()
            shellDefModel.Vertices.Add( pointDef1 ) #0
            shellDefModel.Vertices.Add( pointDef2 ) #1
            shellDefModel.Vertices.Add( pointDef3 ) #2
            
            shellDefModel.Faces.AddFace(0, 1, 2)
            colour = rs.CreateColor( color[0], color[1], color[2] )
            vt = shellDefModel.Vertices
            shellDefModel.FaceNormals.ComputeFaceNormals()
            fid,MPt = shellDefModel.ClosestPoint(vt[0],0.01)
            normalFace = shellDefModel.FaceNormals[fid]
            vectormoltiplicate = rg.Vector3d.Multiply( -normalFace, thick/2 )
            trasl = rg.Transform.Translation( vectormoltiplicate )
            moveShell = rg.Mesh.DuplicateMesh(shellDefModel)
            moveShell.Transform( trasl )
            extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
            return  [shellDefModel,[trasl1, trasl2, trasl3], [rotate1, rotate2, rotate3], extrudeShell ]
    
        def defSolid( ele, node, nodeDisp, scaleDef ):
            
            eleTag = ele[0]
            eleNodeTag = ele[1]
            color = ele[2][1]
            thick = ele[2][1]
            #print( eleNodeTag )
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            index4 = eleNodeTag[3]
            index5 = eleNodeTag[4]
            index6 = eleNodeTag[5]
            index7 = eleNodeTag[6]
            index8 = eleNodeTag[7]
            
            trasl1 = nodeDisp.get( index1 -1 , "never")
            trasl2 = nodeDisp.get( index2 -1 , "never")
            trasl3 = nodeDisp.get( index3 -1 , "never")
            trasl4 = nodeDisp.get( index4 -1 , "never")
            trasl5 = nodeDisp.get( index5 -1 , "never")
            trasl6 = nodeDisp.get( index6 -1 , "never")
            trasl7 = nodeDisp.get( index7 -1 , "never")
            trasl8 = nodeDisp.get( index8 -1 , "never")
            
            ## CREO IL MODELLO DEFORMATO  ##
            pointDef1 = rg.Point3d.Clone( node.get( index1 -1 , "never") )
            pointDef2 = rg.Point3d.Clone( node.get( index2 -1 , "never") )
            pointDef3 = rg.Point3d.Clone( node.get( index3 -1 , "never") )
            pointDef4 = rg.Point3d.Clone( node.get( index4 -1 , "never") )
            pointDef5 = rg.Point3d.Clone( node.get( index5 -1 , "never") )
            pointDef6 = rg.Point3d.Clone( node.get( index6 -1 , "never") )
            pointDef7 = rg.Point3d.Clone( node.get( index7 -1 , "never") )
            pointDef8 = rg.Point3d.Clone( node.get( index8 -1 , "never") )
            vectortrasl1 = rg.Transform.Translation( rg.Vector3d(trasl1.X, trasl1.Y, trasl1.Z)*scaleDef )
            pointDef1.Transform( vectortrasl1 )
            vectortrasl2 = rg.Transform.Translation( rg.Vector3d(trasl2.X, trasl2.Y, trasl2.Z)*scaleDef )
            pointDef2.Transform( vectortrasl2 )
            vectortrasl3 = rg.Transform.Translation( rg.Vector3d(trasl3.X, trasl3.Y, trasl3.Z)*scaleDef )
            pointDef3.Transform( vectortrasl3 )
            vectortrasl4 = rg.Transform.Translation( rg.Vector3d(trasl4.X, trasl4.Y, trasl4.Z)*scaleDef )
            pointDef4.Transform( vectortrasl4 )
            vectortrasl5 = rg.Transform.Translation( rg.Vector3d(trasl5.X, trasl5.Y, trasl5.Z)*scaleDef )
            pointDef5.Transform( vectortrasl1 )
            vectortrasl6 = rg.Transform.Translation( rg.Vector3d(trasl6.X, trasl6.Y, trasl6.Z)*scaleDef )
            pointDef6.Transform( vectortrasl2 )
            vectortrasl7 = rg.Transform.Translation( rg.Vector3d(trasl7.X, trasl7.Y, trasl7.Z)*scaleDef )
            pointDef7.Transform( vectortrasl3 )
            vectortrasl8 = rg.Transform.Translation( rg.Vector3d(trasl8.X, trasl8.Y, trasl8.Z)*scaleDef )
            pointDef8.Transform( vectortrasl4 )
            
            shellDefModel = rg.Mesh()
            shellDefModel.Vertices.Add( pointDef1 ) #0
            shellDefModel.Vertices.Add( pointDef2 ) #1
            shellDefModel.Vertices.Add( pointDef3 ) #2
            shellDefModel.Vertices.Add( pointDef4 ) #3
            shellDefModel.Vertices.Add( pointDef5 ) #4
            shellDefModel.Vertices.Add( pointDef6 ) #5
            shellDefModel.Vertices.Add( pointDef7 ) #6
            shellDefModel.Vertices.Add( pointDef8 ) #7
    
            shellDefModel.Faces.AddFace(0, 1, 2, 3)
            shellDefModel.Faces.AddFace(4, 5, 6, 7)
            shellDefModel.Faces.AddFace(0, 1, 5, 4)
            shellDefModel.Faces.AddFace(1, 2, 6, 5)
            shellDefModel.Faces.AddFace(2, 3, 7, 6)
            shellDefModel.Faces.AddFace(3, 0, 4, 7)
            
            colour = rs.CreateColor( color[0], color[1], color[2] )
            shellDefModel.VertexColors.CreateMonotoneMesh( colour )
            return  [shellDefModel,[trasl1, trasl2, trasl3,trasl4, trasl5, trasl6, trasl7, trasl8 ]]
    
        def defTetraSolid( ele, node, nodeDisp, scaleDef ):
            
            eleTag = ele[0]
            eleNodeTag = ele[1]
            color = ele[2][1]
            #print( eleNodeTag )
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            index4 = eleNodeTag[3]
            
            trasl1 = nodeDisp.get( index1 -1 , "never")
            trasl2 = nodeDisp.get( index2 -1 , "never")
            trasl3 = nodeDisp.get( index3 -1 , "never")
            trasl4 = nodeDisp.get( index4 -1 , "never")
            
            ## CREO IL MODELLO DEFORMATO  ##
            pointDef1 = rg.Point3d.Clone( node.get( index1 -1 , "never") )
            pointDef2 = rg.Point3d.Clone( node.get( index2 -1 , "never") )
            pointDef3 = rg.Point3d.Clone( node.get( index3 -1 , "never") )
            pointDef4 = rg.Point3d.Clone( node.get( index4 -1 , "never") )
            
            vectortrasl1 = rg.Transform.Translation( rg.Vector3d(trasl1.X, trasl1.Y, trasl1.Z)*scaleDef )
            pointDef1.Transform( vectortrasl1 )
            vectortrasl2 = rg.Transform.Translation( rg.Vector3d(trasl2.X, trasl2.Y, trasl2.Z)*scaleDef )
            pointDef2.Transform( vectortrasl2 )
            vectortrasl3 = rg.Transform.Translation( rg.Vector3d(trasl3.X, trasl3.Y, trasl3.Z)*scaleDef )
            pointDef3.Transform( vectortrasl3 )
            vectortrasl4 = rg.Transform.Translation( rg.Vector3d(trasl4.X, trasl4.Y, trasl4.Z)*scaleDef )
            pointDef4.Transform( vectortrasl4 )
    
            shellDefModel = rg.Mesh()
            shellDefModel.Vertices.Add( pointDef1 ) #0
            shellDefModel.Vertices.Add( pointDef2 ) #1
            shellDefModel.Vertices.Add( pointDef3 ) #2
            shellDefModel.Vertices.Add( pointDef4 ) #3
            
            
            shellDefModel.Faces.AddFace( 0, 1, 2 )
            shellDefModel.Faces.AddFace( 0, 1, 3 )
            shellDefModel.Faces.AddFace( 1, 2, 3 )
            shellDefModel.Faces.AddFace( 0, 2, 3 )
            colour = rs.CreateColor( color[0], color[1], color[2] )
            shellDefModel.VertexColors.CreateMonotoneMesh( colour )
            
            return  [shellDefModel,[trasl1, trasl2, trasl3, trasl4]]
        ## node e nodeDisp son dictionary ##
        def defValueTimoshenkoBeam( ele, node, nodeDisp, scaleDef ):
            #---------------- WORLD PLANE ----------------------#
            WorldPlane = rg.Plane.WorldXY
            #--------- Propriety TimoshenkoBeam  ----------------#
            TagEle = ele[0]
            propSection = ele[2]
            indexStart = ele[1][0]
            indexEnd = ele[1][1]
            color = propSection[12]
            E = propSection[1]
            G = propSection[2]
            A = propSection[3]
            Avz = propSection[4]
            Avy = propSection[5]
            Jxx = propSection[6]
            Iy = propSection[7]
            Iz = propSection[8]
            #---- traslation and rotation index start & end ------- #
            traslStart = nodeDisp.get( indexStart -1 , "never")[0]
            rotateStart = nodeDisp.get( indexStart -1 , "never")[1]
            traslEnd = nodeDisp.get( indexEnd -1 , "never")[0]
            rotateEnd = nodeDisp.get( indexEnd -1 , "never")[1]
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
            localTraslStart = rg.Vector3d( traslStart )
            vectorTrasform = rg.Transform.TransformList( xform, [ traslStart, rotateStart, traslEnd, rotateEnd ] )
            #print( vectorTrasform[0] )
            localTraslStart = vectorTrasform[0]
            uI1 = localTraslStart.X # spostamento in direzione dell'asse rosso 
            uI2 = localTraslStart.Y # spostamento in direzione dell'asse verde
            uI3 = localTraslStart.Z # spostamento linea d'asse
            localRotStart = vectorTrasform[1]
            rI1 = localRotStart.X # 
            rI2 = localRotStart.Y # 
            rI3 = localRotStart.Z # 
            localTraslEnd = vectorTrasform[2]
            uJ1 = localTraslEnd.X # spostamento in direzione dell'asse rosso 
            uJ2 = localTraslEnd.Y # spostamento in direzione dell'asse verde
            uJ3 = localTraslEnd.Z # spostamento linea d'asse
            localRotEnd = vectorTrasform[3]
            rJ1 = localRotEnd[0] #  
            rJ2 = localRotEnd[1]  # 
            rJ3 = localRotEnd[2]  # 
            ##------------------ displacement value -------------------------##
            Length = rg.Curve.GetLength( line )
            segmentCount = Length/0.5
            DivCurve = line.DivideByCount( segmentCount, True )
            if DivCurve == None:
                DivCurve = [ 0, Length]
                
            #s = dg.linspace(0,Length, len(PointsDivLength))
            AlphaY = alphat( E, G, Iy, Avz )
            AlphaZ = alphat( E, G, Iz, Avy )
            
            globalTransVector = []
            globalRotVector = []
            defPoint = []
            defSection = []
            #----------------------- local to global-------------------------#
            xform2 = xform.TryGetInverse()
            #----------------------------------------------------------------#
            for index, x in enumerate(DivCurve):
                beamPoint = line.PointAt(DivCurve[index]) 
                ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 3 ##
                u3 = spostu(x, Length, uI3, uJ3)
                u3Vector = u3*axis3
                ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 1 ##
                v1 =  spostv(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
                v1Vector = v1*axis1 
                ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 2 ##
                v2 =  spostw(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
                v2Vector = v2*axis2 
                
                ## RISULTANTE SPOSTAMENTI ##
                transResult = v1Vector + v2Vector + u3Vector
                
                r2x =  thetaz(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
                r1x =  psiy(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
                r3x = phix(x, Length, rI3, rJ3)
                
                rotResult = r1x*axis1 + r2x*axis2 + r3x*axis3
                
                trasl = rg.Transform.Translation( transResult*scaleDef )
                beamPoint.Transform( trasl )
                defPoint.append( beamPoint )
                
                sectionPlane = rg.Plane( beamPoint, axis1, axis2 )
                sectionPlane.Rotate( scaleDef*r1x, axis1, beamPoint )
                sectionPlane.Rotate( scaleDef*r2x, axis2, beamPoint )
                sectionPlane.Rotate( scaleDef*r3x, axis3, beamPoint )
                if dimSection[0] == 'rectangular' :
                    width, height = dimSection[1], dimSection[2]
                    section = AddRectangleFromCenter( sectionPlane, width, height )
                    defSection.append( section )
                elif dimSection[0] == 'circular' :
                    radius1  = dimSection[1]/2
                    radius2  = dimSection[1]/2 - dimSection[2]
                    section1 = AddCircleFromCenter( sectionPlane, radius1 )
                    if (radius1 - radius2 ) == 0 :
                        defSection.append( section1 )
                    else :
                        section2 = AddCircleFromCenter( sectionPlane, radius2 )
                        defSection.append( [ section1, section2 ] )
                elif dimSection[0] == 'doubleT' :
                    Bsup = dimSection[1]
                    tsup = dimSection[2]
                    Binf = dimSection[3]
                    tinf = dimSection[4]
                    H =  dimSection[5]
                    ta =  dimSection[6]
                    yg =  dimSection[7]
                    section = AddIFromCenter( sectionPlane, Bsup, tsup, Binf, tinf, H, ta, yg )
                    defSection.append( section )
                elif dimSection[0] == 'Generic' :
                    radius  = dimSection[1]
                    section = AddCircleFromCenter( sectionPlane, radius )
                    defSection.append( section )
            
                globalTrasl = rg.Vector3d( transResult ) 
                globalTrasl.Transform(xform2[1]) 
                globalTrasl.Transform(xform)
                globalTransVector.append( globalTrasl )
    
           
            defpolyline = rg.PolylineCurve( defPoint )
    
            if dimSection[0] == 'circular' :
                radius1  = dimSection[1]/2
                radius2  = dimSection[1]/2 - dimSection[2]
                if (radius1 - radius2 ) == 0:
                    meshdef = meshLoft3( defSection,  color )
    
                else :
                    defSection1 = [row[0] for row in defSection ]
                    defSection2 = [row[1] for row in defSection ]
                    meshdef = meshLoft3( defSection1,  color )
                    meshdef.Append( meshLoft3( defSection2,  color ) )
                    print( meshdef )
    
            else  :
                meshdef = meshLoft3( defSection,  color )
            return  [  defpolyline, meshdef ,  globalTransVector, globalRotVector ] 
    
        ## node e nodeDisp son dictionary ##
        def defTruss( ele, node, nodeDisp, scale ):
            WorldPlane = rg.Plane.WorldXY
            TagEle = ele[0]
            propSection = ele[2]
            color = propSection[12]
            indexStart = ele[1][0]
            indexEnd = ele[1][1]
            E = propSection[1]
            A = propSection[3]
            
            traslStart = nodeDisp.get( indexStart -1 , "never")
            traslEnd = nodeDisp.get( indexEnd -1 , "never")
            if len( traslStart ) == 2:
                traslStart = nodeDisp.get( indexStart -1 , "never")[0]
                traslEnd = nodeDisp.get( indexEnd -1 , "never")[0]
            pointStart = node.get( indexStart -1 , "never")
            pointEnd = node.get( indexEnd -1 , "never")
            #print( traslStart[1] )
            line = rg.LineCurve( pointStart,  pointEnd )
    
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
            localTraslStart = rg.Vector3d( traslStart )
            vectorTrasform = rg.Transform.TransformList( xform, [ traslStart , traslEnd ] )
            #print( vectorTrasform[0] )
            localTraslStart = vectorTrasform[0]
            uI1 = localTraslStart.X # spostamento in direzione dell'asse rosso 
            uI2 = localTraslStart.Y # spostamento in direzione dell'asse verde
            uI3 = localTraslStart.Z # spostamento linea d'asse
            localTraslEnd = vectorTrasform[1]
            uJ1 = localTraslEnd.X # spostamento in direzione dell'asse rosso 
            uJ2 = localTraslEnd.Y # spostamento in direzione dell'asse verde
            uJ3 = localTraslEnd.Z # spostamento linea d'asse
            ##-------------- displacement value -------------------------##
            Length = rg.Curve.GetLength( line )
            segmentCount = Length/0.5
            DivCurve = line.DivideByCount( segmentCount, True )
            if DivCurve == None:
                DivCurve = [ 0, Length]
            defPoint = []
            defSection = []
            globalTransVector = []
            #----------------------- local to global-------------------------#
            xform2 = xform.TryGetInverse()
            #----------------------------------------------------------------#
            for index, x in enumerate(DivCurve):
                beamPoint = line.PointAt(DivCurve[index]) 
                ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 3 ##
                u3 = spostu(x, Length, uI3, uJ3)
                u3Vector = u3*axis3
                ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 1 ##
                v1 =  x*( uJ1 - uI1 )/Length + uI1
                v1Vector = v1*axis1 
                ## SPOSTAMENTO IN DIREZIONE DELL' ASSE 2 ##
                v2 =  x*( uJ2 - uI2 )/Length + uI2
                v2Vector = v2*axis2 
                ## RISULTANTE SPOSTAMENTI ##
                transResult = v1Vector + v2Vector + u3Vector
                trasl = rg.Transform.Translation( transResult*scale )
                beamPoint.Transform( trasl )
                defPoint.append( beamPoint )
                sectionPlane = rg.Plane( beamPoint, axis1, axis2 )
                if dimSection[0] == 'rectangular' :
                    width, height = dimSection[1], dimSection[2]
                    section = AddRectangleFromCenter( sectionPlane, width, height )
                    defSection.append( section )
                elif dimSection[0] == 'circular' :
                    radius1  = dimSection[1]/2
                    radius2  = dimSection[1]/2 - dimSection[2]
                    section1 = AddCircleFromCenter( sectionPlane, radius1 )
                    if (radius1 - radius2 ) == 0 :
                        defSection.append( section1 )
                    else :
                        section2 = AddCircleFromCenter( sectionPlane, radius2 )
                        defSection.append( [ section1, section2 ] )
                elif dimSection[0] == 'doubleT' :
                    Bsup = dimSection[1]
                    tsup = dimSection[2]
                    Binf = dimSection[3]
                    tinf = dimSection[4]
                    H =  dimSection[5]
                    ta =  dimSection[6]
                    yg =  dimSection[7]
                    section = AddIFromCenter( sectionPlane, Bsup, tsup, Binf, tinf, H, ta, yg )
                    defSection.append( section )
                elif dimSection[0] == 'Generic' :
                    radius  = dimSection[1]
                    section = AddCircleFromCenter( sectionPlane, radius )
                    defSection.append( section )
            
                globalTrasl = rg.Vector3d( transResult ) 
                globalTrasl.Transform(xform2[1]) 
                globalTrasl.Transform(xform)
                globalTransVector.append( globalTrasl )
    
           
            defpolyline = rg.PolylineCurve( defPoint )
    
            if dimSection[0] == 'circular' :
                radius1  = dimSection[1]/2
                radius2  = dimSection[1]/2 - dimSection[2]
                if (radius1 - radius2 ) == 0:
                    meshdef = meshLoft3( defSection,  color )
    
                else :
                    defSection1 = [row[0] for row in defSection ]
                    defSection2 = [row[1] for row in defSection ]
                    meshdef = meshLoft3( defSection1,  color )
                    meshdef.Append( meshLoft3( defSection2,  color ) )
                    #print( meshdef )
    
            else  :
                meshdef = meshLoft3( defSection,  color )
            return  [ defpolyline, meshdef, globalTransVector] 
        ## Mesh from close section eith gradient color ##
        def meshLoft3( point, color ):
            #print( point )
            meshEle = rg.Mesh()
            pointSection1 = point
            for i in range(0,len(pointSection1)):
                for j in range(0, len(pointSection1[0])):
                    vertix = pointSection1[i][j]
                    #print( type(vertix) )
                    meshEle.Vertices.Add( vertix ) 
                    #meshEle.VertexColors.Add( color[0],color[1],color[2] );
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
            colour = rs.CreateColor( color[0], color[1], color[2] )
            meshEle.VertexColors.CreateMonotoneMesh( colour )
            meshElement = meshEle
            #meshdElement.IsClosed(True)
            
            return meshElement
    
        def gradient(value, valueMin, valueMax, colorList ):
    
            if colorList == [] :
                listcolor = [ rs.CreateColor( 201, 0, 0 ),
                            rs.CreateColor( 240, 69, 7),
                            rs.CreateColor( 251, 255, 0 ),
                            rs.CreateColor( 77, 255, 0 ),
                            rs.CreateColor( 0, 255, 221 ),
                            rs.CreateColor( 0, 81, 255 )]
            else :
                listcolor = colorList
    
            n = len( listcolor )
            domain = linspace( valueMin, valueMax, n)
            #print( domain )
            
            for i in range(1,n+1):
                if  domain[i-1] <= value <= domain[i] :
                    return listcolor[ i-1 ]
                elif  valueMax <= value <= valueMax + 0.0000000000001 :
                    return listcolor[ -1 ]
                elif  valueMin - 0.0000000000001 <= value <= valueMin  :
                    return listcolor[ 0 ]
                    
        def updateComponent(interval):
            
            ## Updates this component, similar to using a grasshopper timer 
            
            # Define callback action
            def callBack(e):
                ghenv.Component.ExpireSolution(False)
            
            # Get grasshopper document
            ghDoc = ghenv.Component.OnPingDocument()
            
            # Schedule this component to expire
            ghDoc.ScheduleSolution(interval,gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack)) # Note that the first input here is how often to update the component (in milliseconds)
                
        def ModalView(AlpacaModalOutput, numberMode, speed, Animate, Reset, scale, direction, modelExtrude, colorList ):
        
            global myCounter
            
            
            Animate = False if Animate is None else Animate
            numberMode = 1 if numberMode is None else numberMode
            Reset = False if Reset is None else Reset
            speed = 1 if speed is None else speed
            modelExtrude = True if modelExtrude is None else modelExtrude
                    
                
                
            global ModelDisp
            global ModelCurve
            global ModelShell
            global ModelSolid
            global dimSection
            #global ExtrudedModel
        
            diplacementWrapper = AlpacaModalOutput[0][numberMode-1] # number of mode will start from 1. First, Second, Third ect ect
            EleOut = AlpacaModalOutput[1]
            Period = AlpacaModalOutput[3]
        
        
            # Instantiate/reset persisent starting counter variable
            if "myCounter" not in globals() or Reset :
                myCounter = 0
        
            # Update the variable and component
            if Animate and not Reset:
                myCounter += 1/ ( (speed) * 10 )
                updateComponent(1)
        
            # Output counter
        
            T = Period[numberMode-1]
            w = 2 * mt.pi/T
            #At = math.sin(myCounter)
        
            At = mt.sin(myCounter * w + mt.pi/2)
        
            nodeValue = []
            displacementValue = []
            #ShellOut = AlpacaModalOutput[4]
        
            pointWrapper = []
            dispWrapper = []
        
            for index,item in enumerate(diplacementWrapper):
                nodeValue.append( item[0] )
                displacementValue.append( item[1] )
                pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
                if len(item[1]) == 3:
                    dispWrapper.append( [index, rg.Point3d( item[1][0], item[1][1], item[1][2] ) ] )
                elif len(item[1]) == 6:
                    dispWrapper.append( [index, [rg.Point3d(item[1][0],item[1][1],item[1][2] ), rg.Point3d(item[1][3],item[1][4],item[1][5]) ] ] )
        
            ## Dict. for point ##
            pointWrapperDict = dict( pointWrapper )
            pointDispWrapperDict = dict( dispWrapper )
            ####
        
            ## FOR scala automatica ##
            ## nodeValue è la lista delle cordinate
            rowX = [row[0] for row in nodeValue ]
            rowY = [row[1] for row in nodeValue ]
            rowZ = [row[2] for row in nodeValue ]
        
            scaleMax = max( max(rowX), max(rowY), max(rowZ) )
            scaleMin = min( min(rowX), min(rowY), min(rowZ) )
            coordMax = max( mt.fabs(scaleMin),mt.fabs(scaleMax)) - mt.fabs(scaleMin)
        
            ## displacementValue è la lista degli spostamenti
        
            rowDefX = [row[0] for row in displacementValue ]
            rowDefY = [row[1] for row in displacementValue ]
            rowDefZ = [row[2] for row in displacementValue ]
        
            defMax = max( max(rowDefX), max(rowDefY), max(rowDefZ) )
            defMin = min( min(rowDefX), min(rowDefY), min(rowDefZ) )
            DefMax = max( mt.fabs(defMax),mt.fabs(defMin))
        
            if scale is None:
                scaleDef = scaleAutomatic( coordMax , DefMax )/10
        
            else :
                scaleDef = scale
        
            modelDisp = []
            modelCurve = []
            ShellDefModel = []
            ExtrudedView = []
        
            traslBeamValue = []
            rotBeamValue = []
        
            traslShellValue = []
            rotShellValue = []
            ExtrudedShell = []
        
            SolidDefModel = []
            traslSolidValue = []
        
        
            for ele in EleOut :
                eleType = ele[2][0]
                nNode = len( ele[1] )
                
                if eleType == 'ElasticTimoshenkoBeam' :
                    
                    dimSection = ele[2][10]
                    color = ele[2][12]
                    valueTBeam = defValueTimoshenkoBeam( ele, pointWrapperDict, pointDispWrapperDict, scaleDef*At )
                    defpolyline = valueTBeam[0]
                    meshdef = valueTBeam[1]
                    globalTrans = valueTBeam[2]
                    globalRot = valueTBeam[3]
                    traslBeamValue.append( globalTrans ) 
                    rotBeamValue.append( globalRot )
                    modelCurve.append( defpolyline )
                    modelDisp.append( defpolyline )
                    # estrusione della beam #
                    ExtrudedView.append( meshdef )
                elif eleType == 'Truss' :
                    dimSection = ele[2][10]
                    color = ele[2][12]
                    #print( color )
                    valueTruss = defTruss( ele, pointWrapperDict, pointDispWrapperDict, scaleDef*At )
                    defpolyline = valueTruss[0]
                    meshdef = valueTruss[1]
                    globalTrans = valueTruss[2]
                    traslBeamValue.append( globalTrans ) 
                    modelCurve.append( defpolyline )
                    ExtrudedView.append( meshdef )
                    modelDisp.append( defpolyline )
        
                elif nNode == 4 and eleType != 'FourNodeTetrahedron':
                    shellDefModel = defShellQuad( ele, pointWrapperDict, pointDispWrapperDict, scaleDef*At )
                    ShellDefModel.append( shellDefModel[0] )
                    traslShellValue.append( shellDefModel[1] )
                    rotShellValue.append( shellDefModel[2] )
                    extrudeShell = shellDefModel[3]
                    ExtrudedView.append( extrudeShell )
                    
                elif nNode == 3:
                    #print( nNode )
                    shellDefModel = defShellTriangle( ele, pointWrapperDict, pointDispWrapperDict, scaleDef*At )
                    ShellDefModel.append( shellDefModel[0] )
                    traslShellValue.append( shellDefModel[1] )
                    rotShellValue.append( shellDefModel[2] )
                    extrudeShell = shellDefModel[3]
                    ExtrudedView.append( extrudeShell )
        
                    
                elif nNode == 8:
                    solidDefModel = defSolid( ele, pointWrapperDict, pointDispWrapperDict, scaleDef*At )
                    SolidDefModel.append( solidDefModel[0] )
                    doc.Objects.AddMesh( solidDefModel[0] )
                    traslSolidValue.append( solidDefModel[1] )
                    ExtrudedView.append( solidDefModel[0] )
                    
                elif  eleType == 'FourNodeTetrahedron' :
                    #print(ele)
                    solidDefModel = defTetraSolid( ele, pointWrapperDict, pointDispWrapperDict, scaleDef*At )
                    SolidDefModel.append( solidDefModel[0] )
                    traslSolidValue.append( solidDefModel[1] )
                    ExtrudedView.append( solidDefModel[0] )
        
            ########################################################################################################################
            # MAX an MIN VALOR
            valorVector = []
            # beam valor #
            for valuetrasl in traslBeamValue:
                for valor in valuetrasl:
                    vectorTrasl = rg.Vector3d( valor )
                    if direction == 0:
                        valorVector.append( vectorTrasl.X ) 
                    elif direction == 1:
                        valorVector.append( vectorTrasl.Y )
                    elif direction == 2:
                        valorVector.append( vectorTrasl.Z ) 
                    elif direction == 3:
                        valorVector.append( vectorTrasl.Length )     
            # POINT #
            if len(dispWrapper[0][1]) == 3 :
                PointDisp = [row[1] for row in dispWrapper ] 
            else:
                PointDisp = [row[1][0] for row in dispWrapper ]
        
            for nodeDisp in PointDisp :
                vectorNodeDisp = rg.Vector3d( nodeDisp )
                if direction == 0:
                    valorVector.append( vectorNodeDisp.X ) 
                elif direction == 1:
                    valorVector.append( vectorNodeDisp.Y )
                elif direction == 2:
                    valorVector.append( vectorNodeDisp.Z ) 
                elif direction == 3:
                    valorVector.append( vectorNodeDisp.Length )
            # MAX end MIN on structures point #
            lowerLimit = min( valorVector )
            upperLimit = max( valorVector )
            domainValues = [ lowerLimit, upperLimit ]
            print( lowerLimit, upperLimit )
        #####################################################################################
            colorBeam = []
            numberDivide = []
            for value in traslBeamValue :
                colorValor = []
                for valor in value:
                    vectorTrasl = rg.Vector3d( valor )
        
                    if direction == 0:
                        valorVector = vectorTrasl.X  
                    elif direction == 1:
                        valorVector = vectorTrasl.Y 
                    elif direction == 2:
                        valorVector = vectorTrasl.Z  
                    elif direction == 3:
                        valorVector = vectorTrasl.Length
        
                    #print( valorVector )
        
                    color = gradient( valorVector, lowerLimit, upperLimit, colorList )
                    colorValor.append( color )
                colorBeam.append( colorValor )
                numberDivide.append( len(colorValor) )
            #print( modelCurve[0])
            segment = []
            for curve, segmentCount in zip( modelCurve, numberDivide ):
                #print(segmentCount)
                parameter = curve.DivideByCount( segmentCount - 1, True )
                segmentCurve = []
                for i in range(1, len(parameter)) :
                        p1 =  rg.Curve.PointAt( curve, parameter[i-1] ) 
                        p2 = rg.Curve.PointAt( curve, parameter[i] )
                        segmentCurve.append( rg.Line( p1, p2 ) )
                segment.append( segmentCurve )
        
                #print( segment )
        
            
            for shellEle, value in zip(ShellDefModel,traslShellValue) :
                shellColor = shellEle.DuplicateMesh()
                shellColor.VertexColors.Clear()
                for j in range( 0,shellEle.Vertices.Count ):
                    vectorTrasl = rg.Vector3d( value[j] )
                    if direction == 0:
                        valorVector = vectorTrasl.X  
                    elif direction == 1:
                        valorVector = vectorTrasl.Y 
                    elif direction == 2:
                        valorVector = vectorTrasl.Z  
                    elif direction == 3:
                        valorVector = vectorTrasl.Length
        
                    color = gradient( valorVector, lowerLimit, upperLimit, colorList )
                    shellColor.VertexColors.Add( color )
                modelDisp.append( shellColor)
            #dup.VertexColors.CreateMonotoneMesh(Color.Red)
            #doc.Objects.AddMesh(dup)
            for solidEle, value in zip(SolidDefModel,traslSolidValue) :
                solidColor = solidEle.DuplicateMesh()
                solidColor.VertexColors.Clear()
                for j in range(0,solidEle.Vertices.Count):
                    vectorTrasl = rg.Vector3d( value[j] )
                    if direction == 0:
                        valorVector = vectorTrasl.X  
                    elif direction == 1:
                        valorVector = vectorTrasl.Y 
                    elif direction == 2:
                        valorVector = vectorTrasl.Z  
                    elif direction == 3:
                        valorVector = vectorTrasl.Length
        
                    color = gradient( valorVector, lowerLimit, upperLimit, colorList )
                    solidColor.VertexColors.Add( color )
                modelDisp.append( solidColor )
                    #rg.Collections.MeshVertexColorList.SetColor( solidEle,j, color[0], color[1], color[2] )
        
        
            if modelExtrude == False or modelExtrude == None :
                self.line = segment
                self.colorLine = colorBeam
                return modelDisp
                
            else:
                self.line = []
                self.colorLine = []
                return ExtrudedView
                
                
                
        checkData = True
        
        if not AlpacaModalOutput:
            checkData = False
            msg = "input 'AlpacaModalOutput' failed to collect data"
            ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            modelDisp = ModalView(AlpacaModalOutput, numberMode, speed, Animate, Reset, scale, direction,modelExtrude, colorList )
            return (modelDisp)
            
    def DrawViewportWires(self,arg):
        
        for crvs, colors in zip(self.line, self.colorLine):
            for crv, color in zip(crvs, colors):
                arg.Display.DrawLine(crv, color, 4)

