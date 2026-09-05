#!/usr/bin/env python3
"""Visual component library for the course deck — all-white Tertiary house style.

Ported from the wsq-slides reference engine (tile_grid, flow_h, trainer_slide, cards3,
two_col, big_statement, section, brk) and the COMPACT v2 reference (img_points,
img_full, browser-mock LMS slide), extended with the components the courseware-build
skill mandates: process_map (real connectors), compare_table, chart_slide (native
charts), decision_map and stat_row. Every teaching slide uses one of these — never a
bare bullet wall. Transitions (fade for content, push for section dividers) are
applied once at save time.
"""
import math, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.oxml.ns import qn
from lxml import etree

# ---------------- palette ----------------
BLUE=RGBColor(0x1F,0x6F,0xEB); TEAL=RGBColor(0x10,0xB9,0x81); AMBER=RGBColor(0xF5,0x9E,0x0B)
INK=RGBColor(0x16,0x1B,0x26);  GREY=RGBColor(0x5B,0x63,0x72); LIGHT=RGBColor(0xF5,0xF8,0xFC)
WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE2,0xE8,0xF0); VIOLET=RGBColor(0x7C,0x3A,0xED)
RED=RGBColor(0xDC,0x26,0x26); GREEN=RGBColor(0x12,0x7A,0x3E); NAVY=RGBColor(0x0B,0x12,0x20)
PALETTE=[BLUE,TEAL,VIOLET,AMBER]

