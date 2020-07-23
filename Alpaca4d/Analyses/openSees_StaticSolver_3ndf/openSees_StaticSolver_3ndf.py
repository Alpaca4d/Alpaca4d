import sys
import openseespy.opensees as ops
#from openseespy.postprocessing.Get_Rendering import *


#filename = sys.argv[1]
filename = r'C:\GitHub\Alpaca4d\Grasshopper\assembleData\openSeesModel.txt'
#inputName = filename.split("\\")[-1]


with open(filename, 'r') as f:
    lines = f.readlines()
    openSeesNode = eval( lines[0].strip() )
    GeomTransf = eval( lines[1].strip() )
    openSeesBeam = eval( lines[2].strip() )
    openSeesSupport = eval( lines[3].strip() )
    openSeesNodeLoad = eval( lines[4].strip() )
    openSeesNodalMass = eval( lines[5].strip() )
    openSeesBeamLoad = eval( lines[6].strip() )
    openSeesMatTag = eval( lines[7].strip() )
    openSeesShell = eval(lines[8].strip() )
    openSeesSecTag = eval(lines[9].strip() )
    openSeesSolid = eval(lines[10].strip() )



oNodes = openSeesNode
gT = GeomTransf
openSeesBeam = openSeesBeam
oSupport = openSeesSupport
oNodeLoad = openSeesNodeLoad
#oMass = openSeesNodalMass          TO DOUBLE CHECK
oBeamLoad = openSeesBeamLoad
MatTag = openSeesMatTag
openSeesShell = openSeesShell
openSeesSecTag = openSeesSecTag
openSeesSolid = openSeesSolid





ops.wipe()

# MODEL
# ------------------------------

# Create ModelBuilder (with three-dimensions and 6 DOF/node):

ops.model('BasicBuilder', '-ndm', 3, '-ndf', 3)
#model('basic', '-ndm', ndm, '-ndf', ndf=ndm*(ndm+1)/2)

##INPUT VARIABLE IS NODES CORDINATES OF STRUCTUR IN GRASSHOPER ##

## CREATE NODES IN OPENSEES ##


for i in range(0,len(oNodes)):
    nodeTag = oNodes[i][0] + 1
    ops.node( nodeTag, oNodes[i][1], oNodes[i][2], oNodes[i][3] )
    #print('ops.node( {0}, {1}, {2}, {3})'.format( nodeTag, oNodes[i][1], oNodes[i][2], oNodes[i][3] ) )

## CREATE MATERIAL IN OPENSEES ##

#print(MatTag) # to adjust

for item in MatTag:
    materialDimension = item[0].split("_")[1]
    materialType = item[0].split("_")[2]
    matTag = item[1][0]
    E = item[1][1][0]
    if materialDimension == 'uniaxialMaterial':
        ops.uniaxialMaterial(materialType, matTag , E)
    elif materialDimension == 'nDMaterial':
        ops.nDMaterial('ElasticIsotropic', matTag, E, 0.3)


for item in openSeesSecTag:
    typeSection = item[0].split("_")[1]
    secTag = int(item[1][0])
    E_mod = float( item[1][1][1][1] )
    nu = float( item[1][1][1][3] )
    h = float( item[1][1][0] )
    rho = float( item[1][1][1][4] )
    if typeSection == 'ElasticMembranePlateSection':
        ops.section(typeSection, secTag, E_mod, nu, h, rho)
        #print( 'ops.section( {0}, {1}, {2}, {3}, {4}, {5})'.format( typeSection, int(secTag), float(E_mod), float(nu), float(h), float(rho) ) )
        #print( f"ops.section({typeSection}, {secTag}, {E_mod}, {nu}, {h}, {rho})" )
## CREATE ELEMENT IN OPENSEES ##
'''
# Define geometric transformation:
for i in range(0, len(gT)):
    tag = gT[i][0]
    vec = gT[i][1]
    ops.geomTransf('Linear', tag , *vec)
'''

elementProperties = []

for n in range(0, len(openSeesBeam)):

    eleTag = openSeesBeam[n][1] + 1
    eleType = openSeesBeam[n][0]
    indexStart = openSeesBeam[n][2][0] + 1
    indexEnd = openSeesBeam[n][2][1] + 1
    eleNodes = [ indexStart, indexEnd]
    
    A = openSeesBeam[n][3]
    E = openSeesBeam[n][4]
    G = openSeesBeam[n][5]
    Jxx = openSeesBeam[n][6] 
    Iy = openSeesBeam[n][7] 
    Iz = openSeesBeam[n][8]
    Avz = openSeesBeam[n][11]
    Avy = openSeesBeam[n][12]
    geomTag = int(openSeesBeam[n][9])
    massDens = openSeesBeam[n][10]
    orientVector = openSeesBeam[n][13]
    sectionGeomProperties = openSeesBeam[n][14]     # it is a list with [shape, base, height]
    matTag = openSeesBeam[n][15]
    color = openSeesBeam[n][16]
    elementProperties.append([ eleTag, [eleType, E, G, A, Avz, Avy, Jxx, Iy, Iz, orientVector, sectionGeomProperties, matTag, color] ])


    if eleType is 'Truss':

        ops.element( eleType , eleTag , *[indexStart, indexEnd], float(A), matTag ) # TO CONTROL!!!
        

    #elif eleType is 'ElasticTimoshenkoBeam':

        #ops.element( eleType , eleTag , indexStart, indexEnd, E, G, A, Jxx, Iy, Iz, Avy, Avz, geomTag , '-mass', massDens,'-lMass')
