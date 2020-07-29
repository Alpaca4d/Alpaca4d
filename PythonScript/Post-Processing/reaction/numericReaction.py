"""Generate Model view 
    Inputs:
        AlpacaStaticOutput: Output of solver on static Analyses.
        reactionForcesView : if Boolean Toggle is 'True' view reaction Forces, if ' False ' you don't see .
        reactionMomentsView : if Boolean Toggle is 'True' view reaction Moments, if ' False ' you don't see .
        scale: number that multiplies the reaction.
    Output:
       tagPoints :  nodes tag of Model .
       ReactionForce : Vector of reaction Forces { Rx, Ry, Rz }.
       ReactionMoment : Vector of reaction Moments { Mx, My, Mz }.
       view : element for forces view .
       """

import Rhino.Geometry as rg
import math
import ghpythonlib.treehelpers as th # per data tree
import Grasshopper as gh
import sys



#---------------------------------------------------------------------------------------#
def reaction(AlpacaStaticOutput):

    # define output

    global tagPoints
    global ReactionForce
    global ReactionMoment
   
    scale = 1


    diplacementWrapper = AlpacaStaticOutput[0]
    reactionOut = AlpacaStaticOutput[1]
    #print( len( reactionOut ) )

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
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

if checkData != False :
    tagPoints, ReactionForce, ReactionMoments = reaction( AlpacaStaticOutput )