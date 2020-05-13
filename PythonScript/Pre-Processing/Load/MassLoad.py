import Rhino.Geometry as rg

def pointLoad(Pos, NodalMassTranslation):

    NodalMassTranslation = rg.Point3d(NodalMassTranslation, NodalMassTranslation, NodalMassTranslation)
    return [[Pos, NodalMassTranslation]]

Mass = pointLoad(Pos, NodalMassTranslation)