import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper
#import System as sy #DV
import sys
import rhinoscriptsyntax as rs

'''
ghFilePath = ghenv.LocalScope.ghdoc.Path
ghFileName = ghenv.LocalScope.ghdoc.Name
folderNameLength = len(ghFilePath)-len(ghFileName)-2 #have to remove '.gh'
ghFolderPath = ghFilePath[0:folderNameLength]

outputPath = ghFolderPath + 'assembleData'
wrapperFile = ghFolderPath + 'assembleData\\openSeesModel.txt'

userObjectFolder = Grasshopper.Folders.DefaultUserObjectFolder
fileName = userObjectFolder + 'Alpaca'
'''
fileName = r'C:\GitHub\Alpaca4d\PythonScript\function'
sys.path.append(fileName)
# importante mettere import 'import Rhino.Geometry as rg' prima di importatre DomeFunc
import DomeFunc as dg 
def gradientJet(value, valueMax, valueMin, nColor):
    if nColor == 0:
        listcolo = [rs.CreateColor( 0, 0, 255 ),
                    rs.CreateColor( 0, 128, 255 ),
                    rs.CreateColor( 0, 255, 255 ),
                    rs.CreateColor( 0, 255, 128 ),
                    rs.CreateColor( 128, 255, 0 ),
                    rs.CreateColor( 255, 255, 0 ),
                    rs.CreateColor( 255, 128, 0 ),
                    rs.CreateColor( 204, 0, 0 )]
    elif nColor == 1:
        listcolo = [ rs.CreateColor( 0, 0, 102 ),
                    rs.CreateColor( 0, 0, 255 ),
                    rs.CreateColor( 0, 64, 255 ),
                    rs.CreateColor( 0, 128, 255 ),
                    rs.CreateColor( 0, 191, 255 ),
                    rs.CreateColor( 0, 255, 255 ),
                    rs.CreateColor( 0, 255, 191 ),
                    rs.CreateColor( 0, 255, 128 ),
                    rs.CreateColor( 0, 255, 64 ),
                    rs.CreateColor( 0, 255, 0 ),
                    rs.CreateColor( 64, 255, 0 ),
                    rs.CreateColor( 128, 255, 0 ),
                    rs.CreateColor( 191, 255, 0 ),
                    rs.CreateColor( 255, 255, 0 ),
                    rs.CreateColor( 255, 191, 0 ),
                    rs.CreateColor( 255, 128, 0 ),
                    rs.CreateColor( 255, 64, 0 ),
                    rs.CreateColor( 255, 0, 0 ),
                    rs.CreateColor( 230, 0, 0 ),
                    rs.CreateColor( 204, 0, 0 )]
    #domain = linspace( valueMin,  valueMax, len( listcolo ) )
    n = len( listcolo )
    domain = dg.linspace( valueMin, valueMax, n)
    
    for i in range(1,n):
        if  domain[i-1] <= value <= domain[i]:
            return listcolo[ i ]
        elif  valueMax <= value <= valueMax + 0.00001 :
            return listcolo[ -1 ]
        elif  valueMin - 0.00000000001 <= value <= valueMin  :
            return listcolo[ 0 ]

def gradientJet2(valueMax, valueMin, nColor ):

    if nColor == 0:
        listcolo = [rs.CreateColor( 0, 0, 255 ),
                    rs.CreateColor( 0, 128, 255 ),
                    rs.CreateColor( 0, 255, 255 ),
                    rs.CreateColor( 0, 255, 128 ),
                    rs.CreateColor( 128, 255, 0 ),
                    rs.CreateColor( 255, 255, 0 ),
                    rs.CreateColor( 255, 128, 0 ),
                    rs.CreateColor( 204, 0, 0 )]
    elif nColor == 1:
        listcolo = [ rs.CreateColor( 0, 0, 102 ),
                    rs.CreateColor( 0, 0, 255 ),
                    rs.CreateColor( 0, 64, 255 ),
                    rs.CreateColor( 0, 128, 255 ),
                    rs.CreateColor( 0, 191, 255 ),
                    rs.CreateColor( 0, 255, 255 ),
                    rs.CreateColor( 0, 255, 191 ),
                    rs.CreateColor( 0, 255, 128 ),
                    rs.CreateColor( 0, 255, 64 ),
                    rs.CreateColor( 0, 255, 0 ),
                    rs.CreateColor( 64, 255, 0 ),
                    rs.CreateColor( 128, 255, 0 ),
                    rs.CreateColor( 191, 255, 0 ),
                    rs.CreateColor( 255, 255, 0 ),
                    rs.CreateColor( 255, 191, 0 ),
                    rs.CreateColor( 255, 128, 0 ),
                    rs.CreateColor( 255, 64, 0 ),
                    rs.CreateColor( 255, 0, 0 ),
                    rs.CreateColor( 230, 0, 0 ),
                    rs.CreateColor( 204, 0, 0 )]

    #domain = linspace( valueMin,  valueMax, len( listcolo ) )
    n = len( listcolo )
    diff = (float(valueMax) - valueMin)/( n - 1 )
    domain = [diff * i + valueMin  for i in range(n)]
    return [ listcolo, domain ]

colorList = gradientJet2( max, min, nColor )
color = colorList[0]  #.reverse()
color.reverse()
tag = []
tag.append( str(round(colorList[1][0],2) ) )
for i in range(1,len(colorList[1])):
    tag.append( str(round(colorList[1][i-1],2)) + '< valor < ' + str(round(colorList[1][i],2)) )
domain = colorList[1]
tag.reverse()

colorValue = []
for i in value:
    colorValue.append(gradientJet(i, max, min, nColor))
    print(len(value))