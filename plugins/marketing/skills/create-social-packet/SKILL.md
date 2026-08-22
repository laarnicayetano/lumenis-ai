---
name: create-social-packet
description: Generate a ready-to-use social post packet (a folder of files) for LinkedIn and/or Instagram, built for a sales rep to pick up and post with no extra formatting. Use when the user wants a "social packet," social media post kit, or campaign content package for reps to share on LinkedIn/Instagram. Only these two platforms are supported. Output is real generated files (PDFs, and formatted images if source photos are provided), not placeholder text.
---

# Social post packet builder

Produces a self-contained **campaign folder** a sales rep can open and use directly — no editing, no re-formatting, no guessing what to paste where. Every text document in the packet is generated as an actual PDF (not a description of one) so it opens on any device without a special app and the copy can still be selected and pasted. This skill supports **LinkedIn and Instagram only** — see [references/platforms.md](references/platforms.md) for platform-specific guidance.

The audience for the *posts themselves* is broad (customers across departments). The audience for the *packet* is the sales rep — everything in it should be scannable, low-friction, and require zero extra work from them before they post.

## Input

Before drafting, establish:

- **Campaign name** — used for the folder name (e.g. `OptiLIGHT_Fall_Launch`). Use underscores, no spaces, so it's safe as a folder/file name.
- **Platform(s)**: LinkedIn, Instagram, or both. If not specified, ask — don't default to both.
- **Key message / offer / product** being promoted, and the product's [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) persona(s) this is meant to resonate with when a customer sees it.
- **Source photos**, if any exist, to be formatted into the packet (see Images below). If none are provided, ask whether any exist before assuming there aren't — don't silently skip the folder.
- **Video asset**, if an existing finished video file is being supplied for reformatting/specs — this skill does not produce new video.
- **Destination links** to promote (landing page, booking link, product page, etc.) and any UTM parameters already in use for this campaign, for the tracking doc.
- **Any launch date / expiration** relevant to the campaign, for the README.

If the request is missing any of these and they matter to what gets written, ask rather than inventing campaign details, links, or claims.

## Output: the campaign folder

Build this exact structure (omit numbered folders that don't apply — see notes per item):

```
<Campaign_Name>/
├── 00_READ_ME_FIRST.pdf
├── 01_Post_Copy.pdf
├── 02_Images/
│   └── (formatted photos, or Image_Specs.pdf if none were supplied)
├── 03_Video/              ← only if a video asset/spec is part of this campaign
│   └── Video_Specs.pdf
├── 04_Links_and_Tracking.pdf
└── 05_Compliance_and_Guidelines.pdf
```

At the end, zip the folder (`<Campaign_Name>.zip`) so it's a single download.

### Generating the PDFs

Actually generate these files — write and run Python (`fpdf2` or `reportlab`; pip install if not already available) to render each document straight to PDF. Keep them text-based (not flattened images of text) so the rep can select and copy-paste post copy and links directly out of the PDF. Simple, clean layout — headers, short paragraphs/bullets, no dense formatting — this is a working document for someone about to post in the next five minutes, not a designed brand piece.

### 00_READ_ME_FIRST.pdf

One page. Tells the rep, in order:
1. What campaign this is and what it's for (one line).
2. What's in each numbered item in the folder.
3. Exactly what to do: which file has the copy to paste, where the images are, what link to use.
4. Any launch window / expiration date.
5. A pointer to `05_Compliance_and_Guidelines` — say plainly that it's a placeholder, not official legal sign-off (see Compliance section below).

### 01_Post_Copy.pdf

One section per platform requested (LinkedIn and/or Instagram — never both crammed into one undifferentiated block). For each platform:
- The full caption, ready to copy-paste.
- Hashtags, separated out clearly.
- Suggested link placement (see [references/platforms.md](references/platforms.md) — LinkedIn and Instagram handle this differently).
- Alt text for the image, if an image exists for that post.

Draft the copy following the platform's tone and structure in [references/platforms.md](references/platforms.md), grounded in [marketing:positioning](../positioning/SKILL.md) and [core:brand-context](../../../core/skills/brand-context/SKILL.md) for voice, and the relevant [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) persona for what the audience actually cares about. Never write the same caption verbatim for both platforms.

### 02_Images/

- **If source photos were supplied**: use them. Resize/crop/format each into the platform's required dimensions (see specs in [references/platforms.md](references/platforms.md)) using an image library (e.g. Pillow) — don't just copy the originals in unmodified if their dimensions don't match what the platform needs. Name files descriptively (e.g. `LinkedIn_Feed_1200x627.jpg`, `Instagram_Feed_1080x1350.jpg`).
- **If no source photos exist**: don't invent or generate original photography. Instead create `Image_Specs.pdf` listing exactly what's needed — dimensions, aspect ratio, and count, per platform — so the rep or a designer knows what to drop in. Say plainly in the README that photos still need to be added.
- Do not fabricate or AI-generate imagery meant to depict real products, patients, or clinical results — that's a compliance risk on its own, separate from the placeholder-compliance-doc issue below.

### 03_Video/ (only if applicable)

This skill cannot produce finished video. Only include this folder if the campaign actually has a video component (an existing file to reformat, or a planned Reel). If included, `Video_Specs.pdf` states the target spec (see [references/platforms.md](references/platforms.md) — Instagram Reels vs. LinkedIn native video) and notes that the finished video file itself must be added separately. If there's no video component to this campaign, skip this folder entirely rather than leaving an empty one.

### 04_Links_and_Tracking.pdf

A simple table: destination URL, the tracked/UTM version of it (build one per platform if the user has a UTM convention — ask if unclear rather than inventing tracking parameters), and which post/platform it belongs to. Keep it copy-paste friendly — one link per line, not embedded in prose.

### 05_Compliance_and_Guidelines.pdf

Render this from [references/compliance-reminders.md](references/compliance-reminders.md) as-is, **including its warning banner, unedited**. Do not soften, remove, or paraphrase the warning that this content is a generic placeholder and not official Legal/Regulatory sign-off. This is the one document in the packet where accuracy of framing matters more than polish.

## Notes

- This skill is meant to run in an environment with Python code execution (e.g. claude.ai) so it can actually produce the files, not just describe them. If code execution isn't available, say so explicitly rather than silently handing back only text.
- Always confirm platform(s) and campaign name before generating — the folder name and file count depend on both.
- Pair with [marketing:positioning](../positioning/SKILL.md), [core:brand-context](../../../core/skills/brand-context/SKILL.md), and [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) for voice and tone; see [references/platforms.md](references/platforms.md) for LinkedIn/Instagram specifics.
- If asked to support a platform beyond LinkedIn/Instagram, say this skill is currently scoped to just those two rather than improvising specs for a platform it hasn't been built for.
