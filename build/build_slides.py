#!/usr/bin/env python3
"""Build the course slide deck — highly visual, concept-led, NO step-by-step.

Every teaching slide is a component (tile grid, screenshot + takeaways, process map,
comparison table, native chart, decision map). The detailed click-by-click procedures
live in the Learner Guide and each lab's instruction PDF. The build also writes
slide_map.json so the Lesson Plan cites exact slide numbers.
"""
import os, sys, json
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
REPO=os.path.dirname(HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
from data_teaching import TEACHING
from deck_components import Deck, BLUE, TEAL, VIOLET, AMBER, GREY, INK, RED, GREEN
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4

D=Deck(C, os.path.join(REPO,"courseware","assets"))

def render(spec):
    k=spec[0]
    if   k=="img":     D.img_points(spec[1],spec[2],spec[4],kicker=spec[3],img_w=spec[5] if len(spec)>5 else 6.6)
    elif k=="imgfull": D.img_full(spec[1],spec[2],kicker=spec[3],caption=spec[4])
    elif k=="tile":    D.tile_grid(spec[1],spec[3],kicker=spec[2],cols=spec[4],size=spec[5])
    elif k=="process": D.process_map(spec[1],spec[3],kicker=spec[2],note=spec[4] if len(spec)>4 else None)
    elif k=="compare": D.compare_table(spec[1],spec[3],spec[4],kicker=spec[2],note=spec[5] if len(spec)>5 else None)
    elif k=="two_col": D.two_col(spec[1],spec[3],spec[4],kicker=spec[2],lhead=spec[5],rhead=spec[6],size=13.5,
                                 note=spec[7] if len(spec)>7 else None)
    elif k=="big":     D.big_statement(spec[1],spec[2],spec[3])
    elif k=="decision":D.decision_map(spec[1],spec[2],spec[3],spec[4],kicker="DECISION RULE",
                                      note=spec[5] if len(spec)>5 else None,
                                      ylab=spec[6] if len(spec)>6 else "YES", nlab=spec[7] if len(spec)>7 else "NO")
    elif k=="chart":   D.chart_slide(spec[1],spec[2],spec[3],spec[4],lens=spec[5] if len(spec)>5 else None)
    elif k=="stat":    D.stat_row(spec[1],spec[3],kicker=spec[2],note=spec[4] if len(spec)>4 else None)
    elif k=="flow":    D.flow_h(spec[1],spec[3],kicker=spec[2],note=spec[4] if len(spec)>4 else None)
    elif k=="content": D.content(spec[1],spec[3],kicker=spec[2])
    else: raise ValueError(f"unknown teaching spec kind: {k}")

def traqom_slide():
    D.flow_h("Digital Attendance (Mandatory)",[
      "Trainer displays the SSG digital attendance QR code",
      "Scan it with your phone camera (Singpass app)",
      "Submit your attendance",
      "Repeat for AM, PM and the assessment session"],
      kicker="TRAQOM · SSG DIGITAL ATTENDANCE",color=VIOLET,
      note="Attendance is taken digitally for every session of a WSQ-funded course; a minimum of 75% attendance is required for assessment and funding.")

def assessment_table(kicker):
    D.compare_table("Final Assessment",
      ["","Written Assessment (WA)","Practical Performance (PP)"],
      [["Format","Short-answer questions (SAQ)","Scenario-based practical tasks in Notion"],
       ["What it tests","Underpinning knowledge K1–K9","Practical abilities A1–A7"],
       ["Items","9 questions","5 tasks"],
       ["Duration","1 hour","1 hour"],
       ["Conditions","Open book, individual","Open book, individual"],
       ["Submission","On the LMS","On the LMS, with screenshots as evidence"]],
      kicker=kicker,
      note="Open book: slides, Learner Guide and your own lab work. 75% attendance is required; an appeal process is available.")

AFLOW=["TRAQOM survey — scan the QR code on the LMS",
       "Assessment digital attendance — scan the SSG QR",
       "Sit WA (SAQ) then PP — open book",
       "Submit your answers on the LMS",
       "Sign the Assessment Summary Record"]

LAB_MIN={1:30,2:35,3:35,4:40,5:40,6:45,7:30,8:30,9:40,10:25,11:25,12:25}

# ============================================================ COVER + ADMIN
D.cover("NOTION","CONTENT · PROJECTS · DATA")
D.mark("admin")
D.section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
traqom_slide()
D.trainer_slide("YOUR TRAINER · GENERAL","Your Trainer",
  "General Trainer template —\nto be completed by the trainer",
  [("Name",""),("Title / Designation",""),("Qualifications",""),
   ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
  initials="?",accent=GREY)
D.trainer_slide("YOUR TRAINER",C.TRAINER,"Principal Trainer\nTertiary Infotech Academy Pte Ltd",
  [("Role","Principal Trainer, Tertiary Infotech Academy Pte Ltd"),
   ("Background","PhD — 20+ years of industry and training experience in software, data, AI and digital productivity tools."),
   ("Delivers","WSQ courses on Notion, Microsoft 365 and Copilot, data analytics, AI and web technologies."),
   ("Founder","Founder and lead instructor at Tertiary Infotech / Tertiary Courses.")],
  initials="AA",accent=BLUE)
D.tile_grid("Let's Know Each Other",[
  ("Who you are","Your name, your organisation and your role in it."),
  ("Your content today","Where your team's documents, projects and data live right now."),
  ("Your Notion experience","Never used it, personal use, or already running a team workspace?"),
  ("What you want to build","One thing you would like to manage in Notion by the end of Day 2.")],
  kicker="ICE-BREAKER",cols=2,size=15)
D.tile_grid("Ground Rules",[
  "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
  "Respect each other's views; one conversation at a time.","Step out quietly for calls or breaks.",
  "Be punctual; return from breaks on time.","75% attendance is required for assessment and funding."],
  kicker="HOUSEKEEPING",cols=2,size=15)
D.lms_slide()
D.labs_slide(C.GITHUB_REPO,len(ACT))
D.tile_grid("The Course Scenario — Brightwave Media",[
  ("Brightwave Media Pte Ltd","A twelve-person Singapore content and digital-marketing agency."),
  ("The move to Notion","Company wiki, content operations, client projects and a public help centre in one workspace."),
  ("Day 1 — build the content system","Workspace, wiki, policies, collaboration and rich, styled content (Labs 1–6)."),
  ("Day 2 — run it as a CMS","Databases, permissions, publishing, analytics, integrations and Notion AI (Labs 7–12)."),
  ("One connected story","Every lab adds to the same workspace, so the final result is a complete, governed CMS."),
  ("Mock data supplied","Each lab folder carries the CSV, Markdown, JSON and images the lab needs.")],
  kicker="ONE STORY, TWELVE LABS",cols=2,size=14)
D.compare_table("Skills Framework — Content Management",
  ["TSC element","Detail"],
  [["TSC Title / Code",f"{C.TSC_TITLE}  ·  {C.TSC_CODE}"]]+
  [[f"Ability {c}",d] for c,d in C.ABILITIES]+[[f"Knowledge {c}",d] for c,d in C.KNOWLEDGE[:4]],
  kicker="WSQ ALIGNMENT · PART 1",fsize=10.5)
D.compare_table("Skills Framework — Knowledge Statements",
  ["Code","Knowledge statement","Taught in"],
  [[c,d,t] for (c,d),t in zip(C.KNOWLEDGE,["Topics 1–2 · Lab 2","Topic 3 · Labs 4–5","Topic 5 · Labs 7–8","Topic 4 · Lab 6","Topic 2 · Lab 3","Topic 7 · Lab 10","Topic 6 · Lab 9","Topics 6, 9 · Lab 12","Topic 8 · Lab 11"])],
  kicker="WSQ ALIGNMENT · PART 2",fsize=11)
D.tile_grid("Learning Outcomes",
  [(lo.split(":")[0], lo.split(":",1)[1].strip()) for lo in C.LEARNING_OUTCOMES],
  kicker="BY THE END OF THIS COURSE",cols=1,size=14)
D.tile_grid("Course Outline — Four Learning Units, Nine Topics",[
  ("LU1 · Foundations and Workspace Management","Topic 1 Introduction to Notion · Topic 2 Workspace Collaboration Tools — Labs 1–3 (LO1)"),
  ("LU2 · Content Creation and Management","Topic 3 Pages and Content Blocks · Topic 4 Advanced Content Techniques — Labs 4–6 (LO2)"),
  ("LU3 · Mastering Databases in Notion","Topic 5 Database Essentials · Topic 6 Advanced Database Features — Labs 7–9 (LO3)"),
  ("LU4 · Collaboration, Publishing and Integrations","Topic 7 Collaboration and Publishing · Topic 8 Data Management and Integrations · Topic 9 Notion AI — Labs 10–12 (LO4)")],
  kicker="THE JOURNEY",cols=1,size=14)
D.two_col("Lesson Plan — 2 Days, 9:30am–6:30pm",[
  ("Day 1 — Foundations and content (8 h)",0,True),
  ("AM attendance · introductions · learning outcomes",1),
  ("Topic 1 Introduction to Notion · Labs 1–2",1),
  ("Topic 2 Workspace Collaboration Tools · Lab 3",1),
  ("Lunch (1 hour)",1),
  ("PM attendance · Topic 3 Pages and Content Blocks · Labs 4–5",1),
  ("Topic 4 Advanced Content Techniques · Lab 6",1),
  ("Day 1 recap and Q&A",1)],
  [("Day 2 — Databases, publishing, AI (6 h + 2 h assessment)",0,True),
  ("AM attendance · Topic 5 Database Essentials · Labs 7–8",1),
  ("Topic 6 Advanced Database Features · Lab 9",1),
  ("Lunch (1 hour)",1),
  ("PM attendance · Topic 7 Collaboration and Publishing · Lab 10",1),
  ("Topic 8 Data Management and Integrations · Lab 11",1),
  ("Topic 9 Notion AI · Lab 12 · briefing for assessment",1),
  ("4:30pm WA (SAQ) 1 h · 5:30pm PP 1 h · TRAQOM",1)],
  kicker="SCHEDULE",lhead="Day 1",rhead="Day 2",size=13,
  note="14 training hours + 2 assessment hours · 10-minute tea breaks are within training time · full timings in the Lesson Plan.")
D.mark("briefing")
D.tile_grid("Briefing for Assessment",[
  ("Phones away","Place phones and other materials under the table or on the floor."),
  ("No recording","No photos or recording of assessment scripts, at any point."),
  ("No discussion","Work individually — no discussion once the assessment starts."),
  ("Black or blue pen","Use a black or blue pen for any hard-copy assessment."),
  ("No correction fluid","No liquid paper or correction tape; strike through instead."),
  ("Time is called","Scripts are collected when time is up — submit on the LMS before then.")],
  kicker="BEFORE ASSESSMENT",cols=2,size=14)
assessment_table("FINAL ASSESSMENT")
D.flow_h("Assessment Flow",AFLOW,kicker="ON ASSESSMENT DAY",
  note="The TRAQOM QR code and the assessment submission are both on the LMS — https://lms-tms.tertiaryinfotech.com")

# ============================================================ TOPICS
TOPIC_ACTS={t["num"]:[a for a in ACT if a["topic"]==t["num"]] for t in C.TOPICS}
for t in C.TOPICS:
    n=t["num"]
    D.mark(f"topic{n}")
    D.section(f"TOPIC {t['code']} · {t['lu']} · {t['ka']}", t["title"], t["code"], t["subtitle"])
    D.tile_grid(f"Key Concepts — {t['title']}", t["concepts"],
                kicker=f"TOPIC {t['code']} · WHAT THIS TOPIC COVERS", cols=2, size=13)
    for spec in TEACHING[n]: render(spec)
    for a in TOPIC_ACTS[n]:
        D.mark(f"lab{a['num']}")
        D.lab_overview(f"LAB {a['num']:02d}", a["title"], a["desc"], a["build"], a["apps"],
                       kicker=f"TOPIC {t['code']} · HANDS-ON LAB · {a['level'].upper()}",
                       align=f"{a['km']} · {a['am']}", level=a['level'], minutes=LAB_MIN[a['num']])
        D.process_map(f"How Lab {a['num']:02d} Runs",
                      list(zip(["Prepare","Build","Refine","Verify"],a["flow"])),
                      kicker=f"LAB {a['num']:02d} · WORKFLOW", color=TEAL,
                      note=f"The shape of the work — the full click-by-click procedure is in the Learner Guide (Lab {a['num']:02d}) and the lab's instruction PDF.")
        D.test_slide(a["title"], a["test"], kicker=f"LAB {a['num']:02d} · ACCEPTANCE CHECK")
    if n==2: D.brk("Lunch Break","1 hour · back for PM digital attendance")
    if n==4:
        D.mark("day1end")
        D.tile_grid("Day 1 Recap — What You Can Now Do",[
          ("Workspace and pages","Create a workspace, pages, sub-pages and blocks, and organise the sidebar (Lab 1)."),
          ("Policies and wikis","Import policies, assign owners, verify pages and publish the content policy (Lab 2)."),
          ("Collaboration","Review with comments, mentions, reminders, Inbox and search filters (Lab 3)."),
          ("Rich content","Post and structure an article with blocks, columns and tables (Lab 4)."),
          ("Media and reuse","Images, files, embeds, code blocks, buttons and synced blocks (Lab 5)."),
          ("Curation","Apply a style guide, build a navigation hub, link and backlink, add equations (Lab 6).")],
          kicker="END OF DAY 1 · PM DIGITAL ATTENDANCE",cols=2,size=13)
        D.brk("End of Day 1","See you tomorrow at 9:30am — Databases, Publishing and Notion AI",color=TEAL)
    if n==6: D.brk("Lunch Break","1 hour · back for PM digital attendance")

# ============================================================ CLOSE
D.mark("close")
D.section("WRAP-UP","Course Summary & Next Steps","")
D.tile_grid("What You Achieved",[
  ("LO1 · Policies and permissions","A governed workspace: wiki, verified pages, owners, permissions, teamspaces and locks (Labs 1–3, 10)."),
  ("LO2 · Post and update content","Structured, media-rich, style-compliant articles with navigation and synced components (Labs 4–6)."),
  ("LO3 · Maintain web properties and assets","Relational databases for calendar, projects, tasks, clients and deliverables, with views, rollups, formulas and automations (Labs 7–9)."),
  ("LO4 · Report, recommend, improve","Page analytics and a metrics dashboard, API-backed integrations and plug-in recommendations, and AI-generated visitor-experience ideas (Labs 10–12).")],
  kicker="LEARNING OUTCOMES DELIVERED",cols=1,size=14)
D.tile_grid("Taking This Back to Work",[
  ("Start with the policy","Write the content management policy first; every structure decision follows from it."),
  ("Four sections, then databases","Wiki, content, projects, public — then turn repeated pages into databases."),
  ("Owners and verification","No page without an owner; no policy without an expiry date."),
  ("Measure before you redesign","Read page analytics for a month before changing the navigation."),
  ("Integrate deliberately","Recommend plug-ins against the six criteria; keep the API token out of pages."),
  ("Let AI draft, keep humans accountable","Writer, Autofill and Q&A speed the work; a named person approves what is published.")],
  kicker="NEXT STEPS",cols=2,size=14)
D.tile_grid("Recommended Follow-On Courses",
  [(t.replace("WSQ - ",""),"WSQ funded · Tertiary Infotech Academy") for t in C.RECOMMENDED],
  kicker="CONTINUE THE JOURNEY",cols=1,size=13)
D.tile_grid("Support",[
  ("Email","enquiry@tertiaryinfotech.com — questions during and after the class"),
  ("Telephone","+65 6100 0613"),
  ("Website",C.COURSE_URL.replace("https://","")),
  ("LMS / TMS","lms-tms.tertiaryinfotech.com — courseware, attendance, assessment and TRAQOM survey")],
  kicker="WE ARE HERE TO HELP",cols=2,size=14)
D.mark("assessment_end")
assessment_table("WRAP-UP · FINAL ASSESSMENT")
D.flow_h("Assessment Flow",AFLOW,kicker="ON ASSESSMENT DAY",
  note="Submit both papers on the LMS, then sign the Assessment Summary Record with your assessor.")
traqom_slide()
D.big_statement("Thank You!",
  "You can now build, govern, publish and measure a complete content management system in Notion.",
  "SEE YOU IN CLASS",color=TEAL)
D.mark("end")

OUT=os.path.join(REPO,"courseware",f"{C.SHORT_TITLE}-{C.VERSION}.pptx")
n=D.save(OUT)
with open(os.path.join(HERE,"slide_map.json"),"w") as f: json.dump(D.slide_map,f,indent=1)
print(f"Saved {OUT}  ({n} slides)")
print("Slide map:",json.dumps(D.slide_map))
