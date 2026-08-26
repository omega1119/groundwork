# Quickstart block: static site

---

## Quickstart

Nothing to install. Serve the folder and open it:

```bash
git clone <repo-url>
cd <repo-name>
python3 -m http.server 8000
```

Open <http://localhost:8000>. You should see <what the page shows>.

Stop the server with `Ctrl+C`.

Windows is the same, using `py -3 -m http.server 8000`.

---

## Notes for whoever fills this in

- Document the server even though double-clicking `index.html` usually works. `file://`
  breaks `fetch`, ES modules and some font loading, so the reader who opens the file
  directly hits a confusing failure the moment the page does anything.
- `python3 -m http.server` needs no dependencies, which is why it beats `npx serve` here.
  Only reach for Node if the project already needs it.
- Say what the page should look like. "You should see the hero image and three cards" tells
  the reader whether it worked.
- If there is a build step, this block is wrong. Use `node-web.md`.
- Add an `## Editing` section after Usage, pointing at the specific things someone will
  want to change: the headline text and where it is, the colour variables at `:root` in
  `styles.css`, the images in `assets/`.
- If the page posts a form or calls an API, say where to, and remember that anything in
  client-side JavaScript is public. No keys in the page.
