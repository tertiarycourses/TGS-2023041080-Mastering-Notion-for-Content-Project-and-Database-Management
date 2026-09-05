"""Deterministic mock data for the Brightwave Media scenario used by every lab."""
import random, datetime as dt

PEOPLE = ["Content Manager","Aisha Rahman","Marcus Lim","Priya Nair","Daniel Ong","Sofia Chen"]
CLIENTS = [
    ["CL-001","Nova Retail","Retail","Marcus Lim",6500,"Monthly content retainer — blog, newsletter, social"],
    ["CL-002","Harbour Fintech","Financial services","Priya Nair",9800,"Thought-leadership programme and product launches"],
    ["CL-003","GreenLeaf Foods","Food and beverage","Aisha Rahman",4200,"Recipe content, social calendar, seasonal campaigns"],
    ["CL-004","Meridian Clinics","Healthcare","Daniel Ong",7300,"Patient education hub and newsletter"],
    ["CL-005","Skyline Properties","Real estate","Sofia Chen",5600,"Listing content, market reports, video scripts"],
]
CLIENT_HEADERS = ["Client ID","Name","Industry","Account Manager","Retainer (SGD)","Scope"]

PROJECTS = [
    ["PRJ-01","Nova Retail Launch","Nova Retail","2026-09-14","2026-10-30","In Progress",38000,"Content Manager"],
    ["PRJ-02","Harbour Fintech Thought Leadership Q4","Harbour Fintech","2026-10-01","2026-12-18","Planning",52000,"Priya Nair"],
    ["PRJ-03","GreenLeaf Festive Campaign","GreenLeaf Foods","2026-11-02","2026-12-24","Planning",21000,"Aisha Rahman"],
    ["PRJ-04","Meridian Patient Education Hub","Meridian Clinics","2026-08-18","2026-11-27","In Progress",44000,"Daniel Ong"],
    ["PRJ-05","Skyline Market Report 2027","Skyline Properties","2026-12-01","2027-01-29","Not Started",16500,"Sofia Chen"],
    ["PRJ-06","Brightwave Help Centre Refresh","Brightwave Media","2026-09-07","2026-10-16","In Progress",9000,"Content Manager"],
]
PROJECT_HEADERS = ["Project ID","Name","Client","Start","End","Stage","Budget (SGD)","Lead"]

TASKS = [
    # ID, Name, Project, Parent, Depends on, Assignee, Status, Due, Estimate (h), Priority
    ["T-01","Plan Nova Retail launch content","Nova Retail Launch","","","Content Manager","Done","2026-09-16",4,"High"],
    ["T-02","Draft launch messaging","Nova Retail Launch","T-01","","Aisha Rahman","Done","2026-09-19",6,"High"],
    ["T-03","Approve creative concept","Nova Retail Launch","T-01","T-02","Marcus Lim","In Progress","2026-09-24",2,"High"],
    ["T-04","Produce launch assets","Nova Retail Launch","","T-03","Sofia Chen","Not Started","2026-10-03",16,"High"],
    ["T-05","Write launch blog article","Nova Retail Launch","T-04","T-03","Aisha Rahman","Not Started","2026-10-07",5,"Medium"],
    ["T-06","Design social carousel","Nova Retail Launch","T-04","T-03","Sofia Chen","Not Started","2026-10-08",8,"Medium"],
    ["T-07","Schedule newsletter","Nova Retail Launch","","T-05","Content Manager","Not Started","2026-10-14",2,"Medium"],
    ["T-08","Publish and monitor launch","Nova Retail Launch","","T-06,T-07","Content Manager","Not Started","2026-10-21",3,"High"],
    ["T-09","Post-launch report","Nova Retail Launch","","T-08","Marcus Lim","Not Started","2026-10-30",4,"Low"],
    ["T-10","Interview Harbour Fintech CTO","Harbour Fintech Thought Leadership Q4","","","Priya Nair","Not Started","2026-10-06",3,"High"],
    ["T-11","Draft article 1: Open banking","Harbour Fintech Thought Leadership Q4","","T-10","Priya Nair","Not Started","2026-10-15",6,"High"],
    ["T-12","Draft article 2: Payments security","Harbour Fintech Thought Leadership Q4","","T-10","Daniel Ong","Not Started","2026-10-29",6,"Medium"],
    ["T-13","Client review round","Harbour Fintech Thought Leadership Q4","","T-11,T-12","Priya Nair","Not Started","2026-11-05",2,"Medium"],
    ["T-14","Festive recipe shoot","GreenLeaf Festive Campaign","","","Sofia Chen","Not Started","2026-11-10",10,"High"],
    ["T-15","Write 6 festive social posts","GreenLeaf Festive Campaign","","T-14","Aisha Rahman","Not Started","2026-11-17",6,"Medium"],
    ["T-16","Festive newsletter","GreenLeaf Festive Campaign","","T-15","Aisha Rahman","Not Started","2026-11-24",3,"Medium"],
    ["T-17","Audit existing patient articles","Meridian Patient Education Hub","","","Daniel Ong","Done","2026-08-28",8,"High"],
    ["T-18","Rewrite top 10 articles","Meridian Patient Education Hub","","T-17","Daniel Ong","In Progress","2026-09-30",20,"High"],
    ["T-19","Clinical review of rewrites","Meridian Patient Education Hub","","T-18","Priya Nair","Not Started","2026-10-14",4,"High"],
    ["T-20","Publish hub v1","Meridian Patient Education Hub","","T-19","Content Manager","Not Started","2026-10-28",3,"High"],
    ["T-21","Collect 2026 market data","Skyline Market Report 2027","","","Sofia Chen","Not Started","2026-12-12",6,"Medium"],
    ["T-22","Map Help Centre pages","Brightwave Help Centre Refresh","","","Content Manager","Done","2026-09-09",2,"Medium"],
    ["T-23","Rewrite FAQ section","Brightwave Help Centre Refresh","","T-22","Aisha Rahman","In Progress","2026-09-25",5,"Medium"],
    ["T-24","Publish Help Centre and review analytics","Brightwave Help Centre Refresh","","T-23","Content Manager","Not Started","2026-10-16",3,"High"],
]
TASK_HEADERS = ["Task ID","Name","Project","Parent","Depends on","Assignee","Status","Due","Estimate (h)","Priority"]

