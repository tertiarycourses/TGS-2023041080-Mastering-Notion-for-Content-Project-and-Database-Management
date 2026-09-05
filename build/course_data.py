"""
SINGLE SOURCE OF TRUTH — Mastering Notion for Content, Project, and Database Management.

Every artifact (slide deck PPT, Lesson Plan LP, Learner Guide LG + Markdown mirror,
the labs/ folders and the assessment) is generated from this module plus
data_domain1.py … data_domain4.py (one file per Learning Unit), so titles, lab
numbering, learning outcomes, the schedule and the assessment never drift apart.

Day 1  LU1 Foundations of Notion and Workspace Management  (Topics 1–2)
       LU2 Content Creation and Management                 (Topics 3–4)
Day 2  LU3 Mastering Databases in Notion                   (Topics 5–6)
       LU4 Collaboration, Publishing, and Integrations     (Topics 7–9)

Content sources: the approved v5 trainer deck (reference/), the Notion Help Center
(New to Notion, Intro to databases, Creating a database, Notion AI FAQs,
Everything you can do with Notion AI), the Notion API reference (Database object)
and Thomas Frank's "Notion Databases: The Ultimate Beginner's Guide".
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Mastering Notion for Content, Project, and Database Management"
SHORT_TITLE  = "Mastering Notion for Content, Project, and Database Management"
COURSE_CODE  = "TGS-2023041080"
VERSION      = "v6"
VERSION_DATE = "5 September 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 2
TRAINING_HOURS   = 14
ASSESSMENT_HOURS = 2
COURSE_URL   = "https://www.tertiarycourses.com.sg/wsq-mastering-notion-for-content-project-and-database-management.html"
GITHUB_REPO  = "https://github.com/tertiarycourses/TGS-2023041080-Mastering-Notion-for-Content-Project-and-Database-Management"
LMS_URL      = "https://lms-tms.tertiaryinfotech.com"

# Skills Framework alignment
TSC_TITLE = "Content Management"
TSC_CODE  = "ICT-SNM-3026-1.1"

# ------------------------------------------------------------------ outcomes (verbatim from the TGS record)
LEARNING_OUTCOMES = [
    "LO1: Implement content management policies on Notion adhering to organizational guidelines and permissions",
    "LO2: Post and update content on Notion, ensuring adherence to content creation and curation guidelines",
    "LO3: Maintain web properties and assets in Notion, while staying aware of market offerings",
    "LO4: Report on performance metrics, recommend appropriate plug-ins, and generate ideas to enhance customer and visitor experiences on Notion",
]

KNOWLEDGE = [
    ("K1", "Content management policies, guidelines and permissions on content management"),
    ("K2", "Web content for deployment"),
    ("K3", "Organisation's web properties and assets"),
    ("K4", "Creation and curation of web content guidelines"),
    ("K5", "Web content and platform management systems"),
    ("K6", "Types of performance metrics of content management systems"),
    ("K7", "Customer and visitor experience on web properties and assets"),
    ("K8", "Types of market offerings on content management systems"),
    ("K9", "Types of plug-ins to manage the organisation's web properties and assets"),
]
ABILITIES = [
    ("A1", "Implement content management policies, guidelines and permissions on content management"),
    ("A2", "Post and update content on content management systems"),
    ("A3", "Maintain web properties and assets to uphold standards on user experience"),
    ("A4", "Maintain awareness of market offerings on content management systems"),
    ("A5", "Report on metrics to measure performance of content management systems"),
    ("A6", "Recommend the adoption of appropriate plug-ins to manage and maintain the organisation's web properties and assets"),
    ("A7", "Generate ideas to improve customer and visitor experience on web properties and assets"),
]

# Learning Units (from the approved Course Proposal)
LEARNING_UNITS = [
    ("LU1", "Foundations of Notion and Workspace Management", [1, 2], "LO1", "K1, K5 · A1"),
    ("LU2", "Content Creation and Management",                [3, 4], "LO2", "K2, K4 · A2"),
    ("LU3", "Mastering Databases in Notion",                  [5, 6], "LO3", "K3, K7 · A3, A4"),
    ("LU4", "Collaboration, Publishing, and Integrations",    [7, 8, 9], "LO4", "K6, K8, K9 · A5, A6, A7"),
]

# ------------------------------------------------------------------ the course scenario
SCENARIO_ORG = "Brightwave Media Pte Ltd"
SCENARIO = ("Brightwave Media Pte Ltd is a twelve-person Singapore content and digital-marketing agency. "
            "It is moving its company wiki, content operations, client projects and public help centre "
            "into one Notion workspace. Every lab builds one piece of that workspace, so by the end of "
            "Day 2 you have a complete, governed content management system.")

# ------------------------------------------------------------------ topics (the 9 approved topics)
# concepts are (title, caption) tuples — rendered as dense tile grids on the deck and as
# key-concept bullets in the LP / LG.
TOPICS = [
    dict(num=1, code="01", lu="LU1", day=1, ka="A1 · K1",
         title="Introduction to Notion",
         subtitle="Overview of Notion · what is a block · first page and subpage · workspace and sidebar · navigating and customising · wikis and verified pages",
         concepts=[
            ("One connected workspace", "Notion combines documents, wikis, project trackers and databases in one tool, so content, projects and data live together instead of across five apps."),
            ("Everything is a block", "Text, headings, images, tables, embeds and even databases are blocks. Blocks can be transformed into other types and rearranged by dragging."),
            ("Pages nest inside pages", "A page holds blocks and sub-pages, giving an unlimited hierarchy. Breadcrumbs and the sidebar show where you are."),
            ("The workspace and sidebar", "The sidebar is the map: Teamspaces for shared work, Private for your own pages, Shared for pages shared with you, plus Favorites, Templates, Import and Trash."),
            ("Workspaces are separate", "Each workspace has its own members, plan and content. Switch or add another account from the workspace switcher; move top-level pages to migrate content."),
            ("Wikis and verified pages", "Turn a teamspace page into a wiki to add owners, verification and expiry, so the organisation knows which content is authoritative and current."),
         ]),
    dict(num=2, code="02", lu="LU1", day=1, ka="A1 · K5",
         title="Workspace Collaboration Tools",
         subtitle="Collaborate within a workspace · comments, mentions and reminders · updates and notifications · search",
         concepts=[
            ("Real-time co-editing", "Several people edit the same page at once; avatars show who is where, and page history lets you restore an earlier version."),
            ("Comments and discussions", "Top-level page discussions and inline comments keep feedback next to the content; resolve, react to or reopen threads."),
            ("@-mentions", "Type @ to mention a person, a page or a date. A mentioned person is notified; a mentioned page becomes a link and a backlink."),
            ("Reminders", "Any date mention can carry a reminder, so a review date notifies the owner on the day, in the app and by email or push."),
            ("Updates and notifications", "The Inbox (Updates) collects mentions, comments and page changes across the workspace; tune email and mobile notifications in Settings."),
            ("Search that understands structure", "Quick Find searches titles and content; filter by teamspace, creator, date or page, sort results and search inside a database."),
         ]),
    dict(num=3, code="03", lu="LU2", day=1, ka="A2 · K2",
         title="Pages and Content Blocks",
         subtitle="Writing, editing and customisation · keyboard shortcuts · columns, tables, headings and dividers · images, files and media · code blocks and buttons · synced blocks",
         concepts=[
            ("Slash commands create blocks", "Type / for every block type: basic (text, headings, lists, toggles, quotes, callouts), database, media, embeds and advanced blocks."),
            ("Markdown and shortcuts", "Markdown-style shortcuts (#, -, [], >, ```) and keyboard shortcuts (Cmd/Ctrl+B, Cmd/Ctrl+E, Cmd/Ctrl+Shift+0-9) make writing fast."),
            ("Structure with layout blocks", "Headings build the table of contents, dividers separate sections, simple tables hold small grids and drag-to-side creates columns."),
            ("Media in context", "Upload or embed images, files, video, audio, PDFs and web bookmarks; align, resize and caption them where the content needs them."),
            ("Code blocks and buttons", "Code blocks add syntax highlighting, wrap and copy; buttons insert blocks, add pages or edit properties in one click."),
            ("Synced blocks", "Content that must appear in several places (a footer, a policy notice) is written once in a synced block and edited everywhere at once."),
         ]),
    dict(num=4, code="04", lu="LU2", day=1, ka="A2 · K4",
         title="Advanced Content Techniques",
         subtitle="Customising and styling content · links, backlinks and efficient navigation · math equations and diverse media types",
         concepts=[
            ("Style with intent", "Text colours, background colours, fonts (default, serif, mono), small text and full width are used per the style guide, not per mood."),
            ("Callouts, icons and covers", "Callouts highlight warnings and tips; page icons and cover images make pages recognisable in the sidebar and in search."),
            ("Links and backlinks", "Link inline with @ or [[; every link creates a backlink on the target page, so readers can navigate in both directions."),
            ("Navigation hubs", "A home page with link-to-page blocks, a table of contents block and breadcrumbs gives readers one entry point to the whole space."),
            ("Math equations", "KaTeX equations render as a block (/math) or inline ($$), for pricing formulas, KPIs and technical documentation."),
            ("Curation guidelines", "A style guide, naming convention and review workflow turn individual pages into a consistent, trustworthy body of content."),
         ]),
    dict(num=5, code="05", lu="LU3", day=2, ka="A3 · K3",
         title="Database Essentials",
         subtitle="Introduction to databases in Notion · properties and data sources · tasks, dependencies and linked databases · database views",
         concepts=[
            ("A database is a set of pages", "Every row, card or event is a full Notion page with properties on top and free content below. Full-page or inline, the data is the same."),
            ("Properties give structure", "Title, text, number, select, multi-select, status, date, person, files, checkbox, URL, email, phone, formula, relation, rollup, created/edited time and ID."),
            ("Databases vs spreadsheets", "There are no cell coordinates; each row has the same properties with its own values. That is why the same data can be shown as a board or calendar."),
            ("Views change the lens", "Table, board, list, calendar, timeline, gallery, chart and form are layouts of one data source; each view keeps its own filters, sorts and groups."),
            ("Filters, sorts and groups", "Simple filters target one property; advanced filters combine AND/OR groups. A filtered view also sets defaults on new rows (a forcing function)."),
            ("Data sources and linked views", "A linked view shows an existing data source in another page with its own views; sub-items and dependencies model task hierarchies and date shifting."),
         ]),
    dict(num=6, code="06", lu="LU3", day=2, ka="A4 · K7",
         title="Advanced Database Features",
         subtitle="Relations, rollups and database templates · formula basics and syntax · database automations",
         concepts=[
            ("Relations connect databases", "A relation property links rows in the same or another database, optionally two-way, so a project knows its tasks and a task knows its project."),
            ("Rollups summarise relations", "A rollup reads a property through a relation and aggregates it: count tasks, sum hours, show the earliest due date, percent complete."),
            ("Formulas compute", "Formulas use properties, built-ins and functions (if, dateBetween, format, prop) to produce text, numbers, dates, booleans or lists."),
            ("Database templates", "A template pre-fills page content and property defaults; set one as default per view so every new brief or ticket starts complete."),
            ("Automations act on triggers", "When a property changes or a page is added, an automation can edit properties, add pages, send Slack messages or notify people."),
            ("Market awareness", "Notion competes with Confluence, SharePoint, Coda, Airtable and Monday; know the plan tiers and where each tool fits to advise the organisation."),
         ]),
    dict(num=7, code="07", lu="LU4", day=2, ka="A5 · K6",
         title="Collaboration and Publishing",
         subtitle="Sharing, permissions and member management · collaborative activities · public pages and web publishing · page analytics",
         concepts=[
            ("Permission levels", "Full access, can edit, can edit content (databases only), can comment and can view; set per person, group, teamspace or the whole workspace."),
            ("Members, guests and groups", "Members join the workspace; guests are invited to specific pages; groups make permissions repeatable. Owners manage security settings."),
            ("Teamspaces", "Open, closed or private spaces with their own owners, members and default permissions — the unit of organisation for departments and clients."),
            ("Page lock and view lock", "Lock a page to prevent accidental edits and lock database views so structure stays fixed while data can still change."),
            ("Publish to the web", "Any page can become a public site with a notion.site URL, search-engine indexing, duplication and comment settings, and a public home page."),
            ("Page analytics", "Every page shows views, unique visitors and viewers over time; workspace analytics adds member engagement, content and search behaviour."),
         ]),
    dict(num=8, code="08", lu="LU4", day=2, ka="A6 · K9",
         title="Data Management and Integrations",
         subtitle="Importing data into Notion · embedding and connecting apps · the Notion API · exporting content and data integrity",
         concepts=[
            ("Import from anywhere", "Import Confluence, Evernote, Trello, Asana, Google Docs, Word, Excel, CSV, Markdown and HTML; CSV becomes a database with typed properties."),
            ("Embeds", "Paste a link to embed Google Drive, Maps, Figma, Loom, YouTube, PDFs, Typeform, GitHub gists and 1,900+ other sources inside a page."),
            ("Connections and link previews", "Connect Slack, GitHub, Jira, Google Drive, Zoom and more; pasted links unfurl into live previews and synced databases mirror external issues."),
            ("The Notion API", "An integration with a token calls api.notion.com to create pages, query data sources, update properties and search — the basis for Zapier, Make and custom plug-ins."),
            ("Data model in the API", "A database object holds one or more data sources; each data source has a schema of properties and rows that are pages (API version 2025-09-03)."),
            ("Export and integrity", "Export a page or the whole workspace as PDF, HTML or Markdown + CSV; keep backups, page history and the trash policy in the content plan."),
         ]),
    dict(num=9, code="09", lu="LU4", day=2, ka="A7 · K8",
         title="Notion AI",
         subtitle="What is Notion AI · Writer and Autofill · Q&A, Enterprise Search and the Notion Agent",
         concepts=[
            ("Your AI teammate inside Notion", "Notion AI works in the pages, databases and connected apps you already use: it drafts, edits, summarises, translates, searches and builds."),
            ("Writer — draft and edit inline", "Press Space on an empty line or highlight text: draft, continue writing, fix grammar, shorten, change tone, summarise, translate, brainstorm."),
            ("AI blocks", "/AI block creates a block whose content is regenerated on demand — a living summary, key points or a custom output with specified context."),
            ("Autofill databases", "An AI Autofill property fills summaries, keywords, translations or classifications for every row and can update as pages change."),
            ("Q&A, Enterprise Search and Research Mode", "Ask questions across the workspace, Slack and Google Drive with citations; Research Mode produces reports on open-ended questions."),
            ("The Notion Agent and plans", "The Agent takes on whole tasks (build a database, edit pages). Notion AI is included in Business and Enterprise; Free and Plus get trial responses."),
         ]),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "Foundations, collaboration tools and content creation (Topics 1–4)",
    2: "Databases, publishing, integrations, Notion AI and assessment (Topics 5–9)",
}

# ------------------------------------------------------------------ assessment (per Assessment Plan v5.0)
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 9 questions covering K1–K9, 1 hour, open book.",
    practical="Practical Performance (PP) — 5 scenario-based tasks covering A1–A7, 1 hour, open book.",
    note="A minimum of 75% attendance is required and candidates must be assessed as 'Competent' in every K and A to be eligible for WSQ funding.",
)

# ------------------------------------------------------------------ recommended follow-on courses
RECOMMENDED = [
    "WSQ - Search Engine Optimization (SEO) to Enhance Brand Awareness and Online Business",
    "WSQ - Building Professional Websites with WordPress",
    "WSQ - Building a Successful eCommerce Store with WooCommerce",
    "WSQ - Build Your Online Presence and Website with Wix for Beginners",
    "WSQ - Running a Successful eCommerce Store with Shopify",
]
