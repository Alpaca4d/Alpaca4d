import math as mt
import sys


filename = sys.argv[1]
print(filename)
#filename = r"C:\Users\FORMAT\Desktop\Alpaca_rev02\assembleData\openSeesModel.txt"
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


numEigenvalues = int(sys.argv[2])
#print(numEigenvalues)
#numEigenvalues = 6



oNodes = openSeesNode
gT = GeomTransf
oElement = openSeesBeam
oSupport = openSeesSupport
oNodeLoad = openSeesNodeLoad
oMass = openSeesNodalMass          #TO DOUBLE CHECK
oBeamLoad = openSeesBeamLoad

import openseespy.opensees as ops


ops.wipe()

# MODEL
# ------------------------------

# Create ModelBuilder (with three-dimensions and 6 DOF/node):

ops.model('BasicBuilder', '-ndm', 3, '-ndf', 6)
#model('basic', '-ndm', ndm, '-ndf', ndf=ndm*(ndm+1)/2)

##INPUT VARIABLE IS NODES CORDINATES OF STRUCTUR IN GRASSHOPER ##

## CREATE NODES IN OPENSEES ##

for i in range(0,len(oNodes)):
    nodeTag = oNodes[i][0] + 1
    ops.node( nodeTag, oNodes[i][1], oNodes[i][2], oNodes[i][3] ) 


## CREATE ELEMENT IN OPENSEES ##

# Define geometric transformation:
for i in range(0, len(gT)):
    tag = gT[i][0]
    vec = gT[i][1]
    ops.geomTransf('Linear', tag , *vec) 


elementProperties = []

for n in range(0, len(oElement)):

    eleTag = oElement[n][1] + 1
    eleType = oElement[n][0]
    indexStart = oElement[n][2][0] + 1
    indexEnd = oElement[n][2][1] + 1
    eleNodes = [ indexStart, indexEnd]
    
    A = oElement[n][3]
    E = oElement[n][4]
    G = oElement[n][5]
    Jxx = oElement[n][6] 
    Iy = oElement[n][7] 
    Iz = oElement[n][8]
    Avz = oElement[n][11]
    Avy = oElement[n][12]
    geomTag = int(oElement[n][9])
    massDens = 0
    #massDens = oElement[n][10]
    orientVector = oElement[n][13]
    sectionGeomProperties = oElement[n][14]     # it is a list with [shape, base, height]
    
    elementProperties.append([ eleType, E, G, A, Avz, Avy, Jxx, Iy, Iz, orientVector, sectionGeomProperties ])

    if eleType is 'Truss' :

        ops.element( eleType , eleTag , indexStart, indexEnd, float(A), float(E), 1)
    
    elif eleType is 'ElasticTimoshenkoBeam' :

        ops.element( eleType , eleTag , indexStart, indexEnd, E, G, A, Jxx, Iy, Iz, Avy, Avz, geomTag)
        #ops.element( eleType , eleTag , indexStart, indexEnd, E, G, A, Jxx, Iy, Iz, Avy, Avz, geomTag , '-mass', massDens, '-lMass')


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
#print(2*mt.asin(1))
#print(mt.pi)

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