import Rhino.Geometry as rg
#---------------------------------------------------------------------------------------#

diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]

pointWrapper = []
transWrapper = []
rotWrapper = []

diplacementWrapper = openSeesOutputWrapper[0]
EleOut = openSeesOutputWrapper[2]
nodeValue = []
displacementValue = []
#ShellOut = openSeesOutputWrapper[4]

pointWrapper = []
dispWrapper = []

for index,item in enumerate(diplacementWrapper):
    nodeValue.append( item[0] )
    displacementValue.append( item[1] )
    pointWrapper.append( [index, rg.Point3d(item[0][0],item[0][1],item[0][2]) ] )
    if len(item[1]) == 3:
        dispWrapper.append( [index, rg.Point3d( item[1][0], item[1][1], item[1][2] ) ] )
    elif len(item[1]) == 6:
        dispWrapper.append( [index, [rg.Point3d(item[1][0],item[1][1],item[1][2] ), rg.Point3d(item[1][3],item[1][4],item[1][5]) ] ] )

## Dict. for point ##
pointWrapperDict = dict( pointWrapper )
pointDispWrapperDict = dict( dispWrapper )
####

def DefSolidValue( ele, node, nodeDisp ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    #print( eleNodeTag )
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    index5 = eleNodeTag[4]
    index6 = eleNodeTag[5]
    index7 = eleNodeTag[6]
    index8 = eleNodeTag[7]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")
    trasl2 = nodeDisp.get( index2 -1 , "never")
    trasl3 = nodeDisp.get( index3 -1 , "never")
    trasl4 = nodeDisp.get( index4 -1 , "never")
    trasl5 = nodeDisp.get( index5 -1 , "never")
    trasl6 = nodeDisp.get( index6 -1 , "never")
    trasl7 = nodeDisp.get( index7 -1 , "never")
    trasl8 = nodeDisp.get( index8 -1 , "never")

    return  [trasl1, trasl2, trasl3,trasl4, trasl5, trasl6, trasl7, trasl8 ]

def DefTetraSolidValue( ele, node, nodeDisp ):
    
    eleTag = ele[0]
    eleNodeTag = ele[1]
    color = ele[2][1]
    #print( eleNodeTag )
    index1 = eleNodeTag[0]
    index2 = eleNodeTag[1]
    index3 = eleNodeTag[2]
    index4 = eleNodeTag[3]
    
    trasl1 = nodeDisp.get( index1 -1 , "never")
    trasl2 = nodeDisp.get( index2 -1 , "never")
    trasl3 = nodeDisp.get( index3 -1 , "never")
    trasl4 = nodeDisp.get( index4 -1 , "never")
    return  [trasl1, trasl2, trasl3, trasl4]

trans = []
tag = []
for ele in EleOut :
    tagEle = ele[0]
    eleType = ele[2][0]
    nNode = len( ele[1] )
    if nNode == 8:
        trasl = DefSolidValue( ele, pointWrapperDict, pointDispWrapperDict )
        trans.append(trasl)
        tag.append( tagEle )
    elif eleType == 'FourNodeTetrahedron' :
        trasl  = DefTetraSolidValue( ele, pointWrapperDict, pointDispWrapperDict )
        trans.append(trasl)
        tag.append( tagEle )
        
tagElement = tag
Trans = trans