#!/usr/bin/env python3
"""Generate one self-contained folder per lab: README.md, lab.yaml, the mock data files
the lab needs (CSV, Markdown, JSON, images, PDF, scripts) and a printable instruction PDF.
The workflow PNG is added by build_lab_figures.py."""
import os, sys, re, csv, json, subprocess, shutil, textwrap
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
REPO=os.path.dirname(HERE)
import course_data as C
from data_domain1 import DOMAIN1; from data_domain2 import DOMAIN2
from data_domain3 import DOMAIN3; from data_domain4 import DOMAIN4
import mockdata as M
ACT=DOMAIN1+DOMAIN2+DOMAIN3+DOMAIN4
LABS=os.path.join(REPO,"labs")
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def slug(t): return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",t.lower()).strip("-"))
def folder(a): return os.path.join(LABS,f"lab-{a['num']:02d}-{slug(a['title'])}")
def W(path,text):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    open(path,"w",encoding="utf-8").write(textwrap.dedent(text).lstrip("\n"))
def CSV(path,headers,rows):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(headers); w.writerows(rows)
def JSONF(path,obj):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    json.dump(obj,open(path,"w",encoding="utf-8"),indent=2)

# ---------------------------------------------------------------- per-lab mock data
def data_lab1(d):
    W(f"{d}/brightwave-company-profile.md","""
    # Brightwave Media Pte Ltd — Company Profile

    **Founded:** 2019, Singapore · **Team:** 12 (content, design, account management) · **UEN (fictional):** 201912345K

    Brightwave Media is a content and digital-marketing agency. We plan, write, design and publish content for
    clients in retail, financial services, food and beverage, healthcare and real estate. Current clients include
    Nova Retail, Harbour Fintech, GreenLeaf Foods, Meridian Clinics and Skyline Properties.

    ## Purpose of the Notion workspace
    One connected workspace for the company wiki, content operations, client projects and the public Help Centre,
    governed by a content management policy with named page owners and verified pages.

    ## Values
    - Clarity over cleverness
    - Evidence before opinion
    - One source of truth
    """)
    CSV(f"{d}/workspace-structure.csv",["Level","Section","Page","Purpose"],[
        ["1","Company Home","Company Home","Entry point and dashboard"],
        ["2","Company Wiki","About Brightwave","Who we are, values, clients"],
        ["2","Company Wiki","Policies","Content management policy, naming conventions, style guide"],
        ["2","Company Wiki","Team Directory","People, roles, contacts"],
        ["2","Company Wiki","Onboarding","Checklist for new staff"],
        ["2","Content Hub","Blog Articles","Long-form articles"],
        ["2","Content Hub","Newsletters","Monthly newsletters"],
        ["2","Content Hub","Social Posts","Short-form posts and reels"],
        ["2","Client Projects","Nova Retail Launch","Client project page"],
        ["2","Client Projects","Meridian Patient Education Hub","Client project page"],
        ["2","Help Centre","Getting Started","Public help article"],
        ["2","Help Centre","FAQ","Public FAQ database"]])

def data_lab2(d):
    W(f"{d}/policies/content-management-policy.md","""
    # Content Management Policy

    **Owner:** Content Manager · **Review cycle:** every 90 days · **Applies to:** every page in the Brightwave Media workspace

    ## 1. Ownership
    Every page has exactly one named owner. The owner answers for accuracy, currency and access.

    ## 2. Verification
    Authoritative pages (policies, guidelines, client-facing help) are verified in Notion with a 90-day expiry.
    A page past its expiry is treated as unverified until the owner re-reviews it.

    ## 3. Naming
    Titles follow the Naming Conventions page: Title Case, no dates in titles, no abbreviations, one topic per page.

    ## 4. Templates
    New articles, briefs and tickets are created from approved templates only. Templates are owned by the Content Manager.

    ## 5. Permissions
    Permissions are granted by teamspace and group, never ad hoc to individuals, except guests on client project pages.
    Client guests receive Can comment on their project pages and Can edit content on shared databases.

    ## 6. Publishing
    Only pages in the Help Centre may be published to the web. Publishing requires a verified page and the publish checklist.

    ## 7. Retention
    Stale pages are archived, not deleted. A workspace export is taken quarterly and stored outside Notion.
    """)
    W(f"{d}/policies/naming-conventions.md","""
    # Naming Conventions

    **Owner:** Content Manager · **Review cycle:** every 90 days

    | Rule | Do | Don't |
    |---|---|---|
    | Title Case | Content Management Policy | content management policy |
    | No dates in titles | Newsletter — September | Newsletter 2026-09-01 |
    | No abbreviations | Search Engine Optimisation Checklist | SEO Chklst |
    | One topic per page | Requesting Changes | Requesting Changes and Pricing |
    | Databases are plural nouns | Tasks, Clients, Deliverables | Task DB |
    | Section pages carry an emoji icon and a cover | 📚 Company Wiki | Company Wiki (no icon) |
    """)
    CSV(f"{d}/page-owner-register.csv",["Page","Owner","Verify?","Expiry (days)"],[
        ["Company Home","Content Manager","No",""],["About Brightwave","Content Manager","Yes","90"],
        ["Content Management Policy","Content Manager","Yes","90"],["Naming Conventions","Content Manager","Yes","90"],
        ["Team Directory","Priya Nair","No",""],["Onboarding","Priya Nair","No",""],
        ["Blog Articles","Aisha Rahman","No",""],["Newsletters","Aisha Rahman","No",""],["Social Posts","Sofia Chen","No",""],
        ["Getting Started","Daniel Ong","No",""],["FAQ","Daniel Ong","No",""]])

