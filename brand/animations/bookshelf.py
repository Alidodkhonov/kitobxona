"""Китобхонаи Азим — logo animation.
Story: a shelf of books -> one green book is pulled out -> it becomes the spine of К ->
its pages fan open as the arms -> the arch (пештоқ) rises behind -> name and tagline appear.
Renders SVG frames with cairosvg; ffmpeg assembles them."""
import sys, os, math, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from f2kit import U, L, G, G7, A, W, INK, SAGE, F15, GOLDTXT, GOLDS, GREENS, LGREENS
from brandkit import text_path, NAME, TAG
import cairosvg
from concurrent.futures import ProcessPoolExecutor

FPS = 30
DUR = 8.8
D = 0.65   # extra time given to the shelf opening
ARCH = "M10 98V46C10 26 27 10 50 2C73 10 90 26 90 46V98Z"

# ---------- easing / helpers ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def seg(t, a, b): return clamp((t - a) / (b - a))
def e_out(x): return 1 - (1 - x) ** 3
def e_inout(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def e_back(x, s=1.5): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2
def lerp(a, b, x): return a + (b - a) * x
def hx(c): c = c.lstrip("#"); return [int(c[i:i + 2], 16) for i in (0, 2, 4)]
def mix(c1, c2, x):
    a, b = hx(c1), hx(c2); return "#%02x%02x%02x" % tuple(round(lerp(a[i], b[i], x)) for i in range(3))

# ---------- the scene ----------
def frame_svg(t, Wd=1920, Ht=1080):
    bg = W
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}">',
           f'<rect width="{Wd}" height="{Ht}" fill="{bg}"/>']
    cx, cy = Wd / 2, Ht / 2

    # Phase timing (T runs D seconds behind t: the shelf gets a longer opening)
    T = t - D
    p_in = seg(t, 0.0, 1.1)       # shelf assembles
    p_pull = seg(T, 1.25, 2.25)   # chosen book pulled out, others leave
    p_fan = seg(T, 2.1, 3.7)      # pages fan open
    p_arch = seg(T, 3.95, 4.9)    # arch rises behind the К
    p_move = seg(T, 3.55, 4.35)   # К settles into its place in the arch
    p_col = seg(T, 4.0, 4.4)      # colours invert as the arch covers the К
    p_lock = seg(T, 5.05, 6.25)   # move into lockup
    p_name = seg(T, 5.55, 6.75)   # name wipes in

    # ---- mark placement (mark units -> pixels) ----
    cam = lerp(.9, 1, e_inout(seg(t, 0, 2.7)))   # slow push-in towards the shelf
    S_big = 5.4 * cam                         # mark scale while it is a book on a shelf
    spine_c = (28, 50)                        # centre of the spine in mark units
    mark_c = (52, 50)                         # centre of the full К
    drift = e_inout(seg(T, 2.1, 3.6))
    mc = (lerp(spine_c[0], mark_c[0], drift), 50)
    # symbol stage: arch box (100 units) at scale SA, mark inside at .66
    SA = 6.0
    # lockup stage: horizontal logo geometry (from the brand's horiz())
    nd, nw = text_path("disp", NAME["ru"], 60, 112, 78)
    LW = nw + 130
    SL = 1120 / LW                            # lockup scale in px per unit
    s_arch_l = 1.12                           # arch scale inside lockup
    lock_ox, lock_oy = cx - LW * SL / 2, cy - 116 * SL / 2
    # arch-box origin in px for symbol stage vs lockup stage
    sym_o = (cx - 50 * SA, cy - 50 * SA)
    lck_o = (lock_ox + (-10 * s_arch_l + 4) * SL, lock_oy + (-2 * s_arch_l + 4) * SL)
    lk = e_inout(p_lock)
    arch_scale = lerp(SA, s_arch_l * SL, lk)
    arch_o = (lerp(sym_o[0], lck_o[0], lk), lerp(sym_o[1], lck_o[1], lk))

    # mark transform: before the arch, free at S_big centred on mc; after, locked into arch
    a = e_inout(p_move)
    free_s = S_big
    free_o = (cx - mc[0] * free_s, cy - mc[1] * free_s)
    in_s = .66 * arch_scale
    in_o = (arch_o[0] + 17 * arch_scale, arch_o[1] + 26 * arch_scale)
    ms = lerp(free_s, in_s, a)
    mo = (lerp(free_o[0], in_o[0], a), lerp(free_o[1], in_o[1], a))

    # ---- the arch (behind the mark) ----
    if p_arch > 0:
        r = e_out(p_arch)
        # grows upward from its base: scaleY about the base line (y=98)
        out.append(f'<g transform="translate({arch_o[0]:.2f},{arch_o[1]:.2f}) scale({arch_scale:.4f})">'
                   f'<g transform="translate(50 98) scale({lerp(.86, 1, r):.4f} {r:.4f}) translate(-50 -98)">'
                   f'<path d="{ARCH}" fill="{G}"/></g></g>')

    # ---- the shelf: a row of books on a gold plank, the chosen one is the spine of К ----
    if p_fan < 1 and p_pull < 1:
        g_o = (cx - spine_c[0] * S_big, cy - 50 * S_big)
        # (width, height, cover, bands, label)  left side listed outward from the chosen book
        left = [(16, 72, G7, A, 1), (13, 80, SAGE, G, 0), (19, 66, A, W, 1), (15, 84, G, A, 0), (12, 70, "#4F8A6B", W, 0)]
        right = [(17, 76, "#4F8A6B", W, 1), (14, 82, "#D9B862", G, 0), (20, 70, G7, A, 1), (13, 78, SAGE, G7, 0)]
        books = []; x = 19
        for i, b in enumerate(left):
            x -= b[0] + 1.3; books.append((x, i + 1, 0) + b)
        x = 37
        for i, b in enumerate(right):
            x += 1.3; books.append((x, i + 1, 0) + b); x += b[0]
        books.append((x + 10.8, 5, -8, 15, 74, G, A, 0))   # the last book leans on its neighbour
        x0 = min(bk[0] for bk in books) - 7; x1 = x + 32
        parts = []
        # plank and its soft shadow, opening from the centre
        pk = e_inout(seg(t, 0.0, 0.9))
        pfade = 1 - e_inout(seg(T, 1.45, 2.2))
        if pk > 0.002 and pfade > 0.002:
            mid = 28; hw = (x1 - x0) / 2 * pk; L0 = mid - hw - (mid - (x0 + x1) / 2) * pk
            parts.append('<defs><linearGradient id="sh" x1="0" y1="0" x2="0" y2="1">'
                         f'<stop offset="0" stop-color="{INK}" stop-opacity=".16"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient></defs>')
            parts.append(f'<g opacity="{min(1, pk * 1.6) * pfade:.3f}"><rect x="{L0:.2f}" y="93.6" width="{2 * hw:.2f}" height="6" fill="url(#sh)"/>'
                         f'<rect x="{L0:.2f}" y="90.2" width="{2 * hw:.2f}" height="3.4" rx=".8" fill="{A}"/>'
                         f'<rect x="{L0:.2f}" y="89" width="{2 * hw:.2f}" height="1.4" rx=".6" fill="#D9B862"/></g>')
        for (bx, d, lean, w, h, col, band, label) in books:
            k = e_out(seg(t, 0.3 + d * .09, 1.15 + d * .09))
            leave = e_inout(seg(T, 1.3 + (5 - d) * .05, 2.05 + (5 - d) * .05))
            side = -1 if bx < 19 else 1
            xx = bx + side * 30 * leave
            y = 89 - h - (1 - k) * 9 + leave * 5
            op = k * (1 - leave)
            if op <= 0.002: continue
            body = (f'<rect x="{xx:.2f}" y="{y:.2f}" width="{w}" height="{h}" rx="2.2" fill="{col}"/>'
                    f'<rect x="{xx:.2f}" y="{y:.2f}" width="1.6" height="{h}" fill="{INK}" opacity=".10"/>'
                    f'<rect x="{xx + 2.6:.2f}" y="{y + 5:.2f}" width="{w - 5.2:.2f}" height="2" rx="1" fill="{band}"/>'
                    f'<rect x="{xx + 2.6:.2f}" y="{y + 8.6:.2f}" width="{w - 5.2:.2f}" height="1" rx=".5" fill="{band}"/>'
                    f'<rect x="{xx + 2.6:.2f}" y="{y + h - 7:.2f}" width="{w - 5.2:.2f}" height="2" rx="1" fill="{band}"/>')
            if label:
                body += f'<rect x="{xx + 3.4:.2f}" y="{y + h * .36:.2f}" width="{w - 6.8:.2f}" height="{h * .2:.2f}" rx="1" fill="{band}" opacity=".9"/>'
            tr = f' transform="rotate({lean} {xx:.2f} 89)"' if lean else ""
            parts.append(f'<g opacity="{op:.3f}"{tr}>{body}</g>')
        out.append(f'<g transform="translate({g_o[0]:.2f},{g_o[1]:.2f}) scale({S_big:.4f})">{"".join(parts)}</g>')

    # ---- the К: spine + fanned pages ----
    k_in = e_out(seg(t, 0.3, 1.15))
    lift = math.sin(math.pi * e_inout(p_pull)) * 9  # the pull: up and back down
    c = e_inout(p_col)
    stem_c = mix(G, W, c); band_c = mix(W, G, c); sep_c = mix(W, G, c)
    golds = GOLDS
    greens = [mix(GREENS[i], LGREENS[i], c) for i in range(3)]
    m = []
    sy = 11 - lift - (1 - k_in) * 9
    m.append(f'<g opacity="{k_in:.3f}"><rect x="19" y="{sy:.2f}" width="18" height="78" rx="3.5" fill="{stem_c}"/>'
             f'<rect x="22.5" y="{sy + 7:.2f}" width="11" height="2.4" rx="1.2" fill="{band_c}"/>'
             f'<rect x="22.5" y="{sy + 11.4:.2f}" width="11" height="1.4" rx=".7" fill="{band_c}"/>'
             f'<rect x="22.5" y="{sy + 69.6:.2f}" width="11" height="2.4" rx="1.2" fill="{band_c}"/>'
             f'<rect x="22.5" y="{sy + 65.6:.2f}" width="11" height="1.4" rx=".7" fill="{band_c}"/></g>')
    if p_fan > 0:
        # pages lift off the spine one after another; upper fan (gold) turns up, lower (green) settles down
        for fan, cols, sgn in ((U, golds, -1), (L, greens, 1)):
            for i in range(3):
                st = 2.1 + i * .16 + (0 if sgn < 0 else .08)
                x = seg(T, st, st + .95)
                if x <= 0: continue
                ex = e_back(x, 1.35)
                ang = sgn * -1 * (1 - ex) * 52     # closed: lying along the spine
                sc = lerp(.12, 1, e_out(x))
                op = clamp(x * 3)
                m.append(f'<g opacity="{op:.3f}" transform="translate(41 50) rotate({ang:.2f}) scale({sc:.4f}) translate(-41 -50)">'
                         f'<path d="{fan[i]}" fill="{cols[i]}" stroke="{sep_c}" stroke-width="1.3" stroke-linejoin="round"/></g>')
    out.append(f'<g transform="translate({mo[0]:.2f},{mo[1]:.2f}) scale({ms:.4f})">{"".join(m)}</g>')

    # ---- name + tagline (lockup coordinates) ----
    if p_name > 0:
        nx = e_out(p_name)
        clipw = (nw + 24) * nx
        out.append(f'<defs><clipPath id="cn"><rect x="108" y="0" width="{clipw:.2f}" height="116"/></clipPath></defs>')
        out.append(f'<g transform="translate({lock_ox:.2f},{lock_oy:.2f}) scale({SL:.4f})">'
                   f'<g clip-path="url(#cn)"><g transform="translate({(1 - nx) * -10:.2f} 0)" opacity="{clamp(p_name * 2.5):.3f}">'
                   f'<path d="{nd}" fill="{G}"/></g></g></g>')
    out.append('</svg>')
    return "".join(out)


def render(args):
    i, outdir, Wd, Ht = args
    t = i / FPS
    cairosvg.svg2png(bytestring=frame_svg(t, Wd, Ht).encode(), write_to=f"{outdir}/f{i:04d}.png",
                     output_width=Wd, output_height=Ht)
    return i


if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "frames"
    Wd, Ht = 1920, 1080
    os.makedirs(outdir, exist_ok=True)
    only = [float(x) for x in sys.argv[2:]]
    if only:
        for tt in only:
            cairosvg.svg2png(bytestring=frame_svg(tt, Wd, Ht).encode(), write_to=f"{outdir}/t{tt:.2f}.png",
                             output_width=Wd // 2, output_height=Ht // 2)
        sys.exit()
    n = int(DUR * FPS)
    with ProcessPoolExecutor(2) as ex:
        list(ex.map(render, [(i, outdir, Wd, Ht) for i in range(n)], chunksize=8))
    print("frames", n)