'''
for item in openSeesShell:

    eleType = item[0]
    #print('eleType = ' + str(eleType))
    eleTag = item[1] + 1
    #print('eleTag = ' + str(eleTag))
    eleNodes = item[2]
    #print('eleNodes = ' + str(eleNodes))
    secTag = item[3]
    #print('secTag = ' + str(secTag))
    thick = item[4]
    #print('thick = ' + str(thick))
    
    elementProperties.append([ eleTag, [eleType, thick ] ])

    if (eleType == 'ShellDKGQ') or (eleType == 'ShellDKGT'):

        print('ops.element( {0}, {1}, *{2}, {3})'.format(eleType, eleTag, eleNodes, secTag)     )
        ops.element( eleType , eleTag, *eleNodes, secTag)
'''
solidTag = []
for item in openSeesSolid:

    eleType = item[0]
    #print('eleType = ' + str(eleType))
    eleTag = item[1] + 1
    #print('eleTag = ' + str(eleTag))
    eleNodes = item[2]
    #print('eleNodes = ' + str(eleNodes))
    matTag = item[3]
    #print('matTag = ' + str(matTag))
    force = item[4]
    #print( force)
    color = item[5]

    elementProperties.append([ eleTag, [eleType,color] ])

    if (eleType == 'bbarBrick') or (eleType == 'FourNodeTetrahedron'):
        solidTag.append( eleTag )
        #print('ops.element( {0}, {1}, *{2}, {3}, {4})'.format(eleType, eleTag, eleNodes, matTag, force)     )
        ops.element( eleType , eleTag, *eleNodes, matTag, *force)                           
# transform elementproperties to  Dict to call the object by tag
elementPropertiesDict = dict(elementProperties)

# SUPPORT #

for i in range(0, len(oSupport)):
    indexSupport = oSupport[i][0] + 1
    #print('ops.fix( {0}, {1}, {2}, {3})'.format( indexSupport, oSupport[i][1], oSupport[i][2], oSupport[i][3]) )
    ops.fix( indexSupport, oSupport[i][1], oSupport[i][2], oSupport[i][3] )

## LOAD ##
#plot_model()
# create TimeSeries
ops.timeSeries('Constant', 1)

# create a plain load pattern
ops.pattern('Plain', 1, 1)

## assemble load ##
for i in range(0, len(oNodeLoad)):

    nodetag = oNodeLoad[i][0] + 1
    Force = oNodeLoad[i][1]
    #print(Force[0:3])
    ops.load( nodetag, *Force[0:3] )
    #print( f'ops.load( {nodetag}, *{Force[0:3]} )')

elementLoad = []

for item in openSeesBeamLoad:
    eleTags = item[0] + 1
    Wy = item[1][0]
    Wz = item[1][1]
    Wx = item[1][2]
    loadType = item[2]
    #ops.eleLoad('-ele', eleTags,'-type', '-beamUniform', Wy, Wz, Wx) we need to understand why is wrong
    ops.eleLoad('-ele', eleTags,'-type', '-beamUniform', Wz, Wy, Wx)
    elementLoad.append([ eleTags, Wy, Wz, Wx, loadType] )


TensionFilePath = r'C:\GitHub\Alpaca4d\PythonScript\Analyses\openSees_StaticSolver_3ndf\tension.out' 
#TensionFilePath = os.path.join(workingDirectory, "tension.out")
# ho problemi con shellTag
ops.recorder('Element','-file', TensionFilePath ,'-closeOnWrite','-ele',*solidTag,'stresses')
print(ops.getEleTags())
# ------------------------------
# Start of analysis generation
# ------------------------------

# create SOE
# create constraint handler
#ops.constraints("Plain")
#ops.constraints("Transformation") # to allow Diaphgram constrain

ops.system("BandSPD")

ops.numberer('Plain')

# create constraint handler
ops.constraints("Plain") # to allow Diaphgram constrain

# create integrator
ops.integrator("LoadControl",  1.0 )

# create algorithm
ops.algorithm("Newton")

# create analysis object
ops.analysis("Static")

# perform the analysis
ops.analyze(1)
## OUTPUT FILE ##

## DISPLACEMENT
nodeDisplacementWrapper = []

for i in range(1,len(ops.getNodeTags())+1):
    nodeTag = i
    oNode = ops.nodeCoord( nodeTag ) # cordinate nodo
    oNodeDisp = ops.nodeDisp( nodeTag ) # spostamenti del nodo 
    nodeDisplacementWrapper.append([oNode, oNodeDisp])
    
#print( ops.getNodeTags() )
#-----------------------------------------------------

reactionWrapper = []
ops.reactions()
for i in range(0, len(oSupport)):
    indexSupport = oSupport[i][0] + 1
    ghTag = oSupport[i][0]
    reactionWrapper.append([ghTag, ops.nodeReaction(indexSupport)])

reactionWrapper = reactionWrapper


#-----------------------------------------------------
elementOutputWrapper = []
shellOutputWrapper = []



elementTagList = ops.getEleTags()

for elementTag in elementTagList:
	numberOfNodes = len( ops.eleNodes(elementTag) )
	#print( numberOfNodes )
	elementOutputWrapper.append([ elementTag, ops.eleNodes(elementTag), elementPropertiesDict.setdefault(elementTag) ])
 # need to find a new way to add elementProperties


openSeesOutputWrapper = ([nodeDisplacementWrapper,
                        reactionWrapper,
                        elementOutputWrapper,
                        elementLoad])

#length = len(filename)-len(inputName)
#filefolder = filename[0:length]



#outputFileName = filefolder + 'openSeesOutputWrapper.txt'
outputFileName = r'C:\GitHub\Alpaca4d\Grasshopper\assembleData\openSeesOutputWrapper.txt'

with open(outputFileName, 'w') as f:
    for item in openSeesOutputWrapper:
        f.write("%s\n" % item)