def data_lab3(d):
    CSV(f"{d}/review-feedback.csv",["#","Target text","Action","Owner","Follow-up"],[
        ["1","Founded in 2019","Typo in the paragraph: 'Singpore' → 'Singapore'. Fix directly and resolve.","Content Manager","No"],
        ["2","Current clients include","Add Skyline Properties — signed last month.","Marcus Lim","Yes"],
        ["3","Team: 12","Confirm headcount after the two September hires.","Priya Nair","Yes"],
        ["4","Clarity over cleverness","Link this value to the Style Guide page once it exists.","Aisha Rahman","No"],
        ["5","One source of truth","Add one sentence on why Notion was chosen.","Content Manager","No"],
        ["6","Purpose of the Notion workspace","Mention the public Help Centre explicitly.","Daniel Ong","No"]])
    CSV(f"{d}/reminders.csv",["Comment #","Remind on","Owner"],[["2","tomorrow 9:00 AM","Marcus Lim"],["3","in 3 days 9:00 AM","Priya Nair"]])

def data_lab4(d):
    W(f"{d}/blog-article-draft.md","""
    # Five Content Trends for 2027

    Content teams are entering 2027 with smaller budgets and higher expectations. Based on Brightwave's work with clients across
    retail, fintech, food, healthcare and property, five trends will shape what gets made and how it is measured.

    ## Methodology
    We reviewed 180 pieces of client content published between January and August 2026, interviewed six marketing leads and
    compared engagement across blog, newsletter, social and video channels.

    ## Trend 1 — Long-form articles earn trust
    Articles above 1,200 words generated 2.4 times the return visits of short posts. Depth, sources and a clear table of contents matter more than frequency.

    ## Trend 2 — Short-form video earns reach
    Reels and short videos delivered the highest first-touch reach for retail and food clients, but converted best when paired with a long-form article.

    ## Trend 3 — Help centres become marketing
    Public help content ranked for buying-intent searches. Meridian's patient guides drew more new visitors than its campaign pages.

    ## Trend 4 — Newsletters move to owned platforms
    Open rates held steady while social reach fell; every client added a newsletter to the calendar.

    ## Trend 5 — Content operations in one workspace
    Teams running calendar, briefs, approvals and analytics in one place published 30% faster with fewer revision rounds.

    ## By the numbers
    (table inserted here)

    > "The teams that win are not the ones producing the most — they are the ones who can find, reuse and measure what they already have." — Marketing lead, Harbour Fintech

    ## What to do next
    - Audit your existing content before commissioning new pieces
    - Pair every short-form asset with a long-form anchor
    - Publish your help content publicly and measure it
    """)
    CSV(f"{d}/article-facts-table.csv",["Metric","2025","2026"],[
        ["Long-form return visits (index)","100","240"],["Short video first-touch reach (index)","100","310"],
        ["Help centre share of new visitors","18%","34%"],["Newsletter open rate","31%","33%"],["Average revision rounds","3.1","2.2"]])

