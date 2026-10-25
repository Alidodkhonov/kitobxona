import sys,os,io,math,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from f2kit import *
import cairosvg
from PIL import Image
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"full-kit")
def save(rel,s,pngw=None,pngs=()):
    p=os.path.join(OUT,rel);os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p+".svg","w").write(s)
    if pngw: cairosvg.svg2png(bytestring=s.encode(),write_to=p+".png",output_width=pngw)
    for w in pngs: cairosvg.svg2png(bytestring=s.encode(),write_to=f"{p}-{w}.png",output_width=w)
# 1 MAIN LOGO
save("01-main-logo/logo-primary",horizontal("light"),1200)
save("01-main-logo/logo-primary-on-green",horizontal("dark",bg=G),1200)
save("01-main-logo/logo-primary-transparent-white",horizontal("dark"),1200)
save("01-main-logo/logo-stacked",stacked("light"),900)
save("01-main-logo/logo-stacked-on-green",stacked("dark",bg=G),900)
save("01-main-logo/logo-tajik",horizontal("light","tg"),1200)
save("01-main-logo/logo-latin",horizontal("light","en"),1200)
save("01-main-logo/symbol",svg(100,100,mark("light")),None,(512,1024))
save("01-main-logo/symbol-white",svg(100,100,mark("dark")),None,(512,))
# 2 BADGE / SEAL
def badge(ring=G,inner=W,txt=W,mk="light",dot=A):
    s=f'<circle cx="150" cy="150" r="148" fill="{ring}"/><circle cx="150" cy="150" r="102" fill="{inner}"/>'
    s+=f'<circle cx="150" cy="150" r="140" fill="none" stroke="{dot}" stroke-width="1.5"/><circle cx="150" cy="150" r="108" fill="none" stroke="{dot}" stroke-width="1.5"/>'
    s+=circle_text("КИТОБХОНАИ АЗИМ",17,117,150,150,fk="ui",track=3.2,fill=txt)
    s+=circle_text("ЭЛЕКТРОННАЯ БИБЛИОТЕКА",13,129,150,150,bottom=True,fk="ui5",track=2.4,fill=txt)
    for a in (-90,90):
        x=150+124*math.cos(math.radians(a+90-90));pass
    for a in (math.radians(97),math.radians(-97)):
        s+=f'<circle cx="{150+124*math.sin(a):.1f}" cy="{150-124*math.cos(a)*-0+0:.1f}" r="0" fill="{dot}"/>'
    s+=f'<circle cx="{150-123:.1f}" cy="152" r="3.2" fill="{dot}"/><circle cx="{150+123:.1f}" cy="152" r="3.2" fill="{dot}"/>'
    s+=g(mark(mk),94,94,1.12)
    return svg(300,300,s)
save("02-badge/badge-round",badge(),900)
save("02-badge/badge-round-gold",badge(ring=A,inner=W,txt=G,dot=G),900)
save("02-badge/badge-round-mono",badge(ring=G,inner=W,txt=W,mk="light",dot=W).replace(A,G).replace("#D9B862","#3E7A5C").replace("#EBD49A","#6E9E85"),900)
def arch(ground=G,scheme="dark"):
    return svg(100,110,f'<path d="M8 106V46C8 26 26 11 50 2C74 11 92 26 92 46V106Z" fill="{ground}"/>'+g(mark(scheme),17,30,.66))
save("02-badge/badge-arch",arch(),600)
save("02-badge/badge-arch-light",arch(SAGE,"light"),600)
# 3 ON THE BOOKS
def exlibris():
    w,h=360,500
    s=f'<rect width="{w}" height="{h}" fill="{W}"/><rect x="14" y="14" width="{w-28}" height="{h-28}" fill="none" stroke="{G}" stroke-width="3"/>'
    s+=f'<rect x="22" y="22" width="{w-44}" height="{h-44}" fill="none" stroke="{A}" stroke-width="1.2"/>'
    s+=f'<path d="M80 330V180C80 132 120 100 180 76C240 100 280 132 280 180V330Z" fill="none" stroke="{G}" stroke-width="2.4"/>'
    s+=g(mark("light"),118,132,1.24)
    t,_=text_path("ui",'EX LIBRIS',14,w/2,58,track=6,anchor="middle");s+=f'<path d="{t}" fill="{GOLDTXT}"/>'
    n,_=text_path("disp","Китобхонаи Азим",36,w/2,378,anchor="middle");s+=f'<path d="{n}" fill="{G}"/>'
    t2,_=text_path("ui5","ЭЛЕКТРОННАЯ БИБЛИОТЕКА РЕДКИХ КНИГ",9.5,w/2,402,track=1.8,anchor="middle");s+=f'<path d="{t2}" fill="{GOLDTXT}"/>'
    n2,_=text_path("ui5","№",14,70,448);s+=f'<path d="{n2}" fill="{G}"/><path d="M92 448H290" stroke="{G}" stroke-width="1.2"/>'
    return svg(w,h,s)
