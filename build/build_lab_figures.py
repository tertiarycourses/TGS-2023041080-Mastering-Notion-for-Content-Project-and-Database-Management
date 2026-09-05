#!/usr/bin/env python3
"""Render one workflow figure per lab as a PNG (courseware/assets/figures and the lab folder).

Drawn, not captured: a live-workspace screenshot would carry account names into a
published document and go stale at the next UI change. The drawn figure shows the four
stages of the lab and the artifact produced, in the house palette.
"""
import os, sys, glob
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
REPO=os.path.dirname(HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4
from PIL import Image, ImageDraw, ImageFont

OUT=os.path.join(REPO,"courseware","assets","figures"); os.makedirs(OUT,exist_ok=True)
W,H=1680,560
BLUE=(0x1F,0x6F,0xEB); TEAL=(0x10,0xB9,0x81); VIOLET=(0x7C,0x3A,0xED); AMBER=(0xF5,0x9E,0x0B)
INK=(0x16,0x1B,0x26); GREY=(0x5B,0x63,0x72); LIGHT=(0xF5,0xF8,0xFC); LINE=(0xD8,0xE0,0xEA); WHITE=(255,255,255)

def font(sz,bold=False):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try: return ImageFont.truetype(p,sz)
        except Exception: pass
    return ImageFont.load_default()
F_T=font(34,True); F_S=font(21,True); F_B=font(19); F_C=font(17); F_K=font(18,True)

def wrap(d,text,fnt,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=fnt)<=maxw: cur=t
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
def rrect(d,box,r,fill,outline=None,width=2): d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def arrow(d,x,y,w,color):
    h=7; d.rectangle([x,y-h//2,x+w-14,y+h//2],fill=color); d.polygon([(x+w-14,y-11),(x+w,y),(x+w-14,y+11)],fill=color)

def draw(a,path):
    img=Image.new("RGB",(W,H),WHITE); d=ImageDraw.Draw(img)
    accent=[BLUE,TEAL,VIOLET,AMBER][(a["topic"]-1)%4]
    d.rectangle([0,0,W,10],fill=accent)
    d.text((44,44),f"LAB {a['num']:02d} · WORKFLOW · TOPIC {a['topic']:02d} · {a['km']} · {a['am']}",font=F_K,fill=accent)
    d.text((44,78),wrap(d,a["title"],F_T,W-120)[0],font=F_T,fill=INK)
    d.line([44,140,W-44,140],fill=LINE,width=2)
    labels=["Prepare","Build","Refine","Verify"]; steps=a["flow"]; n=4
    gap=44; x0=44; bw=(W-88-gap*(n-1))//n; y0=190; bh=250
    for i,(lab,txt) in enumerate(zip(labels,steps)):
        x=x0+(bw+gap)*i
        rrect(d,[x,y0,x+bw,y0+bh],16,LIGHT,accent,3); d.rectangle([x,y0,x+bw,y0+9],fill=accent)
        cx=x+bw//2
        d.ellipse([cx-26,y0+34,cx+26,y0+86],fill=accent)
        num=str(i+1); tw=d.textlength(num,font=F_S); d.text((cx-tw/2,y0+47),num,font=F_S,fill=WHITE)
        lw=d.textlength(lab,font=F_S); d.text((cx-lw/2,y0+104),lab,font=F_S,fill=INK)
        for j,l in enumerate(wrap(d,txt,F_C,bw-40)[:3]):
            lw=d.textlength(l,font=F_C); d.text((cx-lw/2,y0+142+j*24),l,font=F_C,fill=GREY)
        if i<n-1: arrow(d,x+bw+8,y0+bh//2,gap-16,accent)
    rrect(d,[44,H-118,W-44,H-34],10,LIGHT,None); d.rectangle([44,H-118,52,H-34],fill=accent)
    d.text((74,H-104),"YOU WILL BUILD",font=F_K,fill=accent)
    for j,l in enumerate(wrap(d,a["build"],F_B,W-160)[:2]): d.text((74,H-76+j*24),l,font=F_B,fill=INK)
    img.save(path,"PNG",optimize=True)

def main():
    made=0
    for a in ACT:
        draw(a,os.path.join(OUT,f"lab-{a['num']:02d}-workflow.png")); made+=1
        g=glob.glob(os.path.join(REPO,"labs",f"lab-{a['num']:02d}-*"))
        if g: draw(a,os.path.join(g[0],f"LAB-{a['num']:02d}-Workflow.png"))
    print(f"rendered {made} workflow figures -> {OUT}")
if __name__=="__main__": main()
