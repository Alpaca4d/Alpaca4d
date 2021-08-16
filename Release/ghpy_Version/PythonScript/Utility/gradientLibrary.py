"""
Preset of gradient colors perfect for Data Visualisation. The script comes from Ladybug and it has been "reshape" for our plug-in
    Inputs:
        gradientIndex: An index refering to one of the following possible gradients:
            0 - Orignal Ladybug
            1 - Nuanced Ladybug
            2 - Multi-colored Ladybug
            3 - Ecotect
            4 - Thermal Comfort Percentage
            5 - Thermal Comfort Colors
            6 - Shade Benefit/Harm
            7 - Shade Harm
            8 - Shade Benefit
            9 - CFD Colors 1
            10 - Radiation Benefit
            11 - Gsa10 Colour
            12 - Gsa9 Colour
    Returns:
        colorsList: A series of colors.
"""


from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, gradientIndex):
        
        import System
        
        gradientIndex = 11 if gradientIndex is None else gradientIndex
        
        def gradientColor(gradientIndex):
            
            gradientLibrary = {
                    0: [System.Drawing.Color.FromArgb(75, 107, 169), System.Drawing.Color.FromArgb(115, 147, 202), System.Drawing.Color.FromArgb(170, 200, 247), System.Drawing.Color.FromArgb(193, 213, 208), System.Drawing.Color.FromArgb(245, 239, 103), System.Drawing.Color.FromArgb(252, 230, 74), System.Drawing.Color.FromArgb(239, 156, 21), System.Drawing.Color.FromArgb(234, 123, 0), System.Drawing.Color.FromArgb(234, 74, 0), System.Drawing.Color.FromArgb(234, 38, 0)],
                    1: [System.Drawing.Color.FromArgb(49,54,149), System.Drawing.Color.FromArgb(69,117,180), System.Drawing.Color.FromArgb(116,173,209), System.Drawing.Color.FromArgb(171,217,233), System.Drawing.Color.FromArgb(224,243,248), System.Drawing.Color.FromArgb(255,255,191), System.Drawing.Color.FromArgb(254,224,144), System.Drawing.Color.FromArgb(253,174,97), System.Drawing.Color.FromArgb(244,109,67), System.Drawing.Color.FromArgb(215,48,39), System.Drawing.Color.FromArgb(165,0,38)],
                    2: [System.Drawing.Color.FromArgb(4,25,145), System.Drawing.Color.FromArgb(7,48,224), System.Drawing.Color.FromArgb(7,88,255), System.Drawing.Color.FromArgb(1,232,255), System.Drawing.Color.FromArgb(97,246,156), System.Drawing.Color.FromArgb(166,249,86), System.Drawing.Color.FromArgb(254,244,1), System.Drawing.Color.FromArgb(255,121,0), System.Drawing.Color.FromArgb(239,39,0), System.Drawing.Color.FromArgb(138,17,0)],
                    3: [System.Drawing.Color.FromArgb(0,0,255), System.Drawing.Color.FromArgb(53,0,202), System.Drawing.Color.FromArgb(107,0,148), System.Drawing.Color.FromArgb(160,0,95), System.Drawing.Color.FromArgb(214,0,41), System.Drawing.Color.FromArgb(255,12,0), System.Drawing.Color.FromArgb(255,66,0), System.Drawing.Color.FromArgb(255,119,0), System.Drawing.Color.FromArgb(255,173,0), System.Drawing.Color.FromArgb(255,226,0), System.Drawing.Color.FromArgb(255,255,0)],
                    4: [System.Drawing.Color.FromArgb(0,0,0), System.Drawing.Color.FromArgb(110,0,153), System.Drawing.Color.FromArgb(255,0,0), System.Drawing.Color.FromArgb(255,255,102), System.Drawing.Color.FromArgb(255,255,255)],
                    5: [System.Drawing.Color.FromArgb(0,136,255), System.Drawing.Color.FromArgb(200,225,255), System.Drawing.Color.FromArgb(255,255,255), System.Drawing.Color.FromArgb(255,230,230), System.Drawing.Color.FromArgb(255,0,0)],
                    6: [System.Drawing.Color.FromArgb(5,48,97), System.Drawing.Color.FromArgb(33,102,172), System.Drawing.Color.FromArgb(67,147,195), System.Drawing.Color.FromArgb(146,197,222), System.Drawing.Color.FromArgb(209,229,240), System.Drawing.Color.FromArgb(255,255,255), System.Drawing.Color.FromArgb(253,219,199), System.Drawing.Color.FromArgb(244,165,130), System.Drawing.Color.FromArgb(214,96,77), System.Drawing.Color.FromArgb(178,24,43), System.Drawing.Color.FromArgb(103,0,31)],
                    7: [System.Drawing.Color.FromArgb(255,255,255), System.Drawing.Color.FromArgb(253,219,199), System.Drawing.Color.FromArgb(244,165,130), System.Drawing.Color.FromArgb(214,96,77), System.Drawing.Color.FromArgb(178,24,43), System.Drawing.Color.FromArgb(103,0,31)],
                    8: [System.Drawing.Color.FromArgb(255,255,255), System.Drawing.Color.FromArgb(209,229,240), System.Drawing.Color.FromArgb(146,197,222), System.Drawing.Color.FromArgb(67,147,195), System.Drawing.Color.FromArgb(33,102,172), System.Drawing.Color.FromArgb(5,48,97)],
                    9: [System.Drawing.Color.FromArgb(0,16,120), System.Drawing.Color.FromArgb(38,70,160), System.Drawing.Color.FromArgb(5,180,222), System.Drawing.Color.FromArgb(16,180,109), System.Drawing.Color.FromArgb(59,183,35), System.Drawing.Color.FromArgb(143,209,19), System.Drawing.Color.FromArgb(228,215,29), System.Drawing.Color.FromArgb(246,147,17), System.Drawing.Color.FromArgb(243,74,0), System.Drawing.Color.FromArgb(255,0,0)],
                    10: [System.Drawing.Color.FromArgb(0,191,48), System.Drawing.Color.FromArgb(255,238,184), System.Drawing.Color.FromArgb(255,0,0)],
                    11: [System.Drawing.Color.FromArgb(204,0,71), System.Drawing.Color.FromArgb(255,182,71), System.Drawing.Color.FromArgb(206,255,115), System.Drawing.Color.FromArgb(26,180, 214),System.Drawing.Color.FromArgb(0,0,207)],
                    12: [System.Drawing.Color.FromArgb(255, 51, 51), System.Drawing.Color.FromArgb(255, 170, 51), System.Drawing.Color.FromArgb(255, 255, 51), System.Drawing.Color.FromArgb(170, 255, 125), System.Drawing.Color.FromArgb(51, 255, 231), System.Drawing.Color.FromArgb(51, 170, 255), System.Drawing.Color.FromArgb(51,51, 255)]}
            
            return gradientLibrary[gradientIndex]
        
        
        colorsList = gradientColor(gradientIndex)
        return colorsList