class Deck:
    def __init__(self, course, assets_dir):
        self.C=course; self.ASSETS=assets_dir
        self.prs=Presentation()
        self.prs.slide_width=Inches(13.333); self.prs.slide_height=Inches(7.5)
        self.SW=self.prs.slide_width; self.SH=self.prs.slide_height
        self.BLANK=self.prs.slide_layouts[6]
        self.page=0
        self.section_idx=set()      # slide indices that get the "push" transition
        self.slide_map={}           # key -> page number (for the Lesson Plan)

    # ---------- primitives ----------
    def mark(self,key): self.slide_map[key]=self.page+1
    def slide(self): return self.prs.slides.add_slide(self.BLANK)
    def rect(self,s,x,y,w,h,color,line=None):
        sp=s.shapes.add_shape(1,int(x),int(y),int(w),int(h)); sp.fill.solid()
        sp.fill.fore_color.rgb=color
        if line is None: sp.line.fill.background()
        else: sp.line.color.rgb=line; sp.line.width=Pt(1)
        sp.shadow.inherit=False; return sp
    def round_rect(self,s,x,y,w,h,color,line=None):
        sp=s.shapes.add_shape(5,int(x),int(y),int(w),int(h)); sp.fill.solid()
        sp.fill.fore_color.rgb=color
        if line is None: sp.line.fill.background()
        else: sp.line.color.rgb=line; sp.line.width=Pt(1)
        sp.shadow.inherit=False; return sp
    def oval(self,s,x,y,w,h,color):
        sp=s.shapes.add_shape(9,int(x),int(y),int(w),int(h)); sp.fill.solid()
        sp.fill.fore_color.rgb=color; sp.line.fill.background(); sp.shadow.inherit=False; return sp
    def diamond(self,s,x,y,w,h,color):
        sp=s.shapes.add_shape(4,int(x),int(y),int(w),int(h)); sp.fill.solid()
        sp.fill.fore_color.rgb=color; sp.line.fill.background(); sp.shadow.inherit=False; return sp
    def arrow(self,s,x,y,w,h,color):
        """Flat right-pointing arrow: shaft rectangle + freeform triangular head."""
        x,y,w,h=int(x),int(y),int(w),int(h)
        headw=min(int(w*0.6),Inches(0.20)); shaftw=max(w-headw,1)
        shafth=max(int(h*0.30),Emu(19050))
        sp=s.shapes.add_shape(1,x,int(y+h/2-shafth/2),shaftw,shafth)
        sp.fill.solid(); sp.fill.fore_color.rgb=color
        sp.line.fill.background(); sp.shadow.inherit=False
        hx=x+shaftw; cy=int(y+h/2); hh=max(int(h*0.62),Emu(38100))
        b=s.shapes.build_freeform(hx,int(cy-hh/2))
        b.add_line_segments([(hx+headw,cy),(hx,int(cy+hh/2))],close=True)
        tri=b.convert_to_shape()
        tri.fill.solid(); tri.fill.fore_color.rgb=color
        tri.line.fill.background(); tri.shadow.inherit=False
        return sp
    def txt(self,s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4,link=None):
        tb=s.shapes.add_textbox(int(x),int(y),int(w),int(h)); tf=tb.text_frame
        tf.word_wrap=True; tf.vertical_anchor=anchor
        for i,l in enumerate(runs):
            p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
            p.alignment=align; p.space_after=Pt(space)
            for t,sz,col,bold in l:
                r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold
                r.font.color.rgb=col; r.font.name="Arial"
                if link and t.startswith("http"): r.hyperlink.address=link
        return tb
    def bullets(self,s,x,y,w,h,items,size=18,color=INK,gap=10):
        tb=s.shapes.add_textbox(int(x),int(y),int(w),int(h)); tf=tb.text_frame; tf.word_wrap=True
        for i,it in enumerate(items):
            p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(gap)
            lvl=it[1] if isinstance(it,tuple) else 0
            text=it[0] if isinstance(it,tuple) else it
            bold=(isinstance(it,tuple) and len(it)>2 and it[2])
            r=p.add_run(); r.text=("•  " if lvl==0 else "–  ")+text
            r.font.size=Pt(size if lvl==0 else size-2); r.font.bold=bold
            r.font.color.rgb=color if lvl==0 else GREY; r.font.name="Arial"
        return tb
    def footer(self,s):
        self.page+=1; C=self.C
        self.txt(s,Inches(0.4),Inches(7.05),Inches(7.5),Inches(0.35),
                 [[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",9,GREY,False)]])
        self.txt(s,Inches(5.0),Inches(7.05),Inches(3.3),Inches(0.35),
                 [[("© 2026 Tertiary Infotech Academy Pte Ltd",9,GREY,False)]],align=PP_ALIGN.CENTER)
        self.txt(s,Inches(12.4),Inches(7.05),Inches(0.6),Inches(0.35),
                 [[(str(self.page),9,GREY,False)]],align=PP_ALIGN.RIGHT)
    def head(self,s,title,kicker=None,kcolor=BLUE):
        self.rect(s,0,0,self.SW,self.SH,WHITE); self.rect(s,0,0,Inches(0.28),Inches(1.55),kcolor)
        if kicker: self.txt(s,Inches(0.85),Inches(0.5),Inches(11.6),Inches(0.4),[[(kicker,14,kcolor,True)]])
        sz=29 if len(title)<=46 else (25 if len(title)<=58 else (20 if len(title)<=84 else 18))
        self.txt(s,Inches(0.85),Inches(0.9),Inches(11.9),Inches(0.9),[[(title,sz,INK,True)]])
        self.rect(s,Inches(0.85),Inches(1.7),Inches(11.63),Inches(0.02),LINE); return s
    def _asset(self,name):
        for p in (os.path.join(self.ASSETS,name), os.path.join(self.ASSETS,"notion",name),
                  os.path.join(self.ASSETS,"notion",name+".jpg"), os.path.join(self.ASSETS,"figures",name)):
            if os.path.exists(p): return p
        return None
    def _picture(self,s,path,x,y,maxw,maxh):
        """Aspect-fit a picture inside (x,y,maxw,maxh) with a thin border card."""
        from PIL import Image
        iw,ih=Image.open(path).size
        w=int(maxw); h=int(w*ih/iw)
        if h>maxh: h=int(maxh); w=int(h*iw/ih)
        px=int(x+(maxw-w)/2); py=int(y+(maxh-h)/2)
        self.rect(s,px-Emu(19050),py-Emu(19050),w+Emu(38100),h+Emu(38100),WHITE,line=LINE)
        s.shapes.add_picture(path,px,py,width=w,height=h)
        return w,h

    # ---------- templates ----------
    def cover(self,badge_top,badge_bot):
        C=self.C; s=self.slide(); self.rect(s,0,0,self.SW,self.SH,WHITE)
        self.rect(s,0,0,self.SW,Inches(0.22),BLUE); self.rect(s,0,Inches(7.28),self.SW,Inches(0.22),TEAL)
        lg=self._asset("tertiary-infotech-logo.png")
        if lg: s.shapes.add_picture(lg,Inches(0.85),Inches(0.7),height=Inches(1.05))
        self.rect(s,Inches(10.55),Inches(0.72),Inches(2.0),Inches(1.0),INK)
        self.txt(s,Inches(10.55),Inches(0.82),Inches(2.0),Inches(0.5),[[(badge_top,19,WHITE,True)]],align=PP_ALIGN.CENTER)
        self.txt(s,Inches(10.55),Inches(1.28),Inches(2.0),Inches(0.4),[[(badge_bot,8,WHITE,True)]],align=PP_ALIGN.CENTER)
        self.txt(s,Inches(0.9),Inches(2.25),Inches(12),Inches(0.6),[[("COURSE SLIDES  ·  WSQ",16,BLUE,True)]])
        self.txt(s,Inches(0.9),Inches(2.75),Inches(11.6),Inches(2.0),[[(C.TITLE,37,INK,True)]])
        self.rect(s,Inches(0.92),Inches(4.85),Inches(2.4),Inches(0.06),TEAL)
        self.txt(s,Inches(0.9),Inches(5.15),Inches(12),Inches(1.4),
                 [[(f"WSQ Course Code: {C.COURSE_CODE}  ·  {C.DAYS}-Day Hands-On Training ({C.TRAINING_HOURS} h training + {C.ASSESSMENT_HOURS} h assessment)",16,GREY,False)],
                  [(f"Skills Framework TSC: {C.TSC_TITLE} ({C.TSC_CODE})",14,GREY,False)],
                  [(f"Conducted by {C.ORG}  ·  {C.UEN.replace('UEN: ','UEN ')}",14,GREY,False)]],space=6)
        self.txt(s,Inches(0.9),Inches(6.5),Inches(12),Inches(0.4),
                 [[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",12,GREY,False)]])
        self.txt(s,Inches(0.9),Inches(6.85),Inches(12),Inches(0.34),
                 [[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])
        self.page+=1
        return s
    def section(self,kicker,title,n,sub=""):
        s=self.slide(); self.rect(s,0,0,self.SW,self.SH,WHITE); self.rect(s,0,0,Inches(0.28),self.SH,BLUE)
        self.rect(s,Inches(0.85),Inches(2.5),Inches(0.14),Inches(2.0),TEAL)
        self.txt(s,Inches(1.25),Inches(2.55),Inches(11),Inches(0.6),[[(kicker,18,BLUE,True)]])
        self.txt(s,Inches(1.25),Inches(3.0),Inches(10.6),Inches(1.6),[[(title,36,INK,True)]])
        if sub: self.txt(s,Inches(1.27),Inches(4.75),Inches(10.6),Inches(1.3),[[(sub,14,GREY,False)]])
        self.txt(s,Inches(10.0),Inches(0.7),Inches(2.8),Inches(1.6),[[(n,72,LINE,True)]],align=PP_ALIGN.RIGHT)
        self.footer(s); self.section_idx.add(len(self.prs.slides)-1); return s
    def content(self,title,items,kicker=None,size=19):
        s=self.head(self.slide(),title,kicker)
        self.bullets(s,Inches(0.85),Inches(1.95),Inches(11.6),Inches(4.9),items,size=size)
        self.footer(s); return s
    def two_col(self,title,left,right,kicker=None,lhead="",rhead="",size=15,note=None):
        s=self.head(self.slide(),title,kicker)
        bh=Inches(4.7) if not note else Inches(4.15)
        self.rect(s,Inches(0.85),Inches(1.95),Inches(5.7),bh,LIGHT)
        self.rect(s,Inches(6.95),Inches(1.95),Inches(5.55),bh,LIGHT)
        self.rect(s,Inches(0.85),Inches(1.95),Inches(5.7),Inches(0.1),BLUE)
        self.rect(s,Inches(6.95),Inches(1.95),Inches(5.55),Inches(0.1),TEAL)
        if lhead: self.txt(s,Inches(1.1),Inches(2.2),Inches(5.2),Inches(0.4),[[(lhead,16,BLUE,True)]])
        if rhead: self.txt(s,Inches(7.2),Inches(2.2),Inches(5.0),Inches(0.4),[[(rhead,16,TEAL,True)]])
        self.bullets(s,Inches(1.1),Inches(2.75),Inches(5.2),bh-Inches(0.95),left,size=size,gap=7)
        self.bullets(s,Inches(7.2),Inches(2.75),Inches(5.05),bh-Inches(0.95),right,size=size,gap=7)
        if note:
            self.rect(s,Inches(0.85),Inches(6.22),Inches(11.65),Inches(0.66),WHITE,line=LINE)
            self.txt(s,Inches(1.1),Inches(6.22),Inches(11.2),Inches(0.66),[[("RULE   ",11,BLUE,True),(note,12.5,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def cards3(self,title,cards,kicker):
        s=self.head(self.slide(),title,kicker); xs=[Inches(0.85),Inches(5.0),Inches(9.15)]
        for i,c in enumerate(cards[:3]):
            x=xs[i]; col=c[0]
            self.rect(s,x,Inches(1.95),Inches(3.65),Inches(4.7),LIGHT)
            self.rect(s,x,Inches(1.95),Inches(3.65),Inches(0.12),col)
            self.txt(s,x+Inches(0.25),Inches(2.2),Inches(3.2),Inches(0.7),[[(c[1],18,col,True)]])
            self.bullets(s,x+Inches(0.25),Inches(3.0),Inches(3.2),Inches(3.35),c[2],size=13,gap=9)
        self.footer(s); return s
    def big_statement(self,line1,line2,kicker,color=BLUE):
        s=self.slide(); self.rect(s,0,0,self.SW,self.SH,WHITE); self.rect(s,0,0,Inches(0.28),self.SH,color)
        self.txt(s,Inches(1.1),Inches(2.2),Inches(11),Inches(0.5),[[(kicker,16,color,True)]])
        self.txt(s,Inches(1.1),Inches(2.8),Inches(11.3),Inches(2.2),[[(line1,36,INK,True)]])
        if line2: self.txt(s,Inches(1.12),Inches(5.0),Inches(11),Inches(1.2),[[(line2,19,GREY,False)]])
        self.footer(s); return s
    def tile_grid(self,title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
        s=self.head(self.slide(),title,kicker,kcolor=accent)
        n=len(items); rows=math.ceil(n/cols)
        X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
        gx=Inches(0.3); gy=Inches(0.26)
        cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows); bd=Inches(0.58)
        for i,it in enumerate(items):
            r=i//cols; c=i%cols
            x=int(X0+(cw+gx)*c); y=int(Y0+(ch+gy)*r); col=PALETTE[i%len(PALETTE)]
            self.rect(s,x,y,cw,ch,LIGHT); self.rect(s,x,y,Inches(0.1),ch,col)
            self.oval(s,x+Inches(0.26),int(y+ch/2-bd/2),bd,bd,col)
            ic=icons[i] if icons else str(i+1)
            self.txt(s,x+Inches(0.26),int(y+ch/2-bd/2),bd,bd,[[(ic,17,WHITE,True)]],
                     align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            tx=x+Inches(1.02); tw=cw-Inches(1.26)
            if isinstance(it,tuple):
                self.txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.14)),
                         [[(it[0],size+1,INK,True)],[(it[1],size-3,GREY,False)]],
                         anchor=MSO_ANCHOR.MIDDLE,space=2)
            else:
                self.txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],
                         anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def flow_h(self,title,steps,kicker=None,color=BLUE,note=None):
        s=self.head(self.slide(),title,kicker,kcolor=color)
        n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
        cw=int((TOTW-gap*(n-1))/n); y=Inches(2.45); ch=Inches(3.15); bd=Inches(0.82)
        for i,st in enumerate(steps):
            x=int(X0+(cw+gap)*i)
            self.rect(s,x,y,cw,ch,LIGHT); self.rect(s,x,y,cw,Inches(0.1),color)
            self.oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
            self.txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),28,WHITE,True)]],
                     align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            self.txt(s,x+Inches(0.16),int(y+Inches(1.5)),cw-Inches(0.32),int(ch-Inches(1.65)),
                     [[(st,13,INK,False)]],align=PP_ALIGN.CENTER)
            if i<n-1:
                self.arrow(s,int(x+cw+Inches(0.06)),int(y+ch/2-Inches(0.11)),int(gap-Inches(0.12)),Inches(0.22),color)
        if note:
            self.txt(s,Inches(0.85),Inches(5.9),Inches(11.7),Inches(0.7),[[(note,13,GREY,False)]],align=PP_ALIGN.CENTER)
        self.footer(s); return s
    def process_map(self,title,nodes,kicker=None,color=BLUE,note=None):
        """Connector-linked process boxes with arrowheads (max 5 nodes)."""
        s=self.head(self.slide(),title,kicker,kcolor=color)
        n=len(nodes); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.5)
        bw=int((TOTW-gap*(n-1))/n); y=Inches(2.7); bh=Inches(2.0)
        for i,nd in enumerate(nodes):
            x=int(X0+(bw+gap)*i)
            self.round_rect(s,x,y,bw,bh,WHITE,line=color)
            self.rect(s,x,y,bw,Inches(0.09),color)
            self.oval(s,x+Inches(0.14),y+Inches(0.2),Inches(0.36),Inches(0.36),color)
            self.txt(s,x+Inches(0.14),y+Inches(0.2),Inches(0.36),Inches(0.36),[[(str(i+1),12,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            ttl,cap=(nd if isinstance(nd,tuple) else (nd,""))
            tsz=15 if len(ttl)<=20 else (13 if len(ttl)<=30 else 12)
            csz=11 if len(cap)<=40 else (10 if len(cap)<=58 else 9)
            self.txt(s,x+Inches(0.55),int(y+Inches(0.16)),bw-Inches(0.7),Inches(0.5),
                     [[(ttl,tsz,INK,True)]],align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.MIDDLE)
            if cap:
                self.txt(s,x+Inches(0.14),int(y+Inches(0.8)),bw-Inches(0.28),Inches(1.1),
                         [[(cap,csz,GREY,False)]],align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP)
            if i<n-1:
                self.arrow(s,int(x+bw+Inches(0.09)),int(y+bh/2-Inches(0.11)),
                           int(gap-Inches(0.18)),Inches(0.22),color)
        if note:
            self.rect(s,Inches(0.85),Inches(5.35),Inches(11.63),Inches(0.9),LIGHT)
            self.txt(s,Inches(1.1),Inches(5.5),Inches(11.1),Inches(0.6),
                     [[("WHY IT MATTERS   ",11,color,True),(note,13,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def decision_map(self,title,question,yes,no,kicker=None,note=None,ylab="YES",nlab="NO"):
        s=self.head(self.slide(),title,kicker,kcolor=VIOLET)
        dx=Inches(0.85); dy=Inches(2.55); dw=Inches(3.3); dh=Inches(2.3)
        self.diamond(s,dx,dy,dw,dh,VIOLET)
        self.txt(s,dx+Inches(0.45),dy+Inches(0.55),dw-Inches(0.9),dh-Inches(1.1),
                 [[(question,12,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        for i,(lbl,col,items) in enumerate([(ylab,TEAL,yes),(nlab,AMBER,no)]):
            y=Inches(2.15)+i*Inches(2.45)
            self.arrow(s,Inches(4.3),int(y+Inches(0.8)),Inches(0.55),Inches(0.2),col)
            self.rect(s,Inches(5.0),y,Inches(7.5),Inches(2.1),LIGHT)
            self.rect(s,Inches(5.0),y,Inches(0.1),Inches(2.1),col)
            self.txt(s,Inches(5.28),int(y+Inches(0.16)),Inches(7.0),Inches(0.4),[[(lbl,13,col,True)]])
            self.bullets(s,Inches(5.28),int(y+Inches(0.6)),Inches(7.0),Inches(1.4),items,size=13,gap=6)
        if note:
            self.txt(s,Inches(0.85),Inches(6.55),Inches(11.6),Inches(0.5),
                     [[("RULE   ",11,VIOLET,True),(note,13,INK,False)]])
        self.footer(s); return s
    def compare_table(self,title,headers,rows,kicker=None,color=BLUE,note=None,fsize=11.5):
        s=self.head(self.slide(),title,kicker,kcolor=color)
        X0=Inches(0.85); TOTW=Inches(11.63); Y0=Inches(2.0)
        ncol=len(headers); labw=int(TOTW*0.24); cw=int((TOTW-labw)/(ncol-1))
        avail=Inches(4.2) if note else Inches(4.7)
        hh=Inches(0.55); rh=min(Inches(0.62),int((avail-hh)/max(len(rows),1)))
        self.rect(s,X0,Y0,labw,hh,color)
        self.txt(s,X0+Inches(0.15),Y0,labw-Inches(0.3),hh,[[(headers[0],12.5,WHITE,True)]],anchor=MSO_ANCHOR.MIDDLE)
        for j,h in enumerate(headers[1:]):
            x=int(X0+labw+cw*j)
            self.rect(s,x,Y0,cw,hh,color)
            self.txt(s,x+Inches(0.12),Y0,cw-Inches(0.24),hh,[[(h,12.5,WHITE,True)]],
                     align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        for i,row in enumerate(rows):
            y=int(Y0+hh+rh*i); bg=LIGHT if i%2==0 else WHITE
            self.rect(s,X0,y,labw,rh,bg,line=LINE)
            self.txt(s,X0+Inches(0.15),y,labw-Inches(0.3),rh,[[(row[0],fsize,INK,True)]],anchor=MSO_ANCHOR.MIDDLE)
            for j,c in enumerate(row[1:]):
                x=int(X0+labw+cw*j)
                self.rect(s,x,y,cw,rh,bg,line=LINE)
                self.txt(s,x+Inches(0.12),y,cw-Inches(0.24),rh,[[(c,fsize-0.5,GREY,False)]],
                         align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        if note:
            ny=int(Y0+hh+rh*len(rows)+Inches(0.2))
            self.rect(s,X0,ny,TOTW,Inches(0.62),WHITE,line=LINE)
            self.txt(s,X0+Inches(0.25),ny,TOTW-Inches(0.4),Inches(0.62),[[("RULE   ",11,color,True),(note,12.5,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def stat_row(self,title,stats,kicker=None,color=BLUE,note=None):
        s=self.head(self.slide(),title,kicker,kcolor=color)
        n=len(stats); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.35)
        cw=int((TOTW-gap*(n-1))/n); y=Inches(2.4); ch=Inches(2.6)
        for i,(val,cap) in enumerate(stats):
            x=int(X0+(cw+gap)*i); col=PALETTE[i%len(PALETTE)]
            self.rect(s,x,y,cw,ch,LIGHT); self.rect(s,x,y,cw,Inches(0.1),col)
            self.txt(s,x+Inches(0.15),int(y+Inches(0.5)),cw-Inches(0.3),Inches(1.1),
                     [[(val,38,col,True)]],align=PP_ALIGN.CENTER)
            self.txt(s,x+Inches(0.2),int(y+Inches(1.7)),cw-Inches(0.4),Inches(0.8),
                     [[(cap,13,INK,False)]],align=PP_ALIGN.CENTER)
        if note:
            self.rect(s,Inches(0.85),Inches(5.5),Inches(11.63),Inches(0.85),WHITE,line=LINE)
            self.txt(s,Inches(1.1),Inches(5.62),Inches(11.1),Inches(0.6),
                     [[(note,13,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def chart_slide(self,title,kind,categories,series,kicker=None,lens=None,
                    color=BLUE,note="Native PowerPoint chart · editable data · indicative teaching figures"):
        """Native pptx chart + a 'what the data shows' panel on the right."""
        s=self.head(self.slide(),title,kicker or "NATIVE CHART",kcolor=color)
        cd=CategoryChartData(); cd.categories=categories
        for nm,vals in series: cd.add_series(nm,vals)
        kinds={"bar":XL_CHART_TYPE.BAR_CLUSTERED,"column":XL_CHART_TYPE.COLUMN_CLUSTERED,
               "line":XL_CHART_TYPE.LINE_MARKERS,"pie":XL_CHART_TYPE.PIE,
               "doughnut":XL_CHART_TYPE.DOUGHNUT,"stacked":XL_CHART_TYPE.COLUMN_STACKED}
        gf=s.shapes.add_chart(kinds[kind],Inches(0.85),Inches(2.0),Inches(8.2),Inches(4.5),cd)
        ch=gf.chart; ch.has_title=False
        ch.font.size=Pt(11); ch.font.name="Arial"
        if len(series)>1 and kind not in ("pie","doughnut"):
            ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.BOTTOM
            ch.legend.include_in_layout=False; ch.legend.font.size=Pt(10)
        elif kind in ("pie","doughnut"):
            ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.RIGHT
            ch.legend.include_in_layout=False; ch.legend.font.size=Pt(10)
        else: ch.has_legend=False
        SER=[BLUE,TEAL,VIOLET,AMBER,RED,GREEN]
        try:
            for pl in ch.plots: pl.vary_by_categories=(kind in ("pie","doughnut"))
        except Exception: pass
        try:
            if kind in ("pie","doughnut"):
                pts=ch.plots[0].series[0].points
                for i in range(len(categories)):
                    pts[i].format.fill.solid(); pts[i].format.fill.fore_color.rgb=SER[i%len(SER)]
            else:
                for i,ser in enumerate(ch.series):
                    col=SER[i%len(SER)]
                    if kind=="line":
                        ser.format.line.color.rgb=col; ser.format.line.width=Pt(2.5)
                        try:
                            m=ser.marker; m.format.fill.solid(); m.format.fill.fore_color.rgb=col; m.format.line.color.rgb=col
                        except Exception: pass
                    else:
                        ser.format.fill.solid(); ser.format.fill.fore_color.rgb=col; ser.format.line.fill.background()
        except Exception: pass
        try:
            pl=ch.plots[0]; pl.has_data_labels=True
            dl=pl.data_labels; dl.font.size=Pt(9); dl.font.color.rgb=GREY
            dl.number_format='0'; dl.number_format_is_linked=False
            if kind in ("pie","doughnut"):
                dl.show_percentage=True; dl.show_value=False; dl.number_format='0%'
        except Exception: pass
        try:
            ca=ch.category_axis; va=ch.value_axis
            for ax in (ca,va):
                ax.tick_labels.font.size=Pt(10); ax.tick_labels.font.name="Arial"; ax.tick_labels.font.color.rgb=GREY
            ca.format.line.color.rgb=LINE; va.format.line.fill.background()
            va.major_gridlines.format.line.color.rgb=LINE; va.major_gridlines.format.line.width=Pt(0.75)
            ca.has_major_gridlines=False
        except Exception: pass
        self.rect(s,Inches(9.3),Inches(2.0),Inches(3.2),Inches(4.5),LIGHT)
        self.rect(s,Inches(9.3),Inches(2.0),Inches(3.2),Inches(0.1),color)
        self.txt(s,Inches(9.6),Inches(2.3),Inches(2.6),Inches(0.4),[[("WHAT THE DATA SHOWS",12,color,True)]])
        if lens: self.txt(s,Inches(9.6),Inches(2.8),Inches(2.6),Inches(2.3),[[(lens,12.5,INK,False)]])
        self.rect(s,Inches(9.55),Inches(5.2),Inches(2.7),Inches(0.02),LINE)
        self.oval(s,Inches(9.6),Inches(5.38),Inches(0.34),Inches(0.34),color)
        self.txt(s,Inches(9.6),Inches(5.38),Inches(0.34),Inches(0.34),[[("?",13,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        self.txt(s,Inches(10.05),Inches(5.3),Inches(2.3),Inches(1.1),[[(note,9.5,GREY,False)]],space=1)
        self.footer(s); return s
    def img_points(self,title,image,points,kicker=None,accent=BLUE,img_w=7.0,note=None):
        """Screenshot/diagram left, colour-coded takeaway tiles right — the workhorse concept slide."""
        s=self.head(self.slide(),title,kicker,kcolor=accent)
        p=self._asset(image)
        area_h=Inches(4.75) if not note else Inches(4.35)
        if p:
            w,h=self._picture(s,p,Inches(0.85),Inches(1.95),Inches(img_w),area_h)
            rx=int(Inches(0.85)+Inches(img_w)+Inches(0.35))
        else:
            rx=Inches(6.5)
        rw=int(Inches(12.48)-rx)
        n=len(points); gy=Inches(0.2); th=int((area_h-gy*(n-1))/n)
        for i,(pt_title,pt_sub) in enumerate(points):
            y=int(Inches(1.95)+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
            self.rect(s,rx,y,rw,th,LIGHT); self.rect(s,rx,y,Inches(0.09),th,col)
            bd=Inches(0.36)
            self.oval(s,rx+Inches(0.22),y+Inches(0.14),bd,bd,col)
            self.txt(s,rx+Inches(0.22),y+Inches(0.14),bd,bd,[[(str(i+1),11,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            self.txt(s,rx+Inches(0.7),y+Inches(0.06),rw-Inches(0.9),Inches(0.5),[[(pt_title,13.5,col,True)]],anchor=MSO_ANCHOR.MIDDLE)
            self.txt(s,rx+Inches(0.28),y+Inches(0.56),rw-Inches(0.5),th-Inches(0.62),[[(pt_sub,11.5,INK,False)]],space=2)
        if note:
            self.rect(s,Inches(0.85),Inches(6.4),Inches(11.63),Inches(0.5),LIGHT)
            self.txt(s,Inches(1.1),Inches(6.4),Inches(11.2),Inches(0.5),[[(note,12,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def img_full(self,title,image,kicker=None,accent=BLUE,caption=None):
        s=self.head(self.slide(),title,kicker,kcolor=accent)
        p=self._asset(image)
        area_h=Inches(4.3) if caption else Inches(4.8)
        if p: self._picture(s,p,Inches(0.85),Inches(1.9),Inches(11.63),area_h)
        if caption:
            self.rect(s,Inches(0.85),Inches(6.3),Inches(11.63),Inches(0.62),LIGHT)
            self.txt(s,Inches(1.1),Inches(6.3),Inches(11.2),Inches(0.62),[[(caption,13,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def trainer_slide(self,kicker,name,role,rows,initials,accent=BLUE):
        s=self.head(self.slide(),"About the Trainer",kicker,kcolor=accent)
        lx=Inches(0.85); lw=Inches(3.65)
        self.rect(s,lx,Inches(1.95),lw,Inches(4.7),LIGHT); self.rect(s,lx,Inches(1.95),lw,Inches(0.12),accent)
        bd=Inches(1.7); ax=int(lx+(lw-bd)/2)
        self.oval(s,ax,Inches(2.5),bd,bd,accent)
        self.txt(s,ax,Inches(2.5),bd,bd,[[(initials,42,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        self.txt(s,lx+Inches(0.15),Inches(4.5),lw-Inches(0.3),Inches(0.6),[[(name,20,INK,True)]],align=PP_ALIGN.CENTER)
        self.txt(s,lx+Inches(0.15),Inches(5.15),lw-Inches(0.3),Inches(1.2),[[(role,12,GREY,False)]],align=PP_ALIGN.CENTER)
        rx=Inches(4.9); rw=Inches(7.6); ry=Inches(1.95); rh=Inches(4.7)
        n=len(rows); gy=Inches(0.2); th=int((rh-gy*(n-1))/n)
        for i,(label,val) in enumerate(rows):
            y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
            self.rect(s,rx,y,rw,th,LIGHT); self.rect(s,rx,y,Inches(0.1),th,col)
            vr=[(val,13,INK,False)] if val else [("____________________________________________",12,LINE,False)]
            self.txt(s,rx+Inches(0.32),y,rw-Inches(0.6),th,[[(label.upper(),10,col,True)],vr],
                     anchor=MSO_ANCHOR.MIDDLE,space=3)
        self.footer(s); return s
    def browser_card(self,s,bx,by,bw,bh,url,color=BLUE):
        self.rect(s,bx,by,bw,bh,WHITE,line=LINE)
        self.rect(s,bx,by,bw,Inches(0.52),RGBColor(0xEE,0xF2,0xF8))
        for i,c in enumerate([RED,AMBER,TEAL]):
            self.oval(s,int(bx+Inches(0.18)+Inches(0.28)*i),int(by+Inches(0.17)),Inches(0.18),Inches(0.18),c)
        self.rect(s,int(bx+Inches(1.2)),int(by+Inches(0.1)),int(bw-Inches(1.5)),Inches(0.34),WHITE,line=LINE)
        self.txt(s,int(bx+Inches(1.35)),int(by+Inches(0.1)),int(bw-Inches(1.8)),Inches(0.34),
                 [[(url,12.5,color,True)]],anchor=MSO_ANCHOR.MIDDLE,link=url)
    def lms_slide(self):
        """Download Course Material — browser-card mock of the LMS portal + numbered how-to tiles."""
        C=self.C
        s=self.head(self.slide(),"Download Course Material",kicker="COURSE PORTAL · LMS/TMS",kcolor=BLUE)
        bx,by,bw,bh=Inches(0.85),Inches(2.0),Inches(6.1),Inches(4.55)
        self.browser_card(s,bx,by,bw,bh,"https://lms-tms.tertiaryinfotech.com")
        self.rect(s,int(bx+Inches(0.25)),int(by+Inches(0.75)),int(bw-Inches(0.5)),Inches(0.75),BLUE)
        self.txt(s,int(bx+Inches(0.45)),int(by+Inches(0.75)),int(bw-Inches(0.9)),Inches(0.75),
                 [[("Tertiary Infotech LMS/TMS",15,WHITE,True)],[("My Courses  ·  Attendance  ·  Assessment",11,RGBColor(0xB3,0xD4,0xFF),False)]],anchor=MSO_ANCHOR.MIDDLE,space=2)
        rows=[(C.SHORT_TITLE,True),("Trainer Slides (PDF)  ⬇",False),("Learner Guide (PDF)  ⬇",False),("Activities / Labs (folder)  ⬇",False),("Assessment Submission  ↗",False)]
        for i,(rt,hd) in enumerate(rows):
            yy=int(by+Inches(1.68)+Inches(0.56)*i)
            self.rect(s,int(bx+Inches(0.25)),yy,int(bw-Inches(0.5)),Inches(0.46),LIGHT if not hd else RGBColor(0xE8,0xF0,0xFE))
            self.txt(s,int(bx+Inches(0.45)),yy,int(bw-Inches(0.9)),Inches(0.46),
                     [[(rt,11.5 if hd else 12,INK if not hd else BLUE,hd)]],anchor=MSO_ANCHOR.MIDDLE)
        steps=[("Sign in","lms-tms.tertiaryinfotech.com — log in with your registered email (OTP or password)."),
               ("Open your course",f"Select '{C.SHORT_TITLE}' under My Courses."),
               ("Download materials","Slides, the Learner Guide and the lab folders — your open-book references for the assessment."),
               ("Submit and survey","Upload your assessment answers and complete the TRAQOM survey QR here.")]
        rx=Inches(7.3); rw=Inches(5.2); gy=Inches(0.2); th=int((Inches(4.55)-gy*3)/4)
        for i,(t1,t2) in enumerate(steps):
            y=int(Inches(2.0)+(th+gy)*i); col=PALETTE[i%4]
            self.rect(s,rx,y,rw,th,LIGHT); self.rect(s,rx,y,Inches(0.09),th,col)
            bd=Inches(0.5)
            self.oval(s,rx+Inches(0.2),int(y+th/2-bd/2),bd,bd,col)
            self.txt(s,rx+Inches(0.2),int(y+th/2-bd/2),bd,bd,[[(str(i+1),16,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            self.txt(s,rx+Inches(0.9),y,rw-Inches(1.1),th,[[(t1,14,col,True)],[(t2,11,INK,False)]],anchor=MSO_ANCHOR.MIDDLE,space=2)
        self.txt(s,Inches(0.85),Inches(6.6),Inches(11.7),Inches(0.4),
                 [[("All course material is downloaded from the LMS/TMS portal — keep it handy: the final assessment is open book.",13,GREY,False)]],align=PP_ALIGN.CENTER)
        self.footer(s); return s
    def labs_slide(self,repo_url,n_labs):
        """Access the Hands-On Labs — GitHub repo (clickable) + clone / ZIP cards + folder anatomy."""
        s=self.head(self.slide(),"Access the Hands-On Labs",kicker="LAB FILES · GITHUB REPOSITORY",kcolor=TEAL)
        self.rect(s,Inches(0.85),Inches(1.95),Inches(11.63),Inches(0.7),LIGHT)
        self.txt(s,Inches(1.1),Inches(1.95),Inches(11.2),Inches(0.7),
                 [[("Repository:  ",13,GREY,True),(repo_url,13,BLUE,True)]],anchor=MSO_ANCHOR.MIDDLE,link=repo_url)
        cards=[(BLUE,"Option A — Clone",["Install Git, then in a terminal run:","git clone "+repo_url+".git","Open the labs/ folder — one sub-folder per lab."]),
               (TEAL,"Option B — Download ZIP",["On GitHub click Code → Download ZIP.","Unzip anywhere on your laptop.","Open labs/ — no tools to install."]),
               (VIOLET,"What each lab folder holds",["README.md — brief, procedure, acceptance test","lab.yaml — metadata, K/A codes, files","Mock data: CSV, Markdown, JSON, images",f"LAB-NN-Instructions.pdf + workflow PNG"])]
        xs=[Inches(0.85),Inches(4.85),Inches(8.85)]
        for i,(col,hd,items) in enumerate(cards):
            x=xs[i]; self.rect(s,x,Inches(2.85),Inches(3.65),Inches(3.4),LIGHT); self.rect(s,x,Inches(2.85),Inches(3.65),Inches(0.1),col)
            self.txt(s,x+Inches(0.22),Inches(3.05),Inches(3.25),Inches(0.5),[[(hd,16,col,True)]])
            self.bullets(s,x+Inches(0.22),Inches(3.6),Inches(3.25),Inches(2.6),items,size=11.5,gap=6)
        self.rect(s,Inches(0.85),Inches(6.35),Inches(11.63),Inches(0.55),RGBColor(0xE8,0xF7,0xEE))
        self.txt(s,Inches(1.1),Inches(6.35),Inches(11.2),Inches(0.55),
                 [[(f"{n_labs} labs · all run in Notion in your browser on a free account · the same folders are on the LMS under Activities",12.5,GREEN,True)]],anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def lab_overview(self,tag,title,desc,build,apps,kicker,align,level="",minutes=None):
        s=self.head(self.slide(),title,kicker,kcolor=TEAL)
        self.rect(s,Inches(0.85),Inches(1.85),Inches(1.5),Inches(0.48),TEAL)
        self.txt(s,Inches(0.85),Inches(1.9),Inches(1.5),Inches(0.4),[[(tag,15,WHITE,True)]],align=PP_ALIGN.CENTER)
        self.rect(s,Inches(2.5),Inches(1.85),Inches(1.7),Inches(0.48),LIGHT)
        self.txt(s,Inches(2.5),Inches(1.9),Inches(1.7),Inches(0.4),[[(align,13,GREY,True)]],align=PP_ALIGN.CENTER)
        if minutes:
            self.rect(s,Inches(4.35),Inches(1.85),Inches(1.5),Inches(0.48),LIGHT)
            self.txt(s,Inches(4.35),Inches(1.9),Inches(1.5),Inches(0.4),[[(f"{minutes} min",13,GREY,True)]],align=PP_ALIGN.CENTER)
        self.txt(s,Inches(0.85),Inches(2.55),Inches(11.7),Inches(1.6),[[(desc,17,INK,False)]])
        self.rect(s,Inches(0.85),Inches(4.3),Inches(11.7),Inches(2.0),LIGHT)
        self.rect(s,Inches(0.85),Inches(4.3),Inches(11.7),Inches(0.1),BLUE)
        self.txt(s,Inches(1.1),Inches(4.55),Inches(11),Inches(0.4),[[("You will build",13,BLUE,True)]])
        self.txt(s,Inches(1.1),Inches(4.95),Inches(11.1),Inches(0.8),[[(build,16,INK,True)]])
        self.txt(s,Inches(1.1),Inches(5.78),Inches(11.2),Inches(0.4),[[("Tools:  ",12,GREY,True),(apps,12,GREY,False)]])
        chips=[("ASSESSED",align,BLUE),("LEVEL",level,TEAL),("EVIDENCE","Screenshots · lab README checklist",VIOLET)]
        cw=Inches(3.75); gx=Inches(0.22); x0=Inches(0.85); y=Inches(6.45)
        for i,(lbl,val,col) in enumerate(chips):
            x=int(x0+(cw+gx)*i)
            self.rect(s,x,y,cw,Inches(0.5),LIGHT); self.rect(s,x,y,Inches(0.07),Inches(0.5),col)
            self.txt(s,x+Inches(0.18),y,cw-Inches(0.3),Inches(0.5),[[(lbl+"   ",9,col,True),(val,10.5,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
        self.footer(s); return s
    def test_slide(self,title,text,kicker,trouble=None):
        s=self.head(self.slide(),title,kicker,TEAL)
        self.rect(s,Inches(0.85),Inches(2.1),Inches(11.7),Inches(2.9),RGBColor(0xE8,0xF7,0xEE))
        self.rect(s,Inches(0.85),Inches(2.1),Inches(11.7),Inches(0.1),GREEN)
        self.txt(s,Inches(1.2),Inches(2.4),Inches(11),Inches(0.5),[[("✅  Acceptance check",18,GREEN,True)]])
        self.txt(s,Inches(1.2),Inches(3.0),Inches(11.1),Inches(1.9),[[(text,15,INK,False)]])
        self.rect(s,Inches(0.85),Inches(5.2),Inches(11.7),Inches(1.5),LIGHT)
        self.rect(s,Inches(0.85),Inches(5.2),Inches(11.7),Inches(0.08),AMBER)
        self.txt(s,Inches(1.2),Inches(5.35),Inches(11),Inches(0.35),[[("IF IT DOES NOT WORK",11,AMBER,True)]])
        tips=trouble or ["Re-read the step: most misses are the page menu (top right) versus the block handle (left of a block).",
                         "Check you are in the right page or teamspace — the sidebar shows the path.",
                         "Full click-by-click steps: Learner Guide and the lab's instruction PDF."]
        for i,tip in enumerate(tips):
            self.oval(s,Inches(1.2)+Inches(3.85)*i,Inches(5.78),Inches(0.3),Inches(0.3),AMBER)
            self.txt(s,Inches(1.2)+Inches(3.85)*i,Inches(5.78),Inches(0.3),Inches(0.3),[[(str(i+1),10,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
            self.txt(s,Inches(1.6)+Inches(3.85)*i,Inches(5.72),Inches(3.35),Inches(0.9),[[(tip,10.5,INK,False)]])
        self.footer(s); return s
    def brk(self,kind,dur,color=AMBER):
        s=self.slide(); self.rect(s,0,0,self.SW,self.SH,WHITE)
        self.rect(s,0,0,self.SW,Inches(0.22),color); self.rect(s,0,Inches(7.28),self.SW,Inches(0.22),color)
        self.rect(s,Inches(5.4),Inches(2.35),Inches(2.53),Inches(0.1),color)
        self.txt(s,0,Inches(2.75),self.SW,Inches(1.2),[[(kind,46,INK,True)]],align=PP_ALIGN.CENTER)
        self.txt(s,0,Inches(4.05),self.SW,Inches(0.8),[[(dur,21,color,True)]],align=PP_ALIGN.CENTER)
        self.page+=1; return s

    # ---------- motion + save ----------
    def _transition(self,s,kind="fade",speed="fast"):
        sld=s._element
        for old in sld.findall(qn("p:transition")): sld.remove(old)
        tr=etree.SubElement(sld,qn("p:transition")); tr.set("spd",speed); tr.set("advClick","1")
        if kind=="fade": etree.SubElement(tr,qn("p:fade"))
        else: etree.SubElement(tr,qn("p:push")).set("dir","l")
        sld.append(tr)
    def save(self,path):
        for i,s in enumerate(self.prs.slides):
            if i in self.section_idx: self._transition(s,"push","med")
            else: self._transition(s,"fade","fast")
        self.prs.save(path); return len(self.prs.slides._sldIdLst)
