import math as mt
import sys
import openseespy.opensees as ops

filename = sys.argv[1]
numEigenvalues = int(sys.argv[2])
inputName = filename.split("\\")[-1]

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



oNodes = openSeesNode
gT = GeomTransf
openSeesBeam = openSeesBeam
oSupport = openSeesSupport
oNodeLoad = openSeesNodeLoad
oMass = openSeesNodalMass         
oBeamLoad = openSeesBeamLoad
MatTag = openSeesMatTag
openSeesShell = openSeesShell
openSeesSecTag = openSeesSecTag


ops.wipe()

# MODEL
# ------------------------------

#model('basic', '-ndm', ndm, '-ndf', ndf=ndm*(ndm+1)/2)
ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)


##INPUT VARIABLE IS NODES CORDINATES OF STRUCTUR IN GRASSHOPER ##

## CREATE NODES IN OPENSEES ##

for i in range(0,len(oNodes)):
    nodeTag = oNodes[i][0] + 1
    ops.node( nodeTag, oNodes[i][1], oNodes[i][2], oNodes[i][3] ) 

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
        print( f"ops.section({typeSection}, {secTag}, {E_mod}, {nu}, {h}, {rho})" )


## CREATE ELEMENT IN OPENSEES ##

# Define geometric transformation:
for i in range(0, len(gT)):
    tag = gT[i][0]
    vec = gT[i][1]
    ops.geomTransf('Linear', tag , *vec) 


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

    elementProperties.append([ eleTag, [eleType, E, G, A, Avz, Avy, Jxx, Iy, Iz, orientVector, sectionGeomProperties, matTag] ])


    if eleType is 'Truss':

        ops.element( eleType , eleTag , *[indexStart, indexEnd], float(A), matTag ) # TO CONTROL!!!
        

    elif eleType is 'ElasticTimoshenkoBeam':

        ops.element( eleType , eleTag , indexStart, indexEnd, E, G, A, Jxx, Iy, Iz, Avy, Avz, geomTag , '-mass', massDens,'-lMass')

# transform elementproperties to  Dict to call the object by tag
elementPropertiesDict = dict(elementProperties)


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

    if (eleType == 'ShellDKGQ') or (eleType == 'ShellDKGT'):

        print('ops.element( {0}, {1}, *{2}, {3})'.format(eleType, eleTag, eleNodes, secTag)     )
        ops.element( eleType , eleTag, *eleNodes, secTag)


# SUPPORT #

for i in range(0, len(oSupport)):
    indexSupport = oSupport[i][0] + 1
    ops.fix( indexSupport, oSupport[i][1], oSupport[i][2], oSupport[i][3], oSupport[i][4], oSupport[i][5], oSupport[i][6] )


## LOAD ##

# create TimeSeries
ops.timeSeries('Constant', 1)

# create a plain load pattern
ops.pattern('Plain', 1, 1)


## assemble MASS ##

for i in range(len(oMass)):
    nodeTag = oMass[i][0] + 1
    massValues = oMass[i][1]
    ops.mass(nodeTag, *massValues)


# ------------------------------
# Start of analysis generation
# ------------------------------
# calculate eigenvalues & print results
#solver = '-genBandArpack'
#solver = '-symmBandLapack'
solver = '-fullGenLapack'
eigenValues =  ops.eigen(solver, numEigenvalues)


## PERIOD ##

period = []
frequency = []


for i in range(numEigenvalues):
    lambd = eigenValues[i]
    omega = mt.sqrt(lambd)
    freq = omega / (2*mt.pi)
    period.append( (2*mt.pi) / (omega) )
    frequency.append(freq)

period = period
## SPOSTAMENTI NODALI ##

## we should find a way to plot for all numberModal. In that case we don't
## have to run the analyses to see every Modes

nodeModalDispWrapper = []

for eigenMode in range(1, numEigenvalues + 1):
    nodeModalDispWrapperTemp = []
    for i in range(0,len(ops.getNodeTags())):

        nodeTag = oNodes[i][0] + 1
        
        oNodeModalDisp = ops.nodeEigenvector( nodeTag ,eigenMode) # spostamenti e rotazioni del nodo 

        Node = ops.nodeCoord( nodeTag ) # cordinate nodo
        nodeModalDispWrapperTemp.append( [Node, oNodeModalDisp] )
    nodeModalDispWrapper.append( nodeModalDispWrapperTemp )

####################################################
numberElement = ops.getEleTags()
elementOutputWrapper = []

for eigenMode in range(1, numEigenvalues + 1):

    eleModalOutputTemp = []
    for i in range(len(ops.getEleTags())):
        tagElement = numberElement[i]
        indexStart = ops.eleNodes(tagElement)[0]
        indexEnd = ops.eleNodes(tagElement)[1]
        dispStart = ops.nodeEigenvector( indexStart, eigenMode )
        dispEnd = ops.nodeEigenvector( indexEnd, eigenMode )
        eleModalOutputTemp.append([ tagElement, ops.eleNodes(tagElement), dispStart, dispEnd, elementProperties[i] ])
    elementOutputWrapper.append( eleModalOutputTemp )
#######################################################################

nodeModalDispWrapper = nodeModalDispWrapper
elementOutputWrapper = elementOutputWrapper

openSeesModalOutputWrapper = ([nodeModalDispWrapper,
                               elementOutputWrapper,
                               period,
                               frequency])


length = len(filename)-len(inputName)
filefolder = filename[0:length]
outputFileName = filefolder+'openSeesModalOutputWrapper.txt'

with open(outputFileName, 'w') as f:
    for item in openSeesModalOutputWrapper:
        f.write("%s\n" % item)