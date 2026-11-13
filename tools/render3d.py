"""Petit moteur de rendu logiciel (numpy) : OBJ Kenney -> sprite isométrique 2:1 calé sur la grille de Mon Monde.
Projection : P(u,v,h) = ((u-v)*A, (u+v)*A/2 - h*VZ)  avec A = 32*R px par unité de case, VZ = 39.19*R (caméra 30°).
Sortie à R=2 (écran haute densité), suréchantillonnage SS puis réduction.
"""
import numpy as np, os, json, sys
from PIL import Image

def load_obj(path, recolor=None):
    base = os.path.dirname(path)
    V, VT, faces = [], [], []
    mats, cur = {}, None
    tex = None
    for l in open(path):
        p = l.split()
        if not p: continue
        if p[0] == 'mtllib':
            mp = os.path.join(base, ' '.join(p[1:]))
            m = None
            for ml in open(mp):
                q = ml.split()
                if not q: continue
                if q[0] == 'newmtl': m = q[1]; mats[m] = {'kd': (1, 1, 1)}
                elif q[0] == 'Kd': mats[m]['kd'] = tuple(map(float, q[1:4]))
                elif q[0] == 'map_Kd': mats[m]['map'] = os.path.join(base, ' '.join(q[1:]))
        elif p[0] == 'usemtl': cur = p[1]
        elif p[0] == 'v': V.append(list(map(float, p[1:4])))
        elif p[0] == 'vt': VT.append(list(map(float, p[1:3])))
        elif p[0] == 'f':
            idx = [q.split('/') for q in p[1:]]
            vi = [int(a[0]) - 1 for a in idx]
            ti = [int(a[1]) - 1 if len(a) > 1 and a[1] else -1 for a in idx]
            for k in range(1, len(vi) - 1):
                faces.append((vi[0], vi[k], vi[k + 1], ti[0], ti[k], ti[k + 1], cur))
    texcache = {}
    cols = []
    for f in faces:
        m = mats.get(f[6], {'kd': (1, 1, 1)})
        c = np.array(m['kd'])
        if 'map' in m and f[3] >= 0:
            if m['map'] not in texcache: texcache[m['map']] = np.asarray(Image.open(m['map']).convert('RGB')).astype(float) / 255
            t = texcache[m['map']]
            uv = np.mean([VT[f[3]], VT[f[4]], VT[f[5]]], axis=0)
            x = int(np.clip(uv[0] % 1.0001, 0, 1) * (t.shape[1] - 1)); y = int(np.clip(1 - (uv[1] % 1.0001), 0, 1) * (t.shape[0] - 1))
            c = c * t[y, x]
        if recolor and f[6] in recolor: c = np.array(recolor[f[6]])
        cols.append(c)
    return np.array(V), faces, np.array(cols), list(mats.keys())