DELIVERABLES = [
    ["D-01","Launch messaging framework","Nova Retail Launch","Document","Approved","Aisha Rahman","2026-09-22"],
    ["D-02","Launch blog article","Nova Retail Launch","Blog","Draft","Aisha Rahman","2026-10-07"],
    ["D-03","Social carousel (6 slides)","Nova Retail Launch","Social","Draft","Sofia Chen","2026-10-08"],
    ["D-04","Launch newsletter","Nova Retail Launch","Newsletter","Draft","Content Manager","2026-10-14"],
    ["D-05","Post-launch performance report","Nova Retail Launch","Report","Draft","Marcus Lim","2026-10-30"],
    ["D-06","Open banking article","Harbour Fintech Thought Leadership Q4","Blog","Draft","Priya Nair","2026-10-15"],
    ["D-07","Payments security article","Harbour Fintech Thought Leadership Q4","Blog","Draft","Daniel Ong","2026-10-29"],
    ["D-08","LinkedIn post series (8)","Harbour Fintech Thought Leadership Q4","Social","Draft","Priya Nair","2026-11-12"],
    ["D-09","Festive recipe photo set","GreenLeaf Festive Campaign","Media","Draft","Sofia Chen","2026-11-10"],
    ["D-10","Festive social posts (6)","GreenLeaf Festive Campaign","Social","Draft","Aisha Rahman","2026-11-17"],
    ["D-11","Festive newsletter","GreenLeaf Festive Campaign","Newsletter","Draft","Aisha Rahman","2026-11-24"],
    ["D-12","Patient article rewrites (10)","Meridian Patient Education Hub","Blog","In Review","Daniel Ong","2026-09-30"],
    ["D-13","Patient education hub structure","Meridian Patient Education Hub","Document","Approved","Content Manager","2026-09-05"],
    ["D-14","Clinical review log","Meridian Patient Education Hub","Document","Draft","Priya Nair","2026-10-14"],
    ["D-15","Market report outline","Skyline Market Report 2027","Document","Draft","Sofia Chen","2026-12-15"],
    ["D-16","Help Centre page map","Brightwave Help Centre Refresh","Document","Published","Content Manager","2026-09-09"],
    ["D-17","FAQ section rewrite","Brightwave Help Centre Refresh","Web page","In Review","Aisha Rahman","2026-09-25"],
    ["D-18","Help Centre analytics baseline","Brightwave Help Centre Refresh","Report","Draft","Content Manager","2026-10-16"],
]
DELIVERABLE_HEADERS = ["Deliverable ID","Name","Project","Type","Status","Owner","Due"]

CHANNELS = ["Blog","Newsletter","Social","Video","Help Centre"]
STATUSES = ["Idea","Draft","In Review","Scheduled","Published"]
TAGS = ["Campaign","Evergreen","SEO","Client","Internal","Product"]
def content_calendar(n=36, seed=7):
    rnd=random.Random(seed); rows=[]
    titles=["Five Content Trends for 2027","How to Brief a Designer","Nova Retail Launch Announcement","Open Banking Explained",
            "Festive Recipe Round-up","Patient Guide: Managing Blood Pressure","Skyline Q4 Market Snapshot","Behind the Scenes at Brightwave",
            "Newsletter #41 — September","Newsletter #42 — October","Reel: Studio Tour","Reel: Product Unboxing",
            "Help Centre: Getting Started","Help Centre: Requesting Changes","Case Study: GreenLeaf Spring","Case Study: Meridian Hub",
            "Payments Security Basics","Content Calendar Template Walkthrough","Interview: Harbour Fintech CTO","Top 10 Notion Tips for Teams",
            "LinkedIn: Hiring a Content Lead","LinkedIn: Our Values","Webinar Recap: Content Ops","Year in Review 2026",
            "Client Onboarding Checklist","Video Script: Skyline Listing","FAQ: Turnaround Times","FAQ: Pricing and Retainers",
            "Style Guide Update Notice","Holiday Posting Schedule","Blog: Measuring Content ROI","Blog: Repurposing Long-form",
            "Social: Team Spotlight — Aisha","Social: Team Spotlight — Daniel","Newsletter #43 — November","Help Centre: Analytics Explained"]
    start=dt.date(2026,9,7)
    for i in range(n):
        status=STATUSES[[0,1,1,2,3,4,4,4][i%8]] if i<32 else "Draft"
        d=start+dt.timedelta(days=rnd.randint(0,84))
        ch=CHANNELS[i%5]; tags=";".join(sorted(rnd.sample(TAGS,rnd.randint(1,2))))
        owner=PEOPLE[rnd.randint(0,5)]
        words=rnd.choice([0,600,850,1200,1500]) if ch in("Blog","Help Centre") else rnd.choice([0,120,180,250])
        url=f"https://brightwave.notion.site/{titles[i].lower().replace(' ','-').replace(':','').replace('#','').replace('—','-')}" if status=="Published" else ""
        rows.append([f"BW-{i+1:03d}",titles[i],status,ch,tags,d.isoformat(),owner,words,url,"Yes" if status in("Scheduled","Published") else "No"])
    return rows
CALENDAR_HEADERS=["ID","Name","Status","Channel","Tags","Publish Date","Owner","Word Count","URL","Approved"]

def page_analytics(seed=11):
    rnd=random.Random(seed); rows=[]
    pages=[("Help Centre Home","Help Centre","Direct"),("Getting Started","Help Centre","Search"),("Requesting Changes","Help Centre","Search"),
           ("FAQ: Turnaround Times","Help Centre","Search"),("FAQ: Pricing and Retainers","Help Centre","Referral"),("Analytics Explained","Help Centre","Search"),
           ("Five Content Trends for 2027","Blog","Social"),("Measuring Content ROI","Blog","Search"),("Case Study: GreenLeaf Spring","Blog","Referral")]
    base={"Help Centre Home":120,"Getting Started":80,"Requesting Changes":60,"FAQ: Turnaround Times":45,"FAQ: Pricing and Retainers":40,
          "Analytics Explained":25,"Five Content Trends for 2027":70,"Measuring Content ROI":50,"Case Study: GreenLeaf Spring":30}
    for w in range(1,13):
        for name,section,channel in pages:
            views=int(base[name]*(1+0.09*w)*rnd.uniform(0.85,1.15)); uniq=int(views*rnd.uniform(0.55,0.75))
            avg=rnd.randint(40,240); comments=rnd.randint(0,4)
            rows.append([f"W{w}",name,section,channel,views,uniq,avg,comments])
    return rows
ANALYTICS_HEADERS=["Week","Page","Section","Channel","Views","Unique Visitors","Avg Time (s)","Comments"]

FEEDBACK_TOPICS=[("Navigation","I could not find the page about turnaround times from the home page.",-1),
 ("Navigation","The menu has too many levels; took me four clicks to reach pricing.",-1),
 ("Search","Search for 'retainer' returned nothing useful.",-1),
 ("Content clarity","The Getting Started article was clear and easy to follow.",1),
 ("Missing topic","There is no page explaining how revisions are counted.",-1),
 ("Speed","Pages load quickly, even the ones with video.",1),
 ("Content clarity","Some articles use jargon like 'deliverable cadence' without explaining it.",-1),
 ("Missing topic","Please add a page on how to give feedback on drafts.",-1),
 ("Navigation","Breadcrumbs helped me get back to the start page.",1),
 ("Search","Search worked once I used the exact article title.",0)]
def visitor_feedback(n=40, seed=5):
    rnd=random.Random(seed); rows=[]; start=dt.date(2026,8,1)
    for i in range(n):
        topic,text,pol=FEEDBACK_TOPICS[i%len(FEEDBACK_TOPICS)]
        d=start+dt.timedelta(days=rnd.randint(0,60))
        who=rnd.choice(["Client","Prospect","Staff","Partner"])
        rows.append([f"FB-{i+1:03d}",d.isoformat(),who,topic,text,rnd.choice([1,2,3,4,5]) if pol==0 else (rnd.choice([4,5]) if pol>0 else rnd.choice([1,2]))])
    return rows
