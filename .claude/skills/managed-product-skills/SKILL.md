---
name: managed-product-skills
description: Create a new Lumenis product context skill, or update an existing one, in this repo. Use when the user wants to add a product, create a product skill, update/refresh a product skill, onboard a new product/department, or "set up a new product." Repo-local — only works in Claude Code with this repo's working tree checked out.
---

# Manage product skills

Creates or updates one consistent context skill per product, matching the
pattern in `core/skills/product-example/` (or any real `core/skills/product-*/SKILL.md`).

## Sources to check

- https://lumenis.com/vision-sitemap.xml
- https://lumenis.com/aesthetics-sitemap.xml

## Step 0 — new product or update?

If it's not already clear from the request, ask whether this is a **new**
product or an **update** to an existing one. Check whether
`core/skills/product-<slug>/SKILL.md` already exists for the product named —
if it does, treat this as an update even if the user said "create."

## Creating a new product skill

1. Ask the user for:
   - Product display name (e.g. "Laser X")
   - Product slug (kebab-case, e.g. "laser-x")
   - One-line description of the product
   - (Optional) known audience, talking points, features, competitors
2. Fetch both sitemaps above and find every URL that relates to this product
   (matching the product name or slug — check both, since a product can
   appear in either the Vision or Aesthetics sitemap, or occasionally both).
   Fetch each matching page and use it as source material for the template
   sections below — target audience, talking points, features, competitors.
   Prefer this over inventing content, but user-supplied info from step 1
   takes precedence if it conflicts with a page. Note in the skill body (or
   to the user) if no matching URLs were found, rather than leaving sections
   silently unsourced.
3. Produce ONE SKILL.md file, mirroring `core/skills/product-example/`:
   - `core/skills/product-<slug>/SKILL.md`
4. Set the frontmatter `name` to `product-<slug>`, and write a description that:
   - names the product explicitly ("Context for <Name> specifically…")
   - says to ASK which product if a request is ambiguous
   - says NOT to use it for other products
5. Use this template for the body:

```markdown
---
name: product-<slug>
description: Context for <Name> specifically — its target audience, key talking points, and features. Use when writing copy, landing pages, campaigns, or answering questions about <Name>. If the request involves a product but does not say which one, ASK which product before proceeding. Do NOT use for other Lumenis products; each has its own skill.
---

# <Name>

<!-- One-line description of the product. -->

## Target audience

<!-- Who buys/uses it. Pain points. -->

## Talking points

<!-- Messages that land for this audience. -->

## Features

<!-- Key features mapped to benefits. -->

## Competitors

<!-- Named competing products/approaches, if known. -->

## How to use this

- Keep messaging consistent with the marketing positioning pillars.
- If it's unclear which product a request is about, ask first.
```

6. Fill in the matching sections using user-supplied content and the sitemap
   pages fetched in step 2; leave `<!-- comment -->` placeholders for
   anything not covered by either. Never invent brand facts.
7. Tell the user the exact save path, then ship via
   [propose-plugin-change](../propose-plugin-change/SKILL.md).

## Updating an existing product skill

1. Read the current `core/skills/product-<slug>/SKILL.md` in full before
   changing anything — never blind-overwrite a file you haven't read.
2. Clarify what the user wants: a full refresh against the sitemaps, or a
   specific fact/section update they already have in hand.
3. Fetch both sitemaps above and find URLs relating to this product, the
   same way as creation — this catches pages added or changed since the
   skill was last written.
4. Merge, don't replace:
   - Fill any section that's still a `<!-- comment -->` placeholder using
     the newly sourced pages.
   - Leave sections with real, already-written content alone unless the
     user asked for a refresh or new source material directly contradicts
     what's there — in that case, flag the conflict and ask before
     overwriting rather than silently replacing it.
   - Never delete existing content just because a sitemap page no longer
     mentions it; pages get reorganized for reasons unrelated to facts
     going stale.
5. Show the user a summary of what changed (added, updated, left alone)
   before saving.
6. Ship via [propose-plugin-change](../propose-plugin-change/SKILL.md).

## Rules for consistency

- Descriptions must disambiguate by product name — this is what prevents the
  wrong product skill firing on an ambiguous request.
- Ground the skill in the sitemap pages found above, not just what the user
  types in directly — those pages are the primary source of truth for
  audience, talking points, features, and competitors.
- Never invent brand facts; use placeholders when unknown.
- On update, never silently overwrite existing user-authored content — merge
  and flag conflicts instead.
- **Never include pricing.** No prices, price ranges, per-session costs, or
  ROI/revenue projections built from a price (e.g. "$X per session ×
  Y sessions"), even if a source (a sitemap page, a pitch deck, etc.)
  states one. Omit that material entirely rather than summarizing it —
  don't launder a dollar figure into a vaguer form. Qualitative business
  value (e.g. "positioned as a new revenue stream for practices") is fine;
  the line is any actual number tied to cost or revenue.

## Platform notes

This skill writes files into `core/skills/` and ships changes via
[propose-plugin-change](../propose-plugin-change/SKILL.md), which needs a
real working tree plus `git`/`gh`. It only works in Claude Code with this
repo checked out — it is intentionally repo-local (not bundled into any
plugin) since its output has nowhere to go outside this repo.