def render(path, out_png, origin='corner', rot=0, R=2, SS=3, recolor=None, scale=1.0):
    V, faces, cols, _ = load_obj(path, recolor)
    V = V * scale
    # (x,y,z) Kenney -> (u,v,h) : centré en largeur, dos collé au fond de la case si le modèle part de z=0
    x, z = V[:, 0], V[:, 2]
    xs = x.max() - x.min(); zs = z.max() - z.min()
    fw = max(1, int(np.ceil(xs - 0.03))); fh = max(1, int(np.ceil(zs - 0.03)))
    U = x - x.min() + (fw - xs) / 2
    Vv = (z - z.min()) if z.min() >= -0.02 and origin == 'corner' else (z - z.min() + (fh - zs) / 2)
    H = V[:, 1]
    for _ in range(rot % 4):
        U, Vv = Vv, fw - U
        fw, fh = fh, fw
    A = 32 * R * SS; VZ = 39.19 * R * SS
    X = (U - Vv) * A; Y = (U + Vv) * A / 2 - H * VZ
    D = 0.612 * (U + Vv) + 0.5 * H                              # plus grand = plus proche
    # cadre : on inclut l'emprise au sol complète
    gx = np.array([0, fw * A, (fw - fh) * A, -fh * A]); gy = np.array([0, fw * A / 2, (fw + fh) * A / 2, fh * A / 2])
    x0 = int(np.floor(min(X.min(), gx.min()))) - 2 * SS; x1 = int(np.ceil(max(X.max(), gx.max()))) + 2 * SS
    y0 = int(np.floor(min(Y.min(), gy.min()))) - 2 * SS; y1 = int(np.ceil(max(Y.max(), gy.max()))) + 2 * SS
    W, Hh = x1 - x0, y1 - y0
    img = np.zeros((Hh, W, 4)); zb = np.full((Hh, W), -1e9)
    L = np.array([0.3, 0.55, 1.0]); L /= np.linalg.norm(L)
    P3 = np.stack([U, Vv, H], 1)
    for i, f in enumerate(faces):
        a, b, c = f[0], f[1], f[2]
        n = np.cross(np.stack([V[b, 0] - V[a, 0], V[b, 1] - V[a, 1], V[b, 2] - V[a, 2]]), np.stack([V[c, 0] - V[a, 0], V[c, 1] - V[a, 1], V[c, 2] - V[a, 2]]))
        nn = np.linalg.norm(n)
        if nn < 1e-12: continue
        n = n / nn
        # normale dans (u,v,h) puis rotation
        nu, nv, nh = n[0], n[2], n[1]
        for _ in range(rot % 4): nu, nv = nv, -nu
        sh = 0.6 + 0.4 * max(0.0, nu * L[0] + nv * L[1] + nh * L[2])
        col = np.clip(cols[i] * sh, 0, 1)
        xs = np.array([X[a], X[b], X[c]]) - x0; ys = np.array([Y[a], Y[b], Y[c]]) - y0; ds = np.array([D[a], D[b], D[c]])
        bx0, bx1 = int(max(0, np.floor(xs.min()))), int(min(W - 1, np.ceil(xs.max())))
        by0, by1 = int(max(0, np.floor(ys.min()))), int(min(Hh - 1, np.ceil(ys.max())))
        if bx1 < bx0 or by1 < by0: continue
        px, py = np.meshgrid(np.arange(bx0, bx1 + 1) + .5, np.arange(by0, by1 + 1) + .5)
        den = (ys[1] - ys[2]) * (xs[0] - xs[2]) + (xs[2] - xs[1]) * (ys[0] - ys[2])
        if abs(den) < 1e-9: continue
        w0 = ((ys[1] - ys[2]) * (px - xs[2]) + (xs[2] - xs[1]) * (py - ys[2])) / den
        w1 = ((ys[2] - ys[0]) * (px - xs[2]) + (xs[0] - xs[2]) * (py - ys[2])) / den
        w2 = 1 - w0 - w1
        m = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
        if not m.any(): continue
        z = w0 * ds[0] + w1 * ds[1] + w2 * ds[2]
        sub = zb[by0:by1 + 1, bx0:bx1 + 1]
        upd = m & (z > sub)
        sub[upd] = z[upd]
        im = img[by0:by1 + 1, bx0:bx1 + 1]
        im[upd, :3] = col; im[upd, 3] = 1
    pil = Image.fromarray((img * 255).astype(np.uint8), 'RGBA')
    pil = pil.resize((max(1, W // SS), max(1, Hh // SS)), Image.LANCZOS)
    pil.save(out_png)
    # ancre = position (dans l'image finale) du coin haut de l'emprise (u=0,v=0,h=0)
    return {'ax': round(-x0 / SS, 1), 'ay': round(-y0 / SS, 1), 'fw': fw, 'fh': fh, 'w': pil.width, 'h': pil.height}

if __name__ == '__main__':
    print(render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'corner', int(sys.argv[4]) if len(sys.argv) > 4 else 0))
