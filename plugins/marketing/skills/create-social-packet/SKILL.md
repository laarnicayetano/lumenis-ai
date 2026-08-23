---
name: create-social-packet
description: Generate a ready-to-use social post packet as a single email for LinkedIn and/or Instagram, built for a sales rep to open on their phone and post with no extra formatting. Use when the user wants a "social packet," social media post kit, or campaign content package for reps to share on LinkedIn/Instagram. Only these two platforms are supported. Output is one plain-text email with everything inline (copy, hashtags, links, image/video guidance) — not a folder of files.
---

# Social post packet builder

Produces a single **email** a sales rep can open and act on directly — no editing, no re-formatting, no guessing what to paste where. This is deliberately an email, not a downloaded folder: a rep posting to Instagram is almost always doing it from their phone, and a zip of PDFs is friction they won't open there. Email is the format they'll already be reading on that device, and it's what they'll actually use. This skill supports **LinkedIn and Instagram only** — see [references/platforms.md](references/platforms.md) for platform-specific guidance.

The audience for the *posts themselves* is broad (customers across departments). The audience for the *email* is the sales rep — everything in it should be scannable, low-friction, and require zero extra work from them before they post.

## Input

Before drafting, establish:

- **Campaign name** — used in the subject line (e.g. "OptiLIGHT Fall Launch — Social Packet").
- **Platform(s)**: LinkedIn, Instagram, or both. If not specified, ask — don't default to both.
- **Key message / offer / product** being promoted, and the product's [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) persona(s) this is meant to resonate with when a customer sees it.
- **Source photos**, if any exist. If none are provided, ask whether any exist before assuming there aren't — don't silently skip that section.
- **Video asset**, if an existing finished video file is being supplied for reformatting/specs — this skill does not produce new video.
- **Destination links** to promote (landing page, booking link, product page, etc.) and any UTM parameters already in use for this campaign.
- **Any launch date / expiration** relevant to the campaign.

If the request is missing any of these and they matter to what gets written, ask rather than inventing campaign details, links, or claims.

## Output: one email

A single plain-text email, addressed to the rep, structured to be read and acted on top-to-bottom in one pass — no separate files to open, nothing to download. Follow [marketing:edit-copy](../edit-copy/SKILL.md)'s plain-text email conventions (no markdown headers/bold rendered in the body — use plain line breaks and labels instead) and this shape:

1. **Subject**: names the campaign plainly, e.g. "Social Packet: OptiLIGHT Fall Launch — LinkedIn + Instagram."
2. **Opening** (2-3 lines): what this is, what it's for, and the one-line instruction — "copy the caption for your platform below, use the image/link as noted, post." Any launch window/expiration goes here.
3. **One section per platform requested** (LinkedIn and/or Instagram, clearly labeled, never merged into one undifferentiated block) — see below.
4. **Links** — the destination URL and its tracked/UTM version per platform, inline, one per line — not buried in prose.
5. **Image/video notes** — see below.
6. **Compliance reminder** — a short version inline (see Compliance below), not the full placeholder document.
7. **Sign-off.**

### Per-platform section

For each platform:
- The full caption, ready to copy-paste, as its own clearly delimited block.
- Hashtags, separated out clearly from the caption.
- Suggested link placement (see [references/platforms.md](references/platforms.md) — LinkedIn and Instagram handle this differently).
- Alt text for the image, if an image exists for that post.

Draft the copy following the platform's tone and structure in [references/platforms.md](references/platforms.md), grounded in [marketing:positioning](../positioning/SKILL.md) and [core:brand-context](../../../core/skills/brand-context/SKILL.md) for voice, and the relevant [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) persona for what the audience actually cares about. Never write the same caption verbatim for both platforms.

### Images

- **If source photos were supplied**: resize/crop/format each into the platform's required dimensions (see specs in [references/platforms.md](references/platforms.md)) using an image library (e.g. Pillow) if code execution is available, and attach the formatted files to the email — note in the relevant platform section which attachment goes with which post. If code execution isn't available, say so and describe the needed crop/dimensions instead of silently skipping formatting.
- **If no source photos exist**: don't invent or generate original photography. Instead, state plainly in that platform's section what's needed — dimensions, aspect ratio, and count — so the rep or a designer knows what to source. Say plainly in the opening that photos still need to be added before posting.
- Do not fabricate or AI-generate imagery meant to depict real products, patients, or clinical results — that's a compliance risk on its own, separate from the placeholder-compliance issue below.

### Video (only if applicable)

This skill cannot produce finished video. Only mention video if the campaign actually has a video component (an existing file to reformat, or a planned Reel). State the target spec inline (see [references/platforms.md](references/platforms.md) — Instagram Reels vs. LinkedIn native video) and note that the finished video file itself must be attached/supplied separately. If there's no video component, don't add a video section at all.

### Compliance

Include a short compliance reminder inline in the email — pull the key points from [references/compliance-reminders.md](references/compliance-reminders.md) (no unapproved medical/clinical claims, before/after images need documented consent, no unapproved pricing/offers, etc.) condensed to what fits a few lines, and **keep its warning intact**: state plainly that this is a generic reminder, not official Legal/Regulatory sign-off. Do not soften or drop that framing to save space — cut length from elsewhere in the email first.

## Notes

- This is one email, not a zip or folder — if code execution isn't available for image formatting, still send the email with the copy/links/specs, just note that images need to be sourced/formatted separately.
- Always confirm platform(s) and campaign name before drafting.
- Pair with [marketing:positioning](../positioning/SKILL.md), [core:brand-context](../../../core/skills/brand-context/SKILL.md), and [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) for voice and tone; see [references/platforms.md](references/platforms.md) for LinkedIn/Instagram specifics.
- If asked to support a platform beyond LinkedIn/Instagram, say this skill is currently scoped to just those two rather than improvising specs for a platform it hasn't been built for.
