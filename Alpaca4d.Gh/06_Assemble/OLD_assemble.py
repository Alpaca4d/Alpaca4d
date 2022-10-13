"""
Create a FEA Model
-
    Args:
        Element:
        Support:
        Load:
        Constraint:
    Returns:
        AlpacaModel:
"""


import os
import sys
import ghpythonlib.treehelpers as th
import Rhino.Geometry as rg
import Rhino.Collections as rc
import rhinoscriptsyntax as rs
from collections import defaultdict, OrderedDict, deque
import copy
import time
import Grasshopper as gh



ghenv.Component.Name = "Assemble Model (Alpaca4d)"
ghenv.Component.NickName = 'AM'
ghenv.Component.Message = "Assemble Model (Alpaca4d)"


## add alpaca install directory to system path

ghcompfolder = gh.Folders.DefaultAssemblyFolder
if ghcompfolder not in sys.path:
    sys.path.append(ghcompfolder)

try:
    from Alpaca4d import alpaca4d as alpaca
    from Alpaca4d import alpaca4dUtil as alpacaUtil
except:
    msg = "Cannot import Alpaca4d. Is the Alpaca4d folder available in " + ghcompfolder + "?"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)


checkData = True

if not Element:
    checkData = False
    msg = "Input parameter Element failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if not Support:
    checkData = False
    msg = "Input parameter Support failed to collect data"
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)


