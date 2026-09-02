"""Same cantilever as beam, shell and brick. Material and section lines come verbatim
from Alpaca.Core (alpaca_lines.txt, written by MassUnits.exe); only the node and element
topology - which carries no units - is generated here."""
import math, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
L, B, H = 6.0, 0.4, 0.1
E, NU, RHO_KG = 2.1e8, 0.0, 7850.0

A = {}
for line in open(os.path.join(HERE, "alpaca_lines.txt")):
    k, _, v = line.strip().partition(" ")
    A[k] = v
ISO, RECT, PLATE, BEAMMASS = A["iso"], A["rect"], A["plate"], A["beammass"]
MASSLINE = A["mass"]        # "mass <tag> mx my mz rx ry rz", written by Alpaca.Core for 1000 kg
ISO_TAG   = ISO.split()[2]
RECT_TAG  = RECT.split()[2]
PLATE_TAG = PLATE.split()[2]

def run(name, T, modes=3):
    p = os.path.join(HERE, name + ".tcl")
    open(p, "w").write("\n".join(T) + "\n")
    r = subprocess.run(["OpenSees", p], capture_output=True, text=True, cwd=HERE)
    o = r.stdout + r.stderr
    m = re.search(r"EIGEN (.+)", o)
    if not m:
        print(o[-1500:]); sys.exit(name + ": no eigenvalues")
    return min(math.sqrt(float(x)) / (2 * math.pi)
               for x in m.group(1).split() if float(x) > 1e-9)

def eig(T, modes=3):
    return T + [f"set lambdaN [eigen -genBandArpack {modes}]", 'puts "EIGEN $lambdaN"', "wipe"]

def beam(nx):
    T = ["wipe", "model BasicBuilder -ndm 3 -ndf 6"]
    for i in range(nx + 1): T.append(f"node {i+1} {L*i/nx} 0 0")
    T.append("fix 1 1 1 1 1 1 1")
    T += [RECT, "geomTransf Linear 1 0 0 1"]
    for i in range(nx):
        T.append(f"element forceBeamColumn {i+1} {i+1} {i+2} 1 "
                 f"NewtonCotes {RECT_TAG} 5 -mass {BEAMMASS}")
    return eig(T)

def shell(nx, ny):
    T = ["wipe", "model BasicBuilder -ndm 3 -ndf 6"]
    nid = {}; k = 0
    for i in range(nx + 1):
        for j in range(ny + 1):
            k += 1; nid[(i, j)] = k
            T.append(f"node {k} {L*i/nx} {B*j/ny - B/2} 0")
    for j in range(ny + 1): T.append(f"fix {nid[(0,j)]} 1 1 1 1 1 1")
    T += [ISO, PLATE]
    e = 0
    for i in range(nx):
        for j in range(ny):
            e += 1
            T.append(f"element ASDShellQ4 {e} {nid[(i,j)]} {nid[(i+1,j)]} "
                     f"{nid[(i+1,j+1)]} {nid[(i,j+1)]} {PLATE_TAG}")
    return eig(T)

def brick(nx, ny, nz):
    T = ["wipe", "model BasicBuilder -ndm 3 -ndf 3"]
    nid = {}; k = 0
    for i in range(nx + 1):
        for j in range(ny + 1):
            for m in range(nz + 1):
                k += 1; nid[(i, j, m)] = k
                T.append(f"node {k} {L*i/nx} {B*j/ny - B/2} {H*m/nz - H/2}")
    for j in range(ny + 1):
        for m in range(nz + 1): T.append(f"fix {nid[(0,j,m)]} 1 1 1")
    T.append(ISO)
    e = 0
    for i in range(nx):
        for j in range(ny):
            for m in range(nz):
                e += 1
                n = [nid[(i,j,m)], nid[(i+1,j,m)], nid[(i+1,j+1,m)], nid[(i,j+1,m)],
                     nid[(i,j,m+1)], nid[(i+1,j,m+1)], nid[(i+1,j+1,m+1)], nid[(i,j+1,m+1)]]
                T.append(f"element SSPbrick {e} {' '.join(map(str,n))} {ISO_TAG} 0 0 0")
    return eig(T)

