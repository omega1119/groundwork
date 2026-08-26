# Quickstart block: Docker

Use alongside a native quickstart, not instead of one. Someone changing the code wants to
run it directly.

---

## Quickstart with Docker

Needs Docker <24> or newer. Check with `docker --version`.

```bash
git clone <repo-url>
cd <repo-name>

cp .env.example .env      # then fill in the values, see Configuration
docker build -t <image-name> .
docker run --rm -p 8000:8000 --env-file .env <image-name>
```

Open <http://localhost:8000>. Stop it with `Ctrl+C`.

Or with Compose:

```bash
docker compose up --build
```

---

## Notes for whoever fills this in

- The port mapping is `host:container`. Get the container port from the `EXPOSE` line or
  the start command, not from habit.
- `--rm` keeps the reader's machine clean. Without it they accumulate stopped containers
  and eventually wonder where their disk went.
- **Never bake secrets into the image.** `--env-file` or Compose `env_file`, and `.env` in
  `.dockerignore` as well as `.gitignore`.
- `.dockerignore` matters as much as `.gitignore`. Without it the build context includes
  `.venv/`, `node_modules/` and `.git/`, which makes builds slow and can leak history into
  the image.
- Say the first build takes a few minutes and later ones are cached. Otherwise the first
  run reads as hung.
- Mention `docker compose down -v` if volumes hold data the reader may want to reset.
