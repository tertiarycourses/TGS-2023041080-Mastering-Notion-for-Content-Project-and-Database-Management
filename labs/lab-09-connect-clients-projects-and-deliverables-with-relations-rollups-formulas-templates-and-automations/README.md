# Lab 09: Connect Clients, Projects and Deliverables with Relations, Rollups, Formulas, Templates and Automations

**Topic 06** · **Day 2** · **Advanced** · **K7 · A4** · **Notion relations, rollups, formulas, database templates, automations**

## Goal

You create the Clients and Deliverables databases, relate Clients → Projects → Tasks and Deliverables, roll up hours, budgets and completion, write formulas for health status and days remaining, build a Project Brief template, add an automation that notifies the owner when a deliverable is approved, and complete a market comparison of Notion against Confluence, Airtable and Monday.

## What you will build

A relational model (Clients, Projects, Tasks, Deliverables) with rollups, formulas, a default project template, one automation and a CMS market comparison table

![Lab 09 workflow](LAB-09-Workflow.png)

*Figure. Lab 09 workflow — the four stages and the artifact produced.*

## Files in this folder

- `clients.csv` — Five clients with industry, account manager and retainer
- `deliverables.csv` — Eighteen deliverables linked to projects
- `formulas.md` — The formulas used in this lab with an explanation of each function
- `automation-rules.csv` — The automation and button rules to configure
- `cms-market-comparison.csv` — Comparison grid of Notion, Confluence, Airtable and Monday.com to complete
- `LAB-09-Instructions.pdf` — printable detailed guide
- `LAB-09-Workflow.png` — the workflow diagram above
- `lab.yaml` — lab metadata (topic, K/A codes, files, acceptance check)

## Procedure

1. **Create the Clients database**

   In Client Projects import clients.csv as Clients (Industry → Select, Account Manager → Person, Retainer (SGD) → Number).

2. **Relate Projects to Clients**

   In Projects add a property Client (Relation) → Clients, turn on Show on Clients and name the reverse property Projects. Replace the old Client select values by picking the related client for each row, then delete the select property.

3. **Relate Tasks to Projects**

   In Tasks add a Relation property Project → Projects with a two-way property Tasks. Assign every task to its project using the Project column in tasks.csv. Return to Lab 8's linked view in Nova Retail Launch and confirm the filter now works.

4. **Create Deliverables and relate them**

   Import deliverables.csv as Deliverables; add a Relation to Projects (two-way, named Deliverables) and a Status property with Draft, In Review, Approved, Published.

5. **Add rollups**

   In Projects add rollups: Total Hours = Tasks → Estimate (h) → Sum; Tasks Done = Tasks → Status → Percent per group Complete; Next Due = Tasks → Due → Earliest date. In Clients add Active Projects = Projects → Name → Count and Total Budget = Projects → Budget → Sum.

6. **Write formulas**

   In Projects add formula Days Left: dateBetween(prop("Dates").end, now(), "days"). Add formula Health: if(prop("Tasks Done") >= 0.8, "🟢 On track", if(prop("Days Left") < 7, "🔴 At risk", "🟡 Watch")). Add formula Budget/Hour: format(round(prop("Budget (SGD)") / prop("Total Hours"))).

7. **Create a Project Brief template**

   In Projects click the arrow next to New → New template. Title it Project Brief, set default Stage = Planning, and add body sections Objectives, Audience, Channels, Deliverables (a linked view of Deliverables filtered to this project), Risks. Set it as Default for all views.

8. **Add an automation**

   In Deliverables click ⚡ Automations → New automation. Trigger: Status is set to Approved. Actions: Edit property Approved On = now; Send notification to the Owner person property with 'Deliverable approved — schedule publishing'. Turn it on and test by approving one deliverable.

9. **Add a button automation**

   In a project page add a /button named Log weekly review whose action Adds a page to Tasks with Name = Weekly review, Project = this project, Due = today + 7 days.

10. **Complete the market comparison**

   Open cms-market-comparison.csv. Create a simple table on a page Market Offerings under Company Wiki and complete the empty cells for Notion, Confluence, Airtable and Monday.com across pricing tier, databases, wiki, API and publishing, using the Notion Help Center and vendor pages. Write two sentences on where Notion fits Brightwave.

## Acceptance check

Clients show Active Projects and Total Budget rollups, each project shows Total Hours, Tasks Done, Next Due, Days Left and a Health formula, new projects open with the Project Brief template, approving a deliverable sets Approved On and notifies the owner, and the Market Offerings table is complete for four tools.

## Evidence to retain

- Screenshots of the Projects table with rollups and formulas, of the automation, and of the market comparison table.

## Steps checklist

- [ ] Step 1: Create the Clients database
- [ ] Step 2: Relate Projects to Clients
- [ ] Step 3: Relate Tasks to Projects
- [ ] Step 4: Create Deliverables and relate them
- [ ] Step 5: Add rollups
- [ ] Step 6: Write formulas
- [ ] Step 7: Create a Project Brief template
- [ ] Step 8: Add an automation
- [ ] Step 9: Add a button automation
- [ ] Step 10: Complete the market comparison

---

*Mastering Notion for Content, Project, and Database Management · TGS-2023041080 · Version v6 · © 2026 Tertiary Infotech Academy Pte Ltd*