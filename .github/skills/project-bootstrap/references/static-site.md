# Track: Static site

A landing page or small site. No build step, no framework, no `npm install`, unless
something in the request genuinely needs one.

## Layout

```
index.html
styles.css            separate file once the CSS passes about 50 lines
main.js               only if there is behaviour
assets/               images, fonts, favicon
README.md
.gitignore
```

One page means one file plus a stylesheet. Resist adding a bundler.

## Serving locally

Opening `index.html` with `file://` breaks `fetch`, ES modules and some font loading, so
the README documents a server even though double-clicking mostly works:

```bash
python3 -m http.server 8000        # then http://localhost:8000
```

That needs no dependencies at all, which is why it beats `npx serve` here.

## Conventions

- One `<h1>` per page, real heading order, `alt` on every image. Accessibility is not a
  later pass.
- `<meta name="viewport" content="width=device-width, initial-scale=1">` in every page.
- Open Graph and description tags on any page meant to be shared.
- CSS custom properties for colours and spacing at `:root`, so a change is one edit.
- System font stack unless a specific font is asked for. A webfont costs load time.
- No CDN `<script>` tag for a library used once. Write the fifteen lines.
- No inline event handlers (`onclick=`). Bind in `main.js`.
- If a form posts anywhere, say where in the README, and never put a secret key in the
  page. Anything in client-side JavaScript is public.

## Deploying

Cheapest to most involved. Pick one and document exactly it, not all three:

| Target | Command |
|---|---|
| GitHub Pages | Push to `main`, enable Pages on the repo, source `/ (root)`. |
| Azure Static Web Apps | `az staticwebapp create ...`, or the VS Code extension. |
| Any static host | Upload the folder. |

## .gitignore

```gitignore
.DS_Store
node_modules/
dist/
```

## README notes

Quickstart block: `templates/quickstart/static-site.md`.

Include a `## Editing` section pointing at the specific things a non-developer will want
to change: the headline, the colours at `:root`, the images in `assets/`. Give the file
and roughly where in it.
