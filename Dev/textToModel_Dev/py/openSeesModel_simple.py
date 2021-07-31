import openseespy.opensees as ops
ops.node(1, 0.0, 0.0, 0.0)
ops.node(2, 5 ,    0.0, 0.0)
ops.node(3, 10,    0.0, 0.0)



ops.node(4, 0.0, 5, 0.0)
ops.node(5, 5 ,   5, 0.0)
ops.node(6, 10,    10, 0.0)


ops.element('forceBeamColumn', 1, 1, 2, ColTransfTag, ColIntTag1, '-mass', 0.0)
ops.element('forceBeamColumn', 2, 2, 3, ColTransfTag, ColIntTag1, '-mass', 0.0)

ops.element("forceBeamColumn", 3, 4, 5, ColTransfTag, ColIntTag1, "-mass", 0.0)
ops.element("forceBeamColumn", 4, 5, 6, ColTransfTag, ColIntTag1, "-mass", 0.0)