def data_lab5(d):
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(f"{d}/media",exist_ok=True)
    def font(sz,b=False):
        try: return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if b else "/System/Library/Fonts/Supplemental/Arial.ttf",sz)
        except Exception: return ImageFont.load_default()
    img=Image.new("RGB",(1600,700),(0x1F,0x6F,0xEB)); dr=ImageDraw.Draw(img)
    for i in range(6): dr.ellipse([1100+i*60,-100+i*40,1500+i*60,300+i*40],outline=(255,255,255),width=3)
    dr.text((80,220),"Five Content Trends",font=font(88,True),fill=(255,255,255))
    dr.text((80,330),"for 2027",font=font(88,True),fill=(0xB3,0xD4,0xFF))
    dr.text((80,520),"Brightwave Media · Insights",font=font(36),fill=(255,255,255))
    img.save(f"{d}/media/brightwave-hero.png","PNG",optimize=True)
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(9,5),dpi=150)
    labels=["Long-form\nreturn visits","Short video\nreach","Help centre\nnew visitors","Newsletter\nopen rate"]
    v25=[100,100,18,31]; v26=[240,310,34,33]
    x=range(len(labels)); ax.bar([i-0.2 for i in x],v25,0.4,label="2025",color="#9CA3AF"); ax.bar([i+0.2 for i in x],v26,0.4,label="2026",color="#1F6FEB")
    ax.set_xticks(list(x)); ax.set_xticklabels(labels,fontname="Arial"); ax.set_title("Content performance 2025 vs 2026 (index / %)",fontname="Arial",fontsize=13)
    ax.legend(frameon=False); ax.spines[["top","right"]].set_visible(False); fig.tight_layout(); fig.savefig(f"{d}/media/brightwave-chart.png"); plt.close(fig)
    # media kit as a small DOCX -> PDF
    doc=Document(); doc.add_heading("Brightwave Media — Media Kit 2026",0)
    doc.add_paragraph("Audience: 12,400 newsletter subscribers · 38,000 monthly blog readers · 21,000 social followers.")
    doc.add_paragraph("Formats: sponsored articles, newsletter placements, social series, video scripts.")
    doc.add_paragraph("Contact: hello@brightwave.example · +65 6100 0000 (fictional)")
    doc.save(f"{d}/media/brightwave-media-kit.docx")
    W(f"{d}/embed-links.md","""
    # Links to embed in Lab 5
    - Video (YouTube): https://www.youtube.com/watch?v=oTahLEX3NXo  (Notion — "What is Notion?")
    - Web bookmark: https://www.notion.com/help/intro-to-databases
    - Map: https://maps.app.goo.gl/  (search "Woods Square Singapore" and copy the share link)
    - PDF: media/brightwave-media-kit.pdf (upload as a file block)
    """)
    W(f"{d}/code-sample.py",'''
    """UTM tagging helper used in Brightwave's tracking script examples."""
    from urllib.parse import urlencode

    def utm_link(url: str, source: str, medium: str, campaign: str) -> str:
        """Return the URL with UTM parameters appended."""
        params = {"utm_source": source, "utm_medium": medium, "utm_campaign": campaign}
        joiner = "&" if "?" in url else "?"
        return f"{url}{joiner}{urlencode(params)}"

    if __name__ == "__main__":
        print(utm_link("https://brightwave.notion.site/five-content-trends", "newsletter", "email", "trends-2027"))
    ''')
    W(f"{d}/brand-footer.md","""
    # Brand footer (synced block)
    ---
    💬 **Brightwave Media** · Content that earns trust. Questions? hello@brightwave.example · Visit the Help Centre → (link the Help Centre page)

    # Article checklist (button: Insert blocks → to-do list)
    - [ ] SEO title under 60 characters
    - [ ] Meta description under 155 characters
    - [ ] Hero image with caption and alt text
    - [ ] Brand footer synced block added
    """)

def data_lab6(d):
    W(f"{d}/style-guide.md","""
    # Brightwave Content Style Guide (Notion)

    **Owner:** Content Manager · **Verified:** every 90 days

    ## Page settings
    - Font: Default (never Serif or Mono for articles)
    - Small text: off · Full width: on for articles
    - Icons: emoji only · Covers: section pages only (never on articles)

    ## Colour
    - Text colour blue: key statistics and figures
    - Background yellow: cautions and caveats
    - No other text colours in body copy

    ## Callouts
    | Purpose | Icon | Background |
    |---|---|---|
    | Tip | 💡 | Blue |
    | Warning / caution | ⚠️ | Yellow |
    | Policy reference | 📕 | Red — must @-mention the policy page |

    ## Structure
    - One Heading 1 per page; Heading 2 per section; Heading 3 for sub-points
    - Table of contents block on every article longer than 800 words
    - Every article links back to Content Hub and forward to at least one related article
    """)
    CSV(f"{d}/navigation-map.csv",["Order","Group","Link to page"],[
        ["1","Start here","Five Content Trends for 2027"],["2","Start here","Content Trends Webinar Recap"],
        ["3","Sections","Blog Articles"],["4","Sections","Newsletters"],["5","Sections","Social Posts"],
        ["6","Reference","Style Guide"],["7","Reference","Content Management Policy"],["8","Reference","Company Home"]])
    W(f"{d}/equations.md","""
    # Equations for the Pricing Formulas page

    ## Block equation — monthly retainer
    ```
    R = h \\times r_{b} + F_{p}
    ```
    where R is the monthly retainer, h the base hours, r_b the blended hourly rate and F_p the platform fees.

    ## Inline equation — return on investment
    ```
    $$ROI = \\frac{Gain - Cost}{Cost}$$
    ```

    ## Inline equation — engagement rate
    ```
    $$E = \\frac{Comments + Reactions}{Unique\\ Visitors}$$
    ```
    """)

