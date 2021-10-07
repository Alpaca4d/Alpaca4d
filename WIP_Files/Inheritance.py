import rhino3dm as rg
import math


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


class CircleCS(ElasticSection):
    def __init__(self, secName, Area, Izz, Iyy, J, alphaY, alphaZ, material, d, t):
        super().__init__(secName, Area, Izz, Iyy, J, alphaY, alphaZ, material)

        self.d = d
        self.t = t
        self.shape = 'circular'
        self.material = material

        self.alphaY = 9.0/10.0
        self.alphaZ = 9.0/10.0

        #self.crv = rg.Circle(rg.Plane.WorldXY, self.d/2.0).ToNurbsCurve( 2, 10 )
        #self.sectionBrep = rg.Brep.CreatePlanarBreps( self.crv, 0.1 )[0]
        
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


class uniAxialMaterialElastic(object):
    def __init__(self, matName, E, Eneg, eta, G, v, rho):
        """Generate a uniaxial Elastic Material
            Inputs:
                matName: Name of the material.
                E: Young's Modulus [MPa].
                eta = damping tangent.
                G: Tangential Modulus [MPa].
                v: Poisson ratio.
                rho: specific weight [kg/m3].
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



material = uniAxialMaterialElastic("s235", 210, 210, 0, 76, 0.3, 2500)
circle = CircleCS(200,10)


print(circle.write_tcl())