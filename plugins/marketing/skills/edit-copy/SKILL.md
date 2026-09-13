---
name: edit-copy
description: Refine or reply to an existing piece of correspondence — tighten, re-tone, soften, or elevate a draft (or draft a reply to an inbound message) rather than writing something from a blank page. Use when the user pastes a draft/inbound message and asks to "refine," "make this sound more X," "soften this," "make it less robotic/fluffy," or "help me reply." Also runs a final clarity pass on copy already on the table — trigger with "run the pass," "referent check," or "final pass." Covers email, Teams/chat messages, and text messages — infer or ask the medium before drafting, since it sets the baseline formality (email professional, text casual, Teams in between). Pair with core:audience-archetypes for who it's for and which correspondence register to use — this skill doesn't own tone itself.
---

# Copy editor

Edits or replies to a specific piece of correspondence — the input is always a real draft or a real inbound message, not a blank-page brief. The job is refining what's there (or answering what came in), not inventing a new piece of copy.

## Input

- **The draft or inbound message** — pasted text. If it's a reply, the inbound message is the thing being responded to; if it's a refinement, the draft is the thing being rewritten.
- **The medium** — email, Teams/chat, or text message. This sets the baseline formality the register operates within (see **Mediums** below) and is a separate axis from tone/register. Infer it when it's obvious (a pasted email thread with a subject/signature, a Teams-style exchange, a text conversation) or from what the user calls it ("draft a text to...", "reply in Teams"); ask if it's genuinely ambiguous and would change the shape of the output.
- **The ask** — what should change. Often phrased as a register shift ("more executive," "warmer," "less robotic") or a structural note ("trim the fluff," "don't mention X"). Take the literal ask at face value before adding anything else.
- **Who it's for and how warm/formal to land** — load [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) and its **Correspondence register** section. Identify the archetype (KOL, physician, practice owner, internal sales/exec, etc.) and the register (polished/warm/executive/diplomatic/concise) from context or the ask; if genuinely unclear, ask rather than guessing.
- **Sender identity** — name, title, and signature block, if this is going out under someone's name. Use what's already in the draft (e.g. a signature at the bottom) rather than asking if it's there; ask only if it's missing and needed.

## Output

- Keep the medium's real constraints — see **Mediums** below for what each one allows and forbids. Never draft email-formal copy for a text, or text-clipped copy for an email.
- When the right register isn't obvious from the ask, offer **two short variants spanning nearby registers** (e.g. "Warm & personal" vs. "Polished & concise") rather than committing to one — this mirrors how these requests actually resolve: the person picks or steers from there. Keep both variants within the medium's formality range (don't let one variant drift into a different medium's register). Once a register is picked or already stated, give one version.
- Preserve every concrete fact from the original (names, dates, dollar figures, commitments already made) — a tone edit should never quietly drop or alter a fact.
- If asked to soften stern or corrective content, keep the substance intact — reword to remove blame/accusation, don't dilute the message into vagueness. The point being made should still land.
- Iterate in place: follow-up asks ("less robotic," "still too fluffy," "add that X happened Friday") are edits to the last version, not a new pass from the original input.

## Mediums

The core loop (draft/inbound → register → edit → iterate) is the same across mediums; what changes is the formality ceiling and the formatting the medium allows.

- **Email** — most formal. Plain text body (no markdown headers/bold), a subject line only if one is being drafted fresh, and a full signature block if the draft had one. Register can span the whole archetype range, from warm to executive/diplomatic.
- **Teams / chat messages** — in between. Still professional, but relaxed: no subject line, shorter lines, a first name or no sign-off at all (skip the full signature block). Light structure (short paragraphs, an occasional line break) is fine; heavy formality reads wrong here even when the ask is "polished" — lean toward warm/concise rather than executive/diplomatic.
- **Text messages** — most casual. Short, clipped, conversational; no subject line, no signature block, contractions expected. Even a "polished" register should still read like a text, not a shrunk email — resist the pull to formalize.

## Notes

- This is an editing skill, not a drafting-from-scratch skill — if the user has no draft and no inbound message to respond to, that's closer to a "write me an email about X" request; still usable here, but expect to ask more upfront about content, not just tone.
- Pair with [core:brand-context](../../../core/skills/brand-context/SKILL.md) if the message needs to reflect company voice beyond the archetype/register.

## Clarity gate

Run this as the last step before delivering any copy — after the tone/register work above, not woven into it. It catches one specific, recurring defect: fluent-sounding copy that makes the reader do work the copy should have done (a header that has to be decoded, a "why it matters" that stops at an abstraction, a "this"/"the surgeons"/"yours" with nothing earlier for it to point to). That defect is invisible to a read-for-flow check, because sounding smooth is exactly what hides it — only a discrete, mechanical scan catches it.

**Flagging is not fixing.** Noticing a vague referent and leaving it in place doesn't count — resolve or rewrite it, never just annotate.

Run all three checks, in order:

1. **Decode** — does each header, subject line, or hook say plainly what the thing is? If the reader has to unpack a clever phrase first, rewrite it plainly.
2. **Trace** — does each "why it matters" land on a concrete effect for that specific reader? "Improves outcomes" or "great for engagement" fails — trace it down to what actually changes, for whom, and why they'd care.
3. **Locate** — can every demonstrative ("this/that/these/those"), pronoun ("it/them/they/yours"), and definite noun phrase ("the surgeons," "the approach") be traced back to an exact earlier word or phrase? If a referent can't be resolved from text before it, rewrite it plainly.

**Auto-fail, no deliberation needed:**
- A demonstrative ("this X," "that X") in an opening clause, headline, eyebrow, or subject line — nothing precedes it to point at.
- A definite noun phrase introducing a group or thing that's never identified anywhere.
- A pronoun whose nearest candidate antecedent is two or more nouns back.

**When to run it:**
- Before delivering any copy deliverable, every time — including revisions and one-line tweaks.
- Immediately and in full when asked to "run the pass," "referent check," or "final pass," on whatever copy is currently on the table.

**Output convention:**
- Substantial deliverables (email going out under someone's name, anything public-facing or multi-paragraph): show a short three-line audit next to the copy — one line each for Decode, Trace, and Locate (confirm clean, or name the fix) — so the check is visible, not just trusted.
- Quick one-line asks: run all three silently, deliver clean copy only.
- An explicit "run the pass" request: always show the full audit, regardless of size.

This gate owns clarity only — it doesn't replace prohibited-terms/compliance review or product-specific evidence checks (e.g. a product skill's claims-reference file, where one exists); those stay separate.

**Worked example**

Draft (opening clause): "The cataract and refractive surgeons pushing **this work** forward have shared how they catch the unhappy patient..."

Locate audit: "this work" is a demonstrative in the opening clause — nothing precedes it, so it has no antecedent. Auto-fail.

Rewrite: "Leading cataract and refractive surgeons have worked out how to catch the unhappy patient hiding behind a perfect 20/20 number, and they've put **their method** into two pieces you can use: a Clinical Field Guide with **their** approach to spotting **that patient**, and a Practice Implementation Kit with **their** plan for catching **that patient** routinely."

Clean audit: "their method" → the surgeons' way of catching the patient, named just before. "that patient" → the unhappy patient hiding behind a 20/20 number, named earlier. "their" (×2) → leading cataract and refractive surgeons. All resolve backward — passes.