def data_lab7(d):
    CSV(f"{d}/content-calendar.csv",M.CALENDAR_HEADERS,M.content_calendar())
def data_lab8(d):
    CSV(f"{d}/projects.csv",M.PROJECT_HEADERS,M.PROJECTS); CSV(f"{d}/tasks.csv",M.TASK_HEADERS,M.TASKS)
def data_lab9(d):
    CSV(f"{d}/clients.csv",M.CLIENT_HEADERS,M.CLIENTS); CSV(f"{d}/deliverables.csv",M.DELIVERABLE_HEADERS,M.DELIVERABLES)
    W(f"{d}/formulas.md","""
    # Formulas used in Lab 9

    | Property | Database | Formula | Notes |
    |---|---|---|---|
    | Days Left | Projects | `dateBetween(prop("Dates").end, now(), "days")` | `.end` reads the end of a date range; negative means overdue |
    | Health | Projects | `if(prop("Tasks Done") >= 0.8, "🟢 On track", if(prop("Days Left") < 7, "🔴 At risk", "🟡 Watch"))` | nested `if`; Tasks Done is a percent rollup (0–1) |
    | Budget/Hour | Projects | `format(round(prop("Budget (SGD)") / prop("Total Hours")))` | `round` then `format` to text; guard division by zero with `if(prop("Total Hours") == 0, "—", …)` |
    | Overdue | Tasks | `and(prop("Due") < now(), prop("Status") != "Done")` | boolean shown as a checkbox |
    | Priority | Ideas (Lab 12) | `prop("Impact") - prop("Effort")` | sort descending |

    ## Functions in one line each
    - `prop("Name")` — read a property of this row
    - `if(condition, then, else)` — branch
    - `dateBetween(a, b, "days")` — difference between dates
    - `now()` — the current date-time
    - `round(x)`, `format(x)`, `toNumber(x)` — numbers and text conversion
    - `and(a, b)`, `or(a, b)`, `empty(x)` — logic
    """)
    CSV(f"{d}/automation-rules.csv",["Type","Database","Trigger","Action 1","Action 2"],[
        ["Automation","Deliverables","Status is set to Approved","Edit property Approved On = now","Send notification to Owner: 'Deliverable approved — schedule publishing'"],
        ["Button","Projects (page body)","Button clicked: Log weekly review","Add page to Tasks: Name = Weekly review, Project = this project, Due = today + 7 days",""],
        ["Automation (optional)","Tasks","Status is set to Done on a Blocking task","Send Slack notification to #content-ops",""]])
    CSV(f"{d}/cms-market-comparison.csv",["Criterion","Notion","Confluence","Airtable","Monday.com"],[
        ["Entry price (per user / month, indicative)","Free; Plus ~USD 10; Business ~USD 20","",""," "],
        ["Documents and wiki","Native pages, wikis, verification","","",""],
        ["Databases and views","Table, board, calendar, timeline, gallery, chart, form","","",""],
        ["Relations, rollups, formulas","Yes","","",""],
        ["Automations","Database automations, buttons","","",""],
        ["Permissions and teamspaces","Workspace, teamspace, page, database levels","","",""],
        ["Public publishing","Publish to web (notion.site)","","",""],
        ["API and integrations","REST API, 1,900+ embeds, connections","","",""],
        ["AI","Notion AI (Business and above)","","",""],
        ["Best fit for Brightwave","","","",""]])

def data_lab10(d):
    CSV(f"{d}/access-matrix.csv",["Role","Company Wiki","Content Hub","Client Projects","Help Centre","Content Calendar","Tasks"],[
        ["Content Manager (owner)","Full access","Full access","Full access","Full access","Full access","Full access"],
        ["Editors (group)","Can edit","Can edit","Can edit","Can edit","Can edit content","Can edit content"],
        ["Designers (group)","Can comment","Can edit","Can edit","Can comment","Can edit content","Can edit content"],
        ["Account Managers (group)","Can comment","Can comment","Full access","Can comment","Can view","Can edit content"],
        ["Client guest","No access","No access","Can comment (own project only)","Public","No access","Can edit content (own project view)"],
        ["Public visitor","No access","No access","No access","View (published)","No access","No access"]])
    CSV(f"{d}/page-analytics-sample.csv",M.ANALYTICS_HEADERS,M.page_analytics())
    W(f"{d}/publish-checklist.md","""
    # Publish-to-web checklist (Help Centre)
    - [ ] Page is verified and its owner is named
    - [ ] No client names, personal data or internal links in the content
    - [ ] Synced brand footer present; images captioned
    - [ ] Search engine indexing: ON · Allow duplicate as template: OFF · Allow comments: OFF
    - [ ] Public home page set; navigation tested in a private window
    - [ ] Page analytics baseline recorded (views, unique visitors) on publish day
    """)

def data_lab11(d):
    CSV(f"{d}/trello-board-export.csv",M.TRELLO_HEADERS,M.TRELLO)
    W(f"{d}/embed-links.md","""
    # Links to embed in Lab 11
    - Google Drive file (any shareable file from your own Drive, or https://docs.google.com/document/d/1YiKwg-dhXgexiOQCIILpqEDk8ZncK1YP/edit)
    - Figma: https://www.figma.com/community/file/1035203688168086460 (community file — open, then copy the file link)
    - Loom: https://www.loom.com/share/ (record a 20-second walkthrough and paste the share link)
    - Google Maps: search "Woods Square Singapore" and copy the share link
    - GitHub pull request or issue: https://github.com/makenotion/notion-sdk-js/pulls (any PR link)
    """)
    api=f"{d}/notion-api"
    W(f"{api}/.env.example","""
    # Copy to .env and fill in — never commit .env or paste the token into a Notion page
    NOTION_TOKEN=<paste-your-internal-integration-secret-here>
    DATABASE_ID=00000000000000000000000000000000
    NOTION_VERSION=2025-09-03
    """)
    JSONF(f"{api}/query-database.json",{"filter":{"property":"Status","status":{"does_not_equal":"Published"}},
          "sorts":[{"property":"Publish Date","direction":"ascending"}],"page_size":20})
    JSONF(f"{api}/create-page.json",{"parent":{"data_source_id":"<DATA_SOURCE_ID>"},
          "properties":{"Name":{"title":[{"text":{"content":"Created via the Notion API — Brightwave Bot"}}]},
                        "Status":{"status":{"name":"Draft"}},"Channel":{"select":{"name":"Blog"}},
                        "Publish Date":{"date":{"start":"2026-10-30"}}}})
    W(f"{api}/query-database.sh","""
    #!/usr/bin/env bash
    # Query the Content Calendar data source. Requires .env with NOTION_TOKEN and DATABASE_ID.
    set -euo pipefail
    cd "$(dirname "$0")"; set -a; source .env; set +a
    # 1) Resolve the data source id from the database (API 2025-09-03: a database holds data_sources[])
    DS=$(curl -s "https://api.notion.com/v1/databases/${DATABASE_ID}" \\
      -H "Authorization: Bearer ${NOTION_TOKEN}" -H "Notion-Version: ${NOTION_VERSION:-2025-09-03}" \\
      | python3 -c 'import sys,json; print(json.load(sys.stdin)["data_sources"][0]["id"])')
    echo "data source: $DS"
    # 2) Query it with the filter body
    curl -s -X POST "https://api.notion.com/v1/data_sources/${DS}/query" \\
      -H "Authorization: Bearer ${NOTION_TOKEN}" -H "Notion-Version: ${NOTION_VERSION:-2025-09-03}" \\
      -H "Content-Type: application/json" --data @query-database.json \\
      | python3 -c '
    import sys, json
    for r in json.load(sys.stdin)["results"]:
        p = r["properties"]
        name = "".join(t["plain_text"] for t in p["Name"]["title"])
        status = (p.get("Status", {}).get("status") or {}).get("name", "")
        print(f"{name:45s} {status}")'
    """)
    W(f"{api}/notion_api.py",'''
    #!/usr/bin/env python3
    """Minimal Notion API client for Lab 11 — query the Content Calendar, then create a page.

    Usage:  python3 notion_api.py query
            python3 notion_api.py create
    Reads NOTION_TOKEN, DATABASE_ID and NOTION_VERSION from .env in this folder (no extra packages).
    """
    import json, os, sys, urllib.request

    HERE = os.path.dirname(os.path.abspath(__file__))
    def load_env():
        env = {}
        for line in open(os.path.join(HERE, ".env")):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1); env[k.strip()] = v.strip()
        return env
    ENV = load_env()
    API = "https://api.notion.com/v1"
    HEADERS = {"Authorization": f"Bearer {ENV['NOTION_TOKEN']}",
               "Notion-Version": ENV.get("NOTION_VERSION", "2025-09-03"),
               "Content-Type": "application/json"}

    def call(method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(API + path, data=data, headers=HEADERS, method=method)
        with urllib.request.urlopen(req) as r:
            return json.load(r)

    def data_source_id():
        db = call("GET", f"/databases/{ENV['DATABASE_ID']}")
        return db["data_sources"][0]["id"]          # a database holds one or more data sources

    def query():
        ds = data_source_id()
        body = json.load(open(os.path.join(HERE, "query-database.json")))
        res = call("POST", f"/data_sources/{ds}/query", body)
        for row in res["results"]:
            p = row["properties"]
            name = "".join(t["plain_text"] for t in p["Name"]["title"])
            status = (p.get("Status", {}).get("status") or {}).get("name", "")
            print(f"{name:45s} {status}")
        print(f"{len(res['results'])} rows")

    def create():
        ds = data_source_id()
        body = json.load(open(os.path.join(HERE, "create-page.json")))
        body["parent"] = {"data_source_id": ds}
        page = call("POST", "/pages", body)
        print("created:", page["url"])

    if __name__ == "__main__":
        {"query": query, "create": create}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
    ''')
    W(f"{d}/api-data-model.md","""
    # The Notion API data model (version 2025-09-03)

    ```
    Database ──── has one or more ───▶ Data source ──── has zero or more ───▶ Page (row)
    (container; inline or full page)   (schema = properties)                 (properties + content blocks)
    ```

    | Object | Key fields | Notes |
    |---|---|---|
    | Database | `object: "database"`, `id`, `title`, `data_sources[] {id, name}`, `is_inline`, `in_trash`, `public_url`, `parent`, `created_time`, `last_edited_time` | Permissions are managed at the database level |
    | Data source | `id`, `properties` (the schema), parent database | Use *Retrieve a data source* for the schema; query rows with `POST /data_sources/{id}/query` |
    | Page | `id`, `properties`, `parent {data_source_id}`, `url` | Every row of a data source is a page |

    Before September 2025 a database had exactly one data source, so the API merged the two concepts. Upgrade the
    `Notion-Version` header to `2025-09-03` to receive the `data_sources` array. Integrations must be *connected* to a page or
    database (⋯ → Connections) before they can read it. Source: developers.notion.com/reference/database
    """)
    CSV(f"{d}/integration-catalogue.csv",M.INTEGRATION_HEADERS+["Score: job to be done (1-5)","Score: permissions (1-5)","Score: cost (1-5)","Score: maintenance (1-5)","Recommend? (Y/N)"],
        [r+["","","","",""] for r in M.INTEGRATIONS])
    W(f"{d}/export-checklist.md","""
    # Export and data integrity checklist
    - [ ] Page export: Five Content Trends for 2027 → PDF (include sub-pages: off)
    - [ ] Workspace export: Settings → Export all workspace content → Markdown & CSV, include sub-pages
    - [ ] ZIP opened; one CSV per database present (Content Calendar, Tasks, Projects, Clients, Deliverables, Content Metrics)
    - [ ] Export stored outside Notion (company drive) with the date: ____________
    - [ ] Next quarterly export scheduled in the Tasks database with a reminder
    - [ ] Trash retention noted: deleted pages recoverable for 30 days; page history per plan
    """)

def data_lab12(d):
    W(f"{d}/ai-prompts.md","""
    # Prompts used in Lab 12

    ## Prompt 1 — Writer draft (Help Centre article)
    > Write a Help Centre article titled "How to Request a Content Change" for clients of a content agency. Audience: marketing managers.
    > Include: when to use the request form, what information to provide (page link, change, deadline, approver), turnaround times
    > (blog 5 working days, social 2, newsletter 3), how to track the request in Notion, and who to contact. Use short headings and a checklist. Tone: friendly, professional.

    ## Prompt 2 — AI block (custom output on the article)
    > Using this page as context, write three LinkedIn post drafts (under 60 words each) that each highlight one trend and end with a question to the reader.

    ## Prompt 3 — Q&A across the workspace
    > What does the Content Management Policy say about verification expiry, and which pages are currently verified?

    ## Prompt 4 — Q&A on client projects (All sources → Client Work teamspace)
    > Which projects are at risk this month and why? Cite the pages you used.

    ## Prompt 5 — Build with AI
    > A public FAQ database for a content agency's Help Centre with properties Question, Answer, Category (select), Audience (select: Client, Prospect, Staff) and Last reviewed (date); include a board view grouped by Category and a table view sorted by Last reviewed.

    ## Prompt 6 — Improvement ideas (source: Visitor Feedback database)
    > From the Visitor Feedback database, list the ten most common visitor problems, how many entries mention each, and propose one specific Help Centre improvement for each problem.
    """)
    CSV(f"{d}/visitor-feedback.csv",M.FEEDBACK_HEADERS,M.visitor_feedback())
    CSV(f"{d}/faq-seed.csv",M.FAQ_HEADERS,M.FAQ_SEED)
    W(f"{d}/improvement-ideas-template.md","""
    # Visitor Experience Plan — template

    **Recommendation to management (3 sentences):**
    1. …
    2. …
    3. …

    | # | Visitor problem | Evidence (count / examples) | Proposed improvement | Impact (1-5) | Effort (1-5) | Priority = Impact − Effort | Owner |
    |---|---|---|---|---|---|---|---|
    | 1 | | | | | | | |
    | 2 | | | | | | | |
    | … | | | | | | | |
    | 10 | | | | | | | |

    Turn the table into an inline database (⋮⋮ → Turn into → Database) to sort by Priority.
    """)

