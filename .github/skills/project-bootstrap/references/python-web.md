# Track: Python web app or API

FastAPI unless something specific argues otherwise. Flask is fine for a five-route app,
Django only when you want the admin and the ORM.

## Layout

```
app/
  main.py           app object, routes
  config.py         settings read from the environment, one place
  models.py         pydantic models
  templates/        Jinja templates, if it serves HTML
  static/
tests/
  test_api.py
requirements.txt
.env.example
Dockerfile          only if it will be containerised
README.md
```

## Setup, actually run these

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "fastapi[standard]" uvicorn pytest httpx
python -m pip freeze > requirements.txt
uvicorn app.main:app --reload --port 8000
```

Record the exact startup line it prints. That is what the README's Quickstart ends with,
so the reader knows it worked. Note the interactive docs at `/docs`, which is the fastest
way for someone to see the API is alive.

## Conventions

- **Configuration comes from the environment, in one module.** No `os.getenv` scattered
  through route handlers. Fail loudly at import when a required variable is missing, so a
  misconfigured deploy dies at start rather than at the first request.
- **Any module-level mutable is shared across every request.** That is a data leak waiting
  to happen in a multi-user app. Keep per-request state in the request.
- Validate input with pydantic models, not by hand.
- Return 404 rather than 403 for a resource the caller is not allowed to see, when the
  existence of the resource is itself information.
- A `/health` route that touches nothing. Hosting platforms need it and it costs one line.
- Never log secrets, tokens or user identifiers you would not want in a support ticket.
- Never interpolate user input into SQL. Parameterise. Same for shell commands: no
  `shell=True` with anything a user supplied.
- Tests hit the app through `TestClient`, so they exercise routing and validation, not
  just functions.

## Secrets

```bash
cp .env.example .env      # then fill it in
```

`.env` is git-ignored. `.env.example` lists every key with a dummy value and a comment
saying where to obtain the real one. The README's Configuration table lists the same keys,
and the two must agree. When they disagree, the code is right and both files are wrong.

## README notes

Quickstart block: `templates/quickstart/python-venv.md`, then the run command and the
`/docs` URL. Add `templates/quickstart/docker.md` if there is a Dockerfile.

Configuration section is mandatory here, one row per variable: name, purpose, default,
required.

Deployment goes in its own section. See `references/azure.md`.
