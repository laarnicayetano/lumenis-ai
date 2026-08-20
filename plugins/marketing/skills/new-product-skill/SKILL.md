---
name: new-product-skill
description: Scaffold a new, consistent product skill set for Lumenis. Use when the user wants to add a product, create a product skill, onboard a new product/department, or "set up a new product". Generates a context skill and a design-overrides skill following the house pattern.
---

# New product skill generator

Creates a consistent pair of skills for a new product, matching the pattern in
`core/skills/product-example/`.

## Steps to follow when invoked

1. Ask the user for:
   - Product display name (e.g. "Laser X")
   - Product slug (kebab-case, e.g. "laser-x")
   - One-line description of the product
   - (Optional) known audience, talking points, features
2. Produce TWO SKILL.md files, mirroring `core/skills/product-example/`:
   - `core/skills/product-<slug>/context/SKILL.md`
   - `core/skills/product-<slug>/design/SKILL.md`
3. In each, set the frontmatter `name` to `product-<slug>-context` /
   `product-<slug>-design`, and write a description that:
   - names the product explicitly ("Context for <Name> specifically…")
   - says to ASK which product if a request is ambiguous
   - says NOT to use it for other products
4. Fill any provided content; leave `<!-- comment -->` placeholders for the rest.
5. Tell the user the exact save paths, and remind them:
   "Commit these to core/skills/product-<slug>/, bump core's version
   (scripts/bump_version.py core minor), rebuild zips, and redistribute."

## Rules for consistency

- Descriptions must disambiguate by product name — this is what prevents the
  wrong product skill firing on an ambiguous request.
- Design skill lists only DELTAS from the global design system.
- Never invent brand facts; use placeholders when unknown.