FEEDBACK_HEADERS=["ID","Date","Visitor Type","Topic","Feedback","Rating (1-5)"]

FAQ_SEED=[
 ["How do I request a content change?","Open the Help Centre page 'How to Request a Content Change', fill in the request form and your account manager confirms within one working day.","Requests","Client"],
 ["What are your turnaround times?","Blog articles 5 working days, social posts 2 working days, newsletters 3 working days from approved brief.","Delivery","Client"],
 ["How many revision rounds are included?","Two rounds per deliverable are included in every retainer; additional rounds are quoted separately.","Delivery","Client"],
 ["How is my retainer calculated?","Retainer = base hours × blended rate + platform fees; see Pricing Formulas in the Company Wiki.","Pricing","Client"],
 ["Who owns the content you produce?","You do, once the invoice is settled; Brightwave retains the right to show the work in its portfolio unless agreed otherwise.","Legal","Client"],
 ["Can I see analytics for my content?","Yes — monthly reports include views, unique visitors and engagement per page; ask your account manager for the dashboard link.","Reporting","Client"],
 ["How do I give feedback on a draft?","Comment directly on the Notion page shared with you; use @ to mention the writer.","Requests","Client"],
 ["What file formats do you deliver?","Notion pages, Google Docs, PDF, PNG/JPG for images and MP4 for video.","Delivery","Client"],
 ["Do you write in languages other than English?","Yes — Chinese, Malay and Tamil through partner translators; AI-assisted drafts are always reviewed by a native speaker.","Delivery","Prospect"],
 ["How do I onboard as a new staff member?","Read Company Wiki → Onboarding, complete the checklist and ask the Content Manager for teamspace access.","Internal","Staff"],
 ["Where is the brand style guide?","Company Wiki → Policies → Style Guide; it is a verified page reviewed every 90 days.","Internal","Staff"],
 ["How do I report a broken page?","Use the Feedback form at the bottom of every Help Centre page or email support@brightwave.example.","Support","Client"],
]
FAQ_HEADERS=["Question","Answer","Category","Audience"]

TRELLO=[
 ["To Do","Write Q4 editorial calendar","Planning;High","2026-10-02","Content Manager"],
 ["To Do","Collect client testimonials","Marketing","2026-10-09","Marcus Lim"],
 ["To Do","Refresh portfolio page","Web;Design","2026-10-16","Sofia Chen"],
 ["Doing","Draft webinar recap","Blog","2026-09-26","Aisha Rahman"],
 ["Doing","Design newsletter template v3","Design","2026-09-30","Sofia Chen"],
 ["Review","Case study: Meridian Hub","Blog;Client","2026-09-24","Daniel Ong"],
 ["Review","Social calendar October","Social","2026-09-25","Aisha Rahman"],
 ["Done","Style guide update","Internal","2026-09-12","Content Manager"],
 ["Done","Onboarding checklist","Internal","2026-09-05","Priya Nair"],
 ["Done","Newsletter #41","Newsletter","2026-09-15","Aisha Rahman"],
]
TRELLO_HEADERS=["List","Card","Labels","Due","Members"]

INTEGRATIONS=[
 ["Zapier","Automation platform","Connect Notion to 7,000+ apps with triggers and actions","Free tier; from USD 20/mo","Read/write via Notion API","Content Manager"],
 ["Make","Automation platform","Visual multi-step scenarios with Notion modules","Free tier; from USD 9/mo","Read/write via Notion API","Content Manager"],
 ["Slack","Communication","Notifications, link previews, database alerts, Notion AI connector","Included with Slack","OAuth connection","All staff"],
 ["Google Drive","Storage","Embed files, link previews, Notion AI connector","Included with Google Workspace","OAuth connection","All staff"],
 ["Figma","Design","Live embeds of frames and prototypes","Free tier","Embed / link preview","Designers"],
 ["Typeform","Forms","Embed forms; send responses to a database via Zapier","Free tier; from USD 25/mo","Embed + Zapier","Marketing"],
 ["Loom","Video","Embed walkthrough recordings","Free tier","Embed","All staff"],
 ["GitHub","Development","Synced databases of issues and PRs; link previews","Free","OAuth connection","Web team"],
 ["Notion Web Clipper","Browser extension","Save web pages into a database","Free","Built-in","Content team"],
 ["Super.so","Website builder","Custom domain, themes and SEO for published Notion pages","From USD 16/mo","Public page","Marketing"],
 ["Notion Calendar","Calendar","Two-way calendar of database dates with Google Calendar","Free","Built-in","All staff"],
 ["Whimsical","Diagrams","Embed flowcharts and wireframes","Free tier","Embed","Designers"],
]
INTEGRATION_HEADERS=["Integration","Category","What it does for Brightwave","Pricing","Access model","Likely owner"]