if checkData:
    
    FolderPath = rs.DocumentPath()
    os.chdir(FolderPath)
    
    # create the object model
    AlpacaModel = alpaca.Model()
    
    
    start = time.clock()
    #subdivide element per type
    
    for element in Element:
        if element.type == "Beam":
            AlpacaModel.beams.append(element)
        elif element.type == "Shell":
            AlpacaModel.shells.append(element)
        elif element.type == "Brick":
            AlpacaModel.bricks.append(element)
    
    
    end = time.clock() - start
    print("time to subdivide element {}".format(end))
    start = time.clock()
    
    # create a list of unique point
    # need to add the rigid constraint
    
    AlpacaModel.getuniquePoints(AlpacaModel.beams, AlpacaModel.shells, AlpacaModel.bricks, Constraint)
    
    
    end = time.clock() - start
    print("time to get uniquepoints {}".format(end))
    start = time.clock()
    
    
    #############
    # create node and assign to object
    #############
    
    if AlpacaModel.uniquePointsThreeNDF:
        AlpacaModel.py.append(alpaca.Model.write3ndf_tcl())
        for point in AlpacaModel.uniquePointsThreeNDF:
            node = alpaca.Node(point)
            node.ndf = 3
            node.setNodeTag(AlpacaModel)
            AlpacaModel.nodes.append( node )
        
            AlpacaModel.py.append(node.write_tcl())
    
    
    if AlpacaModel.uniquePointsSixNDF:
        AlpacaModel.py.append(alpaca.Model.write6ndf_tcl())
        for point in AlpacaModel.uniquePointsSixNDF:
            node = alpaca.Node(point)
            node.ndf = 6
            node.setNodeTag(AlpacaModel)
            AlpacaModel.nodes.append( node )
         
            AlpacaModel.py.append(node.write_tcl())
    
    
    
    end = time.clock() - start
    print("time to create node and assign tag {}".format(end))
    start = time.clock()
    
    
    #################
    # create supports
    #################
    
    for supportNode in Support:
        
        # if the list is empty, skip this operation
        if AlpacaModel.uniquePointsThreeNDF:
            closestPointInThreeNDF = rc.Point3dList.ClosestPointInList(AlpacaModel.uniquePointsThreeNDF, supportNode.Pos)
            if supportNode.Pos.DistanceTo(closestPointInThreeNDF) < 0.001:
                #print("I am in 3ndf")
                supportNode.ndf = 3
                AlpacaModel.threeNDFModel.append(supportNode)
                supportNode.setNodeTag(AlpacaModel)
        
        if AlpacaModel.uniquePointsSixNDF:
            closestPointInSixNDF = rc.Point3dList.ClosestPointInList(AlpacaModel.uniquePointsSixNDF, supportNode.Pos)
            if supportNode.Pos.DistanceTo(closestPointInSixNDF) < 0.001:
                supportNode.ndf = 6
                AlpacaModel.sixNDFModel.append(supportNode)
                supportNode.setNodeTag(AlpacaModel)
        
        
        AlpacaModel.supports.append(supportNode)
        AlpacaModel.py.append(supportNode.write_tcl())
    
    
    end = time.clock() - start
    print("time to create support and assign tag {}".format(end))
    start = time.clock()
    
    
    ####################
    # create constraints
    ####################
    
    
    for constraint in Constraint:
        constraint.setNodeTag(AlpacaModel)
        AlpacaModel.constraints.append(constraint)
    
    ####################
    # create equalDOF when the model has 3df and 6df together
    ####################
    
    
    end = time.clock() - start
    print("time to create constraint and assign tag {}".format(end))
    start = time.clock()
    
    
    Id = []
    IdB = []
    
    def SearchCallback(sender, e):
        Id.Add(e.Id)
        IdB.Add(e.IdB)
    
    
    
    lenThreeNDF = len(AlpacaModel.uniquePointsThreeNDF)
    lenSixNDF = len(AlpacaModel.uniquePointsSixNDF)
    
    
    if not(lenThreeNDF == 0 or lenSixNDF == 0):
        print("brick and beam together")
        rg.RTree.SearchOverlaps(AlpacaModel.RTreeCloudPointThreeNDF, AlpacaModel.RTreeCloudPointSixNDF, 0.001, SearchCallback)
        
        for i,j in zip(Id, IdB):
            print(i,j)
            node_i = AlpacaModel.uniquePointsThreeNDF[i]
            node_j = AlpacaModel.uniquePointsSixNDF[j]
            
            
            equalConstraint = alpaca.EqualDOF(node_i, node_j, True, True, True, False, False, False)
            equalConstraint.masterNodeTag = AlpacaModel.cloudPointThreeNDF.ClosestPoint(node_i) + 1
            equalConstraint.slaveNodesTag = AlpacaModel.cloudPointSixNDF.ClosestPoint(node_j) + 1 + len(AlpacaModel.uniquePointsThreeNDF)
            AlpacaModel.py.append(equalConstraint.write_tcl())
    
    
    
    end = time.clock() - start
    print("time to find common points between 3ndf and 6ndf {}".format(end))
    start = time.clock()
    
    ##########################
    ##########################
    ##########################
    
    crossSection = []
    material = []
    
    for item in Element:
        if item.type != "Brick":
            crossSection.append(item.CrossSection)
            material.append(item.CrossSection.material)
        else:
            material.extend(item.material)
        
    
    uniqueCS = list(set(crossSection))
    
    
    flatten_material = alpacaUtil.flatten_list(material)
    
    
    uniqueMaterial = list(set(flatten_material))
    
    for index, material in enumerate(uniqueMaterial,1):
        material.matTag = index
        AlpacaModel.py.append(material.write_tcl())
    
    
    for index, section in enumerate(uniqueCS,1):
        section.sectionTag = index
        AlpacaModel.py.append(section.write_tcl())
        
    
    
    
    
    
    # write py file
    
    
    # assign tag and node Index to element and shell
    for index, element in enumerate(Element,1):
        element.setTopologyRTree(AlpacaModel)
        element.eleTag = index
        element.setTags()
    
    
    
    end = time.clock() - start
    print("time to assign tags for the elements {}".format(end))
    start = time.clock()
    
    
    
    
    ## define load
    
    Mass = 0
    IsGravity = False
    g_factor = 10.00
    
    for item in Load:
        if item.type == "Gravity Load":
            IsGravity = True
            GravityLoad = item
        if item.type == "PointLoad":
            AlpacaModel.loads.append(item)
        if item.type == "Mass":
            AlpacaModel.masses.append(item)
    
    
    for item in Element:
        if item.type == "Beam":
            length = item.Crv.GetLength()
            Mass += (item.massDens * length)
            if IsGravity:
                gravityPointLoad_1 = alpaca.PointLoad(item.Crv.PointAtStart, g_factor * rg.Vector3d(0,0, -(item.massDens * length / 2)) * GravityLoad.GravityFactor, rg.Vector3d(0,0,0), GravityLoad.TimeSeries)
                gravityPointLoad_2 = alpaca.PointLoad(item.Crv.PointAtEnd, g_factor * rg.Vector3d(0,0, -(item.massDens * length / 2)) * GravityLoad.GravityFactor, rg.Vector3d(0,0,0), GravityLoad.TimeSeries)
                ##print( -(item.massDens * length / 2))
                AlpacaModel.loads.append(gravityPointLoad_1)
                AlpacaModel.loads.append(gravityPointLoad_2)
        if item.type == "Shell":
            meshArea = rg.AreaMassProperties.Compute(item.Mesh).Area
            if item.CrossSection.__class__.__name__ != "LayeredShell":
                areaDensity = item.CrossSection.thickness * item.CrossSection.material.rho
                Mass += areaDensity * meshArea
                if IsGravity:
                    for vertex in item.Mesh.Vertices.ToPoint3dArray():
                        gravityPointLoad = alpaca.PointLoad(vertex, g_factor * rg.Vector3d(0,0, -(areaDensity * meshArea/ len(item.Mesh.Vertices))) * GravityLoad.GravityFactor, rg.Vector3d(0,0,0), GravityLoad.TimeSeries)
                        AlpacaModel.loads.append(gravityPointLoad)
            else:
                for thickness, material in zip(item.CrossSection.thickness, item.CrossSection.material):
                    areaDensity = thickness * material.rho
                    Mass += areaDensity * meshArea
                    if IsGravity:
                        for vertex in item.Mesh.Vertices.ToPoint3dArray():
                            gravityPointLoad = alpaca.PointLoad(vertex, g_factor * rg.Vector3d(0,0, -(areaDensity * meshArea/ len(item.Mesh.Vertices))) * GravityLoad.GravityFactor, rg.Vector3d(0,0,0), GravityLoad.TimeSeries)
                            AlpacaModel.loads.append(gravityPointLoad)


        if item.type == "Brick":
            #print(type(item.Mesh))
            meshVolume = rg.VolumeMassProperties.Compute(item.Mesh).Volume
            density = item.material.rho 
            Mass += density * meshVolume
            if IsGravity:
                for vertex in item.Mesh.Vertices.ToPoint3dArray():
                    gravityPointLoad = alpaca.PointLoad(vertex, g_factor * rg.Vector3d(0,0, -(density * meshVolume / len(item.Mesh.Vertices))) * GravityLoad.GravityFactor, rg.Vector3d(0,0,0), GravityLoad.TimeSeries)
                    #print(len(item.Mesh.Vertices))
                    #print(density)
                    # volume can be zero if mesh faces are not properly rotated
                    #print(meshVolume)
                    #print(-(density * meshVolume / len(item.Mesh.Vertices)))
                    AlpacaModel.loads.append(gravityPointLoad)
    
    #print(AlpacaModel.loads)
    ## load
    
    
    for item in AlpacaModel.loads:
        item.setNodeTag(AlpacaModel)
    
    #print(AlpacaModel.loads)
    
    for item in AlpacaModel.beams:
        AlpacaModel.py.append(item.write_tcl())
    
    for item in AlpacaModel.shells:
        AlpacaModel.py.append(item.write_tcl())
    
    for item in AlpacaModel.bricks:
        AlpacaModel.py.append(item.write_tcl())
    
    
    for item in Constraint:
        AlpacaModel.py.append(item.write_tcl())
    
    
    for item in AlpacaModel.masses:
        item.setNodeTag(AlpacaModel)
        AlpacaModel.py.append(item.write_tcl())
    
    
    timeSeriesDict = alpaca.TimeSeries.getTimeSeries(AlpacaModel.loads)[1]
    AlpacaModel.py.append(alpaca.PointLoad.write_tcl(timeSeriesDict,AlpacaModel))
    
    
    text = AlpacaModel.py
