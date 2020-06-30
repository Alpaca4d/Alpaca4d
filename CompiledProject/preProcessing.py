from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# 1_Define Elements

class MeshToShell(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Mesh to Shell", "Mesh to Shell", """Generate a Shell MITC4 element""", "Alpaca", "1_Element")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5893c851-24e0-4663-bbb6-0b04412d8603")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Mesh()
        self.SetUpParam(p, "Mesh", "Mesh", "QuadMesh representing the structural element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Colour()
        self.SetUpParam(p, "Colour", "Colour", "Colour of the element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "CrossSection", "CrossSection", "Cross section of the mesh.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "shellWrapper", "shellWrapper", "Shell with properties.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAKrSURBVEhL7ZNdSFNhGMfPlUWE2znufc8529xsbc7NHTfJdDWbYpZWkKSyNCj7wNSSJDPLcJoWM/qyGRJEFNlFhBdhEtRteBdUd1ZEWHTRVRfRlbb9e89HRkVQXUQX+8HD4ZzzPP//w/s+D5chw7/BYTLxhPDlhJg7RItwi1JhULKYo34/l2Wk/D5+jsui1FxEiNBAKT8mUuGpSM0f2RN2OQelXkl7qu8sFljMsLzLosg3UUpFQ+ZnCDGF1GRiEeaMYhS5KBpKHRiu82LmSAnenFqD1FgFFi5F8XwgjKn2EJLb/ThQ5UJlwIpcZswae8vitiH7DZEIfRJd7EyL6iIbumvcuLlbwWy8DAvJKNLMIJWswPtEBI97V+MuM0nUFyAWdiDik2GVLGm1VpKWE0Nah51rPE+SMbF2CIPFrWj1b0P1ilI4JWnRUO2wSrGibPGYctLWguBnx7pY2rPzXDpw+hk8LeOpXxjwCTul2OPaipFgJyYjZzAdHdXiengA/aF9qPdU6UaVzfO+nul04cjL+dDVTylfYhaurnsQtxwH7w1rOYQQyZDWEQk/qtjcOOrbhR3OWoRzAvBmOxGxBBFzbMAxXwuGQ+26Qd0J2GJnka1sgqm4DuaSBtiaLsB78gnyD01qOTZBsBvSOmz8ruRbHSm102vhfkxFL2rd34mMYEhpQ5u7HmU0oBXL1R3w9D1C4fk5FN9IIzj+Af74DDx7x5FbUqPlSJLZaUjrSBZ+MxvHF+yndkk2kaA8L4RGz3p0Kc1Iru5BYtVBrdjbMQFf7wOsbIzDHqqAlOvQvrP6dywesoHpdLu5JYb09zidzqVszDayS+9Sl4oVvvpq+uOUsZF+zfLuszjMljCo1hoyf4Ysy8vYJteyQejWN5nfz5ZR+atNzpDhf4PjvgA3CByIXQYHsgAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, Mesh, Colour, CrossSection):
        import Rhino.Geometry as rg
        import Grasshopper as gh
        
        def MeshToShell(Mesh, Colour, CrossSection):
            
            Mesh.Unweld(0, True)
            
            elementType = []
            if Mesh.Vertices.Count == 4:
                elementType = "ShellMITC4"
            else:
                elementType = "ShellDKGT"
            newMesh = Mesh
            
            CrossSection = CrossSection
            colour = Colour
            return[ [ newMesh , elementType, CrossSection, colour] ]
        
        checkData = True
        
        if Mesh is None:
            checkData = False
            msg = "input 'Mesh' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if CrossSection is None:
            checkData = False
            msg = "input 'CrossSection' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            shellWrapper = MeshToShell(Mesh, Colour, CrossSection)
            return shellWrapper

class LineToBeam(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Line to Beam", "Line to Beam", """Generate a Timoshenko Beam element or a Truss element""", "Alpaca", "1_Element")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("62d77f49-538e-4406-8e43-c118566d4ab2")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Curve()
        self.SetUpParam(p, "Line", "Line", "Straight line representing the structural element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Colour()
        self.SetUpParam(p, "Colour", "Colour", "Colour of the element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "CrossSection", "CrossSection", "Cross section of the element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "orientSection", "orientSection", "Rotation angle in degrees about local X-axis.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "beamType", "beamType", "0: Truss  1: Beam. Default is Beam.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "beamWrapper", "beamWrapper", "Beam with properties.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        result = self.RunScript(p0, p1, p2, p3, p4)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAIxSURBVEhLY6Ab+M8QyvyWR9v6BbeOOFSIugBoeOZrbu2/b7m1vi1gl1UGCrFCZKgE3nBrdb7l1v7/kEvzvykTxyWg0E0g5gNLUgN84lETucGltsaXhe9vqKHo/3IX2f9A4fNAzA5WQCWwPEDG4d8+/4r//ybZ/y91BltyCohZwLJUALFqvPL/N9r2/j8aXA22JM9eGmTJcSBmAqugAsjR4FP4v9mu///JMIhP0q0lQZYchUhTB1Rp8SmCLTkTVQK2JN5cHGTJQYg0dUC7voAa2JKLCXlgSyKMxECW7IBIUwdMMhXSAltyPS0TbEmwgSjIkg0QaeqAuTaiBmBL7uSk/P870f6/n64wyJKlEGnqgOWuEuZgSx4UxP//PcHuv5eWEMiS6RBp6oB1/tL2YEuelEb//wW0xFVDEGRJF0SacgDKB1si5NzAljyviPj/o9/uv6OqAMiSWrAKKgBQjt6dqOT3f4t93/+X1aH/v/fZ/rdR4gdZUgBWQQXAzsjAeDhDJfj/Vofe/29qg/5/7bX9b67AB7IkDaKEcsAJtORkgXrU/22OPf/fNQT8/9Jj899EjhdkSTRECYVAmEGYF2jJuXLN+P/bnbr/v23w/V/nIQ+yYBVEBRUAHwOfEBMj41WQJcGyTv9dWXj/3uZQP/eaS9cYqoRywMXAJQmkbikwsh1/AKysQJXWG05tqmZCEGCJZ+AXeMupeQ1Y7f4E1o6FUHHqAmAEML7l1tCBcukBGBgA7Fvc9xvyXtoAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, Line, Colour, CrossSection, orientSection, beamType):       
        import Rhino.Geometry as rg
        import Rhino.RhinoMath
        from System.Drawing import Color
        import ghpythonlib.components as ghcomp
        import Grasshopper as gh
        
        def LineToBeam(Line, CrossSection, Colour):
        
            Line = Line
            if beamType == 1 or None:
                elementType = "ElasticTimoshenkoBeam"
            else:
                elementType = "Truss"
        
            CrossSection = CrossSection
            
            midPoint =  Line.PointAtNormalizedLength(0.5)
            parameter = Line.ClosestPoint(midPoint, 0.01)[1]
            perpFrame = ghcomp.PerpFrame( Line, parameter )
            perpFrame.Rotate(Rhino.RhinoMath.ToRadians(orientSection), perpFrame.ZAxis, perpFrame.Origin)
            vecGeomTransf = [ perpFrame.XAxis, perpFrame.YAxis, perpFrame.ZAxis ]
        
            colour = Colour
            Area = float(CrossSection[0])
            rho = float(CrossSection[6][4])
            massDens = Area * rho
        
        
            return [[Line, elementType, CrossSection, vecGeomTransf, colour, massDens,perpFrame]]
        
        checkData = True
        
        if Line is None:
            checkData = False
            msg = "input 'Line' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if CrossSection is None:
            checkData = False
            msg = "input 'CrossSection' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            beamWrapper = LineToBeam(Line, CrossSection, Colour )
            return beamWrapper

class BrickElement(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Brick Element", "Brick Element", """Generate a Brick Element""", "Alpaca", "1_Element")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5eaa283f-c4d1-45f7-9613-edfc53ef081a")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Mesh()
        self.SetUpParam(p, "Brick", "Brick", "Closed Mesh representing the structural element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Colour()
        self.SetUpParam(p, "Colour", "Colour", "Colour of the element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "nDMaterial", "nDMaterial", "Material element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "solidWrapper", "solidWrapper", "Solid with properties.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAARLSURBVEhL5VVbbFRVFK0fmJgYO3Nn7qPzaOc905l2Oi3TdvqYKX13WvqgpUxrS0sNWrQvgRbQggWkiYWWEmpECwYfRHzWoP3QSEQTo5GYKF/+NZr0y2gMEgUxneU+Zy7eGBISwp+uZOdO9j17rX3X2edM2v8H6enpelkUBijOybJQpKbvHSaj0SOL+iOypFvNNBngshohSwJko/6iLBuq1GV3D1HUl8lG4XUivuok0kdidvSV2/BSbwBPN7nBcikh3VeyrGtWy+4Mvz/tfupqgyQJn4tG4YYvS+RkK4dK8PNzZVgazMOWSCZaw1ZMNLjwzd5CjNNTISFFFq6IomGrSnU7FEWXRR19y7oq92fgRMKPo5t9GKx0YP9GD3bVu/DdU0W4MR9D8mQFLu8pRGOBBf1RG8ZqnZhPZMOTKUKSdN8rRn1cpdVAXdfwT6YIOeXk4VYvJz3VE+BCo0Ty4+ESXJuN4uJYAYZrnFjo8uPSk+sxQr/Z+u7SrJRtovCGSqtBkgzV7OVITgJV9kK+0GExYqrFg19mynnHEZ+CYq+CN7cH8ftcFD+Q4JmtOYgFTJBlI2z1gzC5AhBF4bxKq4GSdYy0z9eE96OzqHNEkPDUpjqiYJ+//EQIq0dK0VZoRVvYmnRSA2Z/GK6eGdhqBhA8sQpzbhmz6R2VVgP51siI9uVtQ5e3DpHMHJwtmcK50mcRd5bBIktcKOxR+NPky4dv5C3kvfArAs98CWukGfaGHTxPI7yk0mpgo8YKT0f244PYPFpdFdgR6ECzK4p2dyVOFk1gk3sDJ/dPfoasqj74Rt+GvXkn3APPw1bdj9DiH7AW1a/Rubmg0mqgPWhjxazrC7Hj3J4PSYjFZk81ah3FtDdhLmCPD8GSX4mc6SsInfkT+WcBR9sehE5fhzmy8SYNzLJKq4H2oIMVt7hi/CuYTbcExnK7sVg8ie3+Vi6QO7sCR8suTnwrHK0TCL34GzKjnUla85FKq4F828KKFyOTeMy/CQVWL+bCO7nAKE0WEx3OSSTZtOSduvovgbyFn8iyfsqNw+QJrtHp/kSl1SBJ+m52Is+XTSeXosfQ5anD7mAvbXApj5cjBzAU6ISsiNTpNS4QOPg1nJ1TsDeNIiuW4BbZqrcl6Zr5VKXVQKPVq0gGTvJu+Qwe9tb/Y1GHuwoNjhJU2Aq4QPb4Mh9Pd99xBOdW1rhFLbv55luC5Ul21ai0GhTlQZEdEGaTM8OMqC2UfC96lAsMBtrxSslB9PjiKYG9H8PeOMztYZvsP/AFzNnr+TtR1F0mnnaV9nZkGAw+smuBCVllGT3eOEUDXis9hEf9bVBMppQVNPNMyBKK8Y0nWy6xUbdYLA+oVHeGIAhmmudpKr7JCNh5YFbJigTv469yIcr/xYgzjLoolaxLVd4lSOghEtrH/heYEO/WqLvOiEUxPURL7kutvHesk0XDELtnKIJq7j+PtLS/AcbWE9DVEMvQAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, Brick, Colour, nDMaterial):
        import Rhino.Geometry as rg
        import Grasshopper as gh
        
        def Solid( Brick, Colour, nDMaterial):
            if Brick.Vertices.Count == 8:
                elementType = "bbarBrick"
            elif Brick.Vertices.Count == 4:
                elementType = "FourNodeTetrahedron"
            else:
                msg = "Not a valid Mesh"
                self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)
            newMesh = Brick
            
            Material = nDMaterial
            colour = Colour
            return[ [ newMesh , elementType, Material, colour ] ]
        
        
        checkData = True
        
        if Brick is None:
            checkData = False
            msg = "input 'Brick' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if nDMaterial is None:
            checkData = False
            msg = "input 'nDMaterial' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            SolidWrapper = Solid( Brick, Colour, nDMaterial )
            return solidWrapper

class Support(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Support", "Support", """Generate support for the structure.""", "Alpaca", "1_Element")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("31d76834-23e7-4358-b245-13b7c321b576")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Point()
        self.SetUpParam(p, "Pos", "Pos", "The point to restrain.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Tx", "Tx", "Translation in X. TRUE if it is Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Ty", "Ty", "Translation in Y. TRUE if it is Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Tz", "Tz", "Translation in Z. TRUE if it is Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Rx", "Rx", "Rotation about the X axis. TRUE if it is Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Ry", "Ry", "Rotation about the Y axis. TRUE if it is Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Rz", "Rz", "Rotation about the Z axis. TRUE if it is Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "supportWrapper", "supportWrapper", "Point with constraint properties.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        p5 = self.marshal.GetInput(DA, 5)
        p6 = self.marshal.GetInput(DA, 6)
        result = self.RunScript(p0, p1, p2, p3, p4, p5, p6)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAIKSURBVEhLzdRPSJNxHMfxZ0xnTdiW+bji0RlOl65kNtlwDtRDLsNu/oHhH5x4FDokxfCQURIUUXjzongQQT0peNODdBHpUCEIUVKHDvqAUamhY78+398eYU73uPms8A2vw/f5/caz59nzTDgXFV0QPzaI1fJt0SsHCmrkJqtPvmv1y5eyLUvKFm35L1d9ma97zRLVi+41ZYu2GvLd//YE9lxp474jyBJVmksycwIk6gV9q07QMcUHg2Bw4nh5bFl7OpiBTRgCBn7IWE1wAGG4CFswBxnJCKvwCcx0AD2CKNj5pLF+oFvSwadYJtiDMT5pKB++Ab1QBjoQ1xv4A1Y+nbFnQN/Ux6ejFQBd2Ss+nSG6v9swyqeTm4SfQL9T2k2ADNf4dHIuoKsY4FMa1QHd38d8Um8Z6P1IuRx4C1/BQgdOqRnoKkJ8SiHaSB+gp+RGEjcTfAZ6T1KK/sDoBOmiF68U1JOkvO4HjfbIdMjJpkLO6HhXRaSwUFzEUluc1irHlZWXLQ4208v3Re55bZuu4uLTb6mnumzo+3BtJDpSzw6FAs73yjLP6y01vQi69uL3vBv0MY/b0adsOZYID+GJ2ZS70FMrRQfv2Nghu2RZx9pTGFY8v1Ui7ocbbSwciGn3XGVGY84srUERHOk67Cp2VPxW8UvxAzrhWHqgR5T+c5LJVpEV538lCH8BgNPH/YA/5QgAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, Pos, Tx, Ty, Tz, Rx, Ry, Rz):
        
        import Grasshopper as gh
        
        
        def SupportWrapper(Pos, Tx, Ty, Tz, Rx, Ry, Rz):
        
            Pos = Pos
        
            Tx = int(False) if Tx is None else Tx
            Ty = int(False) if Ty is None else Ty
            Tz = int(False) if Tz is None else Tz
            Rx = int(False) if Rx is None else Rx
            Ry = int(False) if Ry is None else Ry
            Rz = int(False) if Rz is None else Rz
        
            return [[Pos, Tx, Ty, Tz, Rx, Ry, Rz]]
        
        checkData = True
        
        if Pos is None:
            checkData = False
            msg = "input 'Pos' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            supportWrapper = SupportWrapper(Pos, Tx, Ty, Tz, Rx, Ry, Rz)
            return supportWrapper


# 2_Define Cross Sections

class RectangularCrossSection(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Rectangular Cross Section", "Rectangular Cross Section", """Generate a Rectangular cross section""", "Alpaca", "2_Cross Section")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("44228d7f-fd91-40df-9a53-47f09c0089e8")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "sectionName", "sectionName", "Name of the section.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "base", "base", "Base of cross section [mm].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "height", "height", "Height of cross section [mm].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "uniaxialMaterial", "uniaxialMaterial", "Material element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "CrossSection", "CrossSection", "CrossSection element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAJkSURBVEhLxdBLSFRRGAfwWeS8x1pkNRHW3DvjPHQiK5s08xVMrqLHok3tiqAZZ5xHIhFmEUVEWhZkhVmWWmRGWZZCEAgFQRAFgRG0CILIQKLUrPz6Pr1nceOcw9ii/vBbnXP+f+41/I9sRvtQGqVQEiVQLYprYqhGE0URtBftQdLMQaNmpx/MTh/ygmkRyQPTQg9yg2kBUcGUo4AxxwXG+WQZZM11Ar4llVQkShb66or0QGE7zErwzAgbqKIiUWYGore4JTLB0x8z+gIj+uaK9nJLZAqaP7CBCioSZXpAqbnNLZEpOPmeDZRTkSgmNPY3A/kn3rGBMioSxYzGlFjvFK9EJnD8bcYD40rsDrek+PwEhC5Ocs8Cx4bZwHoqEsWCxpX4XW7JoV2D0Lq1i3vmP/qaDZRSkSg0MKHE+3SPq1pGYcfBN9Cy/SbcCLfCzoZhqG76pLvjP/KKDayjIlGs6LtSe0/3uC4yBH1lzTptmzp0d3yHX7CBEioSZXpA/WOAbGwagQtbOuHctm4In/oMFWe/6M69jc/ZQDEViWJDk2rivu4xs7v+JSTiT7ln3oZnbGAtFYmiDfRzS2TyDjzJaMCOfqjJB9wSGc/+ITYQoiJRHAgHHnJLZDz1j9nAGioShQZ+qqnZD7jrHrGBIioSJRv9cqcGuCUy7vQAG1hNRaLMDKQHuSUyarKfDayiIlFoYMqSWwjZwWpw5IfBEdgAdl8l2L3lYPeUgs1dAjYlBFZXEViXrgRL7gqwLFkO5sUBNiD9RZRG1IYuoXZ0GV3RdKCr6Brq1HShbnQd9aB56F/FYPgNR54SMXE+rM4AAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, sectionName, base, height, uniaxialMaterial):
        
        
        import math
        import Grasshopper as gh
        
        def RectangularCrossSection(sectionName, base, height, uniaxialMaterial):
            
            sectionName = sectionName
            shape = "rectangular"
            base = base / 1000                      # Input value in mm ---> Output m
            height = height / 1000                  # Input value in mm ---> Output m
            Area = base * height
            Ay = Area * 5/6
            Az = Area * 5/6
            Iyy = base*pow(height,3)/12
            Izz = pow(base,3)*height/12
            if height < base:
                k = 1 / (3+4.1*pow((height/base),3/2))
                J = k*base*pow(height,3)
            else:
                k = 1 / (3+4.1*pow((base/height),3/2))
                J = k*height*pow(base,3)
            material = uniaxialMaterial
        
            return [[Area, Ay, Az, Iyy, Izz, J, material, [shape, base, height], sectionName ]]
        
        checkData = True
        
        if sectionName is None:
            checkData = False
            msg = "input 'sectionName' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if base is None:
            checkData = False
            msg = "input 'base' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if height is None:
            checkData = False
            msg = "input 'height' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if uniaxialMaterial is None:
            checkData = False
            msg = "input 'uniaxialMaterial' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            CrossSection = RectangularCrossSection(sectionName, base, height, uniaxialMaterial)
            return CrossSection

class CircularCrossSection(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Circular Cross Section", "Circular Cross Section", """Generate a circular cross section""", "Alpaca", "2_Cross Section")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("1bea41ed-e455-4292-b1b8-a1845e30a9be")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "sectionName", "sectionName", "Name of the section.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "diameter", "diameter", "Diameter of cross section [mm].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "thickness", "thickness", "Wall thickness [mm].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "uniaxialMaterial", "uniaxialMaterial", "Material element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "CrossSection", "CrossSection", "CrossSection element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAOISURBVEhL3ZVpSFRRFMfnvdmdxmK0UieXSSfTqXGiIo2ZsYWoKC0orA+CUYIV9SHas+yDZbmMz/aysgiKCAp0DKKCyMosQcg2yzRbpCIySiMt63TOvWP6wkSiD9EP/jD3f8655757332j+O9RoyahclG3UI9Q9ajLqCJUAuqPoYlrDJHxEJS0GUZsqYLYHXUQu/MxRK6+ACHzc0ATEA6YU4UaSwX9RUCt1AwKa7UsPwOO4nYYcwzAcbQT7HtbIO5gGxt3KSLjJIhaAzXKYNX9YI0+PO6rLb+RTWDdcBVMCamgGWz5JoiqFoUgfFKbQiFw8lIYJTWzHFteI2iHRFGTdD7F73GrB5rbbPlN4DjcDkFzskDUDHiG/gaUFaVC0ROORGUqRGVn2KLDvEnBMxB1xk70Hahe0aBuhqcfZwVBSZm0ousoMwV7R0NN68MWH/Vt16muM+mVyfrQOLZy2hZRpW9CbwgP9Um4oNK22wqaYEzJd9AERlCTcTwkZ09ISi5biX/cLEpayu1uvO7C7DKXdMg37MlmOhOqDZ63nWo93JZTad1YAfb9H0CpN7bhOJDb3WCD016n9NA37EmoauBQ1sC6/go1qOC2nCZb/lOI2XaPEu5zi1PmlmaWOaXaUpf00uuWOkpdniuliZ54X5hQKgSx1X7gI8TmNVB9A7flvLB5nmODu5Rwj1uc8kTJQasvdRe24BO89ToLL5YlFjl9YUIliMoW+953EJtbT/VPuC2nJnprNbtIuJpPOKZXUobXJZ3ABvSp+BWLxhTa6TjyFawbr1GDSm7LOWBe6GH7OMDqpKQUbndT7pLc3kRpmW/Yk3UB7nRWa16QT7W7uS0n2c8yniVFriqnJNpHkUX6xiyqDc3RWdVAT2CITKDaaTwkR4lqiFp7iTUxTUylxKss8nuCUdeDkrewGsvKc7i9wh30dCzaC9PVpmH8g1byDUzONGpCb1QqqueZ0AWcj5excejsTexyjip6BdqAiHb0Z7GMPigwDJ+ARR18u/DTbIyZSgffgbE61AOln3+rMWYKRGfdZjmjd73uOrccmqA/FOmCo2FE5g02AclR/Jm9wiT7vvc/fbpYumDrF6zJQ2lZdT9JQr3xHz0DwpaUAH1haevoMsVk3/1uWXEWDFEJIIjaWsxLZhV/SBrqNOoFbtNn/E9oxd/013keNRdlRP016E3T85//BArFDwNDi+itbTxeAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, sectionName, diameter, thickness, uniaxialMaterial):
        import math
        import Grasshopper as gh
        
        def CircleCrossSection(sectionName, diameter, thickness, uniaxialMaterial):
            sectionName = sectionName
            shape = "circular"
            diameter = diameter / 1000          # Input value in mm ---> Output m
            thickness = thickness / 1000        # Input value in mm ---> Output m
            if thickness == 0 or thickness == diameter / 2:
                Area = math.pow(diameter,2)/4  * math.pi
                Ay = Area * 0.9
                Az = Area * 0.9
                Iyy = math.pow(diameter,4)/64 * math.pi
                Izz = Iyy
                J = pow(diameter,4)/32 * math.pi
            elif thickness < diameter/2 and thickness >= 0:
                Area = (math.pow(diameter,2)-math.pow((diameter-2*thickness),2))/4 * math.pi
                Ay = Area * 0.9
                Az = Area * 0.9
                Iyy = (math.pow(diameter,4)-math.pow((diameter-2*thickness),4))/64 * math.pi
                Izz = Iyy
                J = (math.pow(diameter,4)-math.pow((diameter-2*thickness),4))/32 * math.pi
            else:
                msg = "Incorrect values. Thickness has to be greater than D/2 and greater than 0"
                self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)
        
            material = uniaxialMaterial
        
            return [[ Area, Ay, Az, Iyy, Izz, J, material, [shape, diameter, thickness], sectionName ]]
        
        
        checkData = True
        
        if sectionName is None:
            checkData = False
            msg = "input 'sectionName' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if diameter is None:
            checkData = False
            msg = "input 'diameter' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if thickness is None:
            checkData = False
            msg = "input 'thickness' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if uniaxialMaterial is None:
            checkData = False
            msg = "input 'uniaxialMaterial' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            CrossSection = CircleCrossSection(sectionName, diameter, thickness, uniaxialMaterial)
            return CrossSection

class GenericCrossSection(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Generic Cross Section", "Generic Cross Section", """Generate a Generic cross section""", "Alpaca", "2_Cross Section")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5f512ee2-2cc3-432a-a2b0-50e6b92a6be3")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "sectionName", "sectionName", "Name of the section.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Area", "Area", "Area of cross section [mm2].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Ay", "Ay", "Shear area along Y local axis [mm2].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Az", "Az", "Shear area along Z local axis [mm2].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Iyy", "Iyy", "Moment of Inertia about Y local axis [mm4].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Izz", "Izz", "Moment of Inertia about Z local axis [mm4].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "J", "J", "Primary torsional moment of Inertia about X local axis [mm4].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "uniaxialMaterial", "uniaxialMaterial", "Material element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "CrossSection", "CrossSection", "CrossSection element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        p5 = self.marshal.GetInput(DA, 5)
        p6 = self.marshal.GetInput(DA, 6)
        p7 = self.marshal.GetInput(DA, 7)
        result = self.RunScript(p0, p1, p2, p3, p4, p5, p6, p7)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAJESURBVEhL3ZVdSFNhGMd3HFs7U7NsGM21oZgVeOp0IRURRhixJLRoGo1GRR8glCAh3lSYGSoL/CCiXEWrLsoubFlIURAEQUVdCBkRdhFd9HFTNxVS/57nHW9w3IGzs7yIfvBjnJf3+f/hvC9njn8FF+klFfE0Q7jJMPmM/ET+IL+Sd8nD5F8xi0ySyC9fCd/6ZizYegIlG1vhCVSB18knZM7sJeHfdhLLz33DioswGNxzQZZEeHMu3FMXLoM+9D0jnNUTU3DmF3PBpfR2+7yeuypqGi6drYW54GV6u30m5lRHTIOl/kgPF/wkS8WETcbUgGYaLNUGPspzSIkJm3QpLo9412bh0tLtcVnygCzgwWw5SEIb/GwIbOh+jx0dbwxrwd0JWfKWDJBZ0eJQlIyC7tgoEvVJwxq7pOMF8twql9xKj1vTx9dQXtOmzkn07kzhSjiB4drTiEdH0Nry2FDib+zlAj50v0iw4KYa1P8Mx468wlDDZaRq+nBtwxmc3XIVXbvuGAoWtT+Ur6pWJFjwvEjfbAhg+5tuYLBxOGOdLT80IgtWiwQLHnnLqjNCNsU/oI6cvs76avZzOH8UC0WCBW0kKtrum4ZNt+rUOzjVIi7oF9NZoJITeZ5CLD761DRUqp+fgm/dAQ7nT3kFD2dLiJxUnC4EogOm4Us7x1G8JkbhChccF1M2KSHHSLjnhTC/rh1lzdcR2pdEQeVauvteDv5CHiM9ZM7Uk7fJXySH8u842UNWkjMGn41Gcij/T//3OBy/AVaB2sWGqN/qAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, sectionName, Area, Ay, Az, Iyy, Izz, J, uniaxialMaterial):
        import math
        import Grasshopper as gh
        
        def GenericCrossSection(sectionName, Area, Ay, Az, Iyy, Izz, J, uniaxialMaterial):
            sectionName = sectionName
            shape = "Generic"
            Area = Area / 10**6     # Input value in mm2 ---> Output m
            Ay = Ay / 10**6         # Input value in mm2 ---> Output m
            Az = Az / 10**6         # Input value in mm2 ---> Output m
            Iyy = Iyy / 10**12      # Input value in mm4 ---> Output m
            Izz = Izz / 10*12       # Input value in mm4 ---> Output m
            J = J / 10**12          # Input value in mm4 ---> Output m
            radius = math.pow(2*math.pi*Area,0.5)
            material = uniaxialMaterial
        
            return [[ Area, Ay, Az, Iyy, Izz, J, material, [shape, radius ], sectionName ]]
        
        checkData = True
        
        if sectionName is None:
            checkData = False
            msg = "input 'sectionName' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Area is None:
            checkData = False
            msg = "input 'Area' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Ay is None:
            checkData = False
            msg = "input 'Ay' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Az is None:
            checkData = False
            msg = "input 'Az' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Iyy is None:
            checkData = False
            msg = "input 'Iyy' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Izz is None:
            checkData = False
            msg = "input 'Izz' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if J is None:
            checkData = False
            msg = "input 'J' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if uniaxialMaterial is None:
            checkData = False
            msg = "input 'uniaxialMaterial' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            CrossSection = GenericCrossSection(sectionName, Area, Ay, Az, Iyy, Izz, J, uniaxialMaterial)
            return CrossSection



# 3_Define Materials

class nDMaterial(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "nDMaterial", "nDMaterial", """Generate a n-Dimensional Elastic Isotropic Material""", "Alpaca", "3_Material")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("031cde6d-1623-4742-9734-2ad675a47ae2")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "matName", "matName", "Name of the material.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "E", "E", "Young's Modulus [MPa].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "G", "G", "Tangential Modulus [MPa].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "v", "v", "Poisson ratio.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "rho", "rho", "specific weight [kN/m3].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "fy", "fy", "Yield stress value of the material [MPa]")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "nDMaterial", "nDMaterial", "Material element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        p5 = self.marshal.GetInput(DA, 5)
        result = self.RunScript(p0, p1, p2, p3, p4, p5)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAMJSURBVEhLxZVtSFNhFMev291ac3Nuend9uepcM9vUZsvpNkQqzVopiKAmClqm9ELpsBRHRYpBoNILGe5LGFZQFiFpoWLoiL4GBZGfoyDog6worfB0nt3rsqbZTOoHP/if8zy7Z2zPvZf610jRE+gFf7XGKNCbKAg+QWl0MesEV4Ua/YiSi39B36MWNIDZLL5cUSH1YUznO6EjRp+iY+iv3zS1pUX2YWAgHEQiqkLorQov+oiPP8Bvf3VsTAG1tZLXWEbw3dVBBgzzMUC8yyXzDQ8rICkp7KzQWzVkwBAfeXQ60Sly8dZWGfmP9Hw3AM0ymm6tNrJaqFeEDLjPRz/Sqir65eioAiwWcZ/QC8BGaw5Up+2G+owSsOsy3rKMujNRpSIHZlnIgLt8pCilkiru7ZWD2y37JJVSG4W2H4ZhYrKSjW96HI1w3nEUXLZ9cNpaB9ZE0zzHRWiEbUGQAbf5SIXl59MTU1NKKCigHwq9AIY4ztOe3QBt9ho4ZisDT24bHM8uhw2cDlhWlSxsC4IMuEUCTVN5PT3ybx6PHORyai/pLaDVamzZ3KY5V1YldDoOgdteC2fsdVCe7oR4666ZqKioOGFrEGTADRLy8ugHk5NKKC2VPsPyp/sCB+w8uccIVyrToMi0BdyW/dBua4DNWUUQqzf1CtuWhAy4jpo7OtbP9veHg0ZD1fhXFhGv0XDFloTpRmcqeFtyoKvcBI4UPcSZt3/GE5UhbFsSMuBaZqa4b3xcAXiCplmWCueXgomJVjszDczEkQIDlNmTgOUS7glLy0IGjDQ1yWYGB8OB0+fOYl3nX/kNsdHRW/F+6NNq1XahtSxelSpsbmhIAfX1kncqxvHClNNNHoA7+OW/x1tYKIGREQUYDGGdWDMJhhpfVMw28hBcE7ylpRJobpb5Fm4smZy7mGRq/IqRvDMWIPkxWuCvQsBrtdJgNIqeYyZnvwTt0iY4yc/Uih5ED6NtKOmR51NI74c7KPngSs4vypfQkIj8A1NQcvFXKIuuOSL0HJrmr/4PFPUdNJPeLvAI20IAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, matName, E, G, v, rho, fy):
        
        import Grasshopper as gh
        
        def ElasticMaterial(matName, E, G, v, rho, fy):
        
            E = E * 1000                               # Input value in N/mm2 ---> Output kN/m2
            if v == None:
                G = G * 1000                           # Input value in N/mm2 ---> Output kN/m2
                v = (E / (2 * G)) - 1
            else:
                G = E / (2 * (1 + v))
        
            rho = rho                                  # Force Density
            fy = fy                                    # Input value in N/mm2
            materialDimension = "nDMaterial"
            materialType = "ElasticIsotropic"
            matName = matName + "_" + materialDimension + "_" + materialType
        
            return [[matName, E, G, v, rho, fy, materialType]]
        
        checkData = True
        
        if matName is None:
            checkData = False
            msg = "input 'matName' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if E is None:
            checkData = False
            msg = "input 'E' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if G is None and v is None:
            checkData = False
            msg = "input 'G' or 'v' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if rho is None:
            checkData = False
            msg = "input 'rho' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            nDMaterial = ElasticMaterial(matName, E, G, v, rho, fy)
            return nDMaterial

class uniaxialMaterial(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "uniaxialMaterial", "uniaxialMaterial", """Generate a uniaxial Elastic Material""", "Alpaca", "3_Material")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("830c3037-c8d3-4e02-b58f-25a0361bdfab")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "matName", "matName", "Name of the material.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "E", "E", "Young's Modulus [MPa].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "G", "G", "Tangential Modulus [MPa].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "v", "v", "Poisson ratio.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "rho", "rho", "specific weight [kN/m3].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "fy", "fy", "Yield stress value of the material [MPa]")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "uniaxialMaterial", "uniaxialMaterial", "Material element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        p5 = self.marshal.GetInput(DA, 5)
        result = self.RunScript(p0, p1, p2, p3, p4, p5)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAKvSURBVEhLxZVvSBNxGMd/u91ut7ubV4Ytc7K1pqLTHAMJIqRyGRWj2BuDQRPKF73KYShZL3JUECWVYOibMMygDELSQqXQERH0IkoIe9MbISim2aywP/Tree53s2WWzkZ94MOe5/vj7jlu97sj/xoBPAKe17oMo4A9INV9APJgKmbdZbESfA/iyT+DcdAHzlFebmyrqRESUJayJH2M4ENwCJx/pUWNjeJMd7dMOY7U6NmyiIF3WfkDuPpLQ0MKra01TUCbxdJfyHskutvisqdT7xcEB/Szco68SERM9Pcr1OEwnNCz+TizRG4slzPRx+b1k9NqGd7yBcEBfaxkOJ3ccTx5U5OI/5GLpT9RqFqM42f2uKhnrfwhl5hCer4gOOAWKzWEUIh/PjioUJ/P2KFnqZRaLcaXpwPrqNcuzUC/n8W/BwfcZCUhVisJtLdLtLlZ/CgIpFCPk/isAj/RsstJPbmWd9DvY/GfwQHXWUkMVVX8vdFRK/X7+Tt6lqRCNfOvju1w0IIc81vogyxeHBxwDQueJ5WtrdLXzk6JShLZjRnyVC4qg583ka126sg2T0Ed0BaWCA64ikVlJX97ZMRKg0HhCbRz+yJu8fS0CDbckLgZt2thGuCAK2B5NGqZ7eqSaXY2CWsrOlNy6YZJ2RMNm1WnHqUFDrjs9Ro7hocVCk/QC5uNyGwpM+CAgfp6cbq3V6Z21+ZZ6A9oKxkipqqGT319Cq2rM71WczaNlWw8h/d7G1v+e2LV1SY6MKBQt9twEvqcfHc4sWrNFnwJZoRYMGiiDQ1iIrmxRMl+wVFy+AuU+M1IgvV90K91aRCrqOBpcTH3DGp89veCZ1fn78Tb1AQeBA+BR0HM8P2U1vfhBogHLua3lPoimBYrlmABiCcfB21gxuHAU6BH6/4PhHwHVzW3i/6kg4cAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, matName, E, G, v, rho, fy):
        
        
        import Grasshopper as gh
        
        def ElasticMaterial(matName, E, G, v, rho, fy):
        
            E = E * 1000                               # Input value in N/mm2 ---> Output kN/m2
            if v == None:
                G = G * 1000                           # Input value in N/mm2 ---> Output kN/m2
                v = (E / (2 * G)) - 1
            else:
                G = E / (2 * (1 + v))
        
            rho = rho                                  # Input value kN/m3
            
            fy = fy                                    # Input value in N/mm2
            materialDimension = "uniaxialMaterial"
            materialType = "Elastic"
            matName = matName + "_" + materialDimension + "_" + materialType
            
            return [[matName, E, G, v, rho, fy, materialType]]
        
        checkData = True
        
        if matName is None:
            checkData = False
            msg = "input 'matName' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if E is None:
            checkData = False
            msg = "input 'E' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if G is None and v is None:
            checkData = False
            msg = "input 'G' or 'v' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if rho is None:
            checkData = False
            msg = "input 'rho' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            uniaxialMaterial = ElasticMaterial(matName, E, G, v, rho, fy)
            return uniaxialMaterial



# 4_Define Loads

class PointLoad(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Point Load", "Point Load", """Generate a point load.""", "Alpaca", "4_Load")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("ec152d87-d9a8-447d-b636-770d5e0e8623")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Vector()
        self.SetUpParam(p, "Force", "Force", "Input force vector [kN].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Vector()
        self.SetUpParam(p, "Moment", "Moment", "Input moment vector [kN].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Point()
        self.SetUpParam(p, "Pos", "Pos", "Point to apply the loads.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "LoadWrapper", "LoadWrapper", "Load element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAANmSURBVEhLrVRbSFRRFB3ooyLEpqLMLLPuPWfmzvPec++d0RmdzEwn00SzyN4PsuihZU+jog+DlLAkooJKsDAfAz2QmAhKKwqin6h+qo/+hIiCioqw3T4zh4E+qoGZBZcZ9tlnP9Ze+1iShceTOzHolXcaTNoiTOmFyci+DXYKYQ8FTaMuYU4fDI30RKbbYb9sA5PJa4Q5fWBMvh2dqsCRuTbQNXmzMKcPhibfGJwW70BXySphTg1Bl8tqqKQEK27B3zcNNgrLnRRSHrTfr0wymNwRNMjI5kVO6FyrwvUdBvRtM6B1hReK/RR0RoZ1XaoVV5KH3yPPMJn09ECtG14dLYC7zT44sdILqxc6oL7UAS1LPXBtqw6DTSasWKAAUvfINKUccf3f4FpnjAydXa/BkwN+qArRr0jNHYOR3fj7rCvHDvUOpEiVHgZNCh2rVehu0Dlln3WdFogwf4euSSePLvPA0F4flOTb3hsaLRNHFkwSuZllhybChyzX8KqRpi7eBffH80+GSnVTkyv4zPz+nPHiahymSfLKC8iX18cCEA5QrIiExVEMKNMr/bgHjZgAl65amHni1o1hJ9zHJEyVfjZUOGHrYidKmXQKlzh4VbXFCnB6UIanhTkBDHSpJ9sO2ylSpEmLhRnlS8tCfjr6oa0QPrUXwo9TRbEZIW1nhEscoVDuOE4D08gLVbXnCnMCOJvL1zDBDsopkiq5zacS96KA/dvzw/nwqzOU+A6hEHD462IXkwV2dXUAKdqFFDFGl3LbplJ3XgCHfWEjg+8dRbHgH7GLknzyJWll1dVZxmD1QUOV793CTeZDxuqa+a7wc9MrKZy+hQEb9OOe9HB6NDIQu5wMdI021jnpaDMGfjlRgYso1SoXhUKVcOW0CzeLYche7DKKEn6PHc4T5v8DJbeHvz8fJjj++C7MtGMCuVu4JcA7Fn+Tg9vtnsBUMvJwipIIfhupKvKSEVwuKtxSA5dwuYfA60wFHk9WYL6X/LELKQO5bqupzoNSDFxpyrB+3azYcyGOUwe+Q28jESv09VlHe3utMDycASXFEvg8dLZwSQ2Y4B0P/OBBRuyLRjOhODTnu67PnSlcUgM+DfW84paD2XC8NQuWVOZxiZ4Xx+kB1znK8hgu0TldlxdIkjRWHP0DFstvp+ZXghZyHJMAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, Force, Moment, Pos):
        
        import Rhino.Geometry as rg
        import Grasshopper as gh
        
        def pointLoad(Force, Moment, Pos):
        
            Pos = Pos
            Force = Force                   # Input value in kN ---> Output kN
            Moment = Moment                 # Input value in kNm ---> Output kNm
            loadType = "pointLoad"
        
            return [[Pos, Force, Moment, loadType]]
        
        checkData = True
        
        if Force is None:
            checkData = False
            msg = "input 'Force' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Moment is None:
            checkData = False
            msg = "input 'Moment' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Pos is None:
            checkData = False
            msg = "input 'Pos' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            LoadWrapper = pointLoad(Force, Moment, Pos)
            return LoadWrapper

class LinearLoad(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Linear Load", "Linear Load", """Generate a uniform Distributed Load""", "Alpaca", "4_Load")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("d2fb15cc-0730-46b1-bbc2-4495638a101f")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Vector()
        self.SetUpParam(p, "Force", "Force", "Straight line representing the structural element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Curve()
        self.SetUpParam(p, "Element", "Element", "Cross section of the element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Orientation", "Orientation", "0: Local axis.  1: Global axis. Default is Global axis.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "beamUniformLoad", "beamUniformLoad", "Load element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAARqSURBVEhL7ZN/TFVlGMcv9/JLuPee8573vOfc38AF7gXUgsiQKJkO1EKyiBleYTPJXKZNiSWoQAranCs2+KOWV0EgW621Vs7KP0qTfmrGrEmYUWJFKsJQZ8DlnqfnhfsPyRr9+Ket7/bZPefunO/zPN/3Obr/hDIoK3PKtDl0+8/EmDkxLi4uWlGkvAKq9Flkcv9qyd7bIMYFbZR6Q4/9NVllOVNRRB+l1FQkWS/fI7MLDkYaT5g8QRV/14uOG3Wia5wxljT5xgykKIL7NsZesVjovBxJOfwcdqgyaeMLYrxWKtquJTPq/9zkDSoK2V0tuG7UkhkUcAkCWU6Uky6Z7maMVB4zJQUsCmkpJmp3m+Dm3VbtF9xQQi0D2ZT5T5m841j0+RriGKkizoAsy56Q1fRC05wWwa09SK29doU0d5k8AcZE/6OivbtFiMdrUvmqkAgPUfVqpiy3fzk5QfPTxD5WQ1ya1UpcIavppcpiwRvmRLiPKN0eSpvOGFNGMPv964njnN/svokT7DqIE6yUbJdnM+kQTqDxCTYRx3gFcWIxRQ1ZTS++EUfMyZAvqT0psvzieaN3FDtsXU2s3x0Q3BgH2YERBX2i5ac0Rl/7GCPEbXp9C3Fq5ZI9wCMOWU0vxqSi97DAYqL2JDDp5bPGVH6wL/mopc8/eQYNTXjIS6g6hJv0xV4xHjpwoi5jioYbBY+Jtn4smB+yu1UWJhW/ZU7SCqly1iFL7adNyWM841LR+ss24gouJ5ZzGJHmozboj02DPmMarJXscAmvfzSmwmZiH/zTAmi28k1zUnAhZb1JMmnrEBK1VZJlpNXk5msIH2GXV2Nnw1GcEtcWLqLxs2bntQWy8u0iSemKjo6sQJtnJt3+IFWVsrD6VowCyiSbxs2/Mnr59YQp53HslkfIN2oOpe+miuSHWZGRB/H1TmQgLEw3ir+A5CFThR9VN8/xvDFVW4dGnaFuD2EhXgQLj6Npp9kc+3ZUVOQpfOVrJCDFRgTzU4jmX+XVerbfFUy3GnmRA9xzivg3sIE4gtyU7/cdlP7Gc/cIQj+Ovi8iPHwQHxtAIEWNCfrmqWPHN6VrV3bnaFpTLnAGaotg293ZAXxmGNEjU4URzV8qKYMeQdTCww2tBoN+CP8OREfo4d5EAbYviYPTWzJhpHHBhOH1XQXQX1UCn62ogg+X7YR9WdXwlKeER8S55bB5bu8jPyOgmCIgL5kE2spS4Pu6rAnDQOMiuFLzMHxTvgGOFe6Ajux6qJ/7BBQ5FkJCrA3Cwwzc+BJyFElGpuidqHC99kiGMvxJRQYM7cmZMB2uL4SLlaXwafFWOJy3E/bcvhHWuB+AJJMTZhmiuOFN5ASyF8lETMi0WqMP08GFulz4tXoFdvkkfFBYC813VsJmrw8yiDcoR4nccBw5g7QjSxEnMiPxzxzKE5aN1s1ZC4st88ERo4I+TM9NeWxHkHVIGmJA/pZOItzwOnIcaUDSkRjkX9FcJBexTtz9L51O9zsEcKijZtOWTwAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, Force, Element, Orientation):
        
        
        import Rhino.Geometry as rg
        import ghpythonlib.components as ghcomp
        import Grasshopper as gh
        
        
        def uniformLoad(Force = rg.Vector3d(0,0,0), Element = None, Orientation = 0):
        
            if Orientation == 0:        # Values on local Axis
                localForce = Force      # Input value in kN ---> Output kN 
            else:
                midPoint = Element.PointAtNormalizedLength(0.5)
                midParameter = Element.ClosestPoint(midPoint, 0.01)[1]
                perpFrame = Element.PerpendicularFrameAt(midParameter)[1]
                xForm = rg.Transform.ChangeBasis(rg.Plane.WorldXY, perpFrame )
                localForce = Force
                localForce.Transform(xForm)
        
            elementLoad = Element
            loadType = 'beamUniform'
        
            return [[elementLoad, localForce,  "leaveEmpty", loadType, perpFrame]]
        
        
        checkData = True
        
        if Force is None:
            checkData = False
            msg = "input 'Force' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Element is None:
            checkData = False
            msg = "input 'Element' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            beamUniformLoad = uniformLoad(Force, Element, Orientation)
            return beamUniformLoad

class MassLoad(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Mass Point", "Mass Point", """Add a concentrated Mass to a node.""", "Alpaca", "4_Load")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("4136e613-b68e-4116-a698-e994580bb72d")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "NodalMass", "NodalMass", "Mass at point [kg].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Point()
        self.SetUpParam(p, "Pos", "Pos", "Point to apply the nodal Mass.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Mass", "Mass", "Mass element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAJiSURBVEhL7ZPbS5NhHMefd+/ed+7dyc0GuTZjujnXDupWLbFyQgTaVQf/gLrqxosgCDp4oRd2pJAIKoiCdWNdhRSUFnkYJQkd8CbCLDuwQjdbF9nNt9+7rcXamsZ2FX3gw+D5PTyfd++zsX+aXSLjBiVSx/GDavqktc70qAwIjOu7q67Fy421eB1wIKp2QMlYT2ZcOhToHfbUIDpiwNiYDg9CtvIHRjbbUodPPDRg1Lu2/IFRqQ5vG9x45XdgwuCAgrFjmbGMHDtbwCPkiminS75Kl3vtp7SWveQtvDo2qXZiinwq1eMFOS25sJXXvM9sKY02XhuL1/jx+agPM6fr8PGkBwlXIzp4XXkC7XLA58fj+6bUPY2P6rEYbCoaaCW3/cE2MoftvC4WD/pTh8s+GV61bOB6n7gaZ1QWnCMHyPOqNbhAhnktaG5Mb0tDB8US9Y1IHlqPTz0+xA83Y9FfJMAxFpmRGlKbvoQCSLYG8DUcRNziwz7BlBdoVqhiQxV2/C49TOEAz7jIrORGojeAZ3eq8fy2BbM3nEi2BAoGiD3k3gLuIPNRUuANBeYGXNn3OnXPXCzwd6goMEeB2UvObGB6yFq+AP2RIu80bnw70YLE5SDmrzQheXHDigI6xnc6mNhlJ6uZuDOznIuW4yIfNOuwUOnFgvGX83pP0QANFB5FxffjoSr0dxmwWzDAygRvZpxDd6NCfES/jjxtnBCluSG9LRewNmWHWbM0PqxPvdYDm/SwM8GXGZeO/A3Conbp1n4zbvZWottoKm9ApoopD9o54ZSslRP6aakyPfnPsjD2A7l9Hz3pbcJ9AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, NodalMass, Pos):
        
        import Rhino.Geometry as rg
        import Grasshopper as gh
        
        
        def MassLoad(Pos, NodalMass):
        
            NodalMass = rg.Point3d(NodalMass, NodalMass, NodalMass)
            return [[Pos, NodalMass]]
        
        checkData = True
        
        if Pos is None:
            checkData = False
            msg = "input 'Pos' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if NodalMass is None:
            checkData = False
            msg = "input 'NodalMass' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            Mass = MassLoad(Pos, NodalMass)
            return Mass





class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Alpaca"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return "Marco Pellegrino - Domenico Gaudioso"
    
    def get_Id(self):
        return System.Guid("9bfbb08d-6b4d-446f-b226-cfe680dabf16")

