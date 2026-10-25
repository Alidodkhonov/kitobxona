import math,io,os
from brandkit import text_path,F,TAG,NAME
G="#1F4D3A";G7="#2E6B4F";A="#C9A24A";W="#FAF8F3";INK="#12201A";SAGE="#E7EFE9";F15="#0F1A15";GOLDTXT="#8F6B22"
GOLDS=[A,"#D9B862","#EBD49A"];GREENS=[G,G7,"#4F8A6B"];LGREENS=[W,"#CFE0D6","#9CC5AD"]
U=["M41 50C49 33 62 20 85 10C82 30 67 44 41 50Z","M41 50C48 37 59 27 77 22C74 37 63 46 41 50Z","M41 50C47 41 55 34 68 32C65 42 57 48 41 50Z"]
L=["M41 50C49 67 62 80 85 90C82 70 67 56 41 50Z","M41 50C48 63 59 73 77 78C74 63 63 54 41 50Z","M41 50C47 59 55 66 68 68C65 58 57 52 41 50Z"]
def stem(fg,band,bands=True):
    s=f'<rect x="19" y="11" width="18" height="78" rx="3.5" fill="{fg}"/>'
    if bands: s+=(f'<rect x="23" y="17" width="10" height="2.4" rx="1.2" fill="{band}"/><rect x="23" y="21.6" width="10" height="1.4" rx=".7" fill="{band}"/>'
                 f'<rect x="23" y="80.6" width="10" height="2.4" rx="1.2" fill="{band}"/><rect x="23" y="77" width="10" height="1.4" rx=".7" fill="{band}"/>')
    return s
# scheme: "light" (on white), "dark" (on green/dark), "mono" (one colour), layers 3 or 2 (small sizes)
def mark(scheme="light",layers=3,mono=None,sep=None,bands=True):
    if scheme=="light": st,band,gu,gl,sp=G,W,GOLDS,GREENS,W
    elif scheme=="dark": st,band,gu,gl,sp=W,G,GOLDS,LGREENS,G
    elif scheme=="night": st,band,gu,gl,sp=A,F15,[W,"#E9E4D8","#CFC7B4"],[A,"#B28E3E","#8F7231"],F15
    elif scheme=="gold": st,band,gu,gl,sp=G,A,[W,"#F1ECDF","#E3D9C2"],GREENS,A
    if mono: st=mono;gu=[mono]*3;gl=[mono]*3
    if sep: sp=sep;band=sep
    s=stem(st,band,bands)
    idx=[0,1,2] if layers==3 else [0,2]
    for i in idx: s+=f'<path d="{U[i]}" fill="{gu[i]}" stroke="{sp}" stroke-width="{1.3 if layers==3 else 2.6}" stroke-linejoin="round"/>'
    for i in idx: s+=f'<path d="{L[i]}" fill="{gl[i]}" stroke="{sp}" stroke-width="{1.3 if layers==3 else 2.6}" stroke-linejoin="round"/>'
    return s
def svg(w,h,body,bg=None,rx=0):
    b=f'<rect width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{body}</svg>'
def g(body,x,y,s):return f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.4f})">{body}</g>'
def horizontal(scheme="light",lang="ru",tag=True,word=None,tagc=None,bg=None,mono=None,size=60):
    word=word or (G if scheme=="light" else W);tagc=tagc or (A if scheme!="light" else A)
    if mono: word=tagc=mono
    n,wn=text_path("disp",NAME[lang],size,112,70 if tag else 76)
    body=g(mark(scheme,mono=mono,sep=bg if (mono and bg) else None),0,4,1.08)+f'<path d="{n}" fill="{word}"/>'
    w=wn
    if tag:
        t,wt=text_path("ui5",TAG[lang],12.5,114,98,track=2.0);body+=f'<path d="{t}" fill="{tagc}"/>';w=max(wn,wt)
    return svg(int(w+128),118,body,bg)
def stacked(scheme="light",lang="ru",word=None,tagc=None,bg=None,mono=None):
    word=word or (G if scheme=="light" else W);tagc=tagc or A
    if mono: word=tagc=mono
    n,wn=text_path("disp",NAME[lang],52,0,0);t,wt=text_path("ui5",TAG[lang],11.5,0,0,track=2.0);Wd=int(max(wn,wt)+60);cx=Wd/2
    n,_=text_path("disp",NAME[lang],52,cx,196,anchor="middle");t,_=text_path("ui5",TAG[lang],11.5,cx,226,track=2.0,anchor="middle")
    return svg(Wd,246,g(mark(scheme,mono=mono,sep=bg if (mono and bg) else None),cx-62,8,1.24)+f'<path d="{n}" fill="{word}"/><path d="{t}" fill="{tagc}"/>',bg)
def icon(scheme="dark",bg=G,size=100,pad=.74,layers=3,rx=22):
    o=(100-100*pad)/2
    return svg(100,100,g(mark(scheme,layers),o,o,pad),bg,rx).replace('width="100" height="100"',f'width="{size}" height="{size}"',1)
def circle_text(text,size,r,cx,cy,span_center=0,bottom=False,fk="ui",track=0,fill=W):
    f=F[fk];gs=f.getGlyphSet();cmap=f.getBestCmap();upm=f["head"].unitsPerEm;sc=size/upm;hm=f["hmtx"]
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    adv=[hm[cmap.get(ord(c),".notdef")][0]*sc+track for c in text];total=sum(adv)-track
    ang_total=total/r;cur=-ang_total/2;out=[]
    for c,a in zip(text,adv):
        gname=cmap.get(ord(c),".notdef");w=hm[gname][0]*sc;mid=cur+(w/2)/r
        if bottom:
            x=cx+r*math.sin(mid);y=cy+r*math.cos(mid);rot=-math.degrees(mid)
        else:
            x=cx+r*math.sin(mid);y=cy-r*math.cos(mid);rot=math.degrees(mid)
        pen=SVGPathPen(gs);ca,sa=math.cos(math.radians(rot)),math.sin(math.radians(rot))
        # glyph local: translate(-w/2,0), flip y, scale, rotate, translate(x,y)
        a_=sc*ca;b_=sc*sa;c_=-sc*-sa;d_=-sc*ca
        # matrix for point (gx,gy): local=(gx*sc - w/2, -gy*sc); world = R*local + (x,y)
        tx=x+ca*(-w/2);ty=y+sa*(-w/2)
        tp=TransformPen(pen,(sc*ca,sc*sa,sc*sa,-sc*ca,tx,ty)) if False else TransformPen(pen,(sc*ca,sc*sa,-(-sc*sa),-sc*ca,tx,ty))
        gs[gname].draw(tp);out.append(pen.getCommands());cur+=a/r
    return f'<path d="{" ".join(out)}" fill="{fill}"/>'
