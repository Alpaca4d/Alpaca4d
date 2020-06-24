import sys
import clr
import os

import Rhino.Geometry as rg
import Grasshopper as gh

def Assemble(Element, Support, Load, Mass):
    points = []
    startPointList = []
    endPointList = []
    geomTransf = []
    matWrapper = []
    secTagWrapper = []
    
    for element in Element:
        if (element[1] == "ElasticTimoshenkoBeam") or (element[1] == "Truss"): # element[1] retrieve the type of the beam
            
            startPoint = element[0].PointAt(element[0].Domain[0])
            endPoint = element[0].PointAt(element[0].Domain[1])
            points.append(startPoint)
            points.append(endPoint)
            geomTransf.append(element[3])
            matWrapper.append([element[2][6][0], element[2][6][1:] ]) # to be careful because we are assigning "unixial" inside the solver. We need to find a clever way to assigning outside
        elif (element[1] == "ShellMITC4") or (element[1] == "ShellDKGT"):
            mesh = element[0]
            vertices = mesh.Vertices
            for i in range(vertices.Count):
                points.append( rg.Point3d.FromPoint3f(vertices[i]) )
            matWrapper.append([element[2][2][0], element[2][2][1:] ])
            secTagWrapper.append([element[2][0], element[2][1:] ])
        elif (element[1] == "bbarBrick") or (element[1] == "FourNodeTetrahedron"):
            mesh = element[0]
            vertices = mesh.Vertices
            for i in range(vertices.Count):
                #points.append( rg.Point3d.FromPoint3f(vertices[i]) )
                points.append( rg.Point3d( vertices[i]) )
            matWrapper.append([element[2][0], element[2][1:]])
    
    # create MatTag
    # use dictionary to delete duplicate
    matNameDict = dict(matWrapper)
    
    matNameList = []
    i = 1
    
    for key, value in matNameDict.iteritems():
        temp = [key,i,value]
        matNameList.append(temp)
        i += 1
    
    openSeesMatTag = []
    for item in matNameList:
        openSeesMatTag.append([ item[0], item[1:] ] )
    
    openSeesMatTag = openSeesMatTag
    matNameDict = dict(openSeesMatTag)
    
    
    # create SecTag
    # use dictionary to delete duplicate
    secTagDict = dict(secTagWrapper)
    secTagList = []
    i = 1
    
    for key, value in secTagDict.iteritems():
        temp = [key,i,value]
        secTagList.append(temp)
        i += 1
    
    openSeesSecTag = []
    for item in secTagList:
        openSeesSecTag.append([ item[0], item[1:] ] )
    
    
    openSeesSecTag = openSeesSecTag
    secTagDict = dict(openSeesSecTag)
    
    #print(secTagDict)
    
    # create GeomTransf
    geomTransf = [row[0] for row in geomTransf ]
    geomTransfList = list(dict.fromkeys(geomTransf))
    geomTransfDict = { geomTransfList[i] : i+1 for i in range(len(geomTransfList) ) }
    
    geomTag = geomTransfDict.values() # elemento a dx (tag)
    geomVec = geomTransfDict.keys() # elemento a sx (vettore)
    
    GeomTransf = []
    for i in range(0, len(geomTag) ) :
        GeomTransf.append( [ geomTag[i], list(rg.Vector3d(geomVec[i])) ] )
    
    GeomTransf = GeomTransf
    
    
    
    oPoints = rg.Point3d.CullDuplicates(points, 0.01)       # Collection of all the points of our geometry
    cloudPoints = rg.PointCloud(oPoints)        # Convert to PointCloud to use ClosestPoint Method
    
    
    ## FOR NODE ##
    openSeesNode = []
    
    for nodeTag, node in enumerate(oPoints):
        openSeesNode.append( [nodeTag, node.X, node.Y, node.Z] )
    
    openSeesNode = openSeesNode
    
    
    ## FOR ELEMENT ##
    
    openSeesBeam = []
    openSeesShell = []
    openSeesSolid = []
    MassOfStructure = 0
    
    for eleTag, element in enumerate(Element):
        if (element[1] == "ElasticTimoshenkoBeam") or (element[1] == "Truss"): # element[1] retrieve the type of the beam
            
            start = element[0].PointAt(element[0].Domain[0])
            end = element[0].PointAt(element[0].Domain[1])
            indexStart = cloudPoints.ClosestPoint(start)
            indexEnd = cloudPoints.ClosestPoint(end)
            
            typeElement = element[1]
            eleTag = eleTag
            eleNodes = [indexStart, indexEnd]
            Area = element[2][0]
            Avy = element[2][1]
            Avz = element[2][2]
            E_mod = element[2][6][1]
            G_mod = element[2][6][2]
            Jxx = element[2][5]
            Iy = element[2][3]
            Iz = element[2][4]
            transfTag = geomTransfDict.setdefault(element[3][0])
            axis1 = [ element[3][0].X, element[3][0].Y, element[3][0].Z ]
            axis2 = [ element[3][1].X, element[3][1].Y, element[3][1].Z ]
            axis3 = [ element[3][2].X, element[3][2].Y, element[3][2].Z ]
            orientVector = [ axis1, axis2, axis3 ]
    
            massDens = element[5]
            #print(massDens)
            sectionGeomProperties = element[2][7]
            color = [element[4][0], element[4][1], element[4][2], element[4][3] ]
            matTag = matNameDict.setdefault(element[2][6][0])[0]
            openSeesBeam.append( [typeElement, eleTag, eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag, massDens, Avy, Avz, orientVector, sectionGeomProperties, matTag, color] )
            
            MassOfStructure += element[0].GetLength() * massDens * 100    # kN to kg
            
        elif (element[1] == "ShellMITC4") or (element[1] == "ShellDKGT"):
            typeElement = element[1]
            eleTag = eleTag
            shellNodesRhino = element[0].Vertices
            color = [element[3][0],element[3][1],element[3][2],element[3][3]] 
            indexNode = []
            for node in shellNodesRhino:
                indexNode.append(cloudPoints.ClosestPoint(node) + 1)
            shellNodes = indexNode
            thick = element[2][1]
            secTag = secTagDict.setdefault(element[2][0])[0]
            # sectionProperties = we need to bring some information later probably 
            openSeesShell.append( [ typeElement, eleTag, shellNodes, secTag, thick, color] )
            
            areaMesh = rg.AreaMassProperties.Compute(element[0]).Area
            
            density = element[2][2][4]
            MassOfStructure +=  (areaMesh * thick * density) * 100         # kN to kg
            
            
        elif (element[1] == 'bbarBrick') or (element[1] == "FourNodeTetrahedron"):
            typeElement = element[1]
            eleTag = eleTag
            shellNodesRhino = element[0].Vertices
            indexNode = []
            for node in shellNodesRhino:
                indexNode.append(cloudPoints.ClosestPoint(node) + 1)
            SolidNodes = indexNode
            matTag = matNameDict.setdefault(element[2][0])[0]
            color = [ element[3][0], element[3][1], element[3][2] ]
            # sectionProperties = we need to bring some information later probably 
            openSeesSolid.append( [ typeElement, eleTag, SolidNodes, matTag, [0,0,0], color] )
    
    
    openSeesShell = openSeesShell
    openSeesBeam = openSeesBeam
    openSeesSolid = openSeesSolid
    ## SUPPORT ## 
    
    openSeesSupport = []
    
    for support in Support:
        supportNodeTag = cloudPoints.ClosestPoint(support[0])
        dof_1 = support[1]
        dof_2 = support[2]
        dof_3 = support[3]
        dof_4 = support[4]
        dof_5 = support[5]
        dof_6 = support[6]
        openSeesSupport.append( [supportNodeTag, dof_1, dof_2, dof_3, dof_4, dof_5, dof_6 ] )
    
    openSeesSupport = openSeesSupport
    
    ## FORCE ##
    
    openSeesNodeLoad = []
    openSeesBeamLoad = []
    
    
    for loadWrapper in Load:
        if loadWrapper[3] == "pointLoad":
            nodeTag = cloudPoints.ClosestPoint(loadWrapper[0])
            loadValues = [ loadWrapper[1].X, loadWrapper[1].Y, loadWrapper[1].Z, loadWrapper[2].X, loadWrapper[2].Y, loadWrapper[2].Z ]
            loadType = loadWrapper[3]
            openSeesNodeLoad.append( [nodeTag, loadValues, loadType] )
        elif loadWrapper[3] == "beamUniform":
            for eleTag, element in enumerate(Element):
                equality = rg.GeometryBase.GeometryEquals(loadWrapper[0],element[0])
                if equality:
                    loadValues = [ loadWrapper[1].X, loadWrapper[1].Y, loadWrapper[1].Z ]
                    loadType = loadWrapper[3]
                    openSeesBeamLoad.append( [eleTag, loadValues, loadType] )
                    break
    
    
    openSeesNodeLoad = openSeesNodeLoad
    openSeesBeamLoad = openSeesBeamLoad
    
    
    ## MASS ##
    # find Total mass convering in each node
    
    openSeesNodalMass = []
    
    for item in Mass:
        massNodeTag = cloudPoints.ClosestPoint(item[0])
        massValues = [item[1].X, item[1].Y, item[1].Z]
        openSeesNodalMass.append([ massNodeTag, massValues ])
    
    openSeesNodalMass = openSeesNodalMass
    
    ## ASSEMBLE ##
    
    
    openSeesModel = ([ openSeesNode,
                       GeomTransf,
                       openSeesBeam,
                       openSeesSupport,
                       openSeesNodeLoad,
                       openSeesNodalMass,
                       openSeesBeamLoad,
                       openSeesMatTag,
                       openSeesShell,
                       openSeesSecTag,
                       openSeesSolid])
                       
                       
    ghFilePath = ghenv.LocalScope.ghdoc.Path
    ghFolderPath = os.path.dirname(ghFilePath)
    
    
    outputPath = os.path.join(ghFolderPath,'assembleData')
    if not os.path.exists(outputPath):
       os.makedirs(outputPath)
       
       
    wrapperFile = os.path.join(outputPath,'openSeesModel.txt')
    with open(wrapperFile, 'w') as f:
     for item in openSeesModel:
            f.write("%s\n" % item)
    
    
    return [openSeesModel, MassOfStructure]


checkData = True

if not Element:
    checkData = False
    msg = "input 'Element' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if not Support:
    checkData = False
    msg = "input 'Support' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if not Load:
    msg = "input 'Load' failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData != False:
    openSeesModel = Assemble(Element, Support, Load, Mass)[0]
    MassOfStructure= Assemble(Element, Support, Load, Mass)[1]