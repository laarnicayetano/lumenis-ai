---
name: new-product-skill
description: Scaffold a new, consistent product skill for Lumenis. Use when the user wants to add a product, create a product skill, onboard a new product/department, or "set up a new product". Generates a single context skill following the house pattern.
---

# New product skill generator

Creates one consistent skill for a new product, matching the pattern in
`core/skills/product-example/`.

## Sources to check

- https://lumenis.com/vision-sitemap.xml
- https://lumenis.com/aesthetics-sitemap.xml

## Steps to follow when invoked

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
7. Tell the user the exact save path, and remind them:
   "Commit this to core/skills/product-<slug>/, bump core's version
   (scripts/bump_version.py core minor), rebuild zips, and redistribute."

## Rules for consistency

- Descriptions must disambiguate by product name — this is what prevents the
  wrong product skill firing on an ambiguous request.
- Ground the skill in the sitemap pages found in step 2, not just what the
  user types in step 1 — those pages are the primary source of truth for
  audience, talking points, features, and competitors.
- Never invent brand facts; use placeholders when unknown.
