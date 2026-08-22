---
name: know-before-you-go
description: Generate "know before you go" emails for KOLs (Key Opinion Leaders — doctors presenting at an event), given that event's schedule. Use when the user wants pre-event logistics emails for presenting physicians/speakers/KOLs, or says "know before you go" for an event. Input can be pasted text, a CSV/spreadsheet, or a doc/URL with the schedule; output is one personalized plain-text email per KOL.
---

# Know before you go

Produces a personalized, plain-text "know before you go" email for each KOL (a doctor presenting at the event), thanking them for participating and giving them the logistics they need for their session.

## Input

Accept the event schedule in whatever form the user provides it — pasted text, a CSV/spreadsheet, or a doc/URL. At minimum you need, per KOL (or per KOL's team, since the email is often sent to a coordinator on the presenter's behalf):

- Recipient name (the KOL, or their office coordinator/team contact)
- Event name and venue (venue name + full address)
- A day-by-day breakdown covering, for each day they're involved: arrival/setup time, event start and end times, meals if relevant, and their presentation/session time — including anything special about it (e.g. mic pickup time, presentation order/who precedes them)
- Any staff who will assist with specific logistics (e.g. who to look for at registration, who's running AV) — by name if known
- Any reference materials to point them to (sign-up sheets, detailed schedules, attachments)
- Action items needed _from_ the KOL/team before or during the event (e.g. final slide deck, attendee phone numbers for a group text)

If the schedule is missing day-by-day detail or these logistics, ask the user rather than guessing.

## Output

One plain-text email per KOL (or KOL team) — no HTML, no images. Generate a separate email for each presenter/team found in the schedule. Follow this structure, modeled on a real sent example:

1. **Greeting**: first name, en-dash, e.g. "Hi [Name] –"
2. **Opening**: thank them for their time (reference a prior call/conversation if the input mentions one), say you're looking forward to having them, and state the purpose — "Know Before You Go" for their team as they prepare to attend [Event Name].
3. **Venue line**: venue name + full address on its own line.
4. **Reference materials**: name any sign-up sheets, detailed schedules, or attachments they should expect/use, and note if a schedule is attached.
5. **Day-by-day breakdown**: one labeled section per day (e.g. "Friday:", "Saturday:", "Sunday:"), each a short bullet list covering setup/arrival time, event hours, meals, and their presentation slot — call out any staff who'll assist by name and what they'll help with.
6. **NOTE**: a distinct callout listing what's needed from them (final deck, phone numbers, etc.) — only include if the input specifies action items.
7. **Closing**: warm, enthusiastic thanks, invite questions, and an excited sign-off.

See [example.md](example.md) for a real sent example — reference it for tone and density, but do not reuse verbatim; pull the actual event/venue/day/contact details from the input schedule.

## Tone

Warm, personal, and enthusiastic rather than formal or corporate — first-name basis, conversational phrasing, exclamation points are fine. Still genuinely appreciative of the KOL's time and expertise; just don't stiffen it into boilerplate. Keep the logistics scannable (short bullets per day) even while the surrounding voice stays casual.

## Notes

- If the schedule includes non-KOL attendees or sessions with no listed presenter, skip them — this skill only produces KOL emails.
- Omit sections with no input to draw from (e.g. skip "NOTE" if there are no action items, skip staff call-outs if no names were given) rather than inventing detail.
- Pair with [core:brand-context](../../../core/skills/brand-context/SKILL.md) if the email needs to reflect company voice beyond the tone guidance above.
