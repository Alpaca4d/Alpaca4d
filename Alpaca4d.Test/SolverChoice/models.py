#!/usr/bin/env python3
"""Generate OpenSees decks shaped like the models Alpaca4d actually builds:
a multi-storey 3D frame, a shell slab, and a solid block."""
import sys

E, NU, RHO = 2.1e8, 0.3, 7.85          # kN/m2, -, t/m3  (Alpaca4d's kN-m system)
G = E / (2 * (1 + NU))

def header(ndf):
    return ["wipe", "model basic -ndm 3 -ndf %d" % ndf]

def frame(nx, ny, nz, bay=6.0, storey=3.5):
    """3D moment frame: columns and beams on an nx by ny grid, nz storeys."""
    L = header(6)
    nid, node_at = 1, {}
    for k in range(nz + 1):
        for j in range(ny + 1):
            for i in range(nx + 1):
                L.append("node %d %g %g %g" % (nid, i * bay, j * bay, k * storey))
                node_at[(i, j, k)] = nid
                if k == 0:
                    L.append("fix %d 1 1 1 1 1 1" % nid)
                nid += 1
    L.append("geomTransf Linear 1 0 1 0")
    L.append("geomTransf Linear 2 0 0 1")
    # Column 0.4x0.4, beam 0.3x0.6
    ca, ci = 0.16, 0.16 * 0.16 / 12
    ba, bi = 0.18, 0.3 * 0.6**3 / 12
    e = 1
    for k in range(nz):                                   # columns
        for j in range(ny + 1):
            for i in range(nx + 1):
                L.append("element elasticBeamColumn %d %d %d %g %g %g %g %g %g 1 -mass %g"
                         % (e, node_at[(i, j, k)], node_at[(i, j, k + 1)], ca, E, G,
                            2 * ci, ci, ci, RHO * ca)); e += 1
    for k in range(1, nz + 1):                            # beams
        for j in range(ny + 1):
            for i in range(nx):
                L.append("element elasticBeamColumn %d %d %d %g %g %g %g %g %g 2 -mass %g"
                         % (e, node_at[(i, j, k)], node_at[(i + 1, j, k)], ba, E, G,
                            2 * bi, bi, bi, RHO * ba)); e += 1
        for j in range(ny):
            for i in range(nx + 1):
                L.append("element elasticBeamColumn %d %d %d %g %g %g %g %g %g 2 -mass %g"
                         % (e, node_at[(i, j, k)], node_at[(i, j + 1, k)], ba, E, G,
                            2 * bi, bi, bi, RHO * ba)); e += 1
    L.append("timeSeries Linear 1")
    L.append("pattern Plain 1 1 {")
    for k in range(1, nz + 1):
        for j in range(ny + 1):
            for i in range(nx + 1):
                L.append("  load %d 5.0 0.0 -50.0 0.0 0.0 0.0" % node_at[(i, j, k)])
    L.append("}")
    return L, node_at[(nx, ny, nz)], (nx + 1) * (ny + 1) * nz * 6

def shell(n, size=10.0):
    """Square slab, n by n quads, clamped all round."""
    L = header(6)
    L.append("nDMaterial ElasticIsotropic 1 %g %g %g" % (E, NU, RHO))
    L.append("section PlateFiber 1 1 0.2")
    nid, node_at = 1, {}
    for j in range(n + 1):
        for i in range(n + 1):
            L.append("node %d %g %g 0.0" % (nid, i * size / n, j * size / n))
            node_at[(i, j)] = nid
            if i in (0, n) or j in (0, n):
                L.append("fix %d 1 1 1 1 1 1" % nid)
            nid += 1
    e = 1
    for j in range(n):
        for i in range(n):
            L.append("element ASDShellQ4 %d %d %d %d %d 1" % (e, node_at[(i, j)],
                     node_at[(i + 1, j)], node_at[(i + 1, j + 1)], node_at[(i, j + 1)])); e += 1
    L.append("timeSeries Linear 1")
    L.append("pattern Plain 1 1 {")
    for j in range(1, n):
        for i in range(1, n):
            L.append("  load %d 0.0 0.0 -5.0 0.0 0.0 0.0" % node_at[(i, j)])
    L.append("}")
    return L, node_at[(n // 2, n // 2)], (n - 1) * (n - 1) * 6

def brick(n, size=4.0):
    """Solid block of n^3 SSP bricks, fixed on its base."""
    L = header(3)
    L.append("nDMaterial ElasticIsotropic 1 %g %g %g" % (E, NU, RHO))
    nid, node_at = 1, {}
    for k in range(n + 1):
        for j in range(n + 1):
            for i in range(n + 1):
                L.append("node %d %g %g %g" % (nid, i * size / n, j * size / n, k * size / n))
                node_at[(i, j, k)] = nid
                if k == 0:
                    L.append("fix %d 1 1 1" % nid)
                nid += 1
    e = 1
    for k in range(n):
        for j in range(n):
            for i in range(n):
                L.append("element SSPbrick %d %d %d %d %d %d %d %d %d 1" % (e,
                    node_at[(i, j, k)], node_at[(i+1, j, k)], node_at[(i+1, j+1, k)], node_at[(i, j+1, k)],
                    node_at[(i, j, k+1)], node_at[(i+1, j, k+1)], node_at[(i+1, j+1, k+1)], node_at[(i, j+1, k+1)]))
                e += 1
    L.append("timeSeries Linear 1")
    L.append("pattern Plain 1 1 {")
    for j in range(n + 1):
        for i in range(n + 1):
            L.append("  load %d 2.0 0.0 -2.0" % node_at[(i, j, n)])
    L.append("}")
    return L, node_at[(n, n, n)], (n + 1) * (n + 1) * n * 3

if __name__ == "__main__":
    kind, arg = sys.argv[1], int(sys.argv[2])
    lines, probe, dofs = {"frame": lambda a: frame(a, a, a),
                          "shell": shell, "brick": brick}[kind](arg)
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stderr.write("%d\n" % probe)
