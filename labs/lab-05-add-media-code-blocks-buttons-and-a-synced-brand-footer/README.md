# Lab 05: Add Media, Code Blocks, Buttons and a Synced Brand Footer

**Topic 03** · **Day 1** · **Intermediate** · **K2 · A2** · **Notion media blocks, code blocks, buttons, synced blocks**

## Goal

You enrich the article and the Content Hub with the supplied hero image and chart, an embedded PDF and video bookmark, a syntax-highlighted code sample, a button that inserts a standard 'article checklist', and a synced brand footer that appears on every article and updates from one place.

## What you will build

A media-rich article with captioned images, embeds, a code block, an insert-checklist button and a synced footer used on two pages

![Lab 05 workflow](LAB-05-Workflow.png)

*Figure. Lab 05 workflow — the four stages and the artifact produced.*

## Files in this folder

- `media/brightwave-hero.png` — Hero image for the article
- `media/brightwave-chart.png` — Chart image for the 'By the numbers' section
- `media/brightwave-media-kit.pdf` — PDF to embed as a file block
- `embed-links.md` — Video, bookmark and map links to embed
- `code-sample.py` — UTM tagging helper for the code block
- `brand-footer.md` — Brand footer text and the article checklist
- `LAB-05-Instructions.pdf` — printable detailed guide
- `LAB-05-Workflow.png` — the workflow diagram above
- `lab.yaml` — lab metadata (topic, K/A codes, files, acceptance check)

## Procedure

1. **Upload the hero image**

   Open Five Content Trends for 2027. Under the title type /image → Upload and choose media/brightwave-hero.png. Drag its side handles to full width, then hover and click Caption to add 'Brightwave content trends 2027'.

2. **Add the chart image with alignment**

   Under 'By the numbers' add /image with media/brightwave-chart.png. Use the alignment icons on hover to centre it and resize it to about two-thirds width. Click Replace to see how an image is swapped without losing the caption.

3. **Embed a file and a web bookmark**

   Type /file and upload media/brightwave-media-kit.pdf; then type /web bookmark and paste https://www.notion.com/help/intro-to-databases. Notice the bookmark unfurls with a title and preview. Try /video with a YouTube URL from embed-links.md.

4. **Add a code block with syntax highlighting**

   Under the 'Tracking script' heading type /code, paste the contents of code-sample.py, set the language to Python, toggle Wrap code on, and click the copy icon to confirm it copies. Add a caption 'UTM tagging helper'.

5. **Create a button that inserts the article checklist**

   At the top of Blog Articles type /button, name it Insert article checklist, add the action Insert blocks, and build a to-do list from brand-footer.md's checklist section (SEO title, meta description, hero image, footer). Click Done, then click the button to test it.

6. **Write the brand footer as a synced block**

   At the bottom of the article type /synced block. Inside it add a divider, a callout with the Brightwave contact line from brand-footer.md and a link to the Help Centre page. The red outline marks a synced block.

7. **Reuse the synced block on a second page**

   Click Copy and sync at the top right of the synced block, open another article page (create Content Trends Webinar Recap) and paste. Edit the contact line in one copy and watch the other update.

8. **Unsync a copy and observe**

   On the second page choose the synced block ⋯ → Unsync. Edit it and confirm the original no longer changes. Then delete the unsynced copy and paste the synced version again.

9. **Check media on mobile width**

   Drag the browser narrow (or open Notion on your phone) to confirm the images scale, the columns stack and the code block wraps.

## Acceptance check

The article shows a captioned full-width hero image, a centred chart, an embedded PDF, a web bookmark, a Python code block with wrap on, the Insert article checklist button inserts four to-dos, and the same synced footer appears on two pages and updates in both when edited.

## Evidence to retain

- Screenshot of the article with media and code block, and of the synced block on the second page.

## Steps checklist

- [ ] Step 1: Upload the hero image
- [ ] Step 2: Add the chart image with alignment
- [ ] Step 3: Embed a file and a web bookmark
- [ ] Step 4: Add a code block with syntax highlighting
- [ ] Step 5: Create a button that inserts the article checklist
- [ ] Step 6: Write the brand footer as a synced block
- [ ] Step 7: Reuse the synced block on a second page
- [ ] Step 8: Unsync a copy and observe
- [ ] Step 9: Check media on mobile width

---

*Mastering Notion for Content, Project, and Database Management · TGS-2023041080 · Version v6 · © 2026 Tertiary Infotech Academy Pte Ltd*