import Rhino.Geometry as rg
import math as mt
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper
#import System as sy #DV
import sys
import rhinoscriptsyntax as rs
from scriptcontext import doc

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
#---------------------------------------------------------------------------------------#
def ShellQuad( ele, node):
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

def gradientJet(value, valueMax, valueMin):

    listcolo = [[0, 0, 102 ],
                [0, 0, 255],
                [0, 64, 255],
                [0, 128, 255],
                [0, 191, 255],
                [0, 255, 255],
                [0, 255, 191],
                [0, 255, 128],
                [0, 255, 64],
                [0, 255, 0],
                [64, 255, 0],
                [128, 255, 0],
                [191, 255, 0],
                [255, 255, 0],
                [255, 191, 0],
                [255, 128, 0],
                [255, 64, 0],
                [255, 0, 0],
                [230, 0, 0],
                [204, 0, 0]]

    #domain = linspace( valueMin,  valueMax, len( listcolo ) )
    n = len( listcolo )
    domain = dg.linspace( valueMin, valueMax, n)
    
    for i in range(1,n):
        if  domain[i-1] <= value <= domain[i]:
            return listcolo[ i-1 ]
        elif  valueMax <= value <= valueMax + 0.00001 :
            return listcolo[ -1 ]
        elif  valueMin - 0.00000000001 <= value <= valueMin  :
            print( value, valueMin)
            return listcolo[ 0 ]
#--------------------------------------------------------------------------
diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]
ForceOut = openSeesOutputWrapper[4]
#nodalForce = openSeesOutputWrapper[5]

#nodalForcerDict = dict( nodalForce )

pointWrapper = []
for index,item in enumerate(diplacementWrapper):
    pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
## Dict. for point ##
pointWrapperDict = dict( pointWrapper )


forceWrapper = []
'''
for ele in EleOut :
    eleTag = ele[0]
    eleType = ele[2][0]
    if eleType == "ShellDKGQ" :
            eleNodeTag = ele[1]
            index1 = eleNodeTag[0] 
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]
            index4 = eleNodeTag[3]

            force1 = nodalForcerDict.get( index1  , "never")
            force2 = nodalForcerDict.get( index2  , "never")
            force3 = nodalForcerDict.get( index3  , "never")
            force4 = nodalForcerDict.get( index4  , "never")
            #print( force1, force2, force3, force4 )
            Fi = rg.Vector3d( force1[0], force1[1], force1[2] ) # risultante nodo i
            Mi = rg.Vector3d( force1[3], force1[4], force1[5] )
            Fj = rg.Vector3d( force2[0], force2[1], force2[3] ) # risultante nodo j
            Mj = rg.Vector3d( force2[3], force2[4], force2[5] )
            Fk = rg.Vector3d( force3[0], force3[1], force3[2] ) # risultante nodo k
            Mk = rg.Vector3d( force3[3], force3[4], force3[5] )
            Fw = rg.Vector3d( force4[0], force4[1], force4[2] ) # risultante nodo w
            Mw = rg.Vector3d( force4[3], force4[4], force4[5] )
            forceOut = [[ Fi.X, Fj.X, Fk.X, Fw.X ],
                        [ Fi.Y, Fj.Y, Fk.Y, Fw.Y ],
                        [ Fi.Z, Fj.Z, Fk.Z, Fw.Z ],
                        [ Mi.X, Mj.X,  Mk.X, Mw.X ],
                        [ Mi.Y, Mj.Y, Mk.Y, Mw.Y ],
                        [ Mi.Z, Mj.Z, Mk.Z, Mw.Z ]]

    elif eleType == "ShellDKGT" :
            eleNodeTag = ele[1]
            index1 = eleNodeTag[0]
            index2 = eleNodeTag[1]
            index3 = eleNodeTag[2]

            force1 = nodalForcerDict.get( index1 , "never")
            force2 = nodalForcerDict.get( index2 , "never")
            force3 = nodalForcerDict.get( index3 , "never")
            Fi = rg.Vector3d( force1[0], force1[1], force1[2] ) # risultante nodo i
            Mi = rg.Vector3d( force1[3], force1[4], force1[5] )
            Fj = rg.Vector3d( force2[0], force2[1], force2[3] ) # risultante nodo j
            Mj = rg.Vector3d( force2[3], force2[4], force2[5] )
            Fk = rg.Vector3d( force3[0], force3[1], force3[2] ) # risultante nodo k
            Mk = rg.Vector3d( force3[3], force3[4], force3[5] )
            forceOut = [[ Fi.X, Fj.X, Fk.X ],
                        [ Fi.Y, Fj.Y, Fk.Y ],
                        [ Fi.Z, Fj.Z, Fk.Z ],
                        [ Mi.X, Mj.X,  Mk.X ],
                        [ Mi.Y, Mj.Y, Mk.Y ],
                        [ Mi.Z, Mj.Z, Mk.Z ]]

    forceWrapper .append( [eleTag, forceOut ])
'''
print( ForceOut[0] )
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
shell = []
for ele in EleOut :
    eleTag = ele[0]
    eleType = ele[2][0]
    if eleType == "ShellDKGQ" :
        tag.append( eleTag )
        outputForce = forceWrapperDict.get( eleTag )
        #print( outputForce )
        Fx.append( outputForce[0] )
        Fy.append( outputForce[1] )
        Fz.append( outputForce[2] )
        Mx.append( outputForce[3] )
        My.append( outputForce[4] )
        Mz.append( outputForce[5] )
        shellModel = ShellQuad( ele, pointWrapperDict )
        shell.append( shellModel )
    elif eleType == "ShellDKGT" :
        tag.append( eleTag )
        outputForce = forceWrapperDict.get( eleTag )
        Fx.append( outputForce[0] )
        Fy.append( outputForce[1] )
        Fz.append( outputForce[2] )
        Mx.append( outputForce[3] )
        My.append( outputForce[4] )
        Mz.append( outputForce[5] )
        shellModel = ShellTriangle( ele, pointWrapperDict )
        shell.append( shellModel )
        
tagElement = th.list_to_tree( tag )

fx = th.list_to_tree( Fx )
fy = th.list_to_tree( Fy )
fz = th.list_to_tree( Fz )
mx = th.list_to_tree( Mx )
my = th.list_to_tree( My )
mz = th.list_to_tree( Mz )

if viewForce == 0:
    shellForceValue = Fx
    ForceValue = fx
elif viewForce == 1:
    shellForceValue = Fy
    ForceValue = fy
elif viewForce == 2:
    shellForceValue = Fz
    ForceValue = fz
elif viewForce == 3:
    shellForceValue = Mx
    ForceValue = mx
elif viewForce == 4:
    shellForceValue = My
    ForceValue = mx
elif viewForce == 5:
    ForceValue = mx
    shellForceValue = Mz

maxValue = []
minValue = []
for value in shellForceValue:
    maxValue.append( max( value ))
    minValue.append( min( value ))
maxValue = max( maxValue )
minValue = min( minValue )

modelForce = []
for shellEle, value in zip(shell,shellForceValue) :
    shellColor = shellEle.DuplicateMesh()
    shellColor.VertexColors.Clear()
    for j in range(0,shellEle.Vertices.Count):
        #print( value[j] )
        jetColor = gradientJet(value[j], maxValue, minValue)
        shellColor.VertexColors.Add( jetColor[0],jetColor[1],jetColor[2] )
    modelForce.append( shellColor)