I = B * H**3 / 12.0
mbar = (RHO_KG / 1000.0) * B * H
f_an = (1.875104**2) / (2*math.pi) * math.sqrt(E*I / (mbar * L**4))

fails = 0
def report(what, f, ref, tol):
    global fails
    err = 100*(f/ref - 1); ok = abs(err) <= tol
    if not ok: fails += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {what:<32} f1 = {f:8.4f} Hz   {err:+7.2f} %   (tol {tol:.1f} %)")

print("Same cantilever, three element families")
print(f"  L={L} m, b={B} m, h={H} m, E={E:.3g} kN/m2, nu={NU}, rho={RHO_KG} kg/m3")
print(f"  material and section lines taken verbatim from Alpaca.Core:")
print(f"      {ISO}")
print(f"      {PLATE}")
print(f"      {RECT}")
print(f"      beam -mass {BEAMMASS}")
print(f"\n  analytical f1 = {f_an:.4f} Hz\n")

fb = run("xe_beam",  beam(24))
fs = run("xe_shell", shell(48, 4))
fk = run("xe_brick", brick(48, 4, 4))

print("  vs closed form")
report("beam   ForceBeamColumn x24", fb, f_an, 1.0)
report("shell  ASDShellQ4 48x4",     fs, f_an, 1.0)
report("brick  SSPbrick 48x4x4",     fk, f_an, 2.0)
print("\n  vs each other")
report("shell vs beam", fs, fb, 1.0)
report("brick vs beam", fk, fb, 2.0)
report("brick vs shell", fk, fs, 2.0)

# ---------------------------------------------------------------------------
# Concentrated mass: a massless cantilever carrying 1000 kg at the tip, which is an
# exact SDOF.  k = 3EI/L^3, and the mass value is the one Alpaca.Core wrote.
IZZ = float(RECT.split()[5])
M_T = float(MASSLINE.split()[2])            # 1000 kg, as Alpaca4d converts it
k_sdof = 3 * E * IZZ / L**3
f_sdof = math.sqrt(k_sdof / M_T) / (2 * math.pi)

def sdof(nx=12):
    T = ["wipe", "model BasicBuilder -ndm 3 -ndf 6"]
    for i in range(nx + 1): T.append(f"node {i+1} {L*i/nx} 0 0")
    T.append("fix 1 1 1 1 1 1 1")
    T += [RECT, "geomTransf Linear 1 0 0 1"]
    for i in range(nx):
        T.append(f"element forceBeamColumn {i+1} {i+1} {i+2} 1 NewtonCotes {RECT_TAG} 5 -mass 0")
    T.append(" ".join(["mass", str(nx + 1)] + MASSLINE.split()[2:]))
    return eig(T)

print("\n  concentrated mass (massless cantilever + 1000 kg at the tip)")
print(f"         Alpaca4d wrote:  {MASSLINE}")
print(f"         k = 3EI/L^3 = {k_sdof:.4f} kN/m, m = {M_T} -> f1 = {f_sdof:.4f} Hz")
report("point mass SDOF", run("xe_sdof", sdof()), f_sdof, 1.0)

# What this is guarding against: rho written raw in kg/m3, as it was before the fix.
# Only the nD path is affected, so beam stays right and the other two fall away from it.
print("\n  what the fix repaired (rho written raw, in kg/m3)")
BAD = " ".join(ISO.split()[:-1] + [str(RHO_KG)])
_iso = ISO
globals()["ISO"] = BAD
fs_bad = run("xe_shell_bad", shell(48, 4))
fk_bad = run("xe_brick_bad", brick(48, 4, 4))
globals()["ISO"] = _iso
print(f"         shell would read {fs_bad:8.4f} Hz  ({fs_bad/f_an:.4f} x the closed form)")
print(f"         brick would read {fk_bad:8.4f} Hz  ({fk_bad/f_an:.4f} x the closed form)")
print(f"         beam is unaffected - it never used the nD material")
print(f"         factor = {fs/fs_bad:.4f}, sqrt(1000) = {math.sqrt(1000):.4f}")

print("\nALL PASS" if fails == 0 else f"\n{fails} FAILED")
sys.exit(1 if fails else 0)
