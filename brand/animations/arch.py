"""Китобхонаи Азим — simple reveal of the arch logo (1080x1080, ~3.5 s)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from f2kit import U, L, G, W, GOLDS, LGREENS
import cairosvg
from concurrent.futures import ProcessPoolExecutor

FPS, DUR = 30, 3.6
ARCH = "M10 98V46C10 26 27 10 50 2C73 10 90 26 90 46V98Z"
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def seg(t, a, b): return clamp((t - a) / (b - a))
def e_out(x): return 1 - (1 - x) ** 3
def e_back(x, s=1.4): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2

def frame(t, size=1080):
    a = e_out(seg(t, 0.0, 0.7))                       # arch rises from its base
    sp = e_out(seg(t, 0.45, 1.05))                    # spine slides up
    m = [f'<g opacity="{sp:.3f}" transform="translate(0 {(1 - sp) * 14:.2f})">'
         f'<rect x="19" y="11" width="18" height="78" rx="3.5" fill="{W}"/>'
         f'<rect x="22.5" y="18" width="11" height="2.4" rx="1.2" fill="{G}"/><rect x="22.5" y="22.4" width="11" height="1.4" rx=".7" fill="{G}"/>'
         f'<rect x="22.5" y="80.6" width="11" height="2.4" rx="1.2" fill="{G}"/><rect x="22.5" y="76.6" width="11" height="1.4" rx=".7" fill="{G}"/></g>']
    for k, (fan, cols, sgn) in enumerate(((U, GOLDS, -1), (L, LGREENS, 1))):
        for i in range(3):
            st = 0.95 + i * .14 + k * .07
            x = seg(t, st, st + .6)
            if x <= 0: continue
            o = e_back(x); ang = sgn * (1 - o) * 40; sc = .3 + .7 * o
            m.append(f'<g opacity="{clamp(x * 3):.3f}" transform="translate(41 50) rotate({ang:.2f}) scale({sc:.4f}) translate(-41 -50)">'
                     f'<path d="{fan[i]}" fill="{cols[i]}" stroke="{G}" stroke-width="1.3" stroke-linejoin="round"/></g>')
    s_ = size * .74 / 96; ox = oy = size / 2 - 50 * s_
    pop = 1 + .02 * clamp(1 - abs(t - 1.95) / .25)    # a tiny settle once the К is complete
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
            f'<rect width="{size}" height="{size}" fill="{W}"/>'
            f'<g transform="translate({ox:.2f},{oy:.2f}) scale({s_:.4f}) translate(50 98) scale({pop:.4f}) translate(-50 -98)">'
            f'<g opacity="{clamp(a * 1.5):.3f}" transform="translate(50 98) scale({.9 + .1 * a:.4f} {a:.4f}) translate(-50 -98)"><path d="{ARCH}" fill="{G}"/></g>'
            f'<g transform="translate(17 26) scale(.66)">{"".join(m)}</g></g></svg>')

def render(a):
    i, out = a
    cairosvg.svg2png(bytestring=frame(i / FPS).encode(), write_to=f"{out}/f{i:04d}.png", output_width=1080, output_height=1080)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with ProcessPoolExecutor(2) as ex: list(ex.map(render, [(i, out) for i in range(int(DUR * FPS))], chunksize=8))
