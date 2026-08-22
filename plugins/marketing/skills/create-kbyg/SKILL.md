---
name: create-kbyg
description: Generate "know before you go" pre-event logistics emails, given an event schedule. Use when the user wants a pre-event logistics email or says "know before you go" for an event. Input can be pasted text, a CSV/spreadsheet, or a doc/URL with the schedule; output is one personalized plain-text email per recipient (or recipient group), toned for whichever audience it's for.
---

# Know before you go

Produces a personalized, plain-text "know before you go" email giving a recipient the logistics they need for an event — thanking them for participating and covering what they need to know before they arrive.

This is not KOL-specific. It can be used for any attendee type (a presenting physician/KOL, attending staff, a sales team, etc.) — the recipient's [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) persona determines tone and what to emphasize.

## Input

**Audience**: identify which [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) persona this email is for (e.g. KOL, Practice Owner, Sales/Channel Partner). If it's not clear from the request, ask rather than assuming — a KOL email and an internal sales-team email should not read the same way.

**Event schedule**, in whatever form the user provides it — pasted text, a CSV/spreadsheet, or a doc/URL. At minimum you need, per recipient (or per recipient's team, since the email is often sent to a coordinator on their behalf):

- Recipient name (or their office/team coordinator)
- Event name and venue (venue name + full address)
- A day-by-day breakdown covering, for each day they're involved: arrival/setup time, event start and end times, meals if relevant, and their specific slot/role that day (e.g. presentation time, staffing shift) — including anything special about it (e.g. mic pickup time, presentation order/who precedes them)
- Any staff who will assist with specific logistics (e.g. who to look for at registration, who's running AV) — by name if known
- Any reference materials to point them to (sign-up sheets, detailed schedules, attachments)
- Action items needed _from_ the recipient/team before or during the event (e.g. final slide deck, attendee phone numbers for a group text)

If the schedule is missing day-by-day detail or these logistics, ask the user rather than guessing.

## Output

One plain-text email per recipient (or recipient team) — no HTML, no images. Generate a separate email for each recipient/team found in the schedule. Follow this structure, modeled on a real sent example:

1. **Subject**: The Subject line to use in the email
1. **Greeting**: first name, en-dash, e.g. "Hi [Name] –"
1. **Opening**: thank them for their time (reference a prior call/conversation if the input mentions one), say you're looking forward to having them, and state the purpose — "Know Before You Go" for their team as they prepare to attend [Event Name].
1. **Venue line**: venue name + full address on its own line.
1. **Reference materials**: name any sign-up sheets, detailed schedules, or attachments they should expect/use, and note if a schedule is attached.
1. **Day-by-day breakdown**: one labeled section per day (e.g. "Friday:", "Saturday:", "Sunday:"), each a short bullet list covering setup/arrival time, event hours, meals, and their slot that day — call out any staff who'll assist by name and what they'll help with.
1. **NOTE**: a distinct callout listing what's needed from them (final deck, phone numbers, etc.) — only include if the input specifies action items.
1. **Closing**: thanks, invite questions, and a sign-off — warmth and enthusiasm level set by the audience archetype's tone guidance.

See [example.md](example.md) for real sent examples (written for a KOL audience) — reference them for structure and density, but do not reuse verbatim; pull the actual event/venue/day/contact details from the input schedule, and adjust tone for whichever archetype actually applies.

## Tone

Follow whichever [core:audience-archetypes](../../../core/skills/audience-archetypes/SKILL.md) persona applies to this recipient — don't default to one fixed tone. A KOL email should read warm, personal, and appreciative of their time and expertise; an internal sales-team email can be more brisk and logistics-first. Regardless of archetype, keep the day-by-day logistics scannable (short bullets per day).

## Notes

-Generate the appropriate email for whichever recipient type the schedule covers, matching tone to their archetype.

- Omit sections with no input to draw from (e.g. skip "NOTE" if there are no action items, skip staff call-outs if no names were given) rather than inventing detail.
- Pair with [core:brand-context](../../../core/skills/brand-context/SKILL.md) if the email needs to reflect company voice beyond the archetype's tone guidance.
