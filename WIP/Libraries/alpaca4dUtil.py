import Rhino.Geometry as rg
import ghpythonlib.components as ghcomp

def removeDuplicates(points, tol):
    uniquePoints = ghcomp.Kangaroo2Component.removeDuplicatePts(points, tol)
    return uniquePoints


def RTreeSeach(RTree, searchPoint, tol):

    #closestPoints = []
    closestIndices = []

    #event handler of type RTreeEventArgs
    def SearchCallback(sender, e):
        #closestPoints.Add(pointList[e.Id])
        closestIndices.Add(e.Id)

    for item in searchPoint:
        RTree.Search(rg.Sphere(item, tol), SearchCallback)
        ind = closestIndices
    
    return ind
