# Lab 07: Build the Content Calendar Database with Properties, Views and Filters

**Topic 05** · **Day 2** · **Foundation** · **K3 · A3** · **Notion databases (table, board, calendar, gallery views)**

## Goal

You import the supplied content calendar CSV into a full-page database in the Content Hub, correct the property types, open rows as pages, add board, calendar and gallery views, and build filtered views for each editor so the team maintains every web asset from one source.

## What you will build

A Content Calendar database with typed properties, five views (table, board by status, calendar by publish date, gallery, 'My items'), filters, sorts and grouping

![Lab 07 workflow](LAB-07-Workflow.png)

*Figure. Lab 07 workflow — the four stages and the artifact produced.*

## Files in this folder

- `content-calendar.csv` — Thirty-six content items with status, channel, tags, dates and owners
- `LAB-07-Instructions.pdf` — printable detailed guide
- `LAB-07-Workflow.png` — the workflow diagram above
- `lab.yaml` — lab metadata (topic, K/A codes, files, acceptance check)

## Procedure

1. **Import the CSV**

   Open Content Hub. In the sidebar click Import → CSV and choose content-calendar.csv. Notion creates a full-page database named after the file with one row per line. Rename it Content Calendar and move it under Content Hub.

2. **Inspect the imported properties**

   Every column arrived as a property, but several as Text. Click a column header → Edit property → Type and set: Status → Status, Channel → Select, Tags → Multi-select, Publish Date → Date, Owner → Person (assign yourself), Word Count → Number, URL → URL, Approved → Checkbox.

3. **Open a row as a page**

   Hover the first row's Name and click Open. The properties appear at the top and the page body below. Add a short brief in the body. Click ⋯ → Customize page to hide empty properties, then close the peek.

4. **Add and reorder properties**

   Add a Created time property and an ID property (prefix BW). Drag the columns so Name, Status, Channel, Owner and Publish Date come first; hide Word Count in this view with the eye icon in the property list.

5. **Add a board view by status**

   Click + next to the view tabs → Board. Group by Status; drag a card from Draft to In Review and see its Status update. Turn on Sub-group by Channel.

6. **Add a calendar view**

   Add a Calendar view, choose Show calendar by Publish Date, and drag an item to a new date. Switch to Week view and back to Month.

7. **Add a gallery view**

   Add a Gallery view, set Card preview to Page cover and Card size to Medium, and show the Channel and Status properties on the cards.

8. **Filter, sort and group the table**

   In the Table view add a filter Status is not Published, a sort by Publish Date ascending, and Group by Channel. Then add an advanced filter: Channel is Blog OR (Tags contains Campaign AND Approved is unchecked). Click Save for everyone.

9. **Create a personal 'My items' view**

   Duplicate the Table view, rename it My items and filter Owner contains Me. Add a new row inside this view and notice the Owner is pre-filled — a filtered view is a forcing function.

10. **Lock the database views**

   Click ⋯ at the top right → Lock database so teammates can edit content but not the properties or views. Note the lock icon.

## Acceptance check

Content Calendar contains every row from content-calendar.csv with the corrected property types, has table, board (grouped by Status, sub-grouped by Channel), calendar, gallery and My items views, the advanced filter returns only the matching rows, and the database is locked.

## Evidence to retain

- Screenshots of the table view with filters and of the board view.

## Steps checklist

- [ ] Step 1: Import the CSV
- [ ] Step 2: Inspect the imported properties
- [ ] Step 3: Open a row as a page
- [ ] Step 4: Add and reorder properties
- [ ] Step 5: Add a board view by status
- [ ] Step 6: Add a calendar view
- [ ] Step 7: Add a gallery view
- [ ] Step 8: Filter, sort and group the table
- [ ] Step 9: Create a personal 'My items' view
- [ ] Step 10: Lock the database views

---

*Mastering Notion for Content, Project, and Database Management · TGS-2023041080 · Version v6 · © 2026 Tertiary Infotech Academy Pte Ltd*