DATA={1:data_lab1,2:data_lab2,3:data_lab3,4:data_lab4,5:data_lab5,6:data_lab6,7:data_lab7,8:data_lab8,9:data_lab9,10:data_lab10,11:data_lab11,12:data_lab12}

# ---------------------------------------------------------------- README + lab.yaml
def build_readme(a,d):
    L=[f"# Lab {a['num']:02d}: {a['title']}\n",
       f"**Topic {a['topic']:02d}** · **Day {a['day']}** · **{a['level']}** · **{a['km']} · {a['am']}** · **{a['apps']}**\n",
       "## Goal\n",a["desc"]+"\n","## What you will build\n",a["build"]+"\n",
       f"![Lab {a['num']:02d} workflow](LAB-{a['num']:02d}-Workflow.png)\n",
       f"*Figure. Lab {a['num']:02d} workflow — the four stages and the artifact produced.*\n",
       "## Files in this folder\n"]
    for fn,desc in a["files"]: L.append(f"- `{fn}` — {desc}")
    L+=[f"- `LAB-{a['num']:02d}-Instructions.pdf` — printable detailed guide",
        f"- `LAB-{a['num']:02d}-Workflow.png` — the workflow diagram above",
        "- `lab.yaml` — lab metadata (topic, K/A codes, files, acceptance check)\n",
        "## Procedure\n"]
    for i,(t,dd) in enumerate(a["steps"],1): L+=[f"{i}. **{t}**\n",f"   {dd}\n"]
    L+=["## Acceptance check\n",a["test"]+"\n","## Evidence to retain\n","- "+a["evidence"]+"\n",
        "## Steps checklist\n"]+[f"- [ ] Step {i}: {t}" for i,(t,_) in enumerate(a["steps"],1)]
    L+=["\n---\n",f"*{C.TITLE} · {C.COURSE_CODE} · Version {C.VERSION} · © 2026 {C.ORG}*"]
    open(os.path.join(d,"README.md"),"w",encoding="utf-8").write("\n".join(L))

def build_yaml(a,d):
    import yaml
    doc={"lab":a["num"],"title":a["title"],"course":{"title":C.TITLE,"code":C.COURSE_CODE,"version":C.VERSION},
         "topic":a["topic"],"day":a["day"],"level":a["level"],"alignment":{"knowledge":a["km"],"ability":a["am"]},
         "tools":a["apps"],"objective":a["objective"],"goal":a["desc"],"build":a["build"],
         "workflow":a["flow"],"files":[{"path":fn,"description":desc} for fn,desc in a["files"]],
         "steps":[{"n":i,"title":t,"detail":dd,"done":False} for i,(t,dd) in enumerate(a["steps"],1)],
         "acceptance_check":a["test"],"evidence":a["evidence"]}
    with open(os.path.join(d,"lab.yaml"),"w",encoding="utf-8") as f:
        yaml.safe_dump(doc,f,sort_keys=False,allow_unicode=True,width=110)

# ---------------------------------------------------------------- instruction DOCX -> PDF
def build_instructions(a,d):
    doc=Document(); st=doc.styles["Normal"]; st.font.name="Arial"; st.font.size=Pt(10.5)
    for s in doc.sections:
        s.top_margin=Inches(0.8); s.bottom_margin=Inches(0.8); s.left_margin=Inches(0.9); s.right_margin=Inches(0.9)
    logo=os.path.join(REPO,"courseware","assets","tertiary-infotech-logo.png")
    if os.path.exists(logo):
        p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.RIGHT; p.add_run().add_picture(logo,height=Inches(0.42))
    h=doc.add_paragraph(); r=h.add_run(f"LAB {a['num']:02d} — INSTRUCTIONS"); r.font.size=Pt(11); r.font.bold=True; r.font.color.rgb=RGBColor(0x1F,0x6F,0xEB)
    t=doc.add_paragraph(); r=t.add_run(a["title"]); r.font.size=Pt(20); r.font.bold=True
    m=doc.add_paragraph(); r=m.add_run(f"Topic {a['topic']:02d}  ·  Day {a['day']}  ·  {a['level']}  ·  {a['apps']}  ·  Alignment {a['km']} · {a['am']}"); r.font.size=Pt(9); r.font.color.rgb=RGBColor(0x5B,0x63,0x72)
    fig=os.path.join(d,f"LAB-{a['num']:02d}-Workflow.png")
    def head(txt):
        p=doc.add_paragraph(); r=p.add_run(txt); r.font.size=Pt(12); r.font.bold=True; r.font.color.rgb=RGBColor(0x16,0x1B,0x26)
        p.paragraph_format.space_before=Pt(12); p.paragraph_format.space_after=Pt(4)
    head("Goal"); doc.add_paragraph(a["desc"])
    head("What you will build"); doc.add_paragraph(a["build"])
    if os.path.exists(fig):
        ip=doc.add_paragraph(); ip.alignment=WD_ALIGN_PARAGRAPH.CENTER; ip.add_run().add_picture(fig,width=Inches(6.5))
    head("Files supplied in this folder")
    for fn,desc in a["files"]: doc.add_paragraph(f"{fn} — {desc}",style="List Bullet")
    head("Detailed procedure")
    for i,(ttl,dd) in enumerate(a["steps"],1):
        p=doc.add_paragraph(); r=p.add_run(f"Step {i}. {ttl}"); r.font.bold=True; r.font.size=Pt(10.5)
        p.paragraph_format.space_before=Pt(8); p.paragraph_format.space_after=Pt(2); doc.add_paragraph(dd)
    head("Acceptance check"); doc.add_paragraph(a["test"])
    head("Evidence to retain"); doc.add_paragraph(a["evidence"])
    f=doc.add_paragraph(); r=f.add_run(f"{C.TITLE} · {C.COURSE_CODE} · Version {C.VERSION} · © 2026 {C.ORG}")
    r.font.size=Pt(8); r.font.color.rgb=RGBColor(0x8A,0x93,0xA3); f.paragraph_format.space_before=Pt(18)
    dp=os.path.join(d,f"LAB-{a['num']:02d}-Instructions.docx"); doc.save(dp); return dp

def pdfs(docxs):
    soffice=shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    for dp in docxs:
        subprocess.run([soffice,"--headless","--convert-to","pdf","--outdir",os.path.dirname(dp),dp],check=False,capture_output=True)
        if os.path.exists(dp.replace(".docx",".pdf")): os.remove(dp)

def main(stage="all"):
    os.makedirs(LABS,exist_ok=True)
    if stage in ("all","data"):
        for a in ACT:
            d=folder(a); os.makedirs(d,exist_ok=True); DATA[a["num"]](d); build_readme(a,d); build_yaml(a,d)
            print(f"lab {a['num']:02d} -> {os.path.basename(d)}")
        # media kit docx -> pdf for lab 5
        mk=os.path.join(folder(ACT[4]),"media","brightwave-media-kit.docx")
        if os.path.exists(mk): pdfs([mk])
        # labs index
        L=[f"# Hands-On Labs — {C.TITLE}\n",C.SCENARIO+"\n","| Lab | Topic | Day | Title | Level | K/A |","|---:|---:|---:|---|---|---|"]
        for a in ACT: L.append(f"| {a['num']:02d} | {a['topic']:02d} | {a['day']} | [{a['title']}]({os.path.basename(folder(a))}/README.md) | {a['level']} | {a['km']} · {a['am']} |")
        L+=["\nEach folder contains `README.md`, `lab.yaml`, the mock data the lab needs, `LAB-NN-Instructions.pdf` and `LAB-NN-Workflow.png`.",
            f"\n*{C.COURSE_CODE} · Version {C.VERSION} · © 2026 {C.ORG}*"]
        open(os.path.join(LABS,"README.md"),"w").write("\n".join(L))
    if stage in ("all","pdf"):
        docxs=[build_instructions(a,folder(a)) for a in ACT]; pdfs(docxs); print("instruction PDFs done")

if __name__=="__main__": main(sys.argv[1] if len(sys.argv)>1 else "all")
