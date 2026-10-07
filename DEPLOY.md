# Deploying to Render

## 1. Assemble the deploy repo

```
odoo-render-deploy/
├── Dockerfile
├── render.yaml
├── start.sh
├── library/        <- copy of your library module's files
└── portfolio/      <- copy of your portfolio module's files
```

Copy the module folders directly (don't use git submodules — keeps the
Render build simple).

## 2. Create the Blueprint on Render

1. https://dashboard.render.com → **New** → **Blueprint**
2. Connect GitHub, select the repo
3. Render reads `render.yaml`, proposes a **Web Service** (`odoo-portfolio`,
   Docker, free) + a **PostgreSQL** database (`odoo-db`, free)
4. Click **Deploy Blueprint**

## 3. First-time setup (one-off, via the browser)

Once live at `https://odoo-portfolio-xxxx.onrender.com`:

1. You'll land on the **Database Manager** screen (no database exists yet)
2. Create a database (any name, e.g. `prod`), set an admin email/password —
   this becomes your Odoo login
3. Change the *master password* for the Database Manager itself (defaults to
   `admin` in the base image) — Settings → General Settings, or ask me for a
   hardened config
4. **Apps** → remove the "Apps" filter → search `library` → Install. Same
   for `portfolio`
5. Visit `/portfolio` on your Render URL

## 4. Notes (free tier)

- **Cold starts**: free web service spins down after inactivity; first
  request after that takes 30-50s to wake up.
- **Database expiry**: free Postgres is **deleted 30 days after creation**.
  Upgrade to a paid plan before then if you want to keep it, or just
  recreate it when it happens.
- **No persistent disk**: files uploaded *through the Odoo UI* (not the
  ones baked into the Docker image) reset on every redeploy.
- **Updating modules**: pushing to the branch triggers a rebuild
  automatically, but installed-app code changes still need an explicit
  module update (Apps → your module → Upgrade).
- **Upgrading later**: switch `plan: free` → `plan: starter` (web) and
  `plan: basic-256mb` (database) in `render.yaml`, push, add a persistent
  disk back.

## Why `start.sh` exists

The official `odoo` Docker image can auto-wire its DB connection from env
vars named `HOST`/`PORT`/`USER`/`PASSWORD` — but Render *also* reserves the
name `PORT` for the port your app must listen on. Using the image's default
mapping makes Odoo's DB port collide with Render's app port, and the deploy
times out ("port scan timeout"). `start.sh` sidesteps this: the database
connection uses `DB_HOST`/`DB_PORT`/`DB_USER`/`DB_PASSWORD` (no collision),
and Odoo's HTTP server explicitly binds to `$PORT` via `--http-port`.
