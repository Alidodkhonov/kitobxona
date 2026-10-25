from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
G="#1F4D3A";G2="#2E6B4F";W="#FAF8F3";A="#C9A24A";INK="#12201A";SAGE="#E7EFE9"
import os as _os
_FD=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"fonts")
F={k:TTFont(_os.path.join(_FD,v)) for k,v in {"disp":"Cormorant-700.ttf","disp6":"Cormorant-600.ttf","ui":"Golos-600.ttf","ui5":"Golos-500.ttf"}.items()}
def text_path(fk,text,size,x=0,y=0,track=0,anchor="start"):
    f=F[fk];gs=f.getGlyphSet();cmap=f.getBestCmap();upm=f["head"].unitsPerEm;sc=size/upm
    hmtx=f["hmtx"];width=0;items=[]
    for ch in text:
        g=cmap.get(ord(ch));
        if g is None: g=".notdef"
        items.append((g,width));width+=hmtx[g][0]*sc+track
    width-=track
    if anchor=="middle":x-=width/2
    if anchor=="end":x-=width
    d=[]
    for g,off in items:
        pen=SVGPathPen(gs);tp=TransformPen(pen,(sc,0,0,-sc,x+off,y));gs[g].draw(tp);d.append(pen.getCommands())
    return " ".join(d),width
def mark_g(fg=W,acc=A,snow=None,stroke=6,light=False):
    snow=snow or W
    return (f'<path d="M24 86V47C24 30 36 19 50 11C64 19 76 30 76 47V86" fill="none" stroke="{fg}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round"/>'
      f'<path d="M34 63L50 36L66 63Z" fill="{acc}"/>'
      f'<path d="M43.5 47L50 36L56.5 47L53 45L50 48.5L47 45Z" fill="{snow}"' + (f' stroke="{acc}" stroke-width="1.4" stroke-linejoin="round"' if light else '') + '/>'
      f'<path d="M30.5 67.5C37 63.5 44 63.5 50 67.5V83C44 79 37 79 30.5 83Z" fill="{fg}"/>'
      f'<path d="M69.5 67.5C63 63.5 56 63.5 50 67.5V83C56 79 63 79 69.5 83Z" fill="{fg}"/>')
def svg(w,h,body,bg=None,rx=0):
    b=f'<rect width="{w}" height="{h}" rx="{rx}" fill="{bg}"/>' if bg else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{b}{body}</svg>'
def icon(fg=W,acc=A,bg=G,rx=22,snow=None,light=False):
    return svg(100,100,mark_g(fg,acc,snow,light=light),bg,rx)
def mark_only(fg=G,acc=A,snow=W,light=True):
    return svg(100,100,mark_g(fg,acc,snow,light=light))
TAG={"ru":"ЭЛЕКТРОННАЯ БИБЛИОТЕКА РЕДКИХ КНИГ","tg":"КИТОБХОНАИ ЭЛЕКТРОНИИ КИТОБҲОИ НОДИР","en":"DIGITAL LIBRARY OF RARE BOOKS"}
NAME={"ru":"Китобхонаи Азим","tg":"Китобхонаи Азим","en":"Kitobkhonai Azim"}
def horizontal(lang="ru",fg=G,acc=A,word=None,tagc=None,bg=None,snow=None):
    word=word or fg;tagc=tagc or acc
    n,wn=text_path("disp",NAME[lang],64,128,74)
    t,wt=text_path("ui5",TAG[lang],13.5,130,104,track=2.2)
    W_=int(max(wn,wt)+150)
    body=f'<g transform="translate(6,6) scale(1.12)">{mark_g(fg,acc,snow,light=bg in (None,W,SAGE))}</g><path d="{n}" fill="{word}"/><path d="{t}" fill="{tagc}"/>'
    return svg(W_,124,body,bg)
def stacked(lang="ru",fg=G,acc=A,word=None,tagc=None,bg=None,snow=None):
    word=word or fg;tagc=tagc or acc
    n,wn=text_path("disp",NAME[lang],58,0,0);t,wt=text_path("ui5",TAG[lang],12.5,0,0,track=2.2)
    W_=int(max(wn,wt)+60);cx=W_/2
    n,_=text_path("disp",NAME[lang],58,cx,196,anchor="middle");t,_=text_path("ui5",TAG[lang],12.5,cx,228,track=2.2,anchor="middle")
    body=f'<g transform="translate({cx-60},12) scale(1.2)">{mark_g(fg,acc,snow,light=bg in (None,W,SAGE))}</g><path d="{n}" fill="{word}"/><path d="{t}" fill="{tagc}"/>'
    return svg(W_,250,body,bg)
def wordmark(lang="ru",col=G):
    n,wn=text_path("disp",NAME[lang],64,4,60)
    return svg(int(wn+8),80,f'<path d="{n}" fill="{col}"/>')
