# Quickstart block: Node web app

---

## Quickstart

Needs Node <22> or newer. Check with `node --version`.

```bash
git clone <repo-url>
cd <repo-name>

npm ci
cp .env.example .env      # then fill in the values, see Configuration
npm run dev
```

Prints `<the actual line the dev server prints>`. Open <http://localhost:5173>.

Build and preview the production bundle:

```bash
npm run build
npm run preview
```

---

## Notes for whoever fills this in

- **`npm ci`, not `npm install`**, when a lockfile is committed. It installs exactly the
  locked tree and fails loudly if the lockfile and manifest disagree, which is what you
  want on a fresh clone.
- **Check the script names in `package.json` before writing them down.** `npm run dev` is
  a convention, not a guarantee.

  ```bash
  node -e "console.log(Object.keys(require('./package.json').scripts))"
  ```

- Get the port from the config, not from habit. Vite defaults to 5173, Next to 3000, a
  plain Express app to whatever it was written with.
- If a `.nvmrc` or `engines` field exists, state that version rather than "latest".
- Only mention `.env` if the code reads one, and keep the keys identical to
  `.env.example` and to the Configuration table.
