---
applyTo: "**/*.{ts,tsx,js,jsx,vue,svelte,astro,html,css}"
---

# Web UI

Tailwind CSS is the styling layer for every web UI in this repo. This file wins over any
skill, template or upstream convention that suggests otherwise.

## The rule

- **Style with Tailwind utilities.** Not styled-components, not CSS modules, not Emotion,
  not a hand-rolled `styles.css` full of class rules, not inline `style=` objects.
- **One global stylesheet only**, holding the Tailwind import, the theme block, and font
  declarations. Nothing else belongs in a `.css` file.
- Anything Tailwind genuinely cannot express (complex keyframes, third-party overrides)
  goes in that one stylesheet with a comment saying why, or in an ADR under
  `docs/decisions/` if it is a pattern rather than a one-off.
- Picking a different styling system needs an ADR. "The brief mentioned Material" is not
  an ADR.

## Check the version before you write a single class

Tailwind v3 and v4 have different config formats and different PostCSS wiring. Guessing
produces a build that fails with an unhelpful error.

```bash
cat package.json | python3 -c 'import json,sys; d=json.load(sys.stdin); print({**d.get("dependencies",{}), **d.get("devDependencies",{})}.get("tailwindcss","not installed"))'
```

- **v4 is the default for new projects.** Use v3 only when an existing project pins it.
- **v4 config lives in CSS**, in an `@theme` block, not in `tailwind.config.js`.
- **v4 PostCSS guard:** do not put `tailwindcss` in `postcss.config.js`. Use
  `@tailwindcss/postcss`, or the `@tailwindcss/vite` plugin and no PostCSS entry at all.
  This is the single most common v4 setup failure.

## Tokens, not scattered magic numbers

- Spacing, colour and type scales are defined once in the theme, then used by name.
- Arbitrary values (`w-[437px]`, `text-[#3a7bd5]`) are a smell. One or two in a file is
  fine. A dozen means the value belonged in the theme.
- Dark mode uses the `dark:` variant and the same token names. Design both modes together
  or the second one arrives broken.

## Copy inside components

The repo-wide writing rules apply to anything a user reads, including button labels,
empty states, toasts and `alt` text.

- **No em dashes.** Same rule as everywhere else.
- **No emojis** as UI elements. Use an icon component or an inline SVG.
- No marketing adjectives. Say what the button does.

## If a design skill is loaded

`taste-skill` and friends default to Tailwind v4 already, so they agree with this file
most of the time. Where they differ, this file wins: their brief-to-design-system step can
reach for Material, Carbon, Polaris or plain CSS, and in this repo it must not.

## Before saying it works

Run the build, not just the dev server. Missing Tailwind wiring often only shows up when
the production CSS is generated.

```bash
npm run build
```
