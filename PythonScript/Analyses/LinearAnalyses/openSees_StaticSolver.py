import sys
import openseespy.opensees as ops


filename = sys.argv[1]
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
#oMass = openSeesNodalMass          NOT NECESSARY FOR STATIC ANALYSES
oBeamLoad = openSeesBeamLoad
MatTag = openSeesMatTag
openSeesShell = openSeesShell
openSeesSecTag = openSeesSecTag




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
    print('ops.node( {0}, {1}, {2}, {3})'.format( nodeTag, oNodes[i][1], oNodes[i][2], oNodes[i][3] ) )

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
    print('ops.fix( {0}, {1}, {2}, {3}, {4}, {5}, {6})'.format( indexSupport, oSupport[i][1], oSupport[i][2], oSupport[i][3], oSupport[i][4], oSupport[i][5], oSupport[i][6]) )
    ops.fix( indexSupport, oSupport[i][1], oSupport[i][2], oSupport[i][3], oSupport[i][4], oSupport[i][5], oSupport[i][6] )

## LOAD ##

# create TimeSeries
ops.timeSeries('Constant', 1)

# create a plain load pattern
ops.pattern('Plain', 1, 1)

## assemble load ##
for i in range(0, len(oNodeLoad)):

    nodetag = oNodeLoad[i][0] + 1
    Force = oNodeLoad[i][1]
    ops.load( nodetag, *Force )
    print( f'ops.load( {nodetag}, *{Force} )')

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



ops.recorder('Element','-file','shellElementRecorder.out','-closeOnWrite','-ele', 1,'stresses')

# ------------------------------
# Start of analysis generation
# ------------------------------

# create SOE
ops.system("BandSPD")

ops.numberer('Plain')

# create constraint handler

#ops.constraints("Plain")
ops.constraints("Transformation") # to allow Diaphgram constrain

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
    oNodeDisp = ops.nodeDisp( nodeTag ) # spostamenti e rotazioni del nodo 
    nodeDisplacementWrapper.append([oNode, oNodeDisp])

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
	if numberOfNodes >= 3:
		disp = []
		for nodeIndex in ops.eleNodes(elementTag):
			disp.append(ops.nodeDisp(nodeIndex))

		shellOutputWrapper.append([ elementTag, ops.eleNodes(elementTag), disp])
	elif numberOfNodes == 2:
		disp = []
		for nodeIndex in ops.eleNodes(elementTag):
			disp.append(ops.nodeDisp(nodeIndex))
		elementOutputWrapper.append([ elementTag, ops.eleNodes(elementTag), disp[0], disp[1], elementPropertiesDict.setdefault(elementTag) ]) # need to find a new way to add elementProperties



openSeesOutputWrapper = ([nodeDisplacementWrapper,
                        reactionWrapper,
                        elementOutputWrapper,
                        elementLoad,
                        shellOutputWrapper])


length = len(filename)-len(inputName)
filefolder = filename[0:length]
outputFileName = filefolder+'openSeesOutputWrapper.txt'

with open(outputFileName, 'w') as f:
    for item in openSeesOutputWrapper:
        f.write("%s\n" % item)
