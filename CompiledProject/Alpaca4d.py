from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import GhPython



# 0|Define Materials

class nDMaterial(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "nDMaterial (Alpaca4d)", "nDMaterial", """Generate a n-Dimensional Elastic Isotropic Material""", "Alpaca", "0|Material")
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
        
            E = E * 1000.0                               # Input value in N/mm2 ---> Output kN/m2
            if v == None:
                G = G * 1000.0                           # Input value in N/mm2 ---> Output kN/m2
                v = (E / (2.0 * G)) - 1
            else:
                G = E / (2.0 * (1.0 + v))
        
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
            "uniaxialMaterial (Alpaca4d)", "uniaxialMaterial", """Generate a uniaxial Elastic Material""", "Alpaca", "0|Material")
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
        
            E = E * 1000.0                               # Input value in N/mm2 ---> Output kN/m2
            if v == None:
                G = G * 1000.0                           # Input value in N/mm2 ---> Output kN/m2
                v = (E / (2.0 * G)) - 1.0
            else:
                G = E / (2.0 * (1.0 + v))
        
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


# 1|Define Cross Sections

class RectangularCrossSection(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Rectangular Cross Section (Alpaca4d)", "Rectangular Cross Section", """Generate a Rectangular cross section""", "Alpaca", "1|Cross Section")
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
            "Circular Cross Section (Alpaca4d)", "Circular Cross Section", """Generate a circular cross section""", "Alpaca", "1|Cross Section")
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
            "Generic Cross Section (Alpaca4d)", "Generic Cross Section", """Generate a Generic cross section""", "Alpaca", "1|Cross Section")
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

class doubleTCrossSection(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "double T section (Alpaca4d)", "double T section", """Generate a  double T cross Section""", "Alpaca", "1|Cross Section")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("2b198612-d5c6-4172-b861-8fe8d869cffb")
    
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
        self.SetUpParam(p, "Bsup", "Bsup", "Width Top Flange")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Binf", "Binf", "Width Bottom Flange")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "H", "H", "Height of section [ mm ]")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "tsup", "tsup", "Top Flange thickness [ mm ]")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "tinf", "tinf", "Bottom Flange thickness [ mm ]")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "tw", "tw", "Web thickness [ mm ]")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAIGSURBVEhLYxhIwAXEpkBsQQSWBWKSgQ8Q/ycS/wFibiAmCXgB8X/F7NX/VSsP/VerOf5fvf7Mf42mC/81W6/+12q/8V+r6+5/hfSlMEtEQJpIAWALNBrP/9fuffRfq/POf8P5/+FYu+seWFwpbyPZFtgDMUwzGIMsA1sw799/TjkDZLlPQCwExCQDbSA2AeIMIEZYMB9ogYwuyOBWqLwOEFMErID4v2rFAXgQsYspgyzIBctSAYAtUKs6AreATVSRBhYAUxLcAhHFf0Ax6lqgXn8ayQKFv0Ax6lqAiGRQEClRP4iMak79L88+/N9qxnfqW8DKxPLfpXD//812/f/jam/85xJTpZ4FE4yLXJdbtf5fZ98HtmCj/YT/a2y7/+vwKVPHAmVeOaswOdf/DRErwRY0Ju/6H6Dq/1+UXYC6ceBdehxsQUDHE7LjgBGIJYFYDA27AfF/3Umv/ge3PfpvNvv3f05ZPZAFdUhqYJgZiHGCSCAGZSCQZgysP+PLf4PZP8HJlFPOEKsaIN4NxDhBHAMj43+ZqAn/5RLn/JdLnvdfPnXhf4W0Jf8Vs1b9N5jzC54PQOWSctH2/yolu/6rlO39r1p+4L+wbRLIgssQo7CDOCY2rv/6M7/CDSIFS4W0E7QglpGJ5T+Pmt1/HnXSMbs4OG/gtQAUSZ1A3E8BjgBiegEGBgCt2GE7BlaH+gAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, sectionName, Bsup, Binf, H, tsup, tinf, tw, uniaxialMaterial):
        
        import math
        import Grasshopper as gh
        
        def doubleTCrossSection(sectionName, Bsup, tsup, Binf, tinf, H, tw, uniaxialMaterial):
            sectionName = sectionName
            shape = "doubleT"
            Bsup, tsup, Binf, tinf, H, ta = Bsup/1000, tsup/1000, Binf/1000, tinf/1000, H/1000, tw/1000     # Input value in mm ---> Output m
            A1, y1 = Bsup*tsup, (H - tsup/2 )
            A2, y2 = ( H - tsup -tinf )*ta, (H-tsup-tinf)/2 + tinf
            A3, y3 = Binf*tinf, tinf/2
            yg = ( A1*y1 + A2*y2 + A3*y3 )/(A1 + A2 + A3 )
            Area = A1 + A2 + A3
            ky = Area/ A2
            kz = Area/ ( A1 + A3 )
            Ay = Area/ky # da riguardare
            Az = Area/ky # da riguardare
            Iyy = Bsup*tsup**3/12 + ( Bsup*tsup )*( H - yg - tsup/2 )**2 + ( H -tsup - tinf )**3/12 + ( H - tsup - tinf )*ta*( math.fabs(( H - tsup - tinf )/2 - yg) )**2 + Binf*tinf**3/12 + Binf*tinf*( yg - tinf/2 )**2
            Izz = tsup*Bsup**3/12 + tinf*Binf**3/12 + ( H -tsup - tinf )*ta**3/12
            #J = Iyy + Izz
            J = 1/3*( Bsup*tsup**3 + Binf*tinf**3 + ( H - tsup - tinf )*ta**3 ) # Prandt per sezioni sottile aperte
        
            material = uniaxialMaterial
            print( Iyy, Izz, yg )
        
            return [[ Area, Ay, Az, Iyy, Izz, J, material, [shape, Bsup, tsup, Binf, tinf, H, ta, yg], sectionName ]]
        
        checkData = True
        
        if sectionName is None:
            checkData = False
            msg = "input 'sectionName' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Bsup is None:
            checkData = False
            msg = "input 'Bsup' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if tsup is None:
            checkData = False
            msg = "input 'tsup' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if Binf is None:
            checkData = False
            msg = "input 'Binf' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if tinf is None:
            checkData = False
            msg = "input 'tinf' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if H is None:
            checkData = False
            msg = "input 'H' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if tw is None:
            checkData = False
            msg = "input 'tw' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if uniaxialMaterial is None:
            checkData = False
            msg = "input 'uniaxialMaterial' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            CrossSection = doubleTCrossSection(sectionName, Bsup, tsup, Binf, tinf, H, tw, uniaxialMaterial)
            return CrossSection

class RectangularHollowCrossSection(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Rectangular Hollow Section (Alpaca4d)", "Rectangular Hollow Section", """Generate a Rectangular cross section""", "Alpaca", "1|Cross Section")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("1a9b9268-eeac-440c-9ccd-449aeb0b53eb")
    
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
        p4 = self.marshal.GetInput(DA, 4)
        result = self.RunScript(p0, p1, p2, p3, p4)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAMxSURBVEhLxZXZb0xhGMZ7QWemm15Yugzt7DPtTKO0Ss2iJCIuGokLf4FIdF+IFFVqDXpGiYjY90i16QylEiKhVFFbEYnEhcR+QUJLMa/nPXO+aMTX1A1P8kvOOc/7fs853znn+2L+hxaAZaAW1IBqUAUqQYVGOSjTKAUlYClYAobVKPBBn+oifaoTOEiXwthJN8EGrKQbz1hIN85MseNMFDuWyaTRY1IJvUwRDyTTaPDJVNJCuQfpr/DsfC8CZvNAMkUDSs+QO/iKEhwBSrB5KcHui+LwR685mVmgiMbkFlPO7o/k2fFmRE8QCz6bSlvJ2dArGvYCBQQ1doBmsBOcBORouENu5aWonwWkUgPMZW1qE46ZTDYksgH1ZtzbX4j6ABsy6UC/GrDmtmjIYEMiFyDn2ruUvfW5qPezIZMe9JvLWyNDAiaxIZEHIOAeZW15NuKAAXN5Oznqb4mGiWyw2gJK8unArgTtlJULyLkOAZueinofGzIZwIC5IoSA7giOucHIBivsb9oX9m7v0U5Z+YCcjffJtfGxCPCyIRMHfDFXhMmx+qZoMLb7mk0hX3BhyKtcDnuVdyGfsqjdG8yBN4NrnI0PyLX+oaifCaSKA1/NlWfJ/isgPeRr2hz2K/QbffB4vtXBeZq0+kIglRpgUQO6RUMaG+FA0I277w37lBuhwDZnm28bvxv+axHQN/Sz5qeSKh4MWqrOkX3VDdGQygYrHFAWh/xKvXbKmgvIteER3lmPqJ/OhkxaQAcCrouGFDYkmg/UgCH1wwbwJ/jNUn2e7CtHFFAM1C/IVndV1BewIVMiQMAFBHSJhglsSLQQIOAJ2VZcEfXT2JCJA75bahBQd0008EK3GTSBXWAP2A8Ogy6gBliXXxL1/G9IlQR+WGs6ydP8luKxVBsycskwiZmMDcg1aDB6IoD0Rjfp090Ul5mHpfo1WWs7RUAeDyRTNKD24h83leGwVHeIgKk8kEwcEOE7TvLMo8TsuZSYNUfdWMTmE28tpHhzAcWZ8ikuY4r6ZAZjDunTskTAsFPEagA8xwfAQXAI8HwzR8BRcAwc1zgBeOM5BVpAMvhXion5CQJfvsgrfdM6AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, sectionName, base, height, thickness, uniaxialMaterial):
        
        
        import math
        import Grasshopper as gh
        
        def RectangularHollowCrossSection(sectionName, base, height, thickness, uniaxialMaterial):
            
            sectionName = sectionName
            shape = "rectangularHollow"
            base = base / 1000                      # Input value in mm ---> Output m
            height = height / 1000                  # Input value in mm ---> Output m
            thickness = thickness/1000              # Input value in mm ---> Output m
            Area = base * height - ( base - 2*thickness )*( height - 2*thickness )
            ky = Area/( base*thickness*2 )
            kz = Area/( height*thickness*2 )
            Ay = Area * ky
            Az = Area * kz
            Iyy = base*(height)**3/12 - ( base - 2*thickness )*( height - 2*thickness )**3/12
            Izz = base**3*height/12 - ( base - 2*thickness )**3*( height - 2*thickness )/12
            #J = Iyy + Izz
            J = ( 4*(( base - thickness)*( height - thickness))**2*thickness )/( 2*( height - thickness) + 2*( base - thickness) )
        
            material = uniaxialMaterial
        
            return [[Area, Ay, Az, Iyy, Izz, J, material, [shape, base, height, thickness ], sectionName ]]
        
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
        
        if thickness is None:
            checkData = False
            msg = "input 'thickness' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if uniaxialMaterial is None:
            checkData = False
            msg = "input 'uniaxialMaterial' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            CrossSection = RectangularHollowCrossSection(sectionName, base, height, thickness, uniaxialMaterial)
            return CrossSection

class ShellSection(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Shell Section (Alpaca4d)", "Shell Section", """Generate a Plate cross section""", "Alpaca", "1|Cross Section")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.secondary
    
    def get_ComponentGuid(self):
        return System.Guid("e5559d4b-a93b-461e-a7e4-ff3b48398fbf")
    
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
        self.SetUpParam(p, "thickness", "thickness", "Height of the cross section [mm].")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "nDMaterial", "nDMaterial", "Material element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "CrossSection", "CrossSection", "Elastic Plate Section element.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAOwSURBVEhLtZVpbExhFIaL6tBRqqqm0+m0nW66jbZpqqvaq7ZWrQ2x70tFLLV3LKWK1h5CxB9LSBP7ThAS4g/xRyIqRERoBE0R2+s93/TetkMswZs8mTv3zveeb853zrluP1ELEue8/D8qICAvyA6SRv6pTgd6GzA6uQMM7k0lkPCUVJB48leykXcr+gbj65YsfNzUBfvHRCHB0gqeHnqwB6SUdCR/LIeXoRker0hRAYTKCTE4PD4anzdn4fjkWExI9W8Y7B5ZTWRjv5SRPArzbYkqR2f9H0zPNOPdxkw94N6Rkbg0qxPOTbdjbncLvFu6a8FuEwcJID9UPsEx7rI8PxTjU0xYl2vDvlEddfO36zNQmBWATwys3ds2NBy7RkRgYS8r/Lyaa8FyxdBVp+xmIz5UOBdLSnKifTA5zR+bB4cp053DI3B1drxu/nJtGhb0DNS/H50UK+a1xK4cGyiE1Fbkh+k/vkYj2Zlc35ybiEkMlGT1QjVNtd9U8J/eXZikrt+XZyIluLUE2KMcXVRMcGJKrL54FlPxhinRvm8dEobKiTFwsMJmdgnAhRl2LO8TpD8/NC5azGtIlBg2lBxulSzaXRCBsZ1N2JAXqnKrLZZUFDVIhRx+nt0XQxPa4+DYKNSyCKSU6bNNObpokHvTJrjFNGgGsnBqhhnlg0JV7jfxDO7UpUJ4uioFq/qFqOsz0+KQFqJS84aEKkcXnUi3tcEXHqoskJyKoVzfnp/Iujchg89fl6XrAUr6h+DJSmev1DCN0SZPCVDutGusYFLbLdxbpUcWLOptxat19Wbrma6zrPml2UEq9xdndkJZnk1/vn1YuJi/qvP6TsX+rT3U7q4UxqMgyQ+9ItuqepfFz1anwpHjHBuCHHqfKB8MT2yP63MSuC4D0pj0KXPaNZYnqVrEBtEMpEJucOGSbKvarXw+LHZ2tXCnqD59ewoitYOtJhYxdFUO0TtVxoN0rmZ2f2kysrlb6ejzLEm5N7urRU9fdWk6gnxaSIAS5fYDmcklohpkRKIfqyNVD7BmQP1BHuBEzY1zlqV0uNwrHWgTc3lnmMhPlUyOEMT4G7GT3VvFtIiBFkxKVVJ2mUNuTjcLFrMQzG0MEkCG229LOlDeYDB6NFMzRhtqJ6fGNRp683oEivlz4kv+WFYiL5RP7YzNsYzjYBqbTrpVzJ+XpMKvlZqaS+THfyNvIiY18uqUA5aRIQF571nd838iAykkcqBo66leMEXkv2giqSS/2L2b2zecO3vPlGc8WQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, sectionName, thickness, nDMaterial):
        import math
        import Grasshopper as gh
        
        def ElasticMembranePlateSection(sectionName, thickness, nDMaterial):
            
            sectionName = sectionName
            thickness = thickness / 1000        # Input value in mm ---> Output m
            material = nDMaterial
            sectionType = "ElasticMembranePlateSection"
            sectionProperties = sectionName + "_" + sectionType
            return [[sectionProperties, thickness, material]]
        
        checkData = True
        
        if sectionName is None:
            checkData = False
            msg = "input 'sectionName' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if thickness is None:
            checkData = False
            msg = "input 'thickness' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if nDMaterial is None:
            checkData = False
            msg = "input 'nDMaterial' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            CrossSection = ElasticMembranePlateSection(sectionName, thickness, nDMaterial)
            return CrossSection


# 2|Element

class LinetoBeam(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Line to Beam (Alpaca4d)", "Line to Beam", """Generate a Timoshenko Beam element or a Truss element""", "Alpaca", "2|Element")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("3d4af836-2ddf-47fa-bf6c-0991645a2dcd")
    
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
        
        p = GhPython.Assemblies.MarshalParam()
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
        
        p = GhPython.Assemblies.MarshalParam()
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
        
        def LineToBeam(Line, CrossSection, Colour, orientSection, beamType):
        
            if orientSection is None:
                orientSection = 0
        
            if beamType is None:
                beamType = 1
        
        
        
            Line = Line
            if beamType == 1 or None:
                elementType = "ElasticTimoshenkoBeam"
                if Colour is None:
                    colour = Color.FromArgb(195, 195, 13)
                else:
                    colour = Colour
            elif beamType == 0:
                elementType = "Truss"
                if Colour is None:
                    colour = Color.FromArgb(179, 62, 143)
                else:
                    colour = Colour
        
            CrossSection = CrossSection
            
        
            midPoint =  Line.PointAtNormalizedLength(0.5)
            parameter = Line.ClosestPoint(midPoint, 0.01)[1]
            perpFrame = ghcomp.PerpFrame( Line, parameter )
            perpFrame.Rotate(Rhino.RhinoMath.ToRadians(orientSection), perpFrame.ZAxis, perpFrame.Origin)
            vecGeomTransf = [ perpFrame.XAxis, perpFrame.YAxis, perpFrame.ZAxis ]
        
            Area = float(CrossSection[0])
            rho = float(CrossSection[6][4])
            massDens = Area * rho
        
        
            return [[Line, elementType, CrossSection, vecGeomTransf, colour, massDens, perpFrame]]
        
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
            beamWrapper = LineToBeam(Line, CrossSection, Colour, orientSection, beamType)
            return beamWrapper

class MeshtoShell(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Mesh to Shell (Alpaca4d)", "Mesh to Shell", """Generate a Shell MITC4 element""", "Alpaca", "2|Element")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("aa075ef3-3eb2-48a3-884f-4a9e585f14d8")
    
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
        
        p = GhPython.Assemblies.MarshalParam()
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
        from System.Drawing import Color 
        
        def MeshToShell(Mesh, Colour, CrossSection):
            
            Mesh.Unweld(0, True)
            
            elementType = []
            if Mesh.Vertices.Count == 4:
                elementType = "ShellMITC4"
                if Colour is None:
                    colour = Color.FromArgb(49, 159, 255)
                else:
                    colour = Colour
            else:
                elementType = "shellDKGT"
                if Colour is None:
                    colour = Color.FromArgb(49, 159, 255)
                else:
                    colour = Colour
            newMesh = Mesh
            
            CrossSection = CrossSection
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

class BrickElement(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Brick Element (Alpaca4d)", "Brick Element", """Generate a Brick Element""", "Alpaca", "2|Element")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.primary
    
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
            solidWrapper = Solid( Brick, Colour, nDMaterial )
            return solidWrapper

class Support(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Support (Alpaca4d)", "Support", """Generate support for the structure.""", "Alpaca", "2|Element")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.secondary

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
        self.SetUpParam(p, "Tx", "Tx", "Translation in X. TRUE = Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Ty", "Ty", "Translation in Y. TRUE = Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Tz", "Tz", "Translation in Z. TRUE = Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Rx", "Rx", "Rotation about the X axis. TRUE = Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Ry", "Ry", "Rotation about the Y axis. TRUE = Fixed.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "Rz", "Rz", "Rotation about the Z axis. TRUE = Fixed.")
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


# 3|Define Loads

class PointLoad(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Point Load (Alpaca4d)", "Point Load", """Generate a point load.""", "Alpaca", "3|Load")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5fcdb364-cff0-4315-85e0-f984d8d9a38b")
    
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
            Force = rg.Vector3d(0,0,0) if Force is None else Force                   # Input value in kN ---> Output kN
            Moment = rg.Vector3d(0,0,0) if Moment is None else Moment                 # Input value in kNm ---> Output kNm
            loadType = "pointLoad"
        
            return [[Pos, Force, Moment, loadType]]
        
        checkData = True
        
        
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
            "Linear Load (Alpaca4d)", "Linear Load", """Generate a uniform Distributed Load""", "Alpaca", "3|Load")
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
            "Mass Point (Alpaca4d)", "Mass Point", """Add a concentrated Mass to a node.""", "Alpaca", "3|Load")
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


# 4|Assemble

class Assemble(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Assemble (Alpaca4d)", "Assemble", """Generate a text file model to be sent to OpenSees""", "Alpaca", "4|Model")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("f2c70622-da97-4a8f-a35a-50191848ea9d")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Element", "Element", "Structural element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Support", "Support", "Support element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Load", "Load", "Load element.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Mass", "Mass", "Mass point.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "AlpacaModel", "AlpacaModel", "Assembled Alpaca model.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "MassOfStructure", "MassOfStructure", "Total mass of the structure [kg].")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAMBSURBVEhLtdRJSFRxHAfw9xxncXR01Fym3G0sRwW1LM1QmNBDJHixQ4sL0kEkzUo0izJEwkEQzYooyDAoD4rhoUuZLSZBiIe6FR0ipEIqwspcfn2/zhgenBm1+sKH997/Lf/1/ZW/jB9scp7+n7SDQB/sYcG/TCR8hAVgJRPwT3MBvkER3AFWkgleYzepmts4hjgv3eYxPHSeKsHACi4tXnlKgKr2jvtZJUrVjrmK3OUJPAAfOA+/XEevSarUhki/IY5je9xZtGLYg2HYCbNwF8zgPVpFdUwYk+S0LnwuUvVlK3XOO3/CIfkEXVALHJ7VL1f0+Wi/IVam/FOkXhu2EKHo4123mG1wC35CHpQBK0iB1cWsahzX9FHyzj9ZsjTGHyjqgXvwAuZgGhqAKQBWsAs4H3ZLsCEGR8/BmNQFqj7zOOXLn4HrnON+BWywlELgMzmwuSwrYq44NWRaryiJvOkuHAauEra2BILAXTgHbEgC+MSZdWOTrTkSGejLSXcbtnQKHMBue8oAvAHt4hXm5WJJwmxtfhQrXXFVaeALvAduZp4SC/ybR816TYdWo3bjfEtbUdxMvT163mhULHxopXACOa7Lf5xsKIblPeoEOWHHgmjJlsJk83dLoK53tC5DcuNN47jHxroNfyIOE5MGbCkr5c7JcKK/wsvBI6my0JUvfRU2GalNl+rdFi4KOx/ylGrgB8OhGWaAexTLuKkNwQcoOLg9XPKtQa9y44OeWcMMLM8Ar2kF7i8cLh6vgwm4LbAX/NHOAsMlGuo8XX3OAT88CfchAFR4Cxwa9iQf1p19wI9QBQtcqYKl8nVXEJDov/F5Z+ZJOZNSKVsD4thqDo+PLiTmsrVhWKyNI6KPtHGl+PKFNcXoazjVklYlQ3kdi25mN4uqqNwiSqNLr85n3BAhW9trUTUazs3aEqw3DTQml0t7+jFxpNdIk61CQnWBParWryXqcLckNT1FDx5JQs2gGCzJXM5rDv/g/VAO3I53gD8we+EQHABu1xvATRTlN6ec2AXsJTwAAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, Element, Support, Load, Mass):
        
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
                               
                               
            ghFilePath = self.Attributes.Owner.OnPingDocument().FilePath
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
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if not Support:
            checkData = False
            msg = "input 'Support' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if not Load:
            msg = "input 'Load' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            AlpacaModel, MassOfStructure = Assemble(Element, Support, Load, Mass)
            return (AlpacaModel, MassOfStructure)

class DisassembleModel(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Disassemble Model (Alpaca4d)", "Disassemble Model", """Deconstruct a structural model and show all the elements""", "Alpaca", "4|Model")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("1872eaa1-f567-4db4-947f-3fbaaa01d62c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaModel", "AlpacaModel", "Output of Assemble Model.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "ModelView", "ModelView", "analitic element ( beam, shell, brick ... ).")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "ModelViewExtruded", "ModelViewExtruded", "extruded model .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Points", "Points", "points of model .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Support", "Support", "info support .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Load", "Load", "info Load .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Material", "Material", "info Material.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Section", "Section", "info Section.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
                self.marshal.SetOutput(result[3], DA, 3, True)
                self.marshal.SetOutput(result[4], DA, 4, True)
                self.marshal.SetOutput(result[5], DA, 5, True)
                self.marshal.SetOutput(result[6], DA, 6, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAVbSURBVEhLrVVpcFNVGL1toWhbLEtBsyfNnrwXkrwkTUNIKaWJgFCFaZGOMmVYXNgZisoPijPSlpRKqwWnEEZBlAHECkUZGAR0ZGSRRVQGFAFBRgHFnyJIj99NXwlaZcTxzNx5y73vfPee73zfY3diGVPkxZnSLT8yt9tt9omiVX78f1DPVKfrmHI6v/eKYqVHFNuSEzJqGOsh3/431DFVYilToZ4p35k4wGSkAD87HI4cPtfKpJ61TLG9jqnF5OK/oIYpsmiDcxqYWpBfdUcdU5S90UuD9hwdKNC5YrPtgsflGsfn6OOWlgw1D/4RGEtLfkDoIqbgl+j61Z1z3VDP8nPjaYrrP6hMONLfgJl5RhTYhfZ6ppjR2lONS0oj1mRqQCed2EVMm7q04X4tVvXU4NkHDGvdTmcryTtNpkzB47Hr/H5bf/pgz7E8A35Sm3CSRsghoLGHGmcfMibfnRqYT6dQXV3KFBc58X56v8JkQ4nFgWBRDMWVs+ERhKMybSckScqiyEdI851L0lXPb83W4SqRnX4wH5PsTmzSWnBWY04G4GN3Xz1Wq814yuZAga8AxRNmYVT1ayiduhgF4eGgExwPOhz9ZHravSiur5phQ/mTdsQMth0raMecqPUBPWapLRjncGK9wYqduXosttgxVHQhPGoCRsxtxog5TQiPHA+vIFwh4ldoSDJtJySXMC8UFPBSwoSalSYEvCLm9svH96T3TspD1GjnO0Jtbz3ilOSoyY7hkxai+PGZCEoBjKf5yX3yDxXpdPfJlCl4vTaFJAjbfHbHzTK9FeNIjtFOAdVWB77TmHCG9H0514AXKoqwUfLg6+rRmDbQhKjLhXlKM05rzdhPcjWmq3+nvGwjM5R2cxFV6xjS/+aiXuprVTorKkgOLs+XlMzNWVosI9dca54AbJycHNfXVmGz1433yMqXyW187Y903d/XkHRSLVOd5MXKHSmHYIy7h9pEYTxd+esJ2S2H+hmwrIcGVxoqbpN3jW/oJGu0NjSnq/FuXqcRyshtCVKB10otUx4ml3ll+hTI37NXUoL5zriLXqei2xUr7Bbg6JQomjO12NdHj2dIzgX+aiRCCYTFAOZnaRdsYixDpkyBNzteiXvJKfwE20mCphw9jk+L4uLisbfJb6yrwudPx7CWgvN1fPfxgji2htsxdNBgeJ1Oo0yZQg0bkEOl/umO3rrkR4fJPZzgbSokXsF7RodxbGoUl+MV2CCIWE7StNBJLyiM2Ku3oFhwIeTy36ICa5IpU6hhjkzS7IO2bG1SFh7gIjmo0WynI7tRqbWimZzDpWshRzVl63GeiPm6rrGbpFqUqXlTpkyB2m86kb/VmKbC+7T7NqrgBpUZMUFCMPQcIqUfIiCNRcTqxC6dBQco8U20e07K+9I5MgRvISco0dRifuH9SabuBCV1GFlqFQWpm56r3z7MZL/ll8rg85RiSMkWFA5+EX7pUYSL1yFA+rZRNXP78gDcwmTJyyTtGbqeoi77BbXyiEz9Z5B2q32eaMfgoQkUPfwZwsM2Q3L5IA0KIxL9GJGSdgSdEg7IFuYjkfS82i9T3B2U+d0Bf2VHJLqXCPd1BHyVCBbOo7GATvAYAv4nMFZl2bA8Q3njWwrCc9WQpuqoY9q+MsXdUV5enkH9ZiHt+DefdyQKw0uSJ+EjNCTOe9EhvoZkmPRqhvrWiQEG/k84L3/+70FS+TxO56lg4XwiP4hI7BN4B5Xc5O/lJfRTUsxoTOPVqtolv7o3uFyu7Fi+7aDfOwaBwBT+81ghT90G7X4hFWWL/HjvIClClJdHSJotoij+rc6NTK2Sb/8BjP0B/RGKSGWJ3ywAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaModel):
        
        import Rhino.Geometry as rg
        import math as mt
        import ghpythonlib.treehelpers as th # per data tree
        import Grasshopper as gh
        import rhinoscriptsyntax as rs
        import sys
        
        
        #---------------------------------------------------------------------------------------#
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
            t = linspace( 0 , 1.80*mt.pi, 20 )
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
        
        def ShellQuad( ele, node):
            eleTag = ele[1]
            eleNodeTag = ele[2]
            color = ele[5]
            thick = ele[4]
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            index4 = eleNodeTag[3]
            
            ## CREO IL MODELLO  ##
            point1 = node.get( index1 -1 , "never")
            point2 = node.get( index2 -1 , "never")
            point3 = node.get( index3 -1 , "never")
            point4 =  node.get( index4 -1 , "never")
            
            shellModel = rg.Mesh()
            shellModel.Vertices.Add( point1 ) #0
            shellModel.Vertices.Add( point2 ) #1
            shellModel.Vertices.Add( point3 ) #2
            shellModel.Vertices.Add( point4 ) #3
            
            
            shellModel.Faces.AddFace(0, 1, 2, 3)
            colour = rs.CreateColor( color[0], color[1], color[2] )
            shellModel.VertexColors.CreateMonotoneMesh( colour )
        
            vt = shellModel.Vertices
            shellModel.FaceNormals.ComputeFaceNormals()
            fid,MPt = shellModel.ClosestPoint(vt[0],0.01)
            normalFace = shellModel.FaceNormals[fid]
            vectormoltiplicate = rg.Vector3d.Multiply( -normalFace, thick/2 )
            trasl = rg.Transform.Translation( vectormoltiplicate )
            moveShell = rg.Mesh.DuplicateMesh(shellModel)
            moveShell.Transform( trasl )
            extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
            
            return  [ shellModel, extrudeShell ] 
        
        def ShellTriangle( ele, node ):
            
            eleTag = ele[1]
            eleNodeTag = ele[2]
            color = ele[5]
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            
            
            ## CREO IL MODELLO DEFORMATO  ##
            point1 =  node.get( index1 -1 , "never")
            point2 =  node.get( index2 -1 , "never")
            point3 =  node.get( index3 -1 , "never")
            
            shellModel = rg.Mesh()
            shellModel.Vertices.Add( point1 ) #0
            shellModel.Vertices.Add( point2 ) #1
            shellModel.Vertices.Add( point3 ) #2
            
            shellModel.Faces.AddFace(0, 1, 2)
            colour = rs.CreateColor( color[0], color[1], color[2] )
            shellModel.VertexColors.CreateMonotoneMesh( colour )
            
            vt = shellModel.Vertices
            shellModel.FaceNormals.ComputeFaceNormals()
            fid,MPt = shellModel.ClosestPoint(vt[0],0.01)
            normalFace = shellModel.FaceNormals[fid]
            vectormoltiplicate = rg.Vector3d.Multiply( -normalFace, thick/2 ) 
            trasl = rg.Transform.Translation( vectormoltiplicate )
            moveShell = rg.Mesh.DuplicateMesh(shellModel)
            moveShell.Transform( trasl )
            extrudeShell = rg.Mesh.Offset( moveShell, thick, True, normalFace)
            
            return  [ shellModel, extrudeShell ]
            
        def Solid( ele, node ):
            
            eleTag = ele[1]
            eleNodeTag = ele[2]
            color = ele[5]
            #print( eleNodeTag )
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            index4 = eleNodeTag[3]
            index5 = eleNodeTag[4]
            index6 = eleNodeTag[5]
            index7 = eleNodeTag[6]
            index8 = eleNodeTag[7]
            
            ## CREO IL MODELLO DEFORMATO  ##
            point1 =  node.get( index1 -1 , "never")
            point2 =  node.get( index2 -1 , "never")
            point3 =  node.get( index3 -1 , "never")
            point4 =  node.get( index4 -1 , "never")
            point5 =  node.get( index5 -1 , "never")
            point6 =  node.get( index6 -1 , "never")
            point7 =  node.get( index7 -1 , "never")
            point8 =  node.get( index8 -1 , "never")
            #print( type(pointDef1) ) 
            shellDefModel = rg.Mesh()
            shellDefModel.Vertices.Add( point1 ) #0
            shellDefModel.Vertices.Add( point2 ) #1
            shellDefModel.Vertices.Add( point3 ) #2
            shellDefModel.Vertices.Add( point4 ) #3
            shellDefModel.Vertices.Add( point5 ) #4
            shellDefModel.Vertices.Add( point6 ) #5
            shellDefModel.Vertices.Add( point7 ) #6
            shellDefModel.Vertices.Add( point8 ) #7
        
            shellDefModel.Faces.AddFace(0, 1, 2, 3)
            shellDefModel.Faces.AddFace(4, 5, 6, 7)
            shellDefModel.Faces.AddFace(0, 1, 5, 4)
            shellDefModel.Faces.AddFace(1, 2, 6, 5)
            shellDefModel.Faces.AddFace(2, 3, 7, 6)
            shellDefModel.Faces.AddFace(3, 0, 4, 7)
            
            colour = rs.CreateColor( color[0], color[1], color[2] )
            shellDefModel.VertexColors.CreateMonotoneMesh( colour )
            return  shellDefModel
        
        def TetraSolid( ele, node ):
            
            eleTag = ele[1]
            eleNodeTag = ele[2]
            color = ele[5]
            #print( eleNodeTag )
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            index4 = eleNodeTag[3]
            
            ## CREO IL MODELLO DEFORMATO  ##
            point1 =  node.get( index1 -1 , "never")
            point2 =  node.get( index2 -1 , "never")
            point3 =  node.get( index3 -1 , "never")
            point4 =  node.get( index4 -1 , "never")
            
            #print( type(pointDef1) )
            
            shellDefModel = rg.Mesh()
            shellDefModel.Vertices.Add( point1 ) #0
            shellDefModel.Vertices.Add( point2 ) #1
            shellDefModel.Vertices.Add( point3 ) #2
            shellDefModel.Vertices.Add( point4 ) #3
            
            
            shellDefModel.Faces.AddFace( 0, 1, 2 )
            shellDefModel.Faces.AddFace( 0, 1, 3 )
            shellDefModel.Faces.AddFace( 1, 2, 3 )
            shellDefModel.Faces.AddFace( 0, 2, 3 )
            colour = rs.CreateColor( color[0], color[1], color[2], 0 )
            shellDefModel.VertexColors.CreateMonotoneMesh( colour )
            
            return  shellDefModel
        ## node e nodeDisp son dictionary ##
        def Beam( ele, node):
            TagEle = ele[1]
            indexStart = ele[2][0]
            indexEnd = ele[2][1]
            color = ele[16]
            dimSection = ele[14]
            pointStart = node.get( indexStart  , "never")
            pointEnd = node.get( indexEnd  , "never")
            line = rg.LineCurve( pointStart, pointEnd )
            axis1 =  rg.Vector3d( ele[13][0][0], ele[13][0][1], ele[13][0][2]  )
            axis2 =  rg.Vector3d( ele[13][1][0], ele[13][1][1], ele[13][1][2]  )
            axis3 =  rg.Vector3d( ele[13][2][0], ele[13][2][1], ele[13][2][2]  )
            versor = [ axis1, axis2, axis3 ] 
            
            planeStart = rg.Plane(pointStart, axis1, axis2)
            planeEnd = rg.Plane(pointEnd, axis1, axis2)
            plane = [ planeStart, planeEnd ]
            
            sectionForm = []
            sectionPolyline = []
            for sectionPlane in plane:
                
                if dimSection[0] == 'rectangular' :
                    width, height = dimSection[1], dimSection[2]
                    section = AddRectangleFromCenter( sectionPlane, width, height )
                    sectionForm.append( section )
                elif dimSection[0] == 'circular' :
                    radius1  = dimSection[1]/2
                    radius2  = dimSection[1]/2 - dimSection[2]
                    section1 = AddCircleFromCenter( sectionPlane, radius1 )
                    section2 = AddCircleFromCenter( sectionPlane, radius2 )
                    sectionForm.append( [ section1, section2 ] )
                elif dimSection[0] == 'doubleT' :
                    Bsup = dimSection[1]
                    tsup = dimSection[2]
                    Binf = dimSection[3]
                    tinf = dimSection[4]
                    H =  dimSection[5]
                    ta =  dimSection[6]
                    yg =  dimSection[7]
                    section = AddIFromCenter( sectionPlane, Bsup, tsup, Binf, tinf, H, ta, yg )
                    sectionForm.append( section )
                elif dimSection[0] == 'rectangularHollow' :
                    width, height, thickness = dimSection[1], dimSection[2], dimSection[3]
                    section1 = AddRectangleFromCenter( sectionPlane, width, height )
                    section2 = AddRectangleFromCenter( sectionPlane, width - (2*thickness), height - (2*thickness) )
                    sectionForm.append( [ section1, section2 ] )
                elif dimSection[0] == 'Generic' :
                    radius  = dimSection[1]
                    section = AddCircleFromCenter( sectionPlane, radius )
                    sectionForm.append( section )
                #print(sectionForm)
        
            colour = rs.CreateColor( color[0], color[1], color[2] )
        
            if dimSection[0] == 'circular' :
                sectionForm1 = [row[0] for row in sectionForm ]
                sectionForm2 = [row[1] for row in sectionForm ]
                meshExtr = meshLoft3( sectionForm1,  color )
                meshExtr.Append( meshLoft3( sectionForm2,  color ) )
                sectionStartEnd = [ [sectionForm1[0], sectionForm2[0]], [sectionForm1[-1], sectionForm2[-1]]  ]
                for iSection in sectionStartEnd :
                    iMesh = rg.Mesh()
                    for iPoint, jPoint in zip(iSection[0],iSection[1])  :
                        iMesh.Vertices.Add( iPoint )
                        iMesh.Vertices.Add( jPoint )
                    for i in range(0,len(iSection[0]) - 1): # sistemare
                        index1 = i*2 # 0
                        index2 = index1 + 1 #1
                        index3 = index1 + 3 #2
                        index4 = index1 + 2 #3
                        iMesh.Faces.AddFace(index1, index2, index3, index4)
                    iMesh.Faces.AddFace(index4, index3, 1, 0)
                    iMesh.VertexColors.CreateMonotoneMesh( colour )
                    meshExtr.Append( iMesh )
                    #meshExtr.IsClosed()
            elif  dimSection[0] == 'rectangular' : 
                meshExtr = meshLoft3( sectionForm,  color )
                sectionStartEnd = [ sectionForm[0], sectionForm[-1] ]
                for iSection in sectionStartEnd :
                    iMesh = rg.Mesh()
                    for iPoint in iSection :
                         iMesh.Vertices.Add( iPoint )
                    iMesh.Faces.AddFace(0, 1, 2, 3)
                    iMesh.VertexColors.CreateMonotoneMesh( colour )
                    meshExtr.Append( iMesh )
            elif  dimSection[0] == 'doubleT' : 
                meshExtr = meshLoft3( sectionForm,  color )
                sectionStartEnd = [ sectionForm[0], sectionForm[-1] ]
                for iSection in sectionStartEnd :
                    iMesh = rg.Mesh()
                    for iPoint in iSection :
                         iMesh.Vertices.Add( iPoint )
                    iMesh.Faces.AddFace( 0, 1, 2 )
                    iMesh.Faces.AddFace(2, 3, 5, 0 )
                    iMesh.Faces.AddFace( 3, 4, 5 )
                    iMesh.Faces.AddFace( 5, 6, 11, 0 )
                    iMesh.Faces.AddFace( 6, 7, 8 )
                    iMesh.Faces.AddFace( 8, 9, 11, 6 )
                    iMesh.Faces.AddFace( 9, 10, 11 )
                    #iMesh.Faces.AddFace(3, 2, 1, 4)
                    #iMesh.Faces.AddFace( 5, 6, 11, 0 )
                    #iMesh.Faces.AddFace(7, 8, 9, 10)
                    iMesh.VertexColors.CreateMonotoneMesh( colour )
                    meshExtr.Append( iMesh ) 
            elif  dimSection[0] == 'rectangularHollow' : 
                sectionForm1 = [row[0] for row in sectionForm ]
                sectionForm2 = [row[1] for row in sectionForm ]
                meshExtr = meshLoft3( sectionForm1,  color )
                meshExtr.Append( meshLoft3( sectionForm2,  color ) )
                sectionStartEnd = [ [sectionForm1[0], sectionForm2[0]], [sectionForm1[-1], sectionForm2[-1]]  ]
                for iSection in sectionStartEnd :
                    iMesh = rg.Mesh()
                    for iPoint, jPoint in zip(iSection[0],iSection[1])  :
                        iMesh.Vertices.Add( iPoint )
                        iMesh.Vertices.Add( jPoint )
                    iMesh.Faces.AddFace(0, 1, 3, 2)
                    iMesh.Faces.AddFace(2, 3, 5, 4)
                    iMesh.Faces.AddFace(4, 5, 7, 6)
                    iMesh.Faces.AddFace(6, 7, 1, 0)
                    iMesh.VertexColors.CreateMonotoneMesh( colour )
                    meshExtr.Append( iMesh )
                    #meshExtr.IsClosed()
        
            elif dimSection[0] == 'Generic' :
                meshExtr = meshLoft3( sectionForm,  color )
        
            return [ line, meshExtr, colour ]
        
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


        def disassembleModel(AlpacaModel ):
        
            nodeWrapper = AlpacaModel[0]
            GeomTransf = AlpacaModel[1]
            openSeesBeam = AlpacaModel[2]
            openSeesSupport = AlpacaModel[3]
            openSeesNodeLoad = AlpacaModel[4]
            openSeesMatTag = AlpacaModel[7]
            openSeesShell = AlpacaModel[8]
            openSeesSecTag = AlpacaModel[9]
            openSeesSolid = AlpacaModel[10]
        
            pointWrapper = []
            for item in nodeWrapper:
                point = rg.Point3d(item[1],item[2],item[3])
                pointWrapper.append( [item[0], point ] )
            ## Dict. for point ##
            pointWrapperDict = dict( pointWrapper )
            ####
            Points = [row[1] for row in pointWrapper ]
        
            model = []
            extrudedModel = []
        
            for ele in openSeesBeam :
                eleTag = ele[1]
                beamModel = Beam( ele, pointWrapperDict )
                model.append([ eleTag, beamModel[0] ])
                extrudedModel.append([ eleTag, beamModel[1] ])
        
            for ele in openSeesShell :
                nNode = len( ele[2] )
                eleTag =  ele[1] 
                if nNode == 4 :
                    shellModel = ShellQuad( ele, pointWrapperDict )
                    model.append([ eleTag,shellModel[0] ])
                    extrudedModel.append([ eleTag,shellModel[1] ])
                elif nNode == 3:
                    shellModel = ShellTriangle( ele, pointWrapperDict )
                    model.append([ eleTag,shellModel[0] ])
                    extrudedModel.append([ eleTag,shellModel[1] ])
        
            for ele in openSeesSolid :
                nNode = len( ele[2] )
                eleTag =  ele[1]
                eleType = ele[0] 
                if nNode == 8:
                    solidModel = Solid( ele, pointWrapperDict )
                    model.append([ eleTag, solidModel ])
                    extrudedModel.append([ eleTag, solidModel ])
                elif  eleType == 'FourNodeTetrahedron' :
                    #print(ele)
                    solidModel = TetraSolid( ele, pointWrapperDict )
                    model.append([ eleTag, solidModel ])
                    extrudedModel.append([ eleTag, solidModel ])
        
            modelDict = dict( model )
            modelExstrudedDict = dict( extrudedModel )
            ModelView = []
            ModelViewExtruded = []
            for i in range(0,len(modelDict)):
                ModelView.append( modelDict.get( i  , "never" ))
                ModelViewExtruded.append( modelExstrudedDict.get( i , "never" ))
        
            #--------------------------------------------------------------#
        
        
        
            forceDisplay = []
            for item in openSeesNodeLoad:
                loadWrapper = "{3}; Pos=[{4}]; F={1}; M={2}".format(item[0],item[1][:3],item[1][3:], item[2], pointWrapperDict.get(item[0]))
                forceDisplay.append(loadWrapper)
            Load = forceDisplay
        
        
        
            Support = []
        
            for support in openSeesSupport :
                index = support[0]
                pos = pointWrapperDict.get(index)
                supportType = support[1:]
                supportTypeTemp = []
                for number in supportType:
                    if number == 1:
                        dof = True
                    else:
                        dof = False
                    supportTypeTemp.append(dof)
                supportWrapper = "Support; Pos=[{0}]; DOF={1}".format(pos,supportTypeTemp)
                Support.append( supportWrapper )
        
        
            Material = []
        
            for item in openSeesMatTag:
                Grade= item[0].split("_")[0]
                dimensionType = item[0].split("_")[1]
                typeMat = item[0].split("_")[2]
                E = item[1][1][0]
                G = item[1][1][1]
                v = item[1][1][2]
                gamma = item[1][1][3]
                fy = item[1][1][4]
                Material.append( "grade={}; type={}; E={}; G={}; v={}; gamma={}; fy={}".format(Grade,typeMat,E,G,v,gamma,fy))
        
        
            Section = []
        
            for item in openSeesSecTag:
                name = item[0].split("_")[0]
                typeSec = item[0].split("_")[1]
                Section.append("name={}; type={}".format(name, typeSec))
        
            return ModelView, ModelViewExtruded, Points, Support, Load, Material, Section
        
        checkData = True
        
        if not AlpacaModel:
            checkData = False
            msg = "input 'AlpacaModel' failed to collect data"  
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            ModelView, ModelViewExtruded, Points, Support, Load, Material, Section = disassembleModel( AlpacaModel )
            return (ModelView, ModelViewExtruded, Points, Support, Load, Material, Section)


# 5|Analysis

class StaticAnalyses(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Static Analyses (Alpaca4d)", "Static Analyses", """Calculate the Static Response of the structure""", "Alpaca", "5|Analyses")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.primary
    
    def get_ComponentGuid(self):
        return System.Guid("2e2ee996-5a1f-48e3-93bd-df211c55dce5")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "AlpacaModel", "AlpacaModel", "Assemble model to perform Static Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "AlpacaStaticOutput", "AlpacaStaticOutput", "Analysed Alpaca model.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAKbSURBVEhL7dRfSFNRHAfwe+82d73TnG5LbdqmbolrlcKUiJAgn7IosKCHon9UD2JRgUo9WYH9AcNWyvqDDz1IQYZYkmEtNKGggh586kVKESGhsjRN9+v7u3fGgrtwUVDQFz5w/uycc8/dPUf4G7MM2iBdrf2BnISDMAAF3PA744WjWlHIhyat+ENSwK0VE89eWKEV1bSAUSuq4b6HQODjhkSzB+YH8utpBbNaE4QKq2h4d8zkII9kjqA+DrybhDK/AxNcASdwrEmCONQuu76OW5ZTh+zmHbyG2N3FDT9FOSyF09G6PVqeT+0W4yLiyVmXtsBzrUs/EhyAm/DK7zeQoog8aBiqgXdwHjgbHaLx/UCyJzKkFFHInENbjWn825DWrZ9dTqc0W18vzzU3KxQOp1JfXyo1NiZTIGDgwVMwBi+9knn6rpxHPHmZpHBfGBrBAbqpglt2u0j9/am6urtTKHhRmXqUnK9OzK8laHby5PchiSfRiwHWQAMUZmdLupPHGg541MlHLT4q1Z6+EuJmHxwBG1RkFJbQic5T1PM4V3dyNlibPcMLXNKe/hnIEDd8aMqA75inuTsvU0kbkb/pLVVu9840tJROPAjnzMUu8OReWqTX7vqCP/kDxqyDn0aB23DIWrqN/BdGyF1zZ0LO8c2ircugWKn4+izVdFyjGz3lEV4gGFTIZhM/oZ8P4IKyGcYy1u6mpHTXZ5TfwAuwiZJxclVoUt3VytaP5K/aQRaLOIq+TbDgWKEbRuAwHIcs6DRZs6aLr06Tty5MslPdVS8kfKkVwX7IBL5nFgOn3bG+mjI31JJokAdR56+Fv7qEw1dAPdRBHjdEc9ZSsJpEo4lP8hKt6ddzBs5pxe/hV8dHnz/j//mnIgjfAFbfBYlCcDTMAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaModel):
        
        
        import System
        import os
        import Grasshopper as gh
        
        def InitializeStaticAnalysis(AlpacaModel):
            
            ghFilePath = self.Attributes.Owner.OnPingDocument().FilePath
            workingDirectory = os.path.dirname(ghFilePath) 
            outputFileName = 'openSeesOutputWrapper.txt'
        
            for dirpath, dirnames, filenames in os.walk(workingDirectory):
                for filename in filenames:
                    if filename == outputFileName:
                        file = os.path.join(dirpath,outputFileName)
                        os.remove(file)
        
        
        
            ghFolderPath = os.path.dirname(ghFilePath)
            outputFolder = os.path.join(ghFolderPath,'assembleData')
            wrapperFile = os.path.join( outputFolder,'openSeesModel.txt' )
        
            userObjectFolder = gh.Folders.DefaultUserObjectFolder
            pythonInterpreter = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\WPy64\scripts\winpython.bat')
            fileName = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\LinearAnalyses\openSees_StaticSolver.py')
            
            wrapperFile = '"' + wrapperFile + '"'
            fileName = '"' + fileName + '"'
            
            p = System.Diagnostics.Process()
            p.StartInfo.RedirectStandardOutput = True
            p.StartInfo.RedirectStandardError = True
        
            p.StartInfo.UseShellExecute = False
            p.StartInfo.CreateNoWindow = True
            
            p.StartInfo.FileName = pythonInterpreter
            p.StartInfo.Arguments = fileName + " " + wrapperFile
            p.Start()
            p.WaitForExit()
            
            
            msg = p.StandardError.ReadToEnd()
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)
        
        
            ## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
            ## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py
        
            outputFile = os.path.join(outputFolder, outputFileName)
        
            with open(outputFile, 'r') as f:
                lines = f.readlines()
                nodeDisplacementWrapper = eval( lines[0].strip() )
                reactionWrapper = eval( lines[1].strip() )
                elementOutputWrapper = eval( lines[2].strip() )
                elementLoadWrapper = eval( lines[3].strip() )
                eleForceWrapper = eval( lines[4].strip() )
        
        
            AlpacaLinearStaticOutput = ([nodeDisplacementWrapper,
                                    reactionWrapper,
                                    elementOutputWrapper,
                                    elementLoadWrapper,
                                    eleForceWrapper])
        
            return AlpacaLinearStaticOutput
        
        
        checkData = True
        
        if not AlpacaModel:
            checkData = False
            msg = "input 'AlpacaModel' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            AlpacaStaticOutput = InitializeStaticAnalysis(AlpacaModel)
            #maxDisplacement = None
            return AlpacaStaticOutput

class ModalAnalyses(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Modal Analyses (Alpaca4d)", "Modal Analyses", """Generate a circular cross section""", "Alpaca", "5|Analyses")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.secondary

    def get_ComponentGuid(self):
        return System.Guid("bab459c1-dd65-463e-84fa-67a320a4dfa5")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "AlpacaModel", "AlpacaModel", "Assemble model to perform Modal Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "numVibrationModes", "numVibrationModes", "Script input numVibrationModes.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "AlpacaModalOutput", "AlpacaModalOutput", "Analysed Alpaca model.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "frequency", "frequency", "Frequencies of the corrisponding modes [Hz].")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "period", "period", "Periods of the corrisponding modes [s].")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAOWSURBVEhL3ZVbaFRHGMfnnDm3PXuym41J3LhubiQxF6PdhkKtsaKBRvEhoWpIqT6ECClJwXoh2ja0pYK12pcaMcXivRFvoG19UEkbIURTivhgUhto05QELxUVpNVSrdP/N7N5CHE3VfDFP/w4c/7f7Myeb77zHfZcqwJ0gnx5N1GpoEoNn05rOGcC1/vgjHTG6y3wLTgOcsl4Un1cU2OKnTtdkZGh0UafK1sqAHYAHcwF74IxzdUY+w7XsLpNrPeWLDFFT0+KOHXKE8Gg3KRehVg1WKSGUnvi18p83RhdyD2a2ws86SZQxOfTxOnTntykqcmmH/WoEFsOXlJDqY/A7BLdunHZLRI3/WUiqPG/4LkymkQnmpttuUE4rNMGTcpmNaBSDVkreB20HXSyxS0sTszSHTo7hyYk08o5cwy5QSgkU/SistnboACYYDMIRDU++LtbIhcfcotFvmYMw59UteXlXG7Q0GDRBlQxlNd2wAEd8meg7UNrqrjuLxWrzXQR1szz8OipJigIZoL5YCPKdKSlRaXo5ElPeJ58il3xOVI60/rrjdS/r2Hxr5AizrStsA0VHa9NmsZuZ2ZqoqhIlzmPxfidWEzvKyzUjsHfhzlUOX45O65aPdBPh0qpedMI/QsrpiLjlQVGt293RXd3iujq8kRlJb8Cb6qMJhZ/wwhepcV/Q94jGv8J3mMPdqCigsuFOzv9orRUPwdvngolVeFmK+shbbDNyqL0rVf2RF2qq7NkrletkvUeUXZypTH9/Yu+QjHgzqB//wuskIpMFDWtK9XVpujocEVenva9spMqbYURGv4VqVnA3Tu4p8JIKuqOPzc22qK11aGneFm6Sq+BTWqoFGL6hqNOjqhSiy9T7uSajtL8h87BNNmWuEeHRrVOTW0sx9Ne4b6bM9EaMKZ6p3eDGiCV+aTaX19vCfQhekPRGNlaMNb3O+LXrSbTfsS1eDH3DjWYqVeX8sDeteaU6/AsQH+KfvtYVdu2/A5sAEvBCjLjagPU++n7ECVjo5XZe8FXIM7YebcOOzmPDlrZf3zt5N77xAgPUTyRDoBBcATYZMRF1UWLfyHvoHVmxg99voKHe+zoo0NO9oM1RsbIqL9E7LanfxOfklB0yC+o4ThR/yGk3jHTzx6wItcaeejiMSd6v92O3KVm96Ud/RPhyV7U/6Wycua8GmS8qtYIfFDHU7d8amUdaeJT6CNElfksxdh/LtT+vpyTzI0AAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaModel, numVibrationModes):
        
        
        import System
        import os
        import Grasshopper as gh
        
        def InitializeModalAnalysis(AlpacaModel, numEigenvalues):
            ghFilePath = self.Attributes.Owner.OnPingDocument().FilePath
        
            # delete file if already there
            workingDirectory = os.path.dirname(ghFilePath) 
            outputFileName = 'openSeesModalOutputWrapper.txt'
        
            for dirpath, dirnames, filenames in os.walk(workingDirectory):
                for filename in filenames:
                    if filename == outputFileName:
                        file = os.path.join(dirpath,outputFileName)
                        os.remove(file)
        
        
            ghFolderPath = os.path.dirname(ghFilePath)
            outputFolder = os.path.join(ghFolderPath,'assembleData')
            wrapperFile = os.path.join( outputFolder,'openSeesModel.txt' )
        
        
        
            userObjectFolder = gh.Folders.DefaultUserObjectFolder
            pythonInterpreter = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\WPy64\scripts\winpython.bat')
            fileName = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\DynamicAnalysis\openSees_ModalSolver.py')
            
            wrapperFile = '"' + wrapperFile + '"'
            fileName = '"' + fileName + '"'
            
            p = System.Diagnostics.Process()
            p.StartInfo.RedirectStandardOutput = True
            p.StartInfo.RedirectStandardError = True
        
            p.StartInfo.UseShellExecute = False
            p.StartInfo.CreateNoWindow = True
            
            p.StartInfo.FileName = pythonInterpreter
            p.StartInfo.Arguments = fileName + " " + wrapperFile + " " + str(numVibrationModes)
            p.Start()
            p.WaitForExit()
            
            
            msg = p.StandardError.ReadToEnd()
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)
        
            ## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
            ## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py
        
            outputFile = os.path.join(outputFolder, outputFileName)
        
            with open(outputFile, 'r') as f:
                lines = f.readlines()
                nodeModalDispWrapper = eval( lines[0].strip() )
                elementModalWrapper = eval( lines[1].strip() )
                period = eval( lines[2].strip() )
                frequency = eval( lines[3].strip() )
        
        
            AlpacaModalOutputWrapper = ([nodeModalDispWrapper,
                                    elementModalWrapper,
                                    period,
                                    frequency])
        
            return [AlpacaModalOutputWrapper, period, frequency]
        
        checkData = True
        
        if not AlpacaModel:
            checkData = False
            msg = "input 'AlpacaModel' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if numVibrationModes is None:
            checkData = False
            msg = "input 'numEigenvalues' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            AlpacaModalOutput, period, frequency = InitializeModalAnalysis(AlpacaModel, numVibrationModes)
            return (AlpacaModalOutput, frequency, period)

class GroundMotionAnalyses(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Ground Motion Analyses (Alpaca4d)", "Ground Motion Analyses", """Calculate the Time History Response of the structure""", "Alpaca", "5|Analyses")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.tertiary

    def get_ComponentGuid(self):
        return System.Guid("5137750c-49fe-4940-9980-8265b306aee5")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaModel", "AlpacaModel", "Assembled model to perform Static Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "TmaxAnalyses", "TmaxAnalyses", "Time Frame where the structure will be analyse")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "GroundMotionDirection", "GroundMotionDirection", "Direction of the earthQuake. 1 = X, 2 = Y, 3 = Z")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "GroundMotionValues", "GroundMotionValues", "Acceleration values for each time step")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "GroundMotionTimeStep", "GroundMotionTimeStep", "time step for each acceleration value")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "GroundMotionFactor", "GroundMotionFactor", "Multiplier of the GroundMotionValues")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "TimeStepIncrement", "TimeStepIncrement", "integration step size. Recomended value is 0.1 times the time step")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "Damping", "Damping", "Damping value")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "NewmarkGamma", "NewmarkGamma", "Gamma value to implement the Newmark integrator.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "NewmarkBeta", "NewmarkBeta", "Beta value to implement the Newmark integrator.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "AlpacaGroundmotionOutput", "AlpacaGroundmotionOutput", "Script output AlpacaGroundmotionOutput.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "maxDisplacement", "maxDisplacement", "Maximum displacement of structure [mm].")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "minDisplacement", "minDisplacement", "Minimum displacement of structure [mm].")
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
        p8 = self.marshal.GetInput(DA, 8)
        p9 = self.marshal.GetInput(DA, 9)
        result = self.RunScript(p0, p1, p2, p3, p4, p5, p6, p7, p8, p9)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAK5SURBVEhLtdVPSBRRAAbwmV1nZ3dmWy1Wa9ddzGz9F9Eh+nPIyKQouiRdSg/qoTrZISoyukRGEiYm4aU1DyIUIkGXxLAgiNKSiqItyEqRNgvDijBr3df3zWygtCtm0wc/nPd23rw37715SgtIBnjMS+vjggGIQQv4wdLsBjFDPViau/AC1sJz+AI2sCRumIRTRkmS9gLfotwoWRB2wAfWQSb0ANeiFCwJd893OJHwAw6DZVO0FfgGe+AmPAVLYofNwEV9B0ugA6KwoKyBA9AOnOdHMA184C5gzsNnkI3SX6QYxiEOY8CPqheOgQ9+pxkmgG837+yACPDB7MgBqdIFL83L+SULOKInsI8Vc2QRcC3CRsncXQWgQ4AVyVIC3CHdRmnuVAPv3c5CSFbP9rhyY35ZOXNRzea6JH1zfkTXgQ3XswJRgbtnm1Eykw7cno/BCd7qtMWfPuqrRIldjw1rRWy/GpKGRzBH0GmUJOkQsAFVsQKpBZYrjJIkVbapAfFeLxZHlEzx1uyAB2LKXAOuAzu7A6/gPnB9gsC57wN+C1keWW57puWLEb0o3uXMEVF0pEvyJfyWcnfdg9twGXgsHAQeZhzZlcTfTXmyo7VV9U1tsbujD1whwamJaAVGB+1qMF5hT6/3Ssp+3PtHOOoP8BNOsgLhPxU+mB1SWaNj2eQ45r1FzY6FMUWvtULxEB31u1aKMXQyqOVP97vyvuJeHoqzwi+YD/sGy1mRCHcX64dyZeVGRAtNXVB9E6N6kahVvILT1O3MiXU5g1N9rhViSCuMNSm+W0bLJNkA68zLWQkB93xVmU2vLLW5j/Mtdto9owMYfacjOHzVGXzTkLZ0pFHxNZXYtKNGq39IQV2adygoK6c56rAj0FGjZPSW2z3nEr9blo3Nqj/eoPhrEuX/Ep5dink5M5L0C+p9wtWSmcP2AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaModel, TmaxAnalyses, GroundMotionDirection, GroundMotionValues, GroundMotionTimeStep, GroundMotionFactor, TimeStepIncrement, Damping, NewmarkGamma, NewmarkBeta):
        
        
        import System
        import os
        import Grasshopper as gh
        
        def InitializeGroundMotionAnalysis(AlpacaModel, TmaxAnalyses, GroundMotionDirection, GroundMotionValues, GroundMotionTimeStep, GroundMotionFactor, TimeStepIncrement, Damping, NewmarkGamma, NewmarkBeta):
            ghFilePath = self.Attributes.Owner.OnPingDocument().FilePath
        
            # delete file if already there
            workingDirectory = os.path.dirname(ghFilePath) 
            outputFileName = 'openSeesEarthQuakeAnalysisOutputWrapper.txt'
        
            for dirpath, dirnames, filenames in os.walk(workingDirectory):
                for filename in filenames:
                    if filename == outputFileName:
                        file = os.path.join(dirpath,outputFileName)
                        os.remove(file)
        
        
            ghFolderPath = os.path.dirname(ghFilePath)
            outputFolder = os.path.join(ghFolderPath,'assembleData')
            wrapperFile = os.path.join( outputFolder,'openSeesModel.txt' )
        
        
        
            earthQuakeSettings = []
        
            for item in GroundMotionValues:
                earthQuakeSettings.append( "GROUNDMOTIONVALUES {}".format(item) )
        
            for item in GroundMotionTimeStep:
                earthQuakeSettings.append( "GROUNDMOTIONTIMESTEP {}".format(item) )
        
            earthQuakeSettings.append( "GROUNDMOTIONDIRECTION {}".format(GroundMotionDirection) )
            earthQuakeSettings.append( "GROUNDMOTIONFACTOR {}".format(GroundMotionFactor) )
            earthQuakeSettings.append( "DAMPING {}".format(Damping) )
            earthQuakeSettings.append( "NEWMARKGAMMA {}".format(NewmarkGamma) )
            earthQuakeSettings.append( "NEWMARKBETA {}".format(NewmarkBeta) )
            earthQuakeSettings.append( "TMAXANALYSES {}".format(TmaxAnalyses) )
            earthQuakeSettings.append( "TIMESTEP {}".format(TimeStepIncrement) )
        
        
            earthQuakeSettingsFile = os.path.join( outputFolder,'earthQuakeSettingsFile.txt')
        
            with open(earthQuakeSettingsFile, 'w') as f:
                for item in earthQuakeSettings:
                    f.write("%s\n" % item)
        
        
            userObjectFolder = gh.Folders.DefaultUserObjectFolder
            pythonInterpreter = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\WPy64\scripts\winpython.bat')
            fileName = os.path.join(userObjectFolder, r'Alpaca4d\Analyses\EarthQuakeAnalysis\openSees_EarthQuakeAnalysis.py')
        
        
            fileName = '"' + fileName + '"'
            wrapperFile = '"' + wrapperFile + '"'
            earthQuakeSettingsFile = '"' + earthQuakeSettingsFile + '"'
            
            p = System.Diagnostics.Process()
            p.StartInfo.RedirectStandardOutput = False
            p.StartInfo.RedirectStandardError = True
        
            p.StartInfo.UseShellExecute = False
            p.StartInfo.CreateNoWindow = False
            
            p.StartInfo.FileName = pythonInterpreter
            p.StartInfo.Arguments = fileName + " " + wrapperFile + " " + earthQuakeSettingsFile
            p.Start()
            p.WaitForExit()
            
            
            msg = p.StandardError.ReadToEnd()
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Error, msg)
        
        
        
        
        
        
        
            print("I have finished")
        
            ## READ THE OUTPUT FROM THE OPEENSEES_SOLVER
            ## THE ORDER MUST BE THE SAME OF THE OUTPUT LIST IN OpenSeesStaticSolver.py
        
        
            outputFile = os.path.join(outputFolder, outputFileName)
        
            with open(outputFile, 'r') as f:
                lines = f.readlines()
                nodeDispFilePath = lines[0]
                elementModalWrapper = eval( lines[1].strip() )
                nodeWrapper = eval( lines[2].strip() )
                maxDisplacement = lines[3]
                minDisplacement = lines[4]
        
        
            AlpacaGroundmotionOutput = [nodeDispFilePath, elementModalWrapper, nodeWrapper]
        
            return [AlpacaGroundmotionOutput, maxDisplacement, minDisplacement]
        
        checkData = True
        
        if not AlpacaModel:
            checkData = False
            msg = "input 'AlpacaModel' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if TmaxAnalyses is None:
            checkData = False
            msg = "input 'TmaxAnalyses' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if GroundMotionDirection is None:
            checkData = False
            msg = "input 'GroundMotionDirection' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if not GroundMotionValues:
            checkData = False
            msg = "input 'GroundMotionValues' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if not GroundMotionTimeStep:
            checkData = False
            msg = "input 'GroundMotionTimeStep' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if GroundMotionFactor is None:
            checkData = False
            msg = "input 'GroundMotionFactor' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if TimeStepIncrement is None:
            checkData = False
            msg = "input 'TimeStepIncrement' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if Damping is None:
            checkData = False
            msg = "input 'Damping' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if NewmarkGamma is None:
            checkData = False
            msg = "input 'NewmarkGamma' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if NewmarkBeta is None:
            checkData = False
            msg = "input 'NewmarkBeta' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            AlpacaGroundmotionOutput, maxDisplacement, minDisplacement = InitializeGroundMotionAnalysis(AlpacaModel, TmaxAnalyses, GroundMotionDirection, GroundMotionValues, GroundMotionTimeStep, GroundMotionFactor, TimeStepIncrement, Damping, NewmarkGamma, NewmarkBeta)
            return (AlpacaGroundmotionOutput, maxDisplacement, minDisplacement)


# 6|Numerical Output

class NodeDisplacement(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Node Displacement (Alpaca4d)", "Node Displacement ", """Compute nodal displacement in the Global Axis system""", "Alpaca", "6|Numerical Output")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.primary

    def get_ComponentGuid(self):
        return System.Guid("d4b31c40-fab9-43af-99f6-6e62fc7c418d")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaStaticOutput", "AlpacaStaticOutput", "Static Analyses output solver.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Points", "Points", "Points of the model .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Trans", "Trans", "Translation of the model points.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Rot", "Rot", "Rotation of the model points.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAJTSURBVEhLtZZLaBNRFIZn8hiNlNaKqKUkaTFiM3PvpTOZzNTQdAxYS9tUUIii2QiNuwqu6qKgC5cWu7Mr8YFhDPjArSBuVFR0J6jFhaAr38VN8NHjuZkbsNbVzPjBYZJ7fs7POfcMjPQXUYw8PibxmWqdhAgWll509e6AHlqEdR0bf0qyfBHPNrSyAUlFYsqna+dOwkqjBtCYhq/uDKTtccBc3ZMEQZbnJ494hf8MbpLo3sJNBjyhb+QHry6dWGPAI21PcIOqp/ONfO/u4uya4r9wXElzlBsc9HT+mesv7MOCx1YZ3LywAPFERxPzPZ7MP50YLxtnavDZPQ7v3Fl4X5+B1E4K0Wh03mBszJMFYxuOyo3E4s1E12Y+lreKoswNEvLIYuy7oWllTxYcvve9GDJGRNe0+lihCLZufNMJ2cUFoaKqqqJTemdi2AHs5AMaZvGYm4eHlcl0GpQ+LRdLYFL6hneF/w2RDgebkK3YyeupkRLsLQwDGiyKVDjwUWHRh/tLo7B0/jrYg/oXy7L49oUHbtJ2NLmyxxr64eRtyDE2LVLhgtvEcFy3+AqLI8lxnJipaUn8GfFOQgBfQJvfDRotYGfLjqOBzuhHg5FT3FDIgoEFr1ZrA1B/3Ae3l9Jw+X4/HDicBezwrJD4R1fVjDNCVm48T7eKt8N91gdWnjSHVHWTkPpDZ2zq0NHsquLtGC+rwO9KSP0hOoB/dmCSJqW0W0j9w9/qai0L9Sf/4Q44jpNez7cICy7vbm8RIadD26I2uVwubppaslKp8E8fgST9Bh3qDO1zHLOvAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaStaticOutput):
        
        import Rhino.Geometry as rg
        import Grasshopper as gh
        
        
        def NodeDisp( AlpacaStaticOutput ):
                # define output
        
            global Points
            global Trans
            global Rot
            
            diplacementWrapper = AlpacaStaticOutput[0]
            EleOut = AlpacaStaticOutput[2]
        
            pointWrapper = []
            transWrapper = []
            rotWrapper = []
            #print(diplacementWrapper[0])
            for index,item in enumerate(diplacementWrapper):
                pointWrapper.append(  rg.Point3d(item[0][0],item[0][1],item[0][2])  )
                if len(item[1]) == 3:
                    transWrapper.append(  rg.Vector3d( item[1][0], item[1][1], item[1][2] ) )
                    rotWrapper.append(   rg.Vector3d( 0,0,0 )  )
            
                elif len(item[1]) == 6:
                    transWrapper.append(  rg.Vector3d( item[1][0], item[1][1], item[1][2] ) )
                    rotWrapper.append(   rg.Vector3d( item[1][3],item[1][4],item[1][5] )  )
            
            Points = pointWrapper
            Trans = transWrapper 
            Rot = rotWrapper 
        
            return Points, Trans, Rot
        
        
        checkData = True
        
        if not AlpacaStaticOutput :
            checkData = False
            msg = "input 'AlpacaStaticOutput' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            Points, Trans, Rot = NodeDisp( AlpacaStaticOutput )
            return (Points, Trans, Rot)

class ReactionForces(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Reaction Forces (Alpaca4d)", "Reaction Forces (Alpaca4d)", """Compute the reaction forces""", "Alpaca", "6|Numerical Output")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.primary

    def get_ComponentGuid(self):
        return System.Guid("0be5f38d-6134-4ff3-9702-d2898a4da0c4")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaStaticOutput", "AlpacaStaticOutput", "Output of solver on static Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "tagPoints", "tagPoints", "nodes tag of Model .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "ReactionForce", "ReactionForce", "Vector of reaction Forces { Rx, Ry, Rz }. [kN]")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "ReactionMoment", "ReactionMoment", "Vector of reaction Moments { Mx, My, Mz }. [kN]")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAH0SURBVEhL7ZKxSxxBFMa3CDZJpYje7OxdbmfuXMa7jV6KxKQQTCpBCNiIjZIikEbQSrAIBIz4V1goJKQ50l0XSBuCrQQtbPRudsRIICIW63vju4McenerV1j4gwfzvt33vp331knC00LhDUYpCFIkdZdSsRhjoAlJ3eXeoMFzpXqfKDXSHHWD0WJxsflZGIZZKm8PNJl/OVaIJ6dURzHxahhNy1TeHjR4uxDE335nOor1LZHcYHpW2cJOYuFDPqFBGE5gQZKAxS9T+e2oZTKDdPyPw4HwIR1vzhETLwz3NyltEDvjD4wrfmiWzZN0M4wry5r5Z2DkkWSJPPnecBlHTFZIag1+ER0bHGeGHmvun9tGrvhIsqPTQQpupQ2T/yBO4Z0ZenQ9hokt+NpFSi2ay0/Q/FfE/Qgabtf61SPUd9x8SCbbhvlzVZZ7bQtaYbhYA4PPlFoOPTGMDbDRCQv6Klz10qPLHXBZg9GNkdQaXKZ2/RNsRJKlbkBpA5j9FNz6IFaqh6T24MIiLr9SarnKoJrNDoC+B3t5R1JnHAzKfhjVDprgjFFrNjBu7hlou9B8g6Rk4IgiV36Bpn9xJxiw7H3jiRWY+Xerw/mqvy4ROiVKcJNV+A1/aib/4K2OPLFUv1nXuG7JXaOazvnGy81TehdwnAv/6hsy2W8YaQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaStaticOutput):
        
        import Rhino.Geometry as rg
        import math
        import ghpythonlib.treehelpers as th # per data tree
        import Grasshopper as gh
        
        
        def reaction(AlpacaStaticOutput):
            
            global tagPoints
            global ReactionForce
            global ReactionMoment
            global view
        
            scale = 1
        
        
            diplacementWrapper = AlpacaStaticOutput[0]
            reactionOut = AlpacaStaticOutput[1]

        
            pointWrapper = []
        
            for index,item in enumerate(diplacementWrapper):
                pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
        
            ## Dict. for point ##
            pointWrapperDict = dict( pointWrapper )
        
            ## per scalare le reazioni #
            rowReaction = [row[1] for row in reactionOut ]
        
            valorReaction = []
            for valor in rowReaction:
                rx = math.fabs( valor[0] )
                ry = math.fabs( valor[1] )
                rz = math.fabs( valor[2] )
                mx = math.fabs( valor[3] )
                my = math.fabs( valor[4] )
                mz = math.fabs( valor[5] )
                valorReaction.append( [ rx, ry, rz, mx, my, mz ] )
        
            rx = max([row[0] for row in valorReaction ])
            ry = max([row[1] for row in valorReaction ])
            rz = max([row[2] for row in valorReaction ])
            mx = max([row[3] for row in valorReaction ])
            my = max([row[4] for row in valorReaction ])
            mz = max([row[5] for row in valorReaction ])
            # -------------------------------------------------------#
        
            ReactionForce = []
            ReactionMoment = []
            viewElement = []
            tagPoints = []
            for value in reactionOut:
                pointIndex = value[0]
                tagPoints.append( pointIndex )
                point = pointWrapperDict.get( pointIndex , "never")
                Rx = rg.Vector3d( value[1][0], 0, 0 )
                Ry = rg.Vector3d( 0,value[1][1], 0 )
                Rz = rg.Vector3d( 0,0, value[1][2] )
                Mx = rg.Vector3d( value[1][3], 0, 0 )
                My = rg.Vector3d( 0, value[1][4], 0 )
                Mz = rg.Vector3d( 0,0, value[1][5] )
                Rxyz = Rx + Ry + Rz
                Mxyz = Mx + My + Mz
                viewElement.append( [ point, Rx/rx*scale, Ry/ry*scale, Rz/rz*scale, Mx/mx*scale, My/my*scale, Mz/mz*scale ] )
                ReactionForce.append( Rxyz )
                ReactionMoment.append( Mxyz )
        
            point = [row[0] for row in viewElement ]
            Rx = [row[1] for row in viewElement ]
            Ry = [row[2] for row in viewElement ]
            Rz = [row[3] for row in viewElement ]
            Mx = [row[4] for row in viewElement ]
            My = [row[5] for row in viewElement ]
            Mz = [row[6] for row in viewElement ]
        
        
            return tagPoints, ReactionForce, ReactionMoment
        
        checkData = True
        
        if not AlpacaStaticOutput :
            checkData = False
            msg = "input 'AlpacaStaticOutput' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

        if checkData != False :
            tagPoints, ReactionForce, ReactionMoments = reaction( AlpacaStaticOutput )
            return (tagPoints, ReactionForce, ReactionMoment)

class BeamDisplacement(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Beam Displacement (Alpaca4d)", "Beam Displacement", """Compute the beam displacement """, "Alpaca", "6|Numerical Output")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.secondary

    def get_ComponentGuid(self):
        return System.Guid("7ad38934-180e-48bb-b266-bf495a59e1fa")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaStaticOutput", "AlpacaStaticOutput", "Output of solver on static Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "numberResults", "numberResults", "number of discretizations for beam.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "tagElement", "tagElement", "number of the tag of Beam or Truss element .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "localTrans", "localTrans", "Displacements related to the local axis ( 1-Red, 2-Green, 3-Blue).")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "localRot", "localRot", "Rotation related to the local axis ( 1-Red, 2-Green, 3-Blue).")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "globalTrans", "globalTrans", "Displacements related to the global axis ( XYZ ).")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "globalRot", "globalRot", "Rotation related to the global axis ( XYZ ).")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
                self.marshal.SetOutput(result[3], DA, 3, True)
                self.marshal.SetOutput(result[4], DA, 4, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAIBSURBVEhL7dRPSJNhHAfwzSVztk3f9m6ukY43ze3gnzRHf1ypoKARidBhHsKRpoc0BEkQtJ28yBCMqFt2qUtoFB1CDx0igvASZKII3jqJB+kkxbfv731xM3rBP3sJgr7wged53nfPl5d3z2v7W4nTrMU6KZNkf2sU71JXLTHWVQvumTK2NpKsKlWQuHTaErFy/x8FdfSEzlpghBooSJm00YIxzDmrVGEMs7GyYI3OGMNs/u0ChR7QCjXKQo4xfYI52iZNn+UW0wJZGDWGNifJ/BzVU5gOE9OCVnpOy06PsuPyhqAGmuHzx1Ho1uTQbNAw5dN+MS14FGm7ievpRXTPLqNl4CWa2pcyYvEXqKzxSNF78uu/MI+8w290lwpkYTedodoriA/OQIpUrR5ubxSKegHh8j50JHrwai2MnnuKlHyh307pnrTQT3qmz/bES/P0lHpJvq5ROk8ppytva3hK1UtujeklX+kkmUW+QaoxPHjK6LNsLiW3x0/A4bDLe2nWr2YjpdeM4eHjo0+JoSKkp2O4XzWBiCciT7NOS7QRPpYPX55D1qrpSJFD+aE92IHXjW/w9vICHmo38DFYhtWQhs1TFUgeL5J30K/ffcS46HFJQcmPRGk3BgMNmFYCGHAX46LThUK7/Tuvz+h35hj5r9+hNE1SkuRwHuSs/M9ubLZf+4Dt6yx33FgAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaStaticOutput, numberResults):
        
        import Rhino.Geometry as rg
        import math as mt
        import ghpythonlib.treehelpers as th # per data tree
        import Grasshopper as gh
        import sys
        import rhinoscriptsyntax as rs
        from scriptcontext import doc
        
        #---------------------------------------------------------------------------------------#
        ## -------------FUNZIONI DI FORMA PER TRAVE DI TYMOSHENKO------------------ ##
        
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
        
        def linspace(a, b, n=100):
            if n < 2:
                return b
            diff = (float(b) - a)/(n - 1)
            return [diff * i + a  for i in range(n)]
        ## node e nodeDisp son dictionary ##
        def defValueTimoshenkoBeamValue( ele, node, nodeDisp, numberResults ):
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
            localTraslStart = rg.Point3d( traslStart )
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
            DivCurve = linspace( 0, Length, numberResults )
            if DivCurve == None:
                DivCurve = [ 0, Length]
                
            #s = dg.linspace(0,Length, len(PointsDivLength))
            AlphaY = alphat( E, G, Iy, Avz )
            AlphaZ = alphat( E, G, Iz, Avy )
            
            globalTransVector = []
            globalRotVector = []
            localTransVector = []
            localRotVector = []
            #----------------------- local to global-------------------------#
            xform2 = xform.TryGetInverse()
            #----------------------------------------------------------------#
            for index, x in enumerate(DivCurve):
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
                localTransVector.append( transResult )
        
                r2x =  thetaz(x, Length, uI1, uJ1, rI2, rJ2, AlphaY)
                r1x =  psiy(x, Length, uI2, uJ2, rI1, rJ1, AlphaZ)
                r3x = phix(x, Length, rI3, rJ3)
                
                rotResult = r1x*axis1 + r2x*axis2 + r3x*axis3
                localRotVector.append( rotResult )
                 
                globalRot = rg.Point3d( rotResult ) 
                globalRot.Transform(xform2[1]) 
                globalRot.Transform(xform)
                globalRotVector.append( rg.Vector3d( globalRot ) ) 
                globalTrasl = rg.Point3d( transResult ) 
                globalTrasl.Transform(xform2[1]) 
                globalTrasl.Transform(xform)
                globalTransVector.append( rg.Vector3d( globalTrasl ) )
                
            return  [  localTransVector, localRotVector ,  globalTransVector, globalRotVector ] 
        
        ## node e nodeDisp son dictionary ##
        def defTrussValue( ele, node, nodeDisp, numberResults ):
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
            localTraslStart = rg.Point3d( traslStart )
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
            DivCurve = linspace( 0, Length, numberResults )
            if DivCurve == None:
                DivCurve = [ 0, Length]
        
            globalTransVector = []
            localTransVector = []
            #----------------------- local to global-------------------------#
            xform2 = xform.TryGetInverse()
            #----------------------------------------------------------------#
            for index, x in enumerate(DivCurve):
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
                localTransVector.append( transResult )
                
                globalTrasl = rg.Point3d( transResult ) 
                globalTrasl.Transform(xform2[1]) 
                globalTrasl.Transform(xform)
                globalTransVector.append( rg.Vector3d( globalTrasl ) )
        
            return  [ localTransVector, globalTransVector] 
        
        #--------------------------------------------------------------------------
        def beamDisp( AlpacaStaticOutput, numberResults ):
        
            if numberResults is None :
               numberResults = 2 
        
            diplacementWrapper = AlpacaStaticOutput[0]
            EleOut = AlpacaStaticOutput[2]
            nodeValue = []
            displacementValue = []
        
            pointWrapper = []
            dispWrapper = []
            for index,item in enumerate(diplacementWrapper):
                nodeValue.append( item[0] )
                displacementValue.append( item[1] )
                print( item[0] )
                pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
                if len(item[1]) == 3:
                    dispWrapper.append( [index, rg.Point3d( item[1][0], item[1][1], item[1][2] ) ] )
                elif len(item[1]) == 6:
                    dispWrapper.append( [index, [rg.Point3d(item[1][0],item[1][1],item[1][2] ), rg.Point3d(item[1][3],item[1][4],item[1][5]) ] ] )
        
            ## Dict. for point ##
            pointWrapperDict = dict( pointWrapper )
            pointDispWrapperDict = dict( dispWrapper )
            ####
        
            transLocal = []
            rotLocal = []
            transGlobal = []
            rotGlobal = []
            tag = []
            for ele in EleOut :
                eleTag = ele[0]
                eleType = ele[2][0]
                if eleType == 'ElasticTimoshenkoBeam' :
                    valueTBeam = defValueTimoshenkoBeamValue( ele, pointWrapperDict, pointDispWrapperDict, numberResults )
                    transLocal.append(valueTBeam[0])
                    rotLocal.append(valueTBeam[1])
                    transGlobal.append(valueTBeam[2])
                    rotGlobal.append(valueTBeam[3])
                    tag.append( eleTag )
                elif eleType == 'Truss' :
                    valueTruss = defTrussValue( ele, pointWrapperDict, pointDispWrapperDict, numberResults )
                    transLocal.append(valueTruss[0])
                    rotLocal.append([rg.Vector3d(0,0,0)]*len(valueTruss[0]))
                    transGlobal.append(valueTruss[1])
                    rotGlobal.append([rg.Vector3d(0,0,0)]*len(valueTruss[0]))
                    tag.append( eleTag )
        
            localTrans = th.list_to_tree( transLocal )
            localRot = th.list_to_tree( rotLocal )
            globalTrans = th.list_to_tree( transGlobal )
            globalRot = th.list_to_tree( rotGlobal )
            tagElement = tag
        
            return tagElement, localTrans, localRot, globalTrans, globalRot
        
        
        checkData = True
        
        if not AlpacaStaticOutput :
            checkData = False
            msg = "input 'AlpacaStaticOutput' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            tagElement, localTrans, localRot, globalTrans, globalRot = beamDisp( AlpacaStaticOutput , numberResults )
            return (tagElement, localTrans, localRot, globalTrans, globalRot)

class BeamForces(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Beam Forces (Alpaca4d)", "Beam Forces", """Compute the internal forces of a beam""", "Alpaca", "6|Numerical Output")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.secondary
    
    def get_ComponentGuid(self):
        return System.Guid("a1593306-5f65-4c4d-af95-270566d05a89")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaStaticOutput", "AlpacaStaticOutput", "Output of Static Solver Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "numberResults", "numberResults", "number of discretizations for beam. Defauls is 2.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "tagElement", "tagElement", "Beam or Truss element's tag number.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "N", "N", "normal force values (forces in direction 3) [kN].")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "V1", "V1", "shear force values (forces in direction 1) [kN].")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "V2", "V2", "shear force values (forces in direction 2) [kN].")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Mt", "Mt", "torque value (Moments in direction 3) [kNm].")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "M1", "M1", "bending moment (Moments in direction 1) [kNm].")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "M2", "M2", "bending moment (Moments in direction 2) [kNm].")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
                self.marshal.SetOutput(result[3], DA, 3, True)
                self.marshal.SetOutput(result[4], DA, 4, True)
                self.marshal.SetOutput(result[5], DA, 5, True)
                self.marshal.SetOutput(result[6], DA, 6, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAALVSURBVEhLYyADMBoyc/ppsLLqANkcECEGhvvy8hxvVFT4rmhpsUGFyAPyDGwaDQySVxKZhI86MnGlgQx+IaOo+1pG5eJrKZWMd5JKclCl5AETNs7gYkbRazlMwndjmQW63bm4JF/Kqii/klJ++0pGpe2NvKomVCnZgNefhX9JHJPQ0VQGkdrNQjLSQNdnvZFRqXsjoyr9n4GBCaqOfMDFwCBZwCiyuIhRbMFSQSnLN1Iqp9/Lqyv8pzT8kUEW0PVFjCI7Z/JJLn4lo7wbKkwVIAXEzdIMLOvDmfguT+GSug8MomiIFGUAFLZcTEyMp8sDdL+W++v9D9aV/WbAyrH3looKO0QJZUABiFd1xZj9fzkr6v//lcn/99Z6/vc2lL0BFNcHq6AAGMiJcM9IsFcFGwzDF7oC/5f76j0GymdClJEHzFUl+acBDf/3Y0kC3PBbE0L+t4QafuRgZdwMVMMPUUo6UJYT5lmZ66798928GLjhT2dE/k92VPsqwsO+BKgGFHRkg1wJPo4LIZaKf/fWe/0DGf5pQdz/QFOFP/Ii3J1AeW2IMvJBtL286ElHGZH/7vJi/y93BfzxNZb7LyXE2Q6U04AooQzwlHELzaxgF/6cxCTyX5iH/R9QbBoQy4BlKQWg4veulGL/Bj6ZBwkMgs90GTivAoVZgZgRrIBSACx+fV9Lq5Rv5pdpj2YQmlbEIHoFKCwMxCxgBZSC1zLKE4ClZOIKQXEdPwYB7xoGyU/6DJwFQJ+AgogZoopMAAqeN9IqG9/IKAUCudxGDBy2voz8Z0oZRb96M/D6CZKb9oHlOSO4+pNW6X4jrdz1WlbJBCjMpgesIl1ZeBYVM4r9imMQXB/GIGgN0UEmeC2j9BoYPHveyKq4gioRYGEjYMTKGlbNLPoqm1F0VgqDiDFUKXngtbRywwtpRb2nkpLA+gUB9NnZFcxZWfUsGPiEoELDGjAwAADq5NfuCxJ3AwAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaStaticOutput, numberResults):
        
        import Rhino.Geometry as rg
        import math
        import ghpythonlib.treehelpers as th # per data tree
        import Grasshopper as gh
        import ghpythonlib.components as ghcomp
        import sys
        import rhinoscriptsyntax as rs
        from scriptcontext import doc
        
        
        def linspace(a, b, n=100):
            if n < 2:
                return b
            diff = (float(b) - a)/(n - 1)
            return [diff * i + a  for i in range(n)]
        
        def forceTimoshenkoBeam( ele, node, force, loadDict, numberResults ):
            #---------------- WORLD PLANE ----------------------#
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
            DivCurve = linspace( 0, Length, numberResults )
            if numberResults == None:
                DivCurve = [ 0, Length]
                
            uniformLoad = loadDict.get( TagEle , [0,0,0])
            q1 = uniformLoad[0]
            q2 = uniformLoad[1]
            q3 = uniformLoad[2]
            
            N, V1, V2, Mt, M1, M2 = [], [], [], [], [], [] 
            #----------------------- local to global-------------------------#
            xform2 = xform.TryGetInverse()
            #----------------------------------------------------------------#
            for index, x in enumerate(DivCurve):
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
                
            eleForceValue = [ N, V1, V2, Mt, M1, M2 ]
            return   eleForceValue 
        
        
        def forceTrussValue(  ele, node, force, loadDict, numberResults ):
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
            axis1 =  rg.Vector3d( propSection[9][0][0], propSection[9][0][1], propSection[9][0][2]  )
            axis2 =  rg.Vector3d( propSection[9][1][0], propSection[9][1][1], propSection[9][1][2]  )
            axis3 =  rg.Vector3d( propSection[9][2][0], propSection[9][2][1], propSection[9][2][2]  )
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
            DivCurve = linspace( 0, Length, numberResults )
            if numberResults == None:
                DivCurve = [ 0, Length]
                
            uniformLoad = loadDict.get( TagEle , [0,0,0])
            q1 = uniformLoad[0]
            q2 = uniformLoad[1]
            q3 = uniformLoad[2]
            
            N, V1, V2, Mt, M1, M2 = [], [], [], [], [], [] 
            #----------------------- local to global-------------------------#
            xform2 = xform.TryGetInverse()
            #----------------------------------------------------------------#
            for index, x in enumerate(DivCurve):
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
                
            eleForceValue = [ N, V1, V2, Mt, M1, M2 ]
            return  eleForceValue
        
        
        def beamForces( AlpacaStaticOutput, numberResults ):
        
            # define output
            global tagElement
            global N
            global V1
            global V2
            global Mt
            global M1
            global M2
        
            if numberResults is None:
                numberResults = 2
        
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
            tag = []
        
            for ele in EleOut :
                eleTag = ele[0]
                eleType = ele[2][0]
                if eleType == 'ElasticTimoshenkoBeam' :
                    tag.append( eleTag )
                    valueTBeam = forceTimoshenkoBeam( ele, pointWrapperDict, forceWrapperDict, loadWrapperDict, numberResults )
                    N.append(valueTBeam[0])
                    V1.append(valueTBeam[1])
                    V2.append(valueTBeam[2])
                    Mt.append(valueTBeam[3])
                    M1.append(valueTBeam[4])
                    M2.append(valueTBeam[5])
                elif eleType == 'Truss' :
                    tag.append( eleTag )
                    valueTruss = forceTrussValue( ele, pointWrapperDict, forceWrapperDict, loadWrapperDict, numberResults )
                    N.append(valueTruss[0])
                    V1.append(valueTruss[1])
                    V2.append(valueTruss[2])
                    Mt.append(valueTruss[3])
                    M1.append(valueTruss[4])
                    M2.append(valueTruss[5])
                    
            tagElement = th.list_to_tree( tag )
            N = th.list_to_tree( N )
            V1 = th.list_to_tree( V1 )
            V2 = th.list_to_tree( V2 )
            Mt = th.list_to_tree( Mt )
            M1 = th.list_to_tree( M1 )
            M2 = th.list_to_tree( M2 )
        
            return tagElement, N, V1, V2, Mt, M1, M2
        
        
        checkData = True
        
        if not AlpacaStaticOutput:
            checkData = False
            msg = "input 'AlpacaStaticOutput' failed to collect data"  
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        
        if checkData != False:
            tagElement, N, V1, V2, Mt, M1, M2 = beamForces( AlpacaStaticOutput, numberResults )
            return (tagElement, N, V1, V2, Mt, M1, M2)

class ShellDisplacement(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Shell Displacement (Alpaca4d)", "Shell Displacement", """Compute the shell displacement""", "Alpaca", "6|Numerical Output")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.tertiary

    def get_ComponentGuid(self):
        return System.Guid("00fff614-43bb-471b-ae6b-1641e09e0650")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaStaticOutput", "AlpacaStaticOutput", "Output of solver on static Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "tagElement", "tagElement", "number of the tag of Shell element .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Trans", "Trans", "Translation of the Shell nodes .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Rot", "Rot", "Rotation of the Shell nodes  .")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAAKoSURBVEhL5ZVrSJNRGMd3dbpNnXM2l7rFmFlUkugMA1NLl6bmDVxrYZikaagRy8JC0qDMiiANivCShSVh0gW6YB8jiARBLAhqEFQgEkUERs6n/7PV0D64rfxQ9IMf57znvM9zbi/vEfwNCOFaKHI/LSJB0A7HTNFhhHIC7oLB8I9QwkbozFqlo2cniogGq2i0vZgKUwwuqUT8Fn2HYAQMCC1sU8ikU9WbEmj8dCn11W2g7j3pNHnJTr2oX2vMImeXlfblryZFsPQT3j8DDRzsCyl8b00z0rsLNveMWa6ftJtpNwYcaMjytrO8sshQGW8dr4jjF4QPskksFjnzk+LozkELXanPnOXy20ClO+Grc+V0tT6THh8roGKzgfDua8TwVvKW+o0YFsJ7Rm3oTFt5snt7eJBhRzalmqJ4xk+hFfqctS9MsCNIIp7Ua5Qu1G/DDO5YbOTQr4P855D8KH8bPoNOOAK7YBL8SR50wj4o44ZAKQpWqr6k7DhCua1DlGxvpgj9Cv6CnrPxa4Ko/Xo0ZZcpuY0noIL+IxSKj1taBsnWOzHP3KM3qLQ6km69NHgtrwvnQcZgrDvYTxwrt1S5k+Y4eqgkr4W2bW6ljMp2MpcVzN58ofcOcPFRDFmWK0giEL5BXKIn3DdxIaolM4Vpe6k7pYfupz90O5Q2TDb99tminSpynNXQ4QoNXdbpaCrWRAMaHcmFog+I3ehJ4ZuRjsRT3uRz3b8008VJf/VuVAxWIphGbLwnxcJU5Ggt3qSdSeep2lhDNcZasuptrida/bzk47pltF4WwufRC/mX45NwuVj+uc/cT6nqVA4chU2wGT5Qi8TTJSFKagpTk10RRgqh6CPaa2FA9EuEkq8oGyD/ceeihlvhAcg3X8AXEJMA13mq/ycCwXcMmjPuZEGdywAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaStaticOutput):
        
        import Rhino.Geometry as rg
        import ghpythonlib.treehelpers as th # per data tree
        import Grasshopper as gh
        #---------------------------------------------------------------------------------------#
        def defShellQuadValue( ele, node, nodeDisp ):
            
            eleTag = ele[0]
            eleNodeTag = ele[1]
            
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
            
            return  [[trasl1, trasl2, trasl3, trasl4], [rotate1, rotate2, rotate3, rotate4]]
        
        def defShellTriangleValue( ele, node, nodeDisp, scaleDef ):
            
            eleTag = ele[0]
            eleNodeTag = ele[1]
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            
            trasl1 = nodeDisp.get( index1 -1 , "never")[0]
            rotate1 = nodeDisp.get( index1 -1 , "never")[1]
            
            trasl2 = nodeDisp.get( index2 -1 , "never")[0]
            rotate2 = nodeDisp.get( index2 -1 , "never")[1]
            
            trasl3 = nodeDisp.get( index3 -1 , "never")[0]
            rotate3 = nodeDisp.get( index3 -1 , "never")[1]
            
            return  [[trasl1, trasl2, trasl3], [rotate1, rotate2, rotate3]]
        
        def shellDisp( AlpacaStaticOutput ):
            diplacementWrapper = AlpacaStaticOutput[0]
            EleOut = AlpacaStaticOutput[2]
        
            pointWrapper = []
            transWrapper = []
            rotWrapper = []
        
            diplacementWrapper = AlpacaStaticOutput[0]
            EleOut = AlpacaStaticOutput[2]
            nodeValue = []
            displacementValue = []
        
            pointWrapper = []
            dispWrapper = []
        
            for index,item in enumerate(diplacementWrapper):
                nodeValue.append( item[0] )
                displacementValue.append( item[1] )
                pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
                if len(item[1]) == 3:
                    dispWrapper.append( [index, rg.Vector3d( item[1][0], item[1][1], item[1][2] ) ] )
                elif len(item[1]) == 6:
                    dispWrapper.append( [index, [rg.Vector3d(item[1][0],item[1][1],item[1][2] ), rg.Vector3d(item[1][3],item[1][4],item[1][5]) ] ] )
        
            ## Dict. for point ##
            pointWrapperDict = dict( pointWrapper )
            pointDispWrapperDict = dict( dispWrapper )
            ####
        
            trans = []
            rot = []
            tag = []
            for ele in EleOut :
                tagEle = ele[0]
                eleType = ele[2][0]
                nNode = len( ele[1] )
                if nNode == 4 and eleType != 'FourNodeTetrahedron':
                    trasl = defShellQuadValue( ele, pointWrapperDict, pointDispWrapperDict )
                    trans.append(trasl[0])
                    rot.append(trasl[1])
                    tag.append( tagEle )
                    
                elif nNode == 3:
                    trasl = defShellTriangleValue( ele, pointWrapperDict, pointDispWrapperDict )
                    trans.append(trasl[0])
                    rot.append(trasl[1])
                    tag.append( tagEle )
                    
            tagElement = tag
            Trans = th.list_to_tree( trans )
            Rot = th.list_to_tree( rot )
        
            return tagElement, Trans, Rot
        
        
        checkData = True
        
        if not AlpacaStaticOutput :
            checkData = False
            msg = "input 'AlpacaStaticOutput' failed to collect data"
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            tagElement, Trans, Rot = shellDisp( AlpacaStaticOutput )
            return (tagElement, Trans, Rot)

class ShellForces(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Shell Forces (Alpaca4d)", "Shell Forces", """Compute internal shell forces""", "Alpaca", "6|Numerical Output")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.tertiary

    def get_ComponentGuid(self):
        return System.Guid("7b280ab1-0c7c-4ff8-9815-4d3986ed953b")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaStaticOutput", "AlpacaStaticOutput", "Output of solver on static Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "tagElement", "tagElement", "number of the tag of Beam or Truss element .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Fx", "Fx", "Forces in direction X  of the Shell nodes .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Fy", "Fy", "Forces in direction Y of the Shell nodes .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Fz", "Fz", "Forces in direction Z  of the Shell nodes .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Mx", "Mx", "Moments in direction X  of the Shell nodes .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "My", "My", "Moments in direction Y  of the Shell nodes .")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Mz", "Mz", "Moments in direction Z  of the Shell nodes .")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
                self.marshal.SetOutput(result[3], DA, 3, True)
                self.marshal.SetOutput(result[4], DA, 4, True)
                self.marshal.SetOutput(result[5], DA, 5, True)
                self.marshal.SetOutput(result[6], DA, 6, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAALqSURBVEhLtVVNaNRAFI4/KKKgSLU2mTRtMtlts5tuu0st/aGtRcT+qa2ybS+iiCDYYxVFe9BjD55UEJEKFaUgiIoevOlJUOhBPFgFRdA1mWwr6M2f8b10tkR3t5sW/OAjb17mzTfvZeZFKoYsqbY9YoyKYVEwYp5yiEHFMDw8hR5kxLgrhkXBCH2cVfRuMQwHLnWszQlwSVot3Hn4SqytIDCdlY002sJdGo5KDU8xnnkyfctI5KRw58FTzEGX6J4n6++YFqkR7uII7oIR/ZInG5/ndH2zcBUELP7UVYwJMZS4Za0T5gKgBKs8zazNEj3uErPdIeYDJkejnyoiZUw19uGcVCpVlkgkqoJEH76DDBsz5fp2tKFUzR6h42gvYm5HleYRfcaV6SuX0A/AnzDpzZBlnUnaNkc27mzhTa1dfxF9uffAI7C58xD7C2IdWO8b8DuUsEnILAAzYYpxMVNetxGD2geO8pHJ10ty1/CoL/CRkA34vZhKrzvbrE15pfoXyxUQYRJuTphLA4MwuNCiQeImUvH4AREWHmEF2npHeL1t7xZh4RFWoLmrjycsq16EhUdYgdbuNE/FYp0iLDz+yzeYpXS9MKVkPJ7uOHS84KJBLkvAUSNt0H7HUAiD2nqG+ODEI94/PsX7z93kfWdv8J6xqz57T1/zfS17BhYFHNmsZzI94S+WAzS1w9isfCr0JdzG39DkXuyPxfqhTDNIOCUPG2z7HjynG2KxSZ+2fQt9yGRdXRNTzAvQ+H7ATZ6F53MkXNpOvyzYPf0OSugxELwNPUVFcVepNf1dLAFHMRNIpkZl2OBlVzWvYItA4o0W0xYQdMxXRqqhn7gZLVolXHnwGyW2dSDa6HMrayr8l6UA6U1CRhxEpoQrD64W6YZ576FdP4Hf5l7hLg0s25fqeDkKYPrB0xUE/u2gLHeg3sNgrxHu8ECBUimv6J+cA5ymzLymbRHDgoAM7vunZSUIkzZuIPeB8yFJfwANJ+00XtlwtwAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaStaticOutput):
        
        import Rhino.Geometry as rg
        import math as mt
        import ghpythonlib.treehelpers as th # per data tree
        import Grasshopper as gh
        import sys
        import rhinoscriptsyntax as rs
        from scriptcontext import doc
        
        
        def shellForces( AlpacaStaticOutput ):
        
        
            diplacementWrapper = AlpacaStaticOutput[0]
            EleOut = AlpacaStaticOutput[2]
            ForceOut = AlpacaStaticOutput[4]
        
            pointWrapper = []
            for index,item in enumerate(diplacementWrapper):
                pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
            ## Dict. for point ##
            pointWrapperDict = dict( pointWrapper )
        
            forceWrapper = []
            for item in ForceOut:
                index = item[0]
                if len(item[1]) == 24: #6* numo nodi = 24 elementi quadrati
                    Fi = rg.Vector3d( item[1][0], item[1][1], item[1][2] ) # risultante nodo i
                    Mi = rg.Vector3d( item[1][3], item[1][4], item[1][5] )
                    Fj = rg.Vector3d( item[1][6], item[1][7], item[1][8] ) # risultante nodo j
                    Mj = rg.Vector3d( item[1][9], item[1][10], item[1][11] )
                    Fk = rg.Vector3d( item[1][12], item[1][13], item[1][14] ) # risultante nodo k
                    Mk = rg.Vector3d( item[1][15], item[1][16], item[1][17] )
                    Fw = rg.Vector3d( item[1][18], item[1][19], item[1][20] ) # risultante nodo w
                    Mw = rg.Vector3d( item[1][21], item[1][22], item[1][23] )
                    forceOut = [[ Fi.X, Fj.X, Fk.X, Fw.X ],
                                [ Fi.Y, Fj.Y, Fk.Y, Fw.Y ],
                                [ Fi.Z, Fj.Z, Fk.Z, Fw.Z ],
                                [ Mi.X, Mj.X,  Mk.X, Mw.X ],
                                [ Mi.Y, Mj.Y, Mk.Y, Mw.Y ],
                                [ Mi.Z, Mj.Z, Mk.Z, Mw.Z ]]
                    forceWrapper .append( [index, forceOut ])
        
                if len(item[1]) == 18: #6* numo nodi = 18 elementi quadrati
                    Fi = rg.Vector3d( item[1][0], item[1][1], item[1][2] ) # risultante nodo i
                    Mi = rg.Vector3d( item[1][3], item[1][4], item[1][5] )
                    Fj = rg.Vector3d( item[1][6], item[1][7], item[1][8] ) # risultante nodo j
                    Mj = rg.Vector3d( item[1][9], item[1][10], item[1][11] )
                    Fk = rg.Vector3d( item[1][12], item[1][13], item[1][14] ) # risultante nodo k
                    Mk = rg.Vector3d( item[1][15], item[1][16], item[1][17] )
                    forceOut = [[ Fi.X, Fj.X, Fk.X ],
                                [ Fi.Y, Fj.Y, Fk.Y ],
                                [ Fi.Z, Fj.Z, Fk.Z ],
                                [ Mi.X, Mj.X,  Mk.X ],
                                [ Mi.Y, Mj.Y, Mk.Y ],
                                [ Mi.Z, Mj.Z, Mk.Z ]]
                    forceWrapper .append( [index, forceOut ])
        
            ## Dict. for force ##
            forceWrapperDict = dict( forceWrapper )
            ####
            Fx, Fy, Fz, Mx, My, Mz = [],[],[],[],[],[]
            tag = []
        
            for ele in EleOut :
                eleTag = ele[0]
                eleType = ele[2][0]
                if eleType == "ShellMITC4" :
                    tag.append( eleTag )
                    outputForce = forceWrapperDict.get( eleTag )
                    Fx.append( outputForce[0] )
                    Fy.append( outputForce[1] )
                    Fz.append( outputForce[2] )
                    Mx.append( outputForce[3] )
                    My.append( outputForce[4] )
                    Mz.append( outputForce[5] )
                elif eleType == "ShellDKGT" :
                    tag.append( eleTag )
                    outputForce = forceWrapperDict.get( eleTag )
                    Fx.append( outputForce[0] )
                    Fy.append( outputForce[1] )
                    Fz.append( outputForce[2] )
                    Mx.append( outputForce[3] )
                    My.append( outputForce[4] )
                    Mz.append( outputForce[5] )
                    
            tagElement = th.list_to_tree( tag )
            Fx = th.list_to_tree( Fx )
            Fy = th.list_to_tree( Fy )
            Fz = th.list_to_tree( Fz )
            Mx = th.list_to_tree( Mx )
            My = th.list_to_tree( My )
            Mz = th.list_to_tree( Mz )
        
            return tagElement, Fx, Fy, Fz, Mx, My, Mz
        
        checkData = True
        
        if not AlpacaStaticOutput:
            checkData = False
            msg = "input 'AlpacaStaticOutput' failed to collect data"  
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            tagElement, Fx, Fy, Fz, Mx, My, Mz = shellForces( AlpacaStaticOutput )
            return (tagElement, Fx, Fy, Fz, Mx, My, Mz)

class ShellStress(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Shell Stress (Alpaca4d)", "Shell Stress", """Compute the internal stress on a shell""", "Alpaca", "6|Numerical Output")
        return instance

    def get_Exposure(self): #override Exposure property
        return Grasshopper.Kernel.GH_Exposure.tertiary

    def get_ComponentGuid(self):
        return System.Guid("bacc44e0-0723-4a4d-b519-769a24f9734c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AlpacaStaticOutput", "AlpacaStaticOutput", "Output of solver on static Analyses.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "stressView", "stressView", "stress acting on the shell nodes.\n'0' - sigmaX ( membrane stress X ) ;\n'1' - sigmaY  ( membrane stress Y );\n'2' - sigmaXY ( membrane stress XY );\n'3' - tauX  ( transverse shear forces X );\n'4' - tauY ( transverse shear forces Y ).\n'5' - mX ( bending moment X ) ;\n'6' - my  ( bending moment Y );\n'7' - mxy ( bending moment XY  );")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "shell", "shell", "mesh that represent the shell.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "stressValue", "stressValue", "value of stress acting on the shell nodes.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAANISURBVEhL7ZNbSJNhGMf3uVPDwumWUzc3Uxse0jnX3CgPM8uVYUZnKVQyCgKTDoTYCS3MDqbkxTxVM1uxaVq2UuwiL5IkguiiA4GQ0OkiIrrpcOG/531X0kV09CKoP/z43vd53uf/Pe/7vZ/on5WcSAsMp1aRxAGJRHhqMEpB4wFCxxJ/KjvhCQkTv19boETHsBaXHxuw5UAY5Iqg15TbwFf9ohRECXF7dooMlfUqXLyvR99dAzwt0ei+roe3Tw/XUBSMJjnbTTcRTvxQ0cQhiVR46VgWjIb6SG7EOv4Cm7trouG7Foj3PtRj/SYlpFLhBdUWcZdvKFsQiXpiwmQfi7cp4R7RTRq6/TrU7YzD5ooMbC1ywplXgaKSbSh0rsfu8mxUVxpReyIKh7o0iE2Ssd24CSV3JSUSdxPMcuxqVON8fzQ8bXpcvKfH/vZ4LC8rhzXrDArm96AkqQaF87zIWXxnkpVzO7DG3Iy8HD8sGa0oTCuZUIc7IAjicfINZS/YNTtVjq7RQMfsnHccmYNlqVtRYHMjN38UqywtWJLt54b5uUNYne7CwrxhirdiwaKbPL7c1oWyhH18bJnnQVCQ9Dl5s+sskhF7QpTid8UVamTm70dW/q3PRWexKW47md3gcxa32E5hQXoTqnSlWJdci4WWZlitLhSZGuB0DGKp/RyCZ8RPkGchM/9aScSIKjwHdsc1buh0DPDnkpR6FCdUo5ZMejIuoDulEYNZQ7hi88KXfAy+OQ1oM7eg2nQcMer57Bu4uOM3JCYqxBLFW2PyHthy+rHGdBQuSwf89l5cSDgIb+Jhbv6FntRm/oI+czvqqBGqf0QEM7PvKYYYjFToJk7NPc2N+qnz3rQW9Jrb+A681H1rYg3OUOcs70lvh0qm+kB1Vu7wE6JbKyqVi+WvNsaU45L1PK5mDuBk8j50RtnROV2LYZUBIxq6cZp4GBUadu57eeUvKoLwGWcYUTXThHFtLB5rYvEkIg5jxD31LDSFhrOjuUlIWMHvaoVEEJ5VTg/FA80svNLFc+5EGBAsBL2hfGxg2Z+J/TgdRolswj9Ti5faOFhk01j3pTw7hVokFglj1oC5LxCaerGr2Emo+Oy//lKJRJ8AAgSWcEbrIvgAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, AlpacaStaticOutput, stressView):        
        import Rhino.Geometry as rg
        import ghpythonlib.treehelpers as th
        import Grasshopper as gh
        import sys
        import os
        import rhinoscriptsyntax as rs
        from scriptcontext import doc
        
        
        
        #---------------------------------------------------------------------------------------#
        def ShellStressQuad( ele, node ):
            eleTag = ele[0]
            eleNodeTag = ele[1]
            color = ele[2][2]
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            index4 = eleNodeTag[3]
            
            ## CREO IL MODELLO  ##
            point1 = node.get( index1 -1 , "never")
            point2 = node.get( index2 -1 , "never")
            point3 = node.get( index3 -1 , "never")
            point4 =  node.get( index4 -1 , "never")
            
            shellModel = rg.Mesh()
            shellModel.Vertices.Add( point1 ) #0
            shellModel.Vertices.Add( point2 ) #1
            shellModel.Vertices.Add( point3 ) #2
            shellModel.Vertices.Add( point4 ) #3
            
            shellModel.Faces.AddFace(0, 1, 2, 3)
            colour = rs.CreateColor( color[0], color[1], color[2] )
            shellModel.VertexColors.CreateMonotoneMesh( colour )
            return  shellModel 
        
        def ShellTriangle( ele, node ):
            
            eleTag = ele[0]
            eleNodeTag = ele[1]
            color = ele[2][2]
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            
            
            ## CREO IL MODELLO DEFORMATO  ##
            point1 =  node.get( index1 -1 , "never")
            point2 =  node.get( index2 -1 , "never")
            point3 =  node.get( index3 -1 , "never")
            
            shellModel = rg.Mesh()
            shellModel.Vertices.Add( point1 ) #0
            shellModel.Vertices.Add( point2 ) #1
            shellModel.Vertices.Add( point3 ) #2
            
            shellModel.Faces.AddFace(0, 1, 2)
            colour = rs.CreateColor( color[0], color[1], color[2] )
            shellModel.VertexColors.CreateMonotoneMesh( colour )
            
            return  shellModel
        
        #--------------------------------------------------------------------------
        def shellStressView( AlpacaStaticOutput, stressView ):
        
            global shell
            global stressValue
        
            diplacementWrapper = AlpacaStaticOutput[0]
            EleOut = AlpacaStaticOutput[2]
            ForceOut = AlpacaStaticOutput[4]
            #print( ForceOut[0] )
            #print( ForceOut[1] )
            #nodalForce = openSeesOutputWrapper[5]
        
            #nodalForcerDict = dict( nodalForce )
        
            pointWrapper = []
            for index,item in enumerate(diplacementWrapper):
                pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
            ## Dict. for point ##
            pointWrapperDict = dict( pointWrapper )
        
            shellTag = []
            for item in EleOut:
                if  len(item[1])  == 4:
                     shellTag.append(item[0])
        
            ## Dict. for force ##
            #forceWrapperDict = dict( forceWrapper )
            ghFilePath = self.Attributes.Owner.OnPingDocument().FilePath
            workingDirectory = os.path.dirname(ghFilePath)
            outputFile = os.path.join(workingDirectory, 'assembleData' )
            outputFile = os.path.join(outputFile, 'tensionShell.out' )
            #---------------------------------------------------#
        
            with open(outputFile, 'r') as f:
                lines = f.readlines()
                tensionList = lines[0].split()
                
            #print(len(tensionList)/len(shellTag))
        
            #print(stressView + 24)
            tensionDic = []
            for n,eleTag in enumerate(shellTag) :
                tensionShell = []
                for i in range( (n)*32, ( n + 1 )*32  ):
                    tensionShell.append( float(tensionList[i]) )
                tensionView = [ tensionShell[ stressView ], tensionShell[ stressView + 8 ], tensionShell[ stressView + 16 ], tensionShell[ stressView + 24 ] ]
                tensionDic.append([ eleTag, tensionView ])
        
            stressDict = dict( tensionDic )
            stressValue = th.list_to_tree( stressDict.values() )
            
            #print( stressDict.get(2))
            #print( stressDict )
            #print( tensionList[0], tensionList[8], tensionList[16], tensionList[24] )
            #print( tensionDic[0] )
            
            shell = []
            for ele in EleOut :
                eleTag = ele[0]
                eleType = ele[2][0]
                if eleType == "ShellMITC4" :
                    shellModel = ShellStressQuad( ele, pointWrapperDict )
                    shell.append( shellModel )
                elif eleType == "ShellDKGT" :
                    outputForce = forceWrapperDict.get( eleTag )
                    shellModel = ShellTriangle( ele, pointWrapperDict )
                    shell.append( shellModel )
        
            return shell, stressValue
        
        checkData = True
        
        if not AlpacaStaticOutput :
            checkData = False
            msg = "input 'AlpacaStaticOutput' failed to collect data"  
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if stressView is None :
            checkData = False
            msg = " input 'stressView' failed to collect data"  
            self.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)
        
        if checkData != False:
            shell, stressValue = shellStressView( AlpacaStaticOutput, stressView )
            return (shell, stressValue)




# General Info

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Alpaca4d"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return "Marco Pellegrino - Domenico Gaudioso"
    
    def get_Id(self):
        return System.Guid("9bfbb08d-6b4d-446f-b226-cfe680dabf16")