save("03-on-books/bookplate-ex-libris",exlibris(),1080)
def pdfstamp(dark=False):
    bg=G if dark else W;sc="dark" if dark else "light";tx=W if dark else G
    n,wn=text_path("disp","Китобхонаи Азим",30,64,34);u,wu=text_path("ui5","kitobxona.vercel.app",11,66,52,track=.6)
    w=int(max(wn,wu)+84)
    return svg(w,64,f'<rect width="{w}" height="64" rx="10" fill="{bg}" stroke="{G}" stroke-width="{0 if dark else 1.4}"/>'+g(mark(sc),8,6,.52)+f'<path d="{n}" fill="{tx}"/><path d="{u}" fill="{A if dark else GOLDTXT}"/>')
save("03-on-books/pdf-cover-stamp",pdfstamp(),1000)
save("03-on-books/pdf-cover-stamp-green",pdfstamp(True),1000)
save("03-on-books/page-watermark",svg(100,100,f'<g opacity=".14">{mark("light",mono=G)}</g>'),None,(400,))
def spine():
    n,wn=text_path("disp","Китобхонаи Азим",26,0,0)
    s=f'<rect width="70" height="{int(wn+150)}" fill="{G}"/>'+g(mark("dark",layers=2),11,16,.48)
    n,_=text_path("disp","Китобхонаи Азим",26,0,0)
    s+=f'<g transform="translate(44,90) rotate(90)"><path d="{n}" fill="{W}"/></g>'
    return svg(70,int(wn+150),s)
save("03-on-books/book-spine",spine(),280)
# 4 WEBSITE
def header(dark=False,centered=True):
    sc="dark" if dark else "light";tx=W if dark else G
    n,wn=text_path("disp","Китобхонаи Азим",40,62,40)
    return svg(int(wn+68),56,g(mark(sc),0,2,.52)+f'<path d="{n}" fill="{tx}"/>')
save("04-website/header-logo",header(),800)
save("04-website/header-logo-white",header(True),800)
for sz in (16,32,48):
    save(f"04-website/favicon-{sz}",icon(size=sz,layers=2,pad=.8,rx=20),sz)
save("04-website/favicon",icon(layers=2,pad=.8,rx=20))
save("04-website/og-share-image",svg(1200,630,f'<rect width="1200" height="630" fill="{G}"/>'+g(stacked_body:="",0,0,1)+""),None)
# OG image: stacked centred on green
st=stacked("dark");stw=float(st.split('width="')[1].split('"')[0])
og=svg(1200,630,f'<rect width="1200" height="630" fill="{G}"/><g transform="translate({600-stw*1.6/2:.1f},118) scale(1.6)">'+st.split('>',1)[1].rsplit('</svg>',1)[0]+'</g>')
save("04-website/og-share-image",og,1200)
# 5 MOBILE APP
save("05-mobile-app/app-icon-ios-1024",icon(size=1024,rx=0,pad=.7),1024)
save("05-mobile-app/app-icon-rounded",icon(size=512,pad=.72),512)
save("05-mobile-app/pwa-icon-192",icon(size=192,pad=.74),192)
save("05-mobile-app/pwa-icon-512",icon(size=512,pad=.74),512)
save("05-mobile-app/pwa-maskable-512",icon(size=512,rx=0,pad=.56),512)
save("05-mobile-app/android-foreground-432",svg(100,100,g(mark("dark"),25,25,.5)).replace('width="100" height="100"','width="432" height="432"',1),432)
save("05-mobile-app/app-icon-light",icon("light",bg=W,size=512,pad=.72),512)
sp=stacked("dark");spw=float(sp.split('width="')[1].split('"')[0])
splash=svg(1242,2688,f'<rect width="1242" height="2688" fill="{G}"/><g transform="translate({621-spw*3.1/2:.1f},960) scale(3.1)">'+sp.split('>',1)[1].rsplit('</svg>',1)[0]+'</g>')
save("05-mobile-app/splash-screen",splash,1242)
# 6 SOCIAL
save("06-social/avatar",svg(400,400,f'<circle cx="200" cy="200" r="200" fill="{G}"/>'+g(mark("dark"),88,88,2.24)),400)
hz=horizontal("dark");hw=float(hz.split('width="')[1].split('"')[0])
cover=svg(1500,500,f'<rect width="1500" height="500" fill="{G}"/><g transform="translate({750-hw*1.7/2:.1f},150) scale(1.7)">'+hz.split('>',1)[1].rsplit('</svg>',1)[0]+'</g>')
save("06-social/cover-banner",cover,1500)
# 7 ONE COLOUR
save("07-one-colour/logo-green",horizontal("light",mono=G,bg=None),1200)
save("07-one-colour/logo-white-on-dark",horizontal("light",mono=W,bg=INK),1200)
save("07-one-colour/logo-gold-foil",horizontal("light",mono=A,bg=G),1200)
save("07-one-colour/symbol-night",svg(100,100,mark("night"),F15),None,(512,))
save("07-one-colour/symbol-on-gold",svg(100,100,g(mark("gold"),10,10,.8),A),None,(512,))
print("built")
