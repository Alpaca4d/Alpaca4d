import os
import System.Drawing.Color

import Rhino.Geometry as rg
import Rhino

import ghpythonlib.components as ghcomp

from collections import OrderedDict
from collections import defaultdict

import math
import subprocess
import alpaca4dUtil


#TODO
# USE SELF.TYPEELEMENT TO WRITE THE OBJECT TYPE
# GEOMTRANSFORMATION NEEDS TO BE IS OWN OBJECT
# BEAM INTEGRATION OWN OBJECT

class Model(object):
    def __init__(self, ndm = 3, ndf = 6):
        
        self.ndm = ndm
        self.ndf = ndf

        self.uniquePoints = []
        self.uniquePointsThreeNDF = []
        self.uniquePointsSixNDF = []
        self.cloudPoint = None
        self.RTreeCloudPoint = None


        self.nodes = []
        self.elements = []
        self.supports = []
        self.constraints = []
        self.loads = []
        self.materials = []

        self.timeSeries = {}

        self.beams = []
        self.shells = []
        self.bricks = []

        self.recorder = []
        self.recorderName = None

        #self.pointLoad = defaultdict(list)
        self.pointLoad = []

        self.filename = None

        self.threeNDFModel = []
        self.sixNDFModel = []

        self.analysis = None

        self.py = []


    def getuniquePoints(self, beams, shells, bricks, constraints):
        """Cull Duplicates Points.

        Keyword arguments:
        beams -- List of beams
        shells -- List of shells

        return (List of uniquePoints, PointCloud)
        """

        threeNDFPoints = []
        sixNDFPoints = []

        AllPoints = []

        for beam in beams:
            # need to add an if for truss elements
            PointAtStart = beam.Crv.PointAtStart
            PointAtEnd = beam.Crv.PointAtEnd
            sixNDFPoints.append(PointAtStart)
            sixNDFPoints.append(PointAtEnd)

        for shell in shells:
            vertices = shell.Mesh.Vertices.ToPoint3dArray()
            for node in vertices:
                sixNDFPoints.append(node)
        
        for brick in bricks:
            vertices = brick.Mesh.Vertices.ToPoint3dArray()
            for node in vertices:
                threeNDFPoints.append(node)
        
        for constraint in constraints:
            sixNDFPoints.extend(constraint.slaveNodes, constraint.masterNode)
        
        if not threeNDFPoints:
            self.uniquePointsThreeNDF = []
        else:
            #self.uniquePointsThreeNDF = rg.Point3d.CullDuplicates(threeNDFPoints, 0.001)
            self.uniquePointsThreeNDF = alpaca4dUtil.removeDuplicates(threeNDFPoints, 0.001)
        
        if not sixNDFPoints:
            self.uniquePointsSixNDF = []
        else:
            #self.uniquePointsSixNDF = rg.Point3d.CullDuplicates(sixNDFPoints, 0.001)
            self.uniquePointsSixNDF = alpaca4dUtil.removeDuplicates(sixNDFPoints, 0.001)
        
        
        #self.uniquePoints = self.uniquePointsThreeNDF + self.uniquePointsSixNDF
        if not self.uniquePointsThreeNDF:
            self.uniquePoints = self.uniquePointsSixNDF
        elif not self.uniquePointsSixNDF:
            self.uniquePoints = self.uniquePointsThreeNDF
        else:
            self.uniquePoints = self.uniquePointsThreeNDF + self.uniquePointsSixNDF
        
        self.cloudPoint = rg.PointCloud(self.uniquePoints)
        self.RTreeCloudPoint = rg.RTree.CreateFromPointArray(self.uniquePoints)

        return


    ## override Rhino .ToString() method (display name of the class in Gh)
    def ToString(self):
        return "<Class Model>"

    #TODO
    @staticmethod
    def write3ndf_py():
        return "ops.model('basic', '-ndm', 3, '-ndf', 3)\n"

    @staticmethod
    def write6ndf_py():
        return "ops.model('basic', '-ndm', 3, '-ndf', 6)\n"
    
    #TODO
    @staticmethod
    def write3ndf_tcl():
        return "model BasicBuilder -ndm 3 -ndf 3\n"

    @staticmethod
    def write6ndf_tcl():
        return "model BasicBuilder -ndm 3 -ndf 6\n"

    def writeFile(self, filename):
        
        textFile = self.py
            
        with open(filename, 'w') as f:
            for line in textFile:
                f.write("%s\n" % line)
        self.filename = filename
        pass

    def runOpensees(self, args):

        if args == 'python':
            executable = 'python.exe'
        elif args == 'tcl':
            executable = 'opensees.exe'
        else:
            executable = args

        process = subprocess.Popen([executable, self.filename], shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout, stderr

class Node(object):
    def __init__(self, Pos):
        
        self.Pos = Pos
        self.nodeTag = None
        self.ndf = None

        self.mass = 0

        self.displacement = None
        self.rotation = None

    def setNodeTag(self, cloudPoint):
        self.nodeTag = cloudPoint.ClosestPoint(self.Pos) + 1
        pass

    def setNodeTagRTree(self, RTreeCloudPoint):
        closestIndices = []
        
        #event handler of type RTreeEventArgs
        def SearchCallback(sender, e):
            closestIndices.Add(e.Id)
        
        RTreeCloudPoint.Search(rg.Sphere(self.Pos, 0.001), SearchCallback)
        ind = closestIndices
        
        self.nodeTag = ind[0]
        pass

    def setMassNode(self, MassElement):
        self.mass = MassElement
        pass

    ## override Rhino .ToString() method (display name of the class in Gh)
    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        if self.ndf == 6:
            tcl_text = "node {} {} {} {} -mass {} {} {} {} {} {}".format(self.nodeTag, float(self.Pos.X), float(self.Pos.Y), float(self.Pos.Z), self.mass, self.mass, self.mass, self.mass, self.mass, self.mass)
        elif self.ndf == 3:
            tcl_text = tcl_text = "node {} {} {} {} -mass {} {} {}".format(self.nodeTag, float(self.Pos.X), float(self.Pos.Y), float(self.Pos.Z), self.mass, self.mass, self.mass)
        else:
            raise ValueError('No ndf has been assigned')
        return tcl_text

    def write_py(self):
        if self.ndf == 6:
            py_text = "ops.node({}, {}, {}, {}, '-mass', {}, {}, {}, {}, {}, {})".format(self.nodeTag, float(self.Pos.X), float(self.Pos.Y), float(self.Pos.Z), self.mass, self.mass, self.mass, self.mass, self.mass, self.mass)
        elif self.ndf == 3:
            py_text = "ops.node({}, {}, {}, {}, '-mass', {}, {}, {})".format(self.nodeTag, float(self.Pos.X), float(self.Pos.Y), float(self.Pos.Z), self.mass, self.mass, self.mass)# ops.node(nodeTag, *crds, '-ndf', ndf, '-mass', *mass)
        else:
            raise ValueError('No ndf has been assigned')
        return py_text

#####################################################
### Material ########################################
#####################################################

class uniAxialMaterialElastic(object):
    def __init__(self, matName, E, Eneg, eta, G, v, rho):
        """Generate a uniaxial Elastic Material
            Inputs:
                matName: Name of the material.
                E: Young's Modulus [MPa].
                eta = damping tangent.
                G: Tangential Modulus [MPa].
                v: Poisson ratio.
                rho: specific weight [kN/m3].
                fy: Yield stress value of the material [MPa]"""


        self.matName = matName
        self.E = E
        self.Eneg = Eneg
        self.eta = eta
        self.G = G
        self.v = v
        self.rho = rho

        self.matTag = None

        if self.eta == None:
            self.eta = 0.0

        if self.Eneg == None:
            self.Eneg = E

        self.materialDimension = "uniAxialMaterial"
        self.materialType = "Elastic"

        if self.v == None:
            self.G = G  # Input value in N/mm2 ---> Output kN/m2
            self.v = (E / (2 * G)) - 1
        else:
            self.G = E / (2 * (1 + v))

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        return "uniaxialMaterial Elastic {} {} {} {}\n".format(self.matTag, self.E, self.eta, self.Eneg)

    def write_py(self):
        return "ops.uniaxialMaterial('Elastic', {}, {}, {}, {})\n".format(self.matTag, self.E, self.eta, self.Eneg)

class uniAxialMaterialElasticPlastic(object):
    def __init__(self, matName, E, epsyP, epsyN, eps0, rho):
        """Generate a uniaxial Elastic Material
            Inputs:
                matName: Name of the material.
                matTag: Material identifier number.
                E: Young's Modulus [MPa].
                epsyP: strain or deformation at which material reaches plastic state in tension.
                epsyN: strain or deformation at which material reaches plastic state in compression.
                eps0: initial strain.
                rho: specific weight [kN/m3]
                fy: Yield stress value of the material [MPa]"""


        self.matName = matName
        self.E = E
        self.epsyP = epsyP
        self.epsyN = epsyN
        self.eps0 = eps0
        self.v = v
        self.rho = rho
        
        self.matTag = None

        if self.epsyN == None:
            self.epsyN = epsyP

        self.materialDimension = "uniAxialMaterial"
        self.materialType = "ElasticPlastic"

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        return "uniaxialMateria ElasticPP {} {} {} {} {}\n".format(self.matTag, self.E, self.epsyP, self.epsyN, self.eps0)

    # TODO
    def write_py(self):
        return "ops.uniaxialMateria('ElasticPP',{},{},{},{},{})\n".format(self.matTag, self.E, self.epsyP, self.epsyN, self.eps0)
    

class ElasticIsotropic(object):
    def __init__(self, matName, E, G, rho=0.0, v=None):
        """Generate a n-Dimensional Elastic Isotropic Material
            Inputs:
                matName: Name of the material.
                E: Young's Modulus [MPa].
                G: Tangential Modulus [MPa].
                rho: specific weight [kN/m3].
                v: Poisson ratio.
                fy: Yield stress value of the material [MPa]"""

        self.matName = matName
        self.E = E
        self.G = G
        self.v = v
        self.rho = rho

        self.matTag = None

        self.materialDimension = "nDMaterial"
        self.materialType = "ElasticIsotropic"

        if self.v == None:
            self.v = (E / (2 * G)) - 1

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        tcl_text = "nDMaterial ElasticIsotropic {} {} {} {}\n".format(self.matTag, self.E, self.v, self.rho)
        return tcl_text

    def write_py(self):
        py_text = "ops.nDMaterial('ElasticIsotropic', {}, {}, {}, {})\n".format(self.matTag, self.E, self.v, self.rho)
        return py_text

class ElasticOrthotropic(object):
    def __init__(self, matName, Ex, Ey, Ez, vxy, vyz, vzx, Gxy, Gyz, Gzx, rho):

        self.matName = matName
        self.Ex = Ex
        self.Ey = Ey
        self.Ez = Ez
        self.vxy = vxy
        self.vyz = vyz
        self.vzx = vzx
        self.Gxy = Gxy
        self.Gyz = Gyz
        self.Gzx = Gzx
        self.rho = rho

        self.matTag = None

        self.materialDimension = "nDMaterial"
        self.materialType = "ElasticOrthotropic"

    def ToString(self):
        return "ElasticOrthotropic Material"

    def write_tcl(self):
        # nDMaterial ElasticOrthotropic $matTag $Ex $Ey $Ez $vxy $vyz $vzx $Gxy $Gyz $Gzx <$rho>
        tcl_text = "nDMaterial ElasticOrthotropic {} {} {} {} {} {} {} {} {} {} {}\n".format(self.matTag, self.Ex, self.Ey, self.Ez, self.vxy, self.vyz, self.vzx, self.Gxy, self.Gyz, self.Gzx, self.rho )
        return tcl_text

    def write_py(self):
        py_text = "ops.nDMaterial('ElasticOrthotropic', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})\n".format(self.matTag, self.Ex, self.Ey, self.Ez, self.vxy, self.vyz, self.vzx, self.Gxy, self.Gyz, self.Gzx, self.rho )
        return py_text

#TO REVIEW
class J2Plasticity(object):
    def __init__(self, K, G, sig0, sigInf, delta, H):
        """This command is used to construct an multi dimensional material object that has a von Mises (J2) yield criterium and isotropic hardening.
        matTag (int) 	integer tag identifying material
        K (float) 	    bulk modulus
        G (float) 	    shear modulus
        sig0 (float) 	initial yield stress
        sigInf (float) 	final saturation yield stress
        delta (float) 	exponential hardening parameter
        H (float) 	    linear hardening parameter"""

        self.K = K
        self.G = G
        self.sig0 = sig0
        self.sigInf = sigInf
        self.delta = delta
        self.H = H

        self.matTag = None

        self.materialDimension = "nDMaterial"
        self.materialType = "ElasticIsotropicHardening"

    def ToString(self):
        return write_tcl()

    def write_tcl(self):
        tcl_text = "nDMaterial J2Plasticity {0} {1} {2} {3} {4} {5} {6}\n".format(self.matTag, self.K, self.G, self.sig0, self.sigInf, self.delta, self.H)
        return tcl_text

    def write_py(self):
        py_text = "ops.nDMaterial('J2Plasticity', {0}, {1}, {2}, {3}, {4}, {5}, {6})\n".format(self.matTag, self.K, self.G, self.sig0, self.sigInf, self.delta, self.H)
        return py_text

#####################################################
### Element #########################################
#####################################################

#TODO update the integration text for tcl
class ForceBeamColumn(object):

    def __init__(self, Crv, CrossSection, Colour, OrientSection):

        self.Crv = Crv
        self.CrossSection = CrossSection
        self.Colour = Colour
        self.OrientSection = OrientSection

        self.type = "Beam"
        
        self.eleTag = None
        self.iNode = None
        self.jNode = None

        self.ndf = 6

        self.transfTag = None
        self.integrationTag = None

        self.elementType = "forceBeamColumn"

        self.massDens = self.CrossSection.Area * self.CrossSection.material.rho

    # each element will have a unique tag for Section, TransfTag, IntegrationTag, MaterialTag
    def setTags(self):

        self.transfTag = self.eleTag
        self.integrationTag = self.eleTag

        self.CrossSection.sectionTag = self.eleTag
        self.CrossSection.material.matTag = self.eleTag

        pass


    def getPerpFrame(self):
        line = self.Crv
        midPoint =  line.PointAtNormalizedLength(0.5)
        parameter = line.ClosestPoint(midPoint, 0.01)[1]
        perpFrame = ghcomp.PerpFrame( line, parameter )
        return perpFrame

    def getGeomTransfVector(self):
        axis = self.getPerpFrame().YAxis
        return axis


    def setTopology(self, cloudPoint):
        # cloudPoint is a cloudPoint rhino type
        
        PointAtStart = self.Crv.PointAtStart
        PointAtEnd = self.Crv.PointAtEnd
        
        #CloudPoint = rg.PointCloud(uniquePoint)
        self.iNode = cloudPoint.ClosestPoint(PointAtStart) + 1
        self.jNode = cloudPoint.ClosestPoint(PointAtEnd) + 1
        pass

    def setTopologyRTree(self, RTreeCloudPoint):

        PointAtStart = self.Crv.PointAtStart
        PointAtEnd = self.Crv.PointAtEnd
        
        closestIndices = []
        
        #event handler of type RTreeEventArgs
        def SearchCallback(sender, e):
            closestIndices.Add(e.Id + 1)
        
        for pt in [PointAtStart, PointAtEnd]:
            RTreeCloudPoint.Search(rg.Sphere(pt, 0.001), SearchCallback)
            ind = closestIndices
        
        self.iNode = ind[0]
        self.jNode = ind[1]

        pass

    def beamIntegrationNewtonCotes_py(self, numberOfSection):
        return "ops.beamIntegration('NewtonCotes', {}, {}, {})\n".format( self.integrationTag, self.CrossSection.sectionTag, numberOfSection)

    def beamIntegrationNewtonCotes_tcl(self, numberOfSection):
        return "NewtonCotes {} {}".format( self.CrossSection.sectionTag, numberOfSection)

    #write a text geomTransf
    def geomTransf_py(self):
        return "ops.geomTransf('Linear',{},{},{},{})\n".format(self.transfTag, self.getGeomTransfVector().X, self.getGeomTransfVector().Y, self.getGeomTransfVector().Z)
    
    def geomTransf_tcl(self):
        return "geomTransf Linear {} {} {} {}\n".format(self.transfTag, self.getGeomTransfVector().X, self.getGeomTransfVector().Y, self.getGeomTransfVector().Z)

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        # https://opensees.berkeley.edu/wiki/index.php/Elastic_Timoshenko_Beam_Column_Element

        material = self.CrossSection.material.write_tcl()
        section = self.CrossSection.write_tcl()
        geomTransf = self.geomTransf_tcl()
        integration = self.beamIntegrationNewtonCotes_tcl(5)

        beam = "element forceBeamColumn {} {} {} {} {} -mass {}\n".format(self.eleTag,
                                                                          self.iNode,
                                                                          self.jNode,
                                                                          self.transfTag,
                                                                          integration,
                                                                          self.massDens)
        

        return material + section + geomTransf + beam

    def write_py(self):

        material = self.CrossSection.material.write_py()
        section = self.CrossSection.write_py()
        geomTransf = self.geomTransf_py()
        integration = self.beamIntegrationNewtonCotes_py(5)
        
        beam = "ops.element('forceBeamColumn', {}, {}, {}, {}, {}, '-mass', {})\n".format(self.eleTag,
                                                                                         self.iNode,
                                                                                         self.jNode,
                                                                                         self.transfTag,
                                                                                         self.integrationTag,
                                                                                         self.massDens)
    

    
        return material + section + geomTransf + integration + beam



class ShellMITC4(object):
    def __init__(self, Mesh, CrossSection, Colour):

        self.Mesh = Mesh
        self.CrossSection = CrossSection
        self.Colour = Colour

        self.type = "Shell"

        self.ndf = 6
        
        self.eleTag = None
        self.indexNodes = []

        self.elementType = "ShellMITC4"

    def setTopology(self, cloudPoint):
        self.indexNodes = []
        vertices = self.Mesh.Vertices.ToPoint3dArray()
        for node in vertices:
            self.indexNodes.append( cloudPoint.ClosestPoint(node) + 1 )
        pass

    def setTopologyRTree(self, RTreeCloudPoint):
        self.indexNodes = []
        vertices = self.Mesh.Vertices.ToPoint3dArray()

        closestIndices = []
        
        #event handler of type RTreeEventArgs
        def SearchCallback(sender, e):
            closestIndices.Add(e.Id + 1)
        
        for node in vertices:
            RTreeCloudPoint.Search(rg.Sphere(node, 0.001), SearchCallback)
            ind = closestIndices
        
        self.indexNodes = ind
        pass
    
    def setTags(self):

        self.CrossSection.sectionTag = self.eleTag
        self.CrossSection.material.matTag = self.eleTag

        #self.CrossSection.sectionTag = index
        #self.CrossSection.material.matTag = index
        pass

    def ToString(self):
        return "Class ShellMITC4"

    def write_tcl(self):
        # https://opensees.berkeley.edu/wiki/index.php/Shell_Element
        # element ShellMITC4 $eleTag $iNode $jNode $kNode $lNode $secTag

        material = self.CrossSection.material.write_tcl()
        section = self.CrossSection.write_tcl()

        shell = "element ShellMITC4 {} {} {} {} {} {}\n".format(self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.indexNodes[3], self.CrossSection.sectionTag)

        return material + section + shell

    def write_py(self):

        material = self.CrossSection.material.write_py()
        section = self.CrossSection.write_py()

        shell =  "ops.element('ShellMITC4', {}, {}, {}, {}, {}, {})\n".format(self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.indexNodes[3], self.CrossSection.sectionTag)

        return material + section + shell

class ASDShellQ4(object):
    def __init__(self, Mesh, CrossSection, Colour):

        self.Mesh = Mesh
        self.CrossSection = CrossSection
        self.Colour = Colour

        self.type = "Shell"

        self.ndf = 6
        
        self.eleTag = None
        self.indexNodes = []

        self.elementType = "ASDShellQ4"

    def setTopology(self, cloudPoint):
        self.indexNodes = []
        vertices = self.Mesh.Vertices.ToPoint3dArray()
        for node in vertices:
            self.indexNodes.append( cloudPoint.ClosestPoint(node) + 1 )
        pass
    
    def setTags(self):

        self.CrossSection.sectionTag = self.eleTag
        self.CrossSection.material.matTag = self.eleTag

        #self.CrossSection.sectionTag = index
        #self.CrossSection.material.matTag = index
        pass

    def ToString(self):
        return "Class ASDShellQ4"

    def write_tcl(self):
        # https://opensees.berkeley.edu/wiki/index.php/Shell_Element
        # element ASDShellQ4 $eleTag $iNode $jNode $kNode $lNode $secTag

        material = self.CrossSection.material.write_tcl()
        section = self.CrossSection.write_tcl()

        shell = "element ASDShellQ4 {} {} {} {} {} {}\n".format(self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.indexNodes[3], self.CrossSection.sectionTag)

        return material + section + shell

    def write_py(self):

        material = self.CrossSection.material.write_py()
        section = self.CrossSection.write_py()

        shell =  "ops.element('ASDShellQ4', {}, {}, {}, {}, {}, {})\n".format(self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.indexNodes[3], self.CrossSection.sectionTag)

        return material + section + shell


class ShellNLDKGT(object):
    def __init__(self, Mesh, CrossSection, Colour):

        self.Mesh = Mesh
        self.CrossSection = CrossSection
        self.Colour = Colour

        self.type = "Shell"

        self.ndf = 6
        
        self.eleTag = None
        self.indexNodes = []

        self.elementType = "ShellDKGT"

    def setTopology(self, cloudPoint):
        self.indexNodes = []
        vertices = self.Mesh.Vertices.ToPoint3dArray()
        for node in vertices:
            self.indexNodes.append( cloudPoint.ClosestPoint(node) + 1 )
        pass

    def setTopologyRTree(self, RTreeCloudPoint):
        vertices = self.Mesh.Vertices.ToPoint3dArray()

        closestIndices = []
        
        #event handler of type RTreeEventArgs
        def SearchCallback(sender, e):
            closestIndices.Add(e.Id + 1)
        
        for node in vertices:
            RTreeCloudPoint.Search(rg.Sphere(node, 0.001), SearchCallback)
            ind = closestIndices
        
        self.indexNodes = ind
        pass
    
    def setTags(self):

        self.CrossSection.sectionTag = self.eleTag
        self.CrossSection.material.matTag = self.eleTag

        pass

    def ToString(self):
        return "Class ShellDKGT"

    def write_tcl(self):
        # https://opensees.berkeley.edu/wiki/index.php/ShellNLDKGT
        # element ShellNLDKGT $eleTag $iNode $jNode $kNode $lNode $secTag

        material = self.CrossSection.material.write_tcl()
        section = self.CrossSection.write_tcl()

        shell = "element ShellDKGT {} {} {} {} {}\n".format(self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.CrossSection.sectionTag)

        return material + section + shell

    def write_py(self):

        material = self.CrossSection.material.write_py()
        section = self.CrossSection.write_py()

        shell =  "ops.element('ShellDKGT', {}, {}, {}, {}, {})\n".format(self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.CrossSection.sectionTag)

        return material + section + shell


class stdBrick(object):
    def __init__(self, Brick, material, Colour):

        self.Mesh = Brick
        self.material = material
        self.type = "Brick"

        self.ndf = 3

        self.Colour = Colour

        self.eleTag = None
        self.indexNodes = []

        self.elementType = "stdBrick"
        
            
    def setTopology(self, cloudPoints):
        indexNodes = []
        for iPoint in self.Mesh.Vertices:
            indexNodes.append( cloudPoints.ClosestPoint(iPoint) + 1)
        self.indexNodes = indexNodes
        pass

    def setTopologyRTree(self, RTreeCloudPoint):
        vertices = self.Mesh.Vertices

        closestIndices = []
        
        #event handler of type RTreeEventArgs
        def SearchCallback(sender, e):
            closestIndices.Add(e.Id + 1)
        
        for node in vertices:
            RTreeCloudPoint.Search(rg.Sphere(node, 0.001), SearchCallback)
            ind = closestIndices
        
        self.indexNodes = ind
        pass


    def setTags(self):
        # not sure if this can create some problem
        # have a look at copy the object
        self.material.matTag = self.eleTag
        pass
    
    def ToString(self):
        return "Class Std Brick"
    
    def write_tcl(self):
        material = self.material.write_tcl()
        brick = "element {} {} {} {} {} {} {} {} {} {} {} {} {} {}\n".format( self.elementType, self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.indexNodes[3], self.indexNodes[4], self.indexNodes[5], self.indexNodes[6], self.indexNodes[7], self.material.matTag, 0, 0, 0)
        return material + brick

    def write_py(self):
        material = self.material.write_py()
        brick = "ops.element('{}', {}, *{}, {}, {}, {}, {})\n".format( self.elementType, self.eleTag, self.indexNodes, self.material.matTag, 0, 0, 0)
        return  material + brick


class SSPbrick(object):
    def __init__(self, Brick, material, Colour):

        self.Mesh = Brick
        self.material = material
        self.type = "Brick"

        self.ndf = 3

        self.Colour = Colour

        self.eleTag = None
        self.indexNodes = []

        self.elementType = "SSPbrick"
        
            
    def setTopology(self, cloudPoints):
        indexNodes = []
        for iPoint in self.Mesh.Vertices:
            indexNodes.append( cloudPoints.ClosestPoint(iPoint) + 1)
        self.indexNodes = indexNodes
        pass
    
    
    def setTopologyRTree(self, RTreeCloudPoint):
        vertices = self.Mesh.Vertices

        closestIndices = []
        
        #event handler of type RTreeEventArgs
        def SearchCallback(sender, e):
            closestIndices.Add(e.Id + 1)
        
        for node in vertices:
            RTreeCloudPoint.Search(rg.Sphere(node, 0.001), SearchCallback)
            ind = closestIndices
        
        self.indexNodes = ind
        pass
    


    def setTags(self):
        # not sure if this can create some problem
        # have a look at copy the object
        self.material.matTag = self.eleTag
        pass
    
    def ToString(self):
        return "Class SSP Brick"
    
    def write_tcl(self):
        material = self.material.write_tcl()
        brick = "element {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12} {13}\n".format( self.elementType, self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.indexNodes[3], self.indexNodes[4], self.indexNodes[5], self.indexNodes[6], self.indexNodes[7], self.material.matTag, 0, 0, 0)
        return material + brick

    def write_py(self):
        material = self.material.write_py()
        brick = "ops.element('{}', {}, *{}, {}, {}, {}, {})\n".format( self.elementType, self.eleTag, self.indexNodes, self.material.matTag, 0, 0, 0)
        return  material + brick



class FourNodeTetrahedron(object):
    def __init__(self, Tetra, material, Colour):

        self.Mesh = Tetra
        self.material = material
        self.type = "Brick"

        self.ndf = 3

        self.Colour = Colour

        self.eleTag = None
        self.indexNodes = []

        self.elementType = "FourNodeTetrahedron"
            
    def setTopology(self, cloudPoints):
        indexNodes = []
        for iPoint in self.Mesh.Vertices:
            indexNodes.append( cloudPoints.ClosestPoint(iPoint) + 1)
        self.indexNodes = indexNodes
        pass

    def setTopologyRTree(self, RTreeCloudPoint):
        vertices = self.Mesh.Vertices

        closestIndices = []
        
        #event handler of type RTreeEventArgs
        def SearchCallback(sender, e):
            closestIndices.Add(e.Id + 1)
        
        for node in vertices:
            RTreeCloudPoint.Search(rg.Sphere(node, 0.001), SearchCallback)
            ind = closestIndices
        
        self.indexNodes = ind
        pass

    def setTags(self):
        # not sure if this can create some problem
        # have a look at copy the object
        self.material.matTag = self.eleTag
        pass
    
    def ToString(self):
        return "Class Tetrahedron"
    
    def write_tcl(self):
        material = self.material.write_tcl()
        brick = "element {} {} {} {} {} {} {} {} {} {}\n".format( self.elementType, self.eleTag, self.indexNodes[0], self.indexNodes[1], self.indexNodes[2], self.indexNodes[3], self.material.matTag, 0, 0, 0)
        return material + brick

    def write_py(self):
        material = self.material.write_py()
        brick = "ops.element('{}', {}, *{}, {}, {}, {}, {})".format( self.elementType, self.eleTag, self.indexNodes, self.material.matTag, 0, 0, 0)
        return  material + brick


class Support(object):
    def __init__(self, Pos, Tx = False, Ty = False, Tz = False, Rx = False, Ry = False, Rz = False):
        
        """Generate a Support Boundary Condition
            Inputs:
                Pos: Point Position.
                Tx =
                Ty = 
                Tz = 
                Mx = 
                My = 
                Mz = """
        
        self.Pos = Pos
        
        self.Tx = int(Tx)
        self.Ty = int(Ty)
        self.Tz = int(Tz)
        self.Rx = int(Rx)
        self.Ry = int(Ry)
        self.Rz = int(Rz)
        
        self.nodeTag = None

        self.ndf = None


    def setNodeTag(self, cloudPoint):
        self.nodeTag = cloudPoint.ClosestPoint(self.Pos) + 1
        pass

    def setNodeTagRTree(self, RTreeCloudPoint):
        closestIndices = []
        
        #event handler of type RTreeEventArgs
        def SearchCallback(sender, e):
            closestIndices.Add(e.Id)
        
        RTreeCloudPoint.Search(rg.Sphere(self.Pos, 0.001), SearchCallback)
        ind = closestIndices
        
        self.nodeTag = ind[0]
        pass

    ## override Rhino .ToString() method (display name of the class in Gh)
    def ToString(self):
        return "fix {} {} {} {} {} {} {}".format(self.nodeTag, self.Tx, self.Ty, self.Tz, self.Rx, self.Ry, self.Rz)

    def write_tcl(self):
        if self.ndf == 6:
            tcl_text = "fix {} {} {} {} {} {} {}".format(self.nodeTag, self.Tx, self.Ty, self.Tz, self.Rx, self.Ry, self.Rz)
        elif self.ndf == 3:
            tcl_text = "fix {} {} {} {}".format(self.nodeTag, self.Tx, self.Ty, self.Tz)
        else:
            raise ValueError('No ndf has been assigned')
        return tcl_text

    def write_py(self):
        if self.ndf == 6:
            py_text = "ops.fix({},{},{},{},{},{},{})".format(self.nodeTag, self.Tx, self.Ty, self.Tz, self.Rx, self.Ry, self.Rz)
        elif self.ndf == 3:
            py_text = "ops.fix({},{},{},{})".format(self.nodeTag, self.Tx, self.Ty, self.Tz)
        else:
            raise ValueError('No ndf has been assigned')
        return py_text


#####################################################
### Constraint  #####################################
#####################################################

#TODO 
#ASK FOR A PERP DIRECTION
class RigidDiaphragm(object):
    def __init__(self, masterNode, slaveNodes):
        self.masterNode = masterNode
        self.slaveNodes = slaveNodes

        self.masterNodeTag = None
        self.slaveNodesTag = []
        
        # It is assuming that Diaphgram is Horizontal
        self.perDir = 3 
    
    def setNodeTag(self, cloudPoint):
        
        self.masterNodeTag = cloudPoint.ClosestPoint(self.masterNode) + 1
        for node in self.slaveNodes:
            self.slaveNodesTag.append(cloudPoint.ClosestPoint(node) + 1)
        return
    
    def ToString(self):
        return self.write_tcl()
    
    def write_tcl(self):
        slaveNodesTag = [str(x) for x in self.slaveNodesTag]
        slaveNodesTag = ' '.join(slaveNodesTag)
        tcl_text = "rigidDiaphragm {} {}  {}\n".format(self.perDir, self.masterNodeTag, slaveNodesTag)
        return tcl_text

    def write_py(self):
        py_text = "ops.rigidDiaphragm({}, {}, *{})".format(self.perDir, self.masterNodeTag, self.slaveNodesTag)
        return py_text

#TODO write TCL
class EqualDOF(object):
    def __init__(self, masterNode, slaveNodes, dof_x, dof_y, dof_z, dof_xx, dof_yy, dof_zz):
        self.masterNode = masterNode
        self.slaveNodes = slaveNodes

        self.dof_x = dof_x
        self.dof_y = dof_y
        self.dof_z = dof_z
        self.dof_xx = dof_xx
        self.dof_yy = dof_yy
        self.dof_zz = dof_zz

        self.dof = [self.dof_x, self.dof_y, self.dof_z, self.dof_xx, self.dof_yy, self.dof_zz] 

        self.masterNodeTag = None
        self.slaveNodesTag = None

    def setNodeTag(self, cloudPoint):
        
        self.masterNodeTag = cloudPoint.ClosestPoint(self.masterNode) + 1
        self.slaveNodesTag.append(cloudPoint.ClosestPoint(self.slaveNodes) + 1)
        return

    def ToString(self):
        return self.write_tcl()
    
    def write_tcl(self):
        dofs = []
        for i,dof in enumerate(self.dof,1):
            if dof == True:
                dofs.append(i)

        dofs = ' '.join([str(i) for i in dofs])
        tcl_text = "equalDOF {} {}  {}\n".format(self.masterNodeTag, self.slaveNodesTag, dofs)
        return tcl_text

    def write_py(self):
        py_text = "ops.equalDOF({}, {}, *{})".format(self.masterNodeTag, self.slaveNodesTag, self.dof)
        return py_text


#####################################################
### Cross Section ###################################
#####################################################

#TODO
class CircleCS(object):
    def __init__(self, d, t, material = None):

        self.d = d
        self.t = t
        self.shape = 'circular'
        self.material = material

        self.alphaY = 9.0/10.0
        self.alphaZ = 9.0/10.0

        self.crv = rg.Circle(rg.Plane.WorldXY, self.d/2.0).ToNurbsCurve( 2, 10 )
        self.sectionBrep = rg.Brep.CreatePlanarBreps( self.crv, 0.1 )[0]
        
    def Area(self):
        if self.t == 0 or self.t == self.d / 2:
            Area = math.pow(self.d,2)/4  * math.pi
        elif self.t < self.d/2 and self.t >= 0:
            Area = (pow(self.d,2)-pow((self.d-2*self.t),2))/4 * math.pi
        else:
            Area = None
        return Area

    def AreaY(self):
        return self.Area() * self.alphaY

    def AreaZ(self):
        return self.Area() * self.alphaZ

    def Iyy(self):
        if self.t == 0 or self.t == self.d / 2:
            Iyy = pow(self.d,4)/64 * math.pi
        elif self.t < self.d/2 and self.t >= 0:
            Iyy = (pow(self.d,4)-pow((self.d-2*self.t),4))/64 * math.pi
        else:
            Iyy = None
        return Iyy

    def Izz(self):
        Izz = self.Iyy()
        return Izz

    def J(self):
        if self.t == 0 or self.t == self.d / 2:
            J = pow(self.d,4)/32 * math.pi
        elif self.t < self.d/2 and self.t >= 0:
            J = (pow(self.d,4)-pow((self.d-2*self.t),4))/32 * math.pi
        else:
            J = None
        return J

    def write_tcl(self):
        pass

    def write_py(self):
        pass

    def ToString(self):
        return "Class CircleCS: \
                \n\tshape: {0} \
                \n\tdiameter: {1} \
                \n\tthickness: {2} \
                \n\tArea {3} \
                \n\tAreaY {4} \
                \n\tAreaZ {5} \
                \n\tIyy {6} \
                \n\tIzz {7} \
                \n\tJ {8}".format(self.shape, self.d, self.t, round(self.Area(),3), round(self.AreaY(),3), round(self.AreaZ(),3), round(self.Iyy(),3), round(self.Izz(),3), round(self.J(),3))


#TODO
class RectangularCS(object):
    def __init__(self, b, h, material = None):

        self.b = b
        self.h = h
        self.shape = "Rectangular"
        self.material = material

        self.alphaY = 5.0/6.0
        self.alphaZ = 5.0/6.0


        widthDomain = rg.Interval(-b/2,b/2)
        heightDomain = rg.Interval(-h/2,h/2)
        self.crv = rg.Rectangle3d(rg.Plane.WorldXY, widthDomain, heightDomain).ToNurbsCurve()
        self.sectionBrep = rg.Brep.CreatePlanarBreps( self.crv, 0.1 )[0]
    def Area(self):
        return self.b * self.h

    def AreaY(self):
        return self.Area() * self.alphaY

    def AreaZ(self):
        return self.Area() * self.alphaZ

    def Iyy(self):
        return self.b*pow(self.h,3)/12

    def Izz(self):
        return pow(self.b,3)*self.h/12

    def J(self):
        if self.h < self.b:
            k = 1 / (3+4.1*pow((self.h/self.b),3/2))
            J = k*self.b*pow(self.h,3)
        else:
            k = 1 / (3+4.1*pow((self.b/self.h),3/2))
            J = k*self.h*pow(self.b,3)
        return J
    


    def ToString(self):
        return "Class RectangularCS: \
                \n\tshape: {0} \
                \n\tbase: {1} \
                \n\theight: {2} \
                \n\tArea {3} \
                \n\tAreaY {4} \
                \n\tAreaZ {5} \
                \n\tIyy {6} \
                \n\tIzz {7} \
                \n\tJ {8}".format(self.shape, self.b, self.h, round(self.Area(),3), round(self.AreaY(),3), round(self.AreaZ(),3), round(self.Iyy(),3), round(self.Izz(),3), round(self.J(),3))

    def write_tcl(self):
        pass

    def write_py(self):
        pass



class ElasticSection(object):
    def __init__(self, secName, Area, Izz, Iyy, J, alphaY, alphaZ, material):

        self.secName = secName
        self.Area = Area
        self.Izz = Izz
        self.Iyy = Iyy
        self.J = J
        self.alphaY = alphaY
        self.alphaZ = alphaZ

        self.material = material
    
        self.AreaY = Area * alphaY
        self.AreaZ = Area * alphaZ

        self.crv = None
        self.sectionBrep = None

        self.sectionTag = None

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        tcl_text = "section Elastic {} {} {} {} {} {} {} {} {}\n".format(self.sectionTag, self.material.E, self.Area, self.Izz, self.Iyy, self.material.G, self.J, self.alphaY, self.alphaZ)
        return tcl_text

    def write_py(self):
        py_text = "ops.section('Elastic',{},{},{},{},{},{},{},{},{})\n".format(self.sectionTag, self.material.E, self.Area, self.Izz, self.Iyy, self.material.G, self.J, self.alphaY, self.alphaZ)
        return py_text


#TODO
class PlateFiberSection(object):
    def __init__(self, sectionName, height, material):

        self.sectionName = sectionName
        self.height = height
        self.material = material
        
        self.sectionTag = None

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        # https://opensees.berkeley.edu/wiki/index.php/Plate_Fiber_Section
        #       section PlateFiber $secTag $matTag $h
        return "section PlateFiber {} {} {}\n".format(self.sectionTag, self.material.matTag, self.height)

    def write_py(self):
        return "ops.section('PlateFiber',{},{},{})\n".format(self.sectionTag, self.material.matTag, self.height)

#TODO
class ElasticMembranePlateSection(object):
    def __init__(self, sectionName, height, material):

        self.sectionName = sectionName
        self.material = material
        self.height = height

        self.sectionTag = None

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        # https://opensees.berkeley.edu/wiki/index.php/Elastic_Membrane_Plate_Section
        #       section ElasticMembranePlateSection {$secTag} {$E} {$n} {$h} {$rho}
        return "section ElasticMembranePlateSection {} {} {} {} {}\n".format(self.sectionTag, self.material.E, self.material.v, self.height, self.material.rho)

    def write_py(self):
        return "ops.section('ElasticMembranePlateSection',{},{},{},{},{})\n".format(self.sectionTag, self.material.E, self.material.v, self.height, self.material.rho)

#TODO
class LayeredShell(object):
    def __init__(self, sectionName, materials, thicknesses):

        self.sectionName = sectionName
        self.materials = materials
        self.thicknesses = thicknesses

        self.numLayer = None
        self.sectionTag = None

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        # http://www.luxinzheng.net/download/OpenSEES/En_THUShell_OpenSEES.htm
        # section LayeredShell $sectionTag $nLayers $matTag1 $thickness1...$matTagn $thicknessn
        
        subDividedThickness = []
        for layerThickness in self.thicknesses:
            tempThick = []
            subLayerThickness = layerThickness/3
            tempThick.append(subLayerThickness)
            tempThick = tempThick * 3
            subDividedThickness.append(tempThick)
        
        
        numLayer = 0
        for listElem in subDividedThickness:
            numLayer += len(listElem)

        self.numLayer = numLayer
            
        
        tcl_text = "section LayeredShell {} {} ".format(self.sectionTag, numLayer)
        for i in range(len(self.materials)):
            for j in range(len(subDividedThickness)):
                
                tcl_text += str(self.materials[i].matTag) + " "
                tcl_text += str(subDividedThickness[i][j]) + " "
        
        tcl_text += "\n"
        
        return tcl_text 


    def write_py(self):
        
        subDividedThickness = []
        for layerThickness in self.thicknesses:
            tempThick = []
            subLayerThickness = layerThickness/3
            tempThick.append(subLayerThickness)
            tempThick = tempThick * 3
            subDividedThickness.append(tempThick)
        
        
        numLayer = 0
        for listElem in subDividedThickness:
            numLayer += len(listElem)
        
        self.numLayer = numLayer
        
        py_text = "ops.section('LayeredShell',{},{}, ".format(self.sectionTag, numLayer)
        for i in range(len(self.materials)):
            for j in range(len(subDividedThickness)):
                
                py_text += str(self.materials[i].matTag) + ","
                py_text += str(subDividedThickness[i][j]) + ","
        py_text = py_text[:-1]
        py_text += ")\n"

        return py_text 


# to define 2d elastic section

#####################################################################
### Load ############################################################
#####################################################################

class PointLoad(object):
    def __init__(self, Pos, Force, Moment, TimeSeries):

        self.Pos = Pos
        self.Force = Force
        self.Moment = Moment

        self.nodeTag = None

        self.type = "PointLoad"

        self.ndf = None

        self.PatternTag = None
        self.TimeSeries = TimeSeries


    def setNodeTag(self, cloudPoint):
        self.nodeTag = cloudPoint.ClosestPoint(self.Pos) + 1
        pass

    #TODO
    # Allowing for more than one time series
    @staticmethod
    def write_py(groupsTimeSeries):

        text = []

        for timeSeries in groupsTimeSeries.keys():
            text.append(groupsTimeSeries[timeSeries][0].TimeSeries.write_py())
            text.append("ops.pattern('Plain',{},{})".format(timeSeries, timeSeries)) #patternTag, TimeSeriesTag
            for load in groupsTimeSeries[timeSeries]:
                text.append("ops.load(%s, %s, %s, %s, %s, %s, %s)" % (load.nodeTag, load.Force.X, load.Force.Y, load.Force.Z, load.Moment.X, load.Moment.Y, load.Moment.Z))

        text = "\n".join(text)

        return text

    def ToString(self):
        return "<Class PointLoad>"



    #TODO add the ndf dispatch for writing the load
    @staticmethod
    def write_tcl(groupsTimeSeries, model):

        text = []

        for timeSeries in groupsTimeSeries.keys():
            text.append(groupsTimeSeries[timeSeries][0].TimeSeries.write_tcl())
            text.append("pattern Plain %s %s {" % (timeSeries, timeSeries)) #patternTag, TimeSeriesTag
            for load in groupsTimeSeries[timeSeries]:
                if model.uniquePointsThreeNDF:
                    if load.Pos.DistanceTo(Rhino.Collections.Point3dList.ClosestPointInList(model.uniquePointsThreeNDF,load.Pos)) < 0.001:
                        text.append("\tload %s %s %s %s" % (load.nodeTag, load.Force.X, load.Force.Y, load.Force.Z))
                elif load.Pos.DistanceTo(Rhino.Collections.Point3dList.ClosestPointInList(model.uniquePointsSixNDF,load.Pos)) < 0.001:
                    text.append("\tload %s %s %s %s %s %s %s" % (load.nodeTag, load.Force.X, load.Force.Y, load.Force.Z, load.Moment.X, load.Moment.Y, load.Moment.Z))
            text.append("}")
        text = "\n".join(text)

        return text


class GravityLoad(object):
    def __init__(self, GravityFactor, TimeSeries):
        self.GravityFactor = GravityFactor
        self.TimeSeries = TimeSeries

        self.type = "Gravity Load"
    
    def ToString(self):
        return "Gravity factor {}".format(self.GravityFactor)

#####################################################################
### Analysis ########################################################
#####################################################################


class Analysis(object):
    def __init__(self, Constraint, Numberer, System, Test, Algorithm, Integrator, AnalysisType, NumberOfSteps):

        self.Constraint = Constraint
        self.Numberer = Numberer
        self.System = System
        self.Test = Test
        self.Algorithm = Algorithm
        self.Integrator = Integrator
        self.AnalysisType = AnalysisType
        self.NumberOfSteps = NumberOfSteps

    def ToString(self):
        return "<Class Analyses>"

    def write_tcl(self):
        Constraint = "constraints {}\n".format(self.Constraint)
        Numberer = "numberer {}\n".format(self.Numberer)
        System = "system {}\n".format(self.System)
        Test = "test {}\n".format(self.Test)
        Algorithm = "algorithm {}\n".format(self.Algorithm)
        Integrator = "integrator {}\n".format(self.Integrator)
        AnalysisType = "analysis {}\n".format(self.AnalysisType)
        NumberOfSteps = "analyze {}\n".format(self.NumberOfSteps)

        return Constraint + Numberer + System + Test + Algorithm + Integrator + AnalysisType + NumberOfSteps

    def write_py(self):
        Constraint = "ops.constraints( '{}' )\n".format(self.Constraint)
        Numberer = "ops.numberer( '{}' )\n".format(self.Numberer)
        System = "ops.system( '{}' )\n".format(self.System)
        Test = "ops.test( {} )\n".format(self.Test)
        Algorithm = "ops.algorithm( '{}' )\n".format(self.Algorithm)
        Integrator = "ops.integrator( {} )\n".format(self.Integrator)
        AnalysisType = "ops.analysis( '{}' )\n".format(self.AnalysisType)
        NumberOfSteps = "ops.analyze( {} )\n".format(self.NumberOfSteps)

        return Constraint + Numberer + System + Test + Algorithm + Integrator + AnalysisType + NumberOfSteps
    
#####################################################################
### Time Series #####################################################
#####################################################################


class TimeSeries(object):

    @staticmethod
    def getTimeSeries(Load):

        # Load is the list of Load that goes in the assemble

        groupsTimeSeries = defaultdict(list)

        for obj in Load:
            groupsTimeSeries[id(obj.TimeSeries)].append(obj)

        # change name to the dictionary and assign timeSeriesTag

        for i,value in enumerate(groupsTimeSeries.keys(),1):
            groupsTimeSeries[i] = groupsTimeSeries.pop(value)
            groupsTimeSeries[i][0].TimeSeries.timeSeriesTag = i
        

        # get the list of unique Time Series Object

        TimeSeries = []

        for i,item in enumerate(groupsTimeSeries.keys(),1):
            TimeSeries.append(groupsTimeSeries[i][0].TimeSeries)

        return TimeSeries, groupsTimeSeries
    


class TimeSeriesConstant(object):
    def __init__(self, cFactor):
        self.seriesType = "Constant"
        self.cFactor = cFactor
        self.timeSeriesTag = None

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        return "timeSeries Constant {} -factor {}\n".format(self.timeSeriesTag, self.cFactor)

    def write_py(self):
        return "ops.timeSeries('Constant',{},'-factor', {})\n".format(self.timeSeriesTag, self.cFactor)

class TimeSeriesLinear(object):
    def __init__(self, linearFactor):
        self.seriesType = "linear"
        self.linearFactor = linearFactor
        self.timeSeriesTag = None

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        return "timeSeries Linear {} -factor {}\n".format(self.timeSeriesTag, self.linearFactor)

    def write_py(self):
        return "ops.timeSeries('Linear',{},'-factor', {})\n".format(self.timeSeriesTag, self.linearFactor)

class TimeSeriesTrigonometric(object):
    def __init__(self, tStart, tEnd, period, factor, shift):
        self.seriesType = "Trig"
        self.timeSeriesTag = None

        self.tStart = tStart
        self.tEnd = tEnd

        self.period = period
        self.factor = factor
        self.shift = shift

    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        return "timeSeries Trig {} {} {} {} -factor {} -shift {}\n".format(self.timeSeriesTag, self.tStart, self.tEnd, self.period, self.factor, self.shift)

    def write_py(self):
        return "ops.timeSeries('Trig', {}, {}, {}, {}, '-factor', {}, '-shift', {})\n".format(self.timeSeriesTag, self.tStart, self.tEnd, self.period, self.factor, self.shift)

#TODO
#TO CHECK HOW THE LIST WORKS IN TCL
class TimeSeriesPath(object):
    def __init__(self, values, time, factor):
        self.seriesType = "path"
        self.values = values
        self.time = time
        self.factor = factor
        self.timeSeriesTag = None
    
    def ToString(self):
        return self.write_tcl()

    def write_tcl(self):
        time = [str(x) for x in self.time]
        time = ' '.join(time)
        
        values = [str(x) for x in self.values]
        values = ' '.join(values)
        tcl_text = "timeSeries Path %s -time {%s} -values {%s} -factor %s\n" % (self.timeSeriesTag, time, values, self.factor)
        return tcl_text

    def write_py(self):
        py_text = "ops.timeSeries('Path', {}, '-values', *{}, '-time', *{}, '-factor', {})".format(self.timeSeriesTag, self.values, self.time, self.factor)
        return py_text





###################################################################
###################################################################
###################################################################

class PYRecorder(object):

    @staticmethod
    def node(fileName, nodeTag, dof, respType):
        return "ops.recorder('Node', '-file', '{}', '-time', '-node', {}, '-dof', {}, '{}')".format(fileName, nodeTag, dof, respType)

    @staticmethod
    def element(fileName, eleTag, respType):
        return "ops.recorder('Element', '-file', '{}', '-time', '-ele', {}, '{}')".format(fileName, eleTag, respType)


class PYRecorder_mod(object):

    def __init__(self):

        self.filename = None
        self.respType = None


    def node(self, fileName, nodeTag, dof, respType):

        self.filename = fileName
        self.respType = respType

        return "ops.recorder('Node', '-file', '{}', '-time', '-node', {}, '-dof', {}, '{}')".format(fileName, nodeTag, dof, respType)


    def element(self, fileName, eleTag, respType):

        self.filename = fileName
        self.respType = respType

        return "ops.recorder('Element', '-file', '{}', '-time', '-ele', {}, '{}')".format(fileName, eleTag, respType)


#TODO
#TO ADD THE ELEMENT RECORDER
class TCLRecorder(object):

    @staticmethod
    def mpco(recorderName, displacement, rotation, reactionForce, reactionMoment, modesOfVibration, modesOfVibrationRotational, force, stresses, sectionForce, sectionFiberStress):

        nodeRespType = ''

        if displacement:
            nodeRespType += ' displacement'

        if rotation:
            nodeRespType += ' rotation'

        if reactionForce:
            nodeRespType += ' reactionForce'

        if reactionMoment:
            nodeRespType += ' reactionMoment'

        if modesOfVibration:
            nodeRespType += ' modesOfVibration'

        if modesOfVibrationRotational:
            nodeRespType += ' modesOfVibrationRotational'
        
        elementRespType = ''

        if force:
            elementRespType += ' force'

        if stresses:
            elementRespType += ' stresses'

        if sectionForce:
            elementRespType += ' section.force'
        
        if sectionFiberStress:
            elementRespType += ' section.fiber.stress'
        


        if nodeRespType:
            return "recorder mpco {} -N {} -E {}".format(recorderName, nodeRespType, elementRespType